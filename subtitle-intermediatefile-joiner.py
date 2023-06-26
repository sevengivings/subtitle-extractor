# from timesync data .time & text only .txt to .srt

import sys

def join_srt_files(time_file, text_file, output_file):
    with open(time_file, 'r', encoding='utf-8') as time_input, open(text_file, 'r', encoding='utf-8') as text_input, open(output_file, 'w', encoding='utf-8') as output:
        time_data = time_input.readlines()
        text_data = text_input.readlines()

        if len(time_data) != len(text_data):
            print("Error: The number of time sync entries and subtitle text entries do not match.")
            return

        for i in range(len(time_data)):
            time_entry = time_data[i].strip()
            text_entry = text_data[i].strip()

            output.write(f"{i+1}\n")
            output.write(f"{time_entry}\n")
            output.write(f"{text_entry}\n")
            output.write("\n")

    print("Join complete. New SRT file saved as", output_file)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Please provide the paths to the .time file, .txt file, and the output file as command-line arguments.")
    else:
        time_file = sys.argv[1]
        text_file = sys.argv[2]
        output_file = sys.argv[3]
        join_srt_files(time_file, text_file, output_file)