# subtitle-extractor

A Python program to automate the video AI speech recognition and translation process. Comments and messages are in Korean.

OpenAI의 Whisper와 자막을 위해 조금 변형한 stable-ts를 사용하여 비디오 AI 음성 인식 및 번역 과정을 자동화하기 위한 파이썬 프로그램입니다. 

사용법: python .\subtitle-extractor 'd:\sammple video.mp4' 1 

도중에 프로그램이 입력을 기다리기 위해 멈추는데, 이 때 무료 DeepL 웹/앱 번역기에서 .docx를 수동으로 파일 번역해 준 후 [Enter]를 누르면 번역된 자막이 생성됩니다. 나중에 한국에도 DeepL API가 공개된다면 이 기능도 자동화할 예정입니다. 
