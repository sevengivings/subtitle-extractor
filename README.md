# subtitle-extractor

A Python program to automate the video AI speech recognition and translation process. Comments and messages are in Korean.

OpenAI의 Whisper와 자막을 위해 조금 변형한 stable-ts를 사용하여 비디오 AI 음성 인식 및 번역 과정을 자동화하기 위한 파이썬 프로그램입니다. 

stable-ts : GitHub - jianfch/stable-ts: ASR with reliable word-level timestamps using OpenAI's Whisper(https://github.com/jianfch/stable-ts) 

Whisper : General-purpose speech recognition model(https://github.com/openai/whisper)

Usage: python .\subtitle-extractor.py 'd:\sammple video.mp4' 1 

도중에 프로그램이 입력을 기다리기 위해 멈추는데, 이 때 무료 DeepL 웹/앱 번역기에서 .docx를 수동으로 파일 번역해 준 후 [Enter]를 누르면 번역된 자막이 생성됩니다. 나중에 한국에도 DeepL API가 공개된다면 이 기능도 자동화할 예정입니다. 그 외 사용법은 프로그램에서 출력하는 메시지를 잘 읽어보시기 바랍니다. 

[주요 기능] 

* MP4에서 자막 직접 추출 기능(stable-ts와 Whisper 중 선택 가능)
* 불필요한 한 글자나 두 글자의 자막을 삭제하는 기능
* 같은 말이 반복될 때 첫번째 자막만 사용 
* 여러 줄의 자막을 한 줄로 합치는 기능

[한계]

- 음성 인식이 완전하지 않아서 누락되는 음성이나 잘못 인식될 수 있습니다. 프로페셔널한 용도로 사용은 권장하지 않습니다. 
- stable-ts와 Whisper로 했을 때 자막이 다를 수 있습니다(이 프로그램은 기본적인 옵션만 있음).

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

PS C:\Users\login_id> python

Python 3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>

위 >>> 에서 나오기 위해서는 exit() 을 입력합니다. 

4.VENV 환경 만들어 주기 및 파이썬 패키지 설치하기 

파이썬은 패키지를 필요할 때마다 설치하게 되는데, 시스템에 설치된 파이썬에 그냥 설치하다보면 가끔 뭔가가 꼬이게 되고 문제가 가끔 생기는데 아주 머리가 아픈 경우가 있습니다. 물론, 이 기능만 이용하겠다하면 상관없지만 그래도 제거가 편하도록 가상의 환경을 만들어 줍니다. 아래는 사용자 디렉터리에 그냥 설치했는데 다른 드라이브나 폴더에 해도 됩니다(주의: 경로 상에 한글이 없는 곳에서 작업해주세요. 혹시 윈도우 로그인명이 한글이라면 다른 곳에 설치가 필요합니다.) 

PS C:\Users\login_id > python -m venv venv 

PS C:\Users\login_id > .\venv\Scripts\Activate.ps1 

위와 같이 해주면, 가상 환경 준비가 끝납니다. 처음에 실행할 때 보안 관련 문의가 나오는데 Always를 선택해 줍니다. venv가 성공적으로 실행되면 프롬프트가 바뀝니다. 이 상태에서 필요한 패키지들을 설치합니다. 

(venv) PS C:\Users\login_id > pip install -U git+https://github.com/jianfch/stable-ts.git

(venv) PS C:\Users\login_id > pip install git https://github.com/openai/whisper.git

(venv) PS C:\Users\login_id > pip install python-docx

(venv) PS C:\Users\login_id > pip install pysub-parser


5.GPU버전의 pyTorch설치 

위 과정이 끝나면 바로 쓸 수 있기는 한데, CPU버전의 pyTorch가 설치되는 것 같습니다. 이번에는 GPU버전의 토치를 설치합니다. 

(venv) PS C:\Users\login_id > pip install torch==2.0.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117

잘 설치가 되었는 지 확인하기 위해 python을 입력하고 간단한 프로그램을 짭니다. __version__ 은 언더바가 2개씩 좌우로 있습니다. 

(venv) PS C:\Users\login_id> python

Python 3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.

>>> import torch

>>> print(torch.__version__)

2.0.1+cu117

>>> exit()

6.FFMPEG 설치 및 파이썬 인터프리터 상태에서 영상 자막 만들기 

영상에서 음성을 추출을 하다보니 외부 프로그램이 하나 필요합니다.  

 https://www.gyan.dev/ffmpeg/builds/#release-builds 에서 ffmpeg-release-essentials.zip 을 받아서 압축 해제한 후, 앞으로 작업할 디렉터리나 환경변수에서 Path가 설정되어 있는 곳에 복사하여도 됩니다. 그냥 C:\Users\login_id\venv\Scripts 밑에 복사하는 것이 속편하겠습니다. 짧은 영상 하나를 테스트하는 과정을 보여드립니다(실제로는 중간에 warning이 나오지만 작동에 문제는 없습니다). 
 
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

word_timestamps=True가 기본 값인데, 말하는 중 단어가 하이라이트 되는 기능이 있습니다. 2GB의 VRAM을 가진 그래픽카드라서 small 모델로 했는데, 몇 마디(불행랑->줄행랑, 진출하되겠지는 그냥 파도 소리가 자막화 되었네요)는 잘못 인식했네요.  8GB VRAM이라면 medium으로 하면 됩니다. 

7.명령어로 자막 생성해보기 

이번에는 word_timestamps 옵션과 verbose 도 뺍니다(자세한 인자들은 stable-ts [Enter]를 해보시면 나열 됩니다).  

(venv) PS C:\Users\login_id > stable-ts --model small --device cuda --output_format srt --language ko .\20220902_131203.mp4

.\20220902_131203.srt already exist, overwrite (y/n)? y
Loaded Whisper small model
100%|███████████████████████████████████████████████████████████████████████████| 36.01/36.01 [00:37<00:00,  1.04s/sec]
Saved: C:\Users\login_id\20220902_131203.srt

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
