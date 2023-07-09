# subtitle-extractor
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/sevengivings/subtitle-extractor/blob/master/README.en.md)

A Python script for AI speech recognition of video or audio file using Whisper or stable-ts and translation subtitle using DeepL app or web file translation.  

[Overview] 

MP4/MP3 file -> .SRT subtitle file -> filtering unnecessary subtitle(too short and meaningless repeated) -> time sync data(.time) & subtitle text data(.docx & .txt) -> user intervention for manual translation using DeepL file translation(translated .docx) or translated .txt using another method -> (optional)translated .docx to translated .txt -> join .time and .txt to .srt 

OpenAI의 Whisper와 자막을 위해 조금 변형한 stable-ts를 사용하여 비디오 AI 음성 인식 및 번역 과정을 자동화하기 위한 파이썬 프로그램입니다. 다만 아직까지는 번역할 때에는 성능이 가장 좋아 보이는 DeepL을 통해 파일 번역을 수동으로 하게 되는데, .SRT 자막을 그대로 번역시키면 시각정보 부분에 문제가 생길 수 있어서 텍스트만 따로 .docx로 저장해주는 기능을 가지고 있습니다. 그러한 일련의 작업 과정을 최대한 편리하게 구성해 본 프로그램입니다.   

[주요 기능] 

* MP4에서 자막 직접 추출 기능(stable-ts와 Whisper 중 선택 가능)
* 무료 번역기(DeepL) 이용 시 파일 번역을 위하여 .docx 형태로 자막 텍스트만 저장(클립보드 이용 시 글자 한번에 3천자 제한) 
* 불필요한 한 글자나 두 글자의 자막을 삭제하는 기능
* 같은 말이 반복될 때 첫번째 자막만 사용 
* 여러 줄의 자막을 한 줄로 합치는 기능

[한계]

- 음성 인식이 완전하지 않아서 누락되는 음성이나 잘못 인식될 수 있습니다. 프로페셔널한 용도로 사용은 권장하지 않습니다. 
- stable-ts와 whisper 명령어로 했을 때와 이 프로그램을 사용했을 때, Whisper WebUI를 썼을 때 각각 자막의 품질이나 개수가 다를 수 있습니다(최적화 파라미터가 많아서 모두 알 수 없으며, 참고로 stable-ts는 자막 추출 용도로 최적화한 프로그램이기도 하지만 Whisper 오리지널에 비해 인식 누락이 있는 편입니다. 하지만, 없는데 추출된 귀신 소리, 무의미한 반복, 뒷부분 추출 안되는 등의 문제는 적은 편입니다.)


[관련 프로그램 링크] 

