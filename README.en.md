# Multilanguage README Pattern
[![ko](https://img.shields.io/badge/lang-ko-red.svg)]([https://github.com/sevengivings/subtitle-extractor/blob/master/README.md])

A Python program to automate the video AI speech recognition and translation process. 

(Caution!) Comments and messages are in Korean.

[Overview]

MP4/MP3 file -> .SRT subtitle file -> filtering unnecessary subtitle(too short and meaningless repeated) -> time sync data(.time) & subtitle text data(.docx & .txt) -> user intervention for manual translation using DeepL file translation(translated .docx) or translated .txt using another method -> (optional)translated .docx to translated .txt -> join .time and .txt to .srt

This is a python program to automate the video AI speech recognition and translation process using OpenAI's Whisper and stable-ts with some modifications for subtitles. DeepL seems to have the best performance but currently they do not support API in Korea. If you try to translate .docx file in DeepL app or web, there may be problems with time sync information part in .docx, so I have a function to save the text separately as a .docx. This is a program that organizes the whole process as conveniently as possible.

[Key Features]

- Extract subtitles directly from MP4 (choose between stable-ts and Whisper)
- Save only the subtitle text in .docx format for translating the file(for DeepL App or Web).
- Ability to delete unnecessary one- or two-character meaningless subtitles
- Use only the first subtitle when the same phrase is repeated
- Ability to combine multiple lines of subtitles into a single line

[Limitations]

- Speech recognition is not complete and may result in missing or misrecognized speech. Not recommended for professional use.
- The quality or number of subtitles may be different when using stable-ts and whisper commands, when using this program, and when using Whisper WebUI (there are many optimization parameters, so it is not possible to know all of them; for reference, stable-ts is also a program optimized for subtitle extraction, but it tends to have missing recognition compared to the original Whisper. However, there are fewer problems such as ghost sounds extracted when they are not there, pointless repetition, and the back part not being extracted).

[Reference]

- stable-ts : GitHub - jianfch/stable-ts: ASR with reliable word-level timestamps using OpenAI's Whisper(https://github.com/jianfch/stable-ts)
- Whisper : General-purpose speech recognition model(https://github.com/openai/whisper)
- DeepL : AI translation(https://www.deepl.com/translator) 
