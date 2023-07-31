#
# Naver Papago translator API
# 

# up to 5000 characters a call? 
# up to 10000 characters in a day 

import os
import sys
import urllib.request
import json

# PowerShell 
# Set-Item -Path env:NAVER_CLOUD_ID -Value "your_id_value"
# Set-Item -Path env:NAVER_CLIENT_SECRET -Value "your_password_value"
client_id = os.environ['NAVER_CLOUD_ID'] 
client_secret = os.environ['NAVER_CLIENT_SECRET'] 

source_language = "ja"
target_language = "ko"

split_size = 1000

# use '\n' to seperate lines in the text 
def translate_text(target, text):
    encText = urllib.parse.quote(text)
    data = "source=" + source_language + "&target=" + target + "&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    
    if(rescode==200):
        response_body = response.read()
        json_data = response_body.decode('utf-8')
        translated_text = json.loads(json_data)["message"]["result"]["translatedText"]
        translated_list = translated_text.split('\n')
        #print(translated_list)    
        
        return translated_list
    else:
        print("Error Code:" + rescode)
        
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
    
    for string in subtitle_text_list:
        if current_length + len(string) <= split_size:
            current_list.append(string)
            current_length += len(string)
        else:
            split_lists.append(current_list)
            current_list = [string]
            current_length = len(string)
        
        total_length += len(string)

    if current_list:
        split_lists.append(current_list)
     
    # translate each splitted list 
    text_translated_list_all = [] 
    for split_list in split_lists:
        string = '\n'.join(split_list)
        # print(string)        
        result = translate_text(target_language, string)
        text_translated_list_all.append(result)
        print(f"[Info]{len(split_list)} sentences translated") 
    
    # Save the subtitle text to a new file.
    # create a new file with the same name as the input file, consider file name contains multiple '.' 
    output_file_name = input_file_name.rsplit(".", 1)[0]
            
    with open(output_file_name + "_translated.srt", "w", encoding="utf-8") as fout:       
        i = 0 
        for lists in text_translated_list_all:
            for string in lists: 
                fout.write(f"{i+1}\n")
                fout.write(f"{time_sync_data_list[i]}\n")
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
            print("Usage: python subtitle-translator-papago.py '.\INPUT.SRT' 1 \n")
            sys.exit(1)
            
        translate_file(input_file_name, skip_textlength)
        sys.exit(0)
    else: 
        print("Usage: python subtitle-translator-papago.py '.\INPUT.SRT' 1 \n")
        sys.exit(1)