- stable-ts : GitHub - jianfch/stable-ts: ASR with reliable word-level timestamps using OpenAI's Whisper(https://github.com/jianfch/stable-ts) 
- Whisper : General-purpose speech recognition model(https://github.com/openai/whisper)
- DeepL : AI translation(https://www.deepl.com/translator)

[사용법]
```
(venv) PS C:\Users\login_id> python .\subtitle-extractor.py --skip-textlength=1 'd:\sammple video.mp4'
```
--skip-textlength 뒤에 있는 숫자 1은 1글자 자막을 무시하겠다는 의미입니다. 

(생략할 경우 기본값 설정) --model=medium --device=cuda --audio-language=ja --subtitle-language=kr 

```
subtitle-extractor : AI subtitle extraction and translation helper tool

model:medium
device:cuda
audio language:ja
subtitle language:ko
igonore n characters:1
audio:D:\sample video.mp4 

Python version: 3.11.3 (tags/v3.11.3:f3909b8, Apr  4 2023, 23:49:59) [MSC v.1934 64 bit (AMD64)]
Torch version: 2.0.1+cu117

[입력] 번역에 stable-ts를 쓰려면 1, Whisper는 2를 입력 후 [Enter]를 누르세요:
```
위 메시지가 나오는데, 1이나 2를 입력합니다. Whisper는 조금 느리지만 텍스트를 더 많이 추출합니다. 장단점이 있으므로 비교하며 이용하셔도 좋을 것 같습니다. Whisper가 오류로 추출이 안될 때에는 stable-ts가 되는 경우가 많습니다.

잠시 기다리면 음성 추출이 시작되며 시각과 자막이 표시되어 진행 상황을 파악할 수 있습니다. 

```
[00:00.000 --> 00:02.000] はじめまして
```

추출이 완료되면 아래 메시지가 표시됩니다. 

```
Saved: D:\sample video.srt
[정보] 전체 자막 길이:  462
[정보] 짧아서 무시된 자막 종류:  24
[정보] 반복되어 무시된 자막 종류:  7
[작업] 직접 번역을 하기 위해 DeepL의 파일 번역 기능에 다음 파일을 사용하세요.  D:\sample video.docx
[입력] 번역된 파일이름을 넣거나 엔터를 누르면 D:\sample video ko.docx가 사용됩니다:
```

위 메시지가 나오면 이 때 무료 DeepL 웹/앱 번역기에서 .docx를 수동으로 파일 번역해 준 후 [Enter]를 누르면 번역된 자막이 생성됩니다. 

만약 다른 번역기를 사용하고 싶을 경우 D:\sample video.txt 파일을 이용하여 번역을 한 후에 따로 D:\sample video ko.txt파일을 만듭니다. 그리고, 그 내용을 확인하여 광고 문구가 뒤에 추가되었으면 삭제해 줍니다(라인 수가 다르면 처리가 안됨) 

아래 메시지가 나오면 잠시 번역 결과를 한번 더 검토할 수 있습니다. 
```
D:\sample video ko.txt파일이 저장되었습니다.
[작업] 계속하려면 [Enter]를 누르거나 필요시 다음 파일을 편집할 수 있습니다: D:\sample video ko.txt
```

이 때 D:\sample video ko.txt파일을 열어서 DeepL 파일 번역 시 번역이 누락된 부분을 추가 번역하고 저장한 후 [Enter]를 누르면 작업이 완료됩니다.  

```
[정보] 새 자막이 저장되었습니다. D:\sample video ko.srt
[정보] 최종 자막이 저장되었습니다.
[정보] 완료하였습니다.
```

나중에 한국에도 유/무료 DeepL API가 공개된다면 이 기능도 자동화할 예정입니다. 그 외 사용법은 프로그램에서 출력하는 메시지를 잘 읽어보시기 바랍니다. 


[윈도우10/11 기준 준비 작업] 

1.파이썬 설치 
 
파이썬이 현재 3.11.3이 릴리즈 중이지만, 최신 버전이 그다지 중요하지 않으므로 아래 버전으로 설치를 합니다. 윈도우11의 명령 프롬프트나 파워쉘 아무데서나 python이라고 치면 실행될 수 있도록 하는 것이 목표입니다. 

https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

2.CUDA 설치

브라우저로 편리하게 이용이 가능한 Whisper WebUI판에서는 cuda 11.7을 requirements.txt에 명시를 해 놓아서 같은 버전으로 설치해 봅니다. 설치 완료 후 cuda가 설치되어 있는 지 확인하려면 파워쉘(Windows PowerShell 앱)을 띄우고, nvidia-smi 라고 명령을 내려 보면 알 수 있습니다.

https://developer.nvidia.com/cuda-11-7-1-download-archive?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local

3.파워쉘 실행

윈도우키를 누르고 R키를 누르면 좌측에 실행 창이 나타납니다. 이곳에 "powershell"을 입력하고 확인을 누르면 파워쉘을 실행할 수 있습니다(이외에 다양한 방법으로 실행 가능). 
 
파워쉘 창에서 python이라고 치고 [Enter]키를 누르면 다음과 같이 응답이 나와야 합니다. 
```
PS C:\Users\login_id> python

Python 3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
위 >>> 에서 나오기 위해서는 exit() 을 입력합니다. 

4.VENV 환경 만들어 주기 및 파이썬 패키지 설치하기 

파이썬은 패키지를 필요할 때마다 설치하게 되는데, 시스템에 설치된 파이썬에 그냥 설치하다보면 가끔 뭔가가 꼬이게 되고 문제가 가끔 생기는데 아주 머리가 아픈 경우가 있습니다. 물론, 이 기능만 이용하겠다하면 상관없지만 그래도 제거가 편하도록 가상의 환경을 만들어 줍니다. 

아래는 사용자 디렉터리에 그냥 설치했는데 다른 드라이브나 폴더에 해도 됩니다(주의: 경로 상에 한글이 없는 곳에서 작업해주세요. 혹시 윈도우 로그인명이 한글이라면 다른 곳에 설치가 필요합니다.)

용량이 4.5GB가량 되므로 적절한 디스크 드라이브에 설치하시면 좋습니다. 
```
PS C:\Users\login_id> python -m venv venv 
PS C:\Users\login_id> .\venv\Scripts\Activate.ps1 
```
위와 같이 해주면, 가상 환경 준비가 끝납니다. 처음에 실행할 때 보안 관련 문의가 나오는데 Always를 선택해 줍니다. venv가 성공적으로 실행되면 프롬프트가 바뀝니다. 이 상태에서 필요한 패키지들을 설치합니다. 
```
(venv) PS C:\Users\login_id> pip install -U git+https://github.com/jianfch/stable-ts.git
(venv) PS C:\Users\login_id> pip install git+https://github.com/openai/whisper.git
(venv) PS C:\Users\login_id> pip install python-docx
(venv) PS C:\Users\login_id> pip install pysub-parser
```

5.GPU버전의 pyTorch설치 

위 과정이 끝나면 바로 쓸 수 있기는 한데, CPU버전의 pyTorch가 설치되는 것 같습니다. 이번에는 GPU버전의 토치를 설치합니다. 
```
(venv) PS C:\Users\login_id> pip install torch==2.0.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
```
잘 설치가 되었는 지 확인하기 위해 python을 입력하고 간단한 프로그램을 짭니다. (주의) "__version__" 은 글자의 좌우에 언더바가 2개씩 있습니다. 
```
(venv) PS C:\Users\login_id> python
Python 3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> print(torch.__version__)
2.0.1+cu117
>>> exit()
```
6.FFMPEG 설치 및 파이썬 인터프리터 상태에서 영상 자막 만들기 

영상에서 음성을 추출을 하다보니 외부 프로그램이 하나 필요합니다.  

https://www.gyan.dev/ffmpeg/builds/#release-builds 에서 ffmpeg-release-essentials.zip 을 받아서 압축 해제한 후, 앞으로 작업할 디렉터리나 환경변수에서 Path가 설정되어 있는 곳에 복사하여도 됩니다. 그냥 C:\Users\login_id\venv\Scripts 밑에 복사하는 것이 속편하겠습니다. 짧은 영상 하나를 테스트하는 과정을 보여드립니다(실제로는 중간에 warning이 나오지만 작동에 문제는 없습니다). 
```
(venv) PS C:\Users\login_id> python
Python 3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> import stable_whisper
>>> model = stable_whisper.load_model("small", device="cuda")
>>> result = model.transcribe(verbose=True, word_timestamps=False, language="ko", audio="20220902_131203.mp4")
[00:12.800 --> 00:16.080]  아 아까 딱 찍었어야 되는데
[00:19.580 --> 00:21.580]  불행랑을 치는 걸 찍었어야 되는데
[00:30.000 --> 00:34.980]  진출하되겠지
>>> result.to_srt_vtt("20220902_131203.srt")
Saved: C:\Users\login_id\20220902_131203.srt
>>> exit()
```
word_timestamps=True가 기본 값인데, 말하는 중 단어가 하이라이트 되는 기능이 있습니다. 2GB의 VRAM을 가진 그래픽카드라서 small 모델로 했는데, 몇 마디(불행랑->줄행랑, 진출하되겠지는 그냥 파도 소리가 자막화 되었네요)는 잘못 인식했네요.  8GB VRAM이라면 medium으로 하면 됩니다. 

7.명령어로 자막 생성해보기 

이번에는 word_timestamps 옵션과 verbose 도 뺍니다(자세한 인자들은 stable-ts [Enter]를 해보시면 나열 됩니다).  
```
(venv) PS C:\Users\login_id > stable-ts --model small --device cuda --output_format srt --language ko .\20220902_131203.mp4
```
.\20220902_131203.srt already exist, overwrite (y/n)? y

Loaded Whisper small model

100%|███████████████████████████████████████████████████████████████████████████| 36.01/36.01 [00:37<00:00,  1.04s/sec]

Saved: C:\Users\login_id\20220902_131203.srt
```
0
00:00:00,520 --> 00:00:13,100
<font color="#00ff00">아</font> 아까 딱 찍었어야 되는데

1
00:00:13,100 --> 00:00:13,420
아 <font color="#00ff00">아까</font> 딱 찍었어야 되는데

2
00:00:13,420 --> 00:00:14,460
아 아까 <font color="#00ff00">딱</font> 찍었어야 되는데

3
00:00:14,460 --> 00:00:15,020
아 아까 딱 <font color="#00ff00">찍었어야</font> 되는데

4
00:00:15,020 --> 00:00:15,380
아 아까 딱 찍었어야 <font color="#00ff00">되는데</font>

5
00:00:15,380 --> 00:00:20,120
<font color="#00ff00">불행랑을</font> 치는 걸 찍었어야 되는데

6
00:00:20,120 --> 00:00:20,320
불행랑을 <font color="#00ff00">치는</font> 걸 찍었어야 되는데

7
00:00:20,320 --> 00:00:20,380
불행랑을 치는 <font color="#00ff00">걸</font> 찍었어야 되는데

8
00:00:20,380 --> 00:00:20,740
불행랑을 치는 걸 <font color="#00ff00">찍었어야</font> 되는데

9
00:00:20,740 --> 00:00:21,020
불행랑을 치는 걸 찍었어야 <font color="#00ff00">되는데</font>

10
00:00:30,000 --> 00:00:34,880
<font color="#00ff00">요</font> biết은 괜찮은 건가?

11
00:00:34,880 --> 00:00:35,900
요 <font color="#00ff00">biết은 괜찮은 건가?</font>

12
00:00:35,900 --> 00:00:36,000
<font color="#00ff00">그게</font> 
```

8.subtitle-extractor.py 받아서 이용하기  

만약 git를 설치해 두었다면 아래와 같이 받으면 됩니다. 그렇지 않다면 https://github.com/sevengivings/subtitle-extractor에 접속해서 우측에 "<> CODE"라는 명령버튼이 보입니다. 버튼을 누르면 Download ZIP 메뉴를 통해 압축 파일로 받을 수 있고, 적당한 곳에 압축 해제한 후 이용할 수 있습니다.

```
(venv) C:\Users\login_id> git clone https://github.com/sevengivings/subtitle-extractor
```

(주의) 만약 한글로 된 안내 메시지를 보려면 압축 파일의 locales 디렉토리도 필요합니다. 


[단일 exe로 만들기] 

지금까지는 python .\subtitle-extractor.py로 실행을 했습니다. 다소 불편하므로 exe파일로 만든 후, venv\Scripts에 복사하여 아무 드라이브나 디렉토리에서도 실행할 수 있도록 해보겠습니다. 

```
(venv) C:\Users\login_id> pip install pyinstaller
(venv) C:\Users\login_id> pyinstaller --onefile .\subtitle-extractor.py 
```

위 결과로 나오는 C:\Users\login_id\dist\subtitle-extractor.exe를 C:\Users\login_id\venv\Scripts로 복사하면 됩니다. 이제 venv를 활성화만 시키면 어느 곳에서나 실행이 가능해집니다. 

위 방식으로 만들면 약 2.4GB의 크기를 가지고 있어서 만들어지는데 오래 걸립니다. 
