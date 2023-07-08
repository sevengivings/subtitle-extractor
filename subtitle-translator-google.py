#
# subtitle-translator-google.py 
#

# Needs Google Cloud Account, up to 500,000 characters free translation 
# You can choose api_key or ADC for credential

import os 
import sys
import requests 

split_size = 1000
target_language = "ko"

# https://cloud.google.com/translate/docs/basic/translating-text?hl=ko#translate_translate_text-python
# This script is used to translate subtitles using Google Cloud Translate service 
# Google ADC(Application Default Credentials) is used to authenticate the request.
# https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to 

# Set up Application Default Crendentials 
# https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev 
# Install and initialize the gcloud CLI.
# Create credential file: gcloud auth application-default login
def translate_text_adc(target: str, text: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    try:
        from google.cloud import translate_v2 as translate
    except ModuleNotFoundError:
        print(
            "Please install the Cloud client library using "
            '"pip install google-cloud-translate==2.0.1"'
        )
        sys.exit(1)

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    #print("Text: {}".format(result["input"]))
    #print("Translation: {}".format(result["translatedText"]))
    #print("Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result 

# PowerShell 
# Set-Item -Path env:GOOGLE_API_KEY -Value "your_api_key"
def translate_text_apikey(target, text):
    api_key = os.environ['GOOGLE_API_KEY'] 
    endpoint = 'https://translation.googleapis.com/language/translate/v2'

    text = text
    target_language = target

    params = {
        'key': api_key,
        'q': text,
        'target': target_language
    }

    response = requests.post(endpoint, params=params)
    data = response.json()
    translated_texts = [item['translatedText'] for item in data['data']['translations']]
    # print(translated_texts)
    
    return translated_texts

# removes unnecessary short and repeated characters from the subtitle text and translate using Google Cloud Translate 
def translate_file(input_file_name, skip_textlength):
    # Check if the file exists.
    if not os.path.exists(input_file_name):
        raise FileNotFoundError(f"The file {input_file_name} does not exist.")

    # Open the input file.
    with open(input_file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()

    subtitle_text = {}
    subtitle_text_list = []
    time_sync_data_list = [] 
    time_sync_data = ""

    deleted_line = 0
    deleted_subtitle_text =  set()
    ignored_line = 0    
    ignored_subtitle = set()    

    latest_subtitle_text = ""
    
    # Iterate over the lines in the file.
    for line in lines: 
        # Ignore empty lines and lines that contain only numbers.
        if line.strip() == "" or line.strip().isdigit():
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
                    if latest_subtitle_text ==  line.strip():
                        ignored_subtitle.add(line.strip())
                        ignored_line = ignored_line + 1
                        continue
                
                    latest_subtitle_text = subtitle_text[time_sync_data] = line.strip()
                    subtitle_text_list.append(latest_subtitle_text)
                    time_sync_data_list.append(time_sync_data)
                else: 
                    # join multiple lines of text into one line 
                    subtitle_text[time_sync_data] = subtitle_text[time_sync_data] + ", " + line.strip()
                    subtitle_text_list.append(subtitle_text[time_sync_data])   
                    time_sync_data_list.append(time_sync_data)              
            else: 
                deleted_line = deleted_line + 1
                deleted_subtitle_text.add(line.strip())
                
    # split lists into small lists 
    current_length = 0
    total_length = 0 
    current_list = [] 
    split_lists = []
 
     
    # Google Cloud Translate only supports maximum text segments : 128 
    num_of_segments = 0 
    for string in subtitle_text_list:
        if current_length + len(string) <= split_size and num_of_segments < 127:
            current_list.append(string)
            current_length += len(string)
            num_of_segments += 1
        else:
            split_lists.append(current_list)
            current_list = [string]
            current_length = len(string)
            num_of_segments = 0
        
        total_length += len(string)

    if current_list:
        split_lists.append(current_list)
     
    # translate each splitted list 
    text_translated_list_all = [] 
    for split_list in split_lists:
        if os.environ['GOOGLE_API_KEY'] != None: 
            result = translate_text_apikey(target_language, split_list)
            translated_list = result 
        else:
            result = translate_text_adc(target_language, split_list)
            translated_list = [res['translatedText'] for res in result]
        
        text_translated_list_all.append(translated_list)
        print(f"[Info]{len(split_list)} sentences translated") 
    
    # Save the subtitle text to a new file.
    # create a new file with the same name as the input file, consider file name contains multiple '.' 
    output_file_name = input_file_name.rsplit(".", 1)[0]
            
    with open(output_file_name + "_translated.srt", "w", encoding="utf-8") as fout:       
        i = 0 
        for lists in text_translated_list_all:
            for string in lists: 
                fout.write(f"{i+1}\n")
                fout.write(f"{time_sync_data_list.pop()}\n")
                fout.write(f"{string.strip()}\n")
                if i != len(time_sync_data_list)-1:
                    fout.write("\n")     
                i += 1                 
    
    # Print the total_length
    print("\n[Info]Number of characters: ", total_length)
    
    if len(deleted_subtitle_text) > 0:
        print("[Info]Number of short subtitles: ", deleted_line)          
        output_file_name = input_file_name.rsplit(".", 1)[0] 
        with open(output_file_name + "_deleted.txt", "w", encoding="utf-8") as f3:
            for text in deleted_subtitle_text:
                f3.write(text + "\n")
                
    if len(ignored_subtitle) > 0:
        print("\n[Info]Number of repeated subtitles: ", ignored_line)
        output_file_name = input_file_name.rsplit(".", 1)[0]
        with open(output_file_name + "_repeated.txt", "w", encoding="utf-8") as f4:
            for text in ignored_subtitle:
                f4.write(text + "\n")
                
    print("[Info]Done")

if __name__ == "__main__":
    # pass file name as argument 
    if len(sys.argv) > 2:
        input_file_name = sys.argv[1]
        try: 
            skip_textlength = int(sys.argv[2]) 
        except  ValueError:
            print("Input number only for second argument.\n")
            print("Usage: python subtitle-translator-google.py '.\INPUT.SRT' 1 \n")
            sys.exit(1)
            
        translate_file(input_file_name, skip_textlength)
        sys.exit(0)
    else: 
        print("Usage: python subtitle-translator-google.py '.\INPUT.SRT' 1 \n")
        sys.exit(1)