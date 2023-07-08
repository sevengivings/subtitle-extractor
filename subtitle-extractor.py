# Extract subtitle from video, save as .docx for translating and convert to .srt

# Requires:
# - stable-ts (https://github.com/jianfch/stable-ts) (pip install stable-ts)
# - whisper (https://github.com/openai/whisper) (pip install git+https://github.com/openai/whisper.git )
# - torch + cuda
# - ffmpeg.exe (https://www.ffmpeg.org/) for stable-ts and whisper 
# - python-docx

# OS: Windows 10/11 

import os 
import sys
import docx 
import argparse
import torch
import stable_whisper
import whisper 
from whisper.utils import get_writer
import numpy as np
import gettext
import locale 

# stable-ts  
def extract_audio_stable_whisper(model_name, device, audio_language, input_file_name, output_file_name): 
    # Check if the file exists.
    if not os.path.exists(input_file_name):
        raise FileNotFoundError(f"The file {input_file_name} does not exist.")

    # Extract the audio from the video.
    model = stable_whisper.load_model(model_name, device=device)
    result = model.transcribe(verbose=True, word_timestamps=False, language=audio_language, audio=input_file_name)
    result.to_srt_vtt(output_file_name + ".srt", word_level=False)

# Whisper 
def extract_audio_whisper(model_name, device, audio_language, input_file_name):
    # Check if the file exists.
    if not os.path.exists(input_file_name):
        raise FileNotFoundError(f"The file {input_file_name} does not exist.")

    model = whisper.load_model(model_name).to(device)
    temperature = tuple(np.arange(0, 1.0 + 1e-6, 0.2))  # copied from Whisper original code 
    result = model.transcribe(input_file_name, temperature=temperature, verbose=True, word_timestamps=False, condition_on_previous_text=False, language=audio_language)
    output_dir = os.path.dirname(input_file_name)
    writer = get_writer("srt", output_dir)
    writer(result, input_file_name) 

