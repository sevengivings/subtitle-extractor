# Extract subtitle from video, save as .docx for translating and convert to .srt

# Requires:
# - stable-ts (https://github.com/jianfch/stable-ts) (pip install stable-ts)
# - whisper (https://github.com/openai/whisper) (pip install git+https://github.com/openai/whisper.git )
# - torch + cuda
# - ffmpeg (https://www.ffmpeg.org/) for stable-ts 
# - python-docx

# OS: Windows 10/11 

import os 
import sys
import docx 

import torch
import stable_whisper
import whisper 
from whisper.utils import get_writer
import numpy as np

whisper_model = "medium"  # small:2GB VRAM
whisper_device = "cuda" if torch.cuda.is_available() else "cpu"
whisper_language = "ja"
target_language = " ko"   # for DeepL

# stable-ts  
def extract_audio_stable_whisper(input_file_name, output_file_name): 
    # Check if the file exists.
    if not os.path.exists(input_file_name):
        raise FileNotFoundError(f"The file {input_file_name} does not exist.")

    # Extract the audio from the video.
    model = stable_whisper.load_model(whisper_model, device=whisper_device)
    result = model.transcribe(verbose=True, word_timestamps=False, language=whisper_language, audio=input_file_name)
    result.to_srt_vtt(output_file_name + ".srt", word_level=False)

# Whisper 
def extract_audio_whisper(input_file_name):
    # Check if the file exists.
    if not os.path.exists(input_file_name):
        raise FileNotFoundError(f"The file {input_file_name} does not exist.")

    model = whisper.load_model(whisper_model).to(whisper_device)
    temperature = tuple(np.arange(0, 1.0 + 1e-6, 0.2))  # copied from Whisper original code 
    result = model.transcribe(input_file_name, temperature=temperature, verbose=True, word_timestamps=False, language=whisper_language)
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
    print("\n최종 글자수(개행문자포함): ", text_total_length)
    
    if len(deleted_subtitle_text) > 0: 
        print("\n짧아서 무시된 자막 갯수: ", deleted_line)
        print("짧아서 삭제한 자막 목록은 별도 파일로 저장합니다.")
        output_file_name = input_file_name.rsplit(".", 1)[0] 
        with open(output_file_name + "_짧아서삭제된자막제거목록.txt", "w", encoding="utf-8") as f3:
            for text in deleted_subtitle_text:
                f3.write(text + "\n")
                #print(text)

    if len(ignored_subtitle) > 0:
        print("\n반복되어 무시한 자막 갯수: ", ignored_line)
        print("반복되어 무시한 자막 목록을 별도 파일로 저장합니다.")
        output_file_name = input_file_name.rsplit(".", 1)[0]
        with open(output_file_name + "_반복된자막제거목록.txt", "w", encoding="utf-8") as f4:
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
            
    print (output_file_name + ".txt" + "를 저장하였습니다.")

def join_srt_files(time_file, text_file, output_file):
    with open(time_file, 'r', encoding='utf-8') as time_input, open(text_file, 'r', encoding='utf-8') as text_input, open(output_file, 'w', encoding='utf-8') as output:
        time_data = time_input.readlines()
        text_data = text_input.readlines()
        if len(time_data) != len(text_data):
            print("오류: 자막 갯수와 시각 동기 자료 갯수가 다릅니다.")
            return
        for i in range(len(time_data)):
            time_entry = time_data[i].strip()
            text_entry = text_data[i].strip()
            output.write(f"{i+1}\n")
            output.write(f"{time_entry}\n")
            output.write(f"{text_entry}\n")
            output.write("\n")
    
    print("\n새로운 자막이 생성되었습니다: ", output_file)