# srt -> .time, .txt, .docx 
# skip_textlength : 0 = all, 1 = igonore 1 character, 2 = ignore 2 characters
def srt_split(input_file_name, skip_textlength):
    # Check if the file exists.
    if not os.path.exists(input_file_name):
        raise FileNotFoundError(f"The file {input_file_name} does not exist.")

    # Open the input file.
    with open(input_file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Create a key-value dictionary to store the subtitle text.
    # key = time sync data, value = line of text
    subtitle_text = {}
    # initialize time_sync_data 
    time_sync_data = ""
    
    # number of line deleted 
    deleted_line = 0  
    # non-duplicated deleted subtitle text list, use set() to remove duplicated item  
    deleted_subtitle_text =  set()

    # ignored number of line 
    ignored_line = 0
    # for ignoring repeated subtitle 
    ignored_subtitle = set()
    # last subtitle text 
    last_subtitle_text = ""
    
    # Iterate over the lines in the file.
    for line in lines: 
        # Ignore empty lines and lines that contain only numbers.
        if line.strip() == "" or line.strip().isdigit():
            time_sync_data = ""
            continue

        # If the line contains "-->", it is time sync data.
        elif line.find("-->") != -1:
            # save time sync data to a varible for later use. 
            time_sync_data = line.strip()

        # Otherwise, the line is subtitle text.
        else:
            # ignore short text under n characters
            if len(line.strip()) > skip_textlength and time_sync_data.find('-->') != -1:
                # Add the line of text to the dictionary.
                value = subtitle_text.get(time_sync_data, "")
                if value is None or value == "":
                    
                    # Ignore repeated subtitles that say the same thing 
                    if last_subtitle_text ==  line.strip():
                        ignored_subtitle.add(line.strip())
                        ignored_line = ignored_line + 1
                        continue
                
                    subtitle_text[time_sync_data] = line.strip()
                    last_subtitle_text = line.strip()
                else: 
                    # If the subtitle text is repeated, combine them into one line.
                    subtitle_text[time_sync_data] = subtitle_text[time_sync_data] + ", " + line.strip() 
                # print(time_sync_data, line)
            else: 
                deleted_line = deleted_line + 1
                deleted_subtitle_text.add(line.strip())

    text_total_length = 0
    
    # Save the subtitle text to a new file.
    # create a new file with the same name as the input file, consider file name contains multiple '.' 
    output_file_name = input_file_name.rsplit(".", 1)[0]
    
    # add extension to the output file name
    f1 = open(output_file_name + ".txt", "w", encoding="utf-8")
    f2 = open(output_file_name + ".time", "w", encoding="utf-8")
    
    # docx file name 
    docx_file_name = output_file_name + ".docx"
    doc = docx.Document()
    doc.save(docx_file_name)
    
    # iterate all subtitle_text and time_sync_data
    for time_sync in subtitle_text:
        f2.write(time_sync + "\n")
        f1.write(subtitle_text[time_sync] + "\n")
        
        para = doc.add_paragraph()
        run = para.add_run(subtitle_text[time_sync])
        
        # CRLF included 
        text_total_length = text_total_length +  len(subtitle_text[time_sync]) + 2 
            
    doc.save(docx_file_name)
    
    # Print the total_length
    print(_("Info: The total length of subtitles is: "), text_total_length)
    
    if len(deleted_subtitle_text) > 0: 
        print(_("Info: The short subtitles are ignored: "), deleted_line)
        output_file_name = input_file_name.rsplit(".", 1)[0] 
        with open(output_file_name + "_short_subtitle_ignored.txt", "w", encoding="utf-8") as f3:
            for text in deleted_subtitle_text:
                f3.write(text + "\n")
                #print(text)

    if len(ignored_subtitle) > 0:
        print(_("Info: The repeated subtitles are ignored: "), ignored_line)
        output_file_name = input_file_name.rsplit(".", 1)[0]
        with open(output_file_name + "_repeated_subtitles_ignored.txt", "w", encoding="utf-8") as f4:
            for text in ignored_subtitle:
                f4.write(text + "\n")
                #print(text)

def docx_to_txt(input_file_name): 
    # Check if the file exists.
    if not os.path.exists(input_file_name):
        raise FileNotFoundError(f"The file {input_file_name} does not exist.")

    # open a docx file and read it
    docx_file = docx.Document(input_file_name)

    # create a new file with the same name as the input file, consider file name contains multiple '.' 
    output_file_name = input_file_name.rsplit(".", 1)[0]

    # save the content of docx file to a new file with the same name as the input file
    with open(output_file_name + ".txt", "w", encoding="utf-8") as f:
        for paragraph in docx_file.paragraphs:
            if len(paragraph.text) < 1:
                print (paragraph.text)
                continue
            f.write(paragraph.text + "\n")
            
    print (output_file_name + _(".txt file is saved"))

def join_srt_files(time_file, text_file, output_file):
    with open(time_file, 'r', encoding='utf-8') as time_input, open(text_file, 'r', encoding='utf-8') as text_input, open(output_file, 'w', encoding='utf-8') as output:
        time_data = time_input.readlines()
        text_data = text_input.readlines()
        if len(time_data) != len(text_data):
            print(_("Error: time and text file must have the same number of lines"))
            return
        for i in range(len(time_data)):
            time_entry = time_data[i].strip()
            text_entry = text_data[i].strip()
            output.write(f"{i+1}\n")
            output.write(f"{time_entry}\n")
            output.write(f"{text_entry}\n")
            output.write("\n")
    
    print(_("Info: new srt file is saved"), output_file)

if __name__ == "__main__":
    appname = 'subtitle-extractor'
    localedir = './locales'
        
    en_i18n = gettext.translation(appname, localedir, fallback=True, languages=['ko'])  # All messages are in Korean
    en_i18n.install()

    parser= argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("audio", type=str, help="audio/video file(s) to transcribe")
    parser.add_argument("--model", default="medium", help="name of the stable-ts or Whisper model to use")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu", help="device to use for PyTorch inference")
    parser.add_argument("--audio_language", type=str, default="ja", help="language spoken in the audio, specify None to perform language detection")
    parser.add_argument("--subtitle_language", type=str, default="ko", help="subtitle target language need only if you plan to use DeepL file translation manually")
    parser.add_argument("--skip_textlength", type=int, default=1, help="skip short text in the subtitles, useful for removing meaningless words")
    
    args = parser.parse_args().__dict__
    model_name: str = args.pop("model")
    device: str = args.pop("device")
    audio_language: str = args.pop("audio_language")
    subtitle_language: str = args.pop("subtitle_language")
    input_file_name: str = args.pop("audio")
    skip_textlength: int = args.pop("skip_textlength")

    print("subtitle-extractor : AI subtitle extraction and translation helper tool")
    print("\nmodel:" + model_name + "\ndevice:" + device  + "\naudio language:" + audio_language + "\nsubtitle language:" + subtitle_language  + "\nigonore n characters:" + str(skip_textlength) + "\naudio:" + input_file_name)
    print("\nPython version: " + sys.version)
    print("Torch version: " + torch.__version__ + "\n")

    if skip_textlength < 0:
        skip_textlength = 0 

    # create a new file with the same name as the input file, consider file name contains multiple '.' 
    output_file_name = input_file_name.rsplit(".", 1)[0]

    # to determine transcribing method, get user input 
    # print ("Input the number of the transcribing method you want to use: 1 for Stable-ts, 2 for Whisper") 
    number_selected = input(_("Input transcribing method. 1 for Stable-ts, 2 for Whisper: "))
    try: 
        number_selected = int(number_selected)
    except ValueError:
        print(_("Error: Enter numbers only"))
        sys.exit(1)

    # AI speech recognition  
    # Check if the file exists
    if not os.path.exists(output_file_name + ".srt"):           
        if number_selected == 1:     
            extract_audio_stable_whisper(model_name, device, audio_language, input_file_name, output_file_name)
        elif number_selected == 2:
            extract_audio_whisper(model_name, device, audio_language, input_file_name)
        else: 
            print(_("Error: Enter numbers only")) 
            sys.exit(1)
    else: 
        print(_("Warning: File already exists"))

    # Separate text and visuals in .SRT and save subtitle text as .docx for translation. 
    # Removed short sentences and repeated subtitles.  
    srt_split(output_file_name + ".srt", skip_textlength)

    # Get the translated file name from console if not from DeepL file translation
    print(_("Info: You should translate .docx manullay using DeepL file translation, use "), output_file_name + ".docx")
    # input file name from console  
    file_name = input(_("Input another translated file name or press [Enter] to continue...(") + output_file_name + " " + subtitle_language + _(".docx will be used.): "))
    
    # If input is not given, use default file name.
    if len(file_name) < 1: 
        file_name = output_file_name + " " + subtitle_language + ".docx"

    if not os.path.exists(file_name): 
        print(_("Error: File not found translated "), file_name)
        sys.exit(1)
    
    # If input file is .txt, docx_to_txt is not used, instead .srt is used to refer to .txt file name.
    if not file_name.endswith(".txt"):
        # Extract .txt from .docx
        docx_to_txt(file_name)
        # "\n>> " + file_name.rsplit(".", 1)[0] + 
        input(_("Press [Enter] to continue... or edit ") + file_name.rsplit(".", 1)[0] + ".txt ")
    
    text_file_name = file_name.rsplit(".", 1)[0]
    
    # Change the name of original .srt
    os.rename(output_file_name + ".srt", output_file_name + "_original.srt")

    # Create the final subtitle file joining with .time and .txt.
    join_srt_files(output_file_name + ".time", text_file_name + ".txt", text_file_name + ".srt")
    
    # Change the name of final srt same as video file name 
    print (_("Info: final srt file is saved"))
    if (text_file_name != output_file_name):
        os.rename(text_file_name + ".srt", output_file_name + ".srt")
    
    # Delete intermediate files.
    os.unlink (output_file_name + ".time")
    os.unlink (output_file_name + ".txt")

    # If translated .txt is not provided, there is no ~ ko.docx or ~ ko.txt file.
    # If translated .txt is provided by the user, it is not deleted.
    if not file_name.endswith(".txt"):
        try: 
            os.unlink (output_file_name + " " + subtitle_language + ".docx")
            os.unlink (output_file_name + " " + subtitle_language + ".txt")
            os.unlink (output_file_name + ".docx")
        except FileNotFoundError: 
            pass
    
    print(_("Done"))

    sys.exit(0)