if __name__ == "__main__":
    # pass file name as argument 
    if len(sys.argv) > 2:
        input_file_name = sys.argv[1]
        try: 
            skip_textlength = int(sys.argv[2]) 
        except  ValueError:
            print("두번째 인자는 0,1,2,3등 무시할 자막의 문자 길이 지정을 위한 숫자를 넣어주세요.\n")
            print("Usage: python .\subtitle-extractor.py '.\sample file.mp4' 1 \n")
            sys.exit(1)

        print("Torch version: " + torch.__version__)

        if skip_textlength < 0:
            skip_textlength = 0 

        # create a new file with the same name as the input file, consider file name contains multiple '.' 
        output_file_name = input_file_name.rsplit(".", 1)[0]

        # to determine transcribing method, get user input 
        # print ("Input the number of the transcribing method you want to use: 1 for Stable-ts, 2 for Whisper") 
        number_selected = input(">> Stable-ts를 쓰려면 1, Whisper를 쓰려면 2를 입력하고 [Enter]를 누르세요 : ")
        try: 
            number_selected = int(number_selected)
        except ValueError:
            print("입력은 숫자 1이나 2만 유효합니다.")
            sys.exit(1)

        # AI speech recognition  
        # Check if the file exists
        if not os.path.exists(output_file_name + ".srt"):           
            if number_selected == 2:     
                extract_audio_whisper(input_file_name)
            else:
                extract_audio_stable_whisper(input_file_name, output_file_name)
        else: 
            print("이미 자막이 있어서 추출을 생략합니다.")

        # Separate text and visuals in .SRT and save subtitle text as .docx for translation. 
        # Removed short sentences and repeated subtitles.  
        srt_split(output_file_name + ".srt", skip_textlength)

        # Get the translated file name from console if not from DeepL file translation
        print("\n" + output_file_name + ".docx를 외부 번역프로그램에서 파일 번역한 후 다음을 진행합니다.\n")
        print("다른 폴더에 있는 경우 전체 경로를 입력하여야 하고 따옴표나 쌍따옴표는 필요 없습니다.")
        # input file name from console  
        file_name = input("\n>> .docx 혹은 .txt 이름을 입력하거나 엔터를 누르세요(DeepL이용 시 기본값: " + output_file_name + target_language + ".docx): ")
        
        # If input is not given, use default file name.
        if len(file_name) < 1: 
            file_name = output_file_name + target_language + ".docx"

        if not os.path.exists(file_name): 
            print(file_name + "이 없어서 종료합니다. 타 프로그램에서 번역한 경우 파일 이름을 입력해주세요.")
            sys.exit(1)
        
        # If input file is .txt, docx_to_txt is not used, instead .srt is used to refer to .txt file name.
        if not file_name.endswith(".txt"):
            # 번역된 .docx에서 .txt를 추출
            # Extract .txt from .docx
            docx_to_txt(file_name)
            input("\n>> " + file_name.rsplit(".", 1)[0] + ".txt의 번역을 검토 및 변경하거나 계속 진행하려면 [Enter]를 누르세요.")
        
        text_file_name = file_name.rsplit(".", 1)[0]
        
        # Change the name of original .srt
        os.rename(output_file_name + ".srt", output_file_name + "_original.srt")

        # Create the final subtitle file joining with .time and .txt.
        join_srt_files(output_file_name + ".time", text_file_name + ".txt", text_file_name + ".srt")
        
        # Change the name of final srt same as video file name 
        print ("\n기존 srt는 _original을 붙였고, 최종 번역된 srt는 mp4 파일명과 같게 변경했습니다.")
        if (text_file_name != output_file_name):
            os.rename(text_file_name + ".srt", output_file_name + ".srt")
        
        # Delete intermediate files.
        os.unlink (output_file_name + ".time")
        os.unlink (output_file_name + ".txt")

        # If translated .txt is not provided, there is no ~ ko.docx or ~ ko.txt file.
        # If translated .txt is provided by the user, it is not deleted.
        if not file_name.endswith(".txt"):
            try: 
                os.unlink (output_file_name + target_language + ".docx")
                os.unlink (output_file_name + target_language + ".txt")
                os.unlink (output_file_name + ".docx")
            except FileNotFoundError: 
                pass

        sys.exit(0)
    else: 
        print("음성 추출할 MP3/4 파일 이름과 의미 없는 한 글자와 같이 너무 짧은 자막 제거를 위한 글자수를 넣어주세요.\n")
        print("팁: 파일 이름 입력 시에 앞쪽 글자 몇 개 입력 후에 [Tab]키를 누르면 파일 이름이 자동 완성됩니다.\n")
        print("Usage: python .\subtitle-extractor.py 'E:\video\sample video file.mp4' 1 \n")
        sys.exit(1)