[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/sevengivings/subtitle-extractor/blob/main/README.en.md)
# What's in this repository  

- subtitle-extractor.py : Tools for creating foreign video (audio) subtitles. User can translate text via DeepL(or else) app/web file translation service manually. DeepL API translation is also possible if you provide DEEPL_API_KEY environmental variable.   
- subtitle-intermediatefile-joiner.py : Tool to recombine SRT subtitles that have been separated into time(.time) and text(.txt)
- subtitle-translator-deepl-rapidapi.py : Tool to translate SRT subtitles via the DeepL(rapidapi) translation API
- subtitle-translator-google.py : Tool to translate SRT subtitles via Google Cloud translation API
- subtitle-translator-papago.py : Tool to translate SRT subtitles via Naver Papago translation API 
- subtitle-util.py : Simple utility SRT translation using DeepL App file translation, unlike above scripts it use pysubparser.

To remove meaningless or ghost subtitles during transcribing, I decoded a .SRT format by myself and remove too short or repeated subtitles. 

You can find another Python script(transcription using Whisper or stable-ts and automatic translation using various translation APIs) => https://github.com/sevengivings/subtitle-xtranslator     

# subtitle-extractor

A Python script for AI speech recognition of video or audio file using Whisper or stable-ts and translation subtitle using DeepL app or web file translation. DeepL API translation is also possible if you provide DEEPL_API_KEY environmental variable(2023-08-17 update). 

## [Overview] 

MP4/MP3 file -> .SRT subtitle file -> filtering unnecessary subtitle(too short and meaningless repeated) -> time sync data(.time) & subtitle text data(.docx & .txt) -> user intervention for manual translation using DeepL file translation(translated .docx) or translated .txt using another method -> (optional)translated .docx to translated .txt -> join .time and .txt to .srt 

if you provide your own DEEPL_API_KEY environmental variable, subtitle-extractor.py will translate subtitles automatically. (ex: in PowerShell, Set-Item -Path env:DEEPL_API_KEY -Value "YOUR_DEEPL_API_KEY")  

OpenAI의 Whisper와 자막을 위해 조금 변형한 stable-ts를 사용하여 비디오 AI 음성 인식 및 번역 과정을 자동화하기 위한 파이썬 프로그램입니다. 다만 아직까지는 번역할 때에는 성능이 가장 좋아 보이는 DeepL을 통해 파일 번역을 수동으로 하게 되는데, .SRT 자막을 그대로 번역시키면 시각정보 부분에 문제가 생길 수 있어서 텍스트만 따로 .docx로 저장해주는 기능을 가지고 있습니다. 그러한 일련의 작업 과정을 최대한 편리하게 구성해 본 프로그램입니다.   

만약 DEEP_API_KEY 환경 변수를 제공하면 수동 번역 필요 없이 자동으로 API 번역을 실행합니다(예: 파워쉘에서는 Set-Item -Path env:DEEPL_API_KEY -Value "YOUR_DEEPL_API_KEY").  

## [주요 기능] 

* MP4에서 자막 직접 추출 기능(stable-ts와 Whisper 중 선택 가능)
* 파일 번역을 위하여 .docx 형태로 자막 텍스트만 저장(시간 정보는 .time 파일로 분리)
* DeepL 앱을 이용한 수동 번역 혹은 DeepL API를 이용한 자동 번역 지원 
* 불필요한 한 글자나 의미 없는 두 글자의 자막을 삭제하는 기능
* 같은 말이 반복될 때 첫번째 자막만 사용 
* 여러 줄의 자막을 한 줄로 합치는 기능

## [한계]

- 음성 인식이 완전하지 않아서 누락되는 음성이나 잘못 인식될 수 있습니다. 프로페셔널한 용도로 사용은 권장하지 않습니다. 
- stable-ts와 whisper 명령어로 했을 때와 이 프로그램을 사용했을 때, Whisper WebUI를 썼을 때 각각 자막의 품질이나 개수가 다를 수 있습니다(최적화 파라미터가 다양하며, 참고로 stable-ts는 자막 추출 용도로 최적화한 프로그램이기도 하지만 Whisper 오리지널에 비해 인식 누락이 있는 편입니다. 하지만, 없는데 추출된 귀신 소리, 무의미한 반복, 뒷부분 추출 안되는 등의 문제는 적은 편입니다.)
- 유료 API를 사용할 경우 사전에 본 프로그램을 충분히 테스트한 후에 이용하시기 바랍니다. 이 스크립트의 사용 시에 발생하는 알 수 없는 오류나 잠재된 버그로 인해 생기는 각종 피해에 대해 어떠한 책임도 지지 않습니다. 

## [관련 프로그램 링크] 

- stable-ts : GitHub - jianfch/stable-ts: ASR with reliable word-level timestamps using OpenAI's Whisper(https://github.com/jianfch/stable-ts) 
- Whisper : General-purpose speech recognition model(https://github.com/openai/whisper)
- DeepL : AI translation(https://www.deepl.com/translator), API(https://www.deepl.com/pro-api?cta=header-pro-api)

## [2023-08-17 수정 사항] 

- 우리나라에 정식 오픈한 DeepL API 번역 기능을 추가하였습니다. 파워쉘의 경우 Set-Item -Path env:DEEPL_API_KEY -Value "여러분의 DEEPL API KEY" 환경 변수를 설정하면, 자동으로 번역이 이루어집니다. 개발자용 무료 버전에서는 50만자/월까지 무료로 이용 가능합니다. 
- --framework를 추가하여, stable-ts 혹은 whisper를 미리 선택할 수 있습니다. 이 옵션을 사용하지 않으면 추가 입력을 받아서 처리합니다(기존과 동일한 방법으로 작동). 
- --audio_language는 --language로 변경하고, 기본은 언어 자동 인식으로 변경했습니다. 30초간 말이 없는 경우 인식에 실패하므로 --language 뒤에 en, ko, ja, fr 등 키워드를 넣으면 좋습니다.
- stable-ts를 위하여 --demucs, --vad, --vad_threshold, --mel_first 옵션을 사용할 수 있습니다.
- --condition_on_previous_text 값은 False로 기본값을 다시 복구했습니다. 

## [사용법]

Whisper나 stable-ts의 경우 많은 옵션을 줄 수 있지만, 본 스크립트에서는 가장 기본적인 것만 사용하였습니다. 만약 상세한 옵션이 필요하다면 소스 코드를 수정해야 합니다. 

다음은 도움말을 알아보는 예시입니다. 

```
인공지능 음성추출 및 DeepL 수동 혹은 API번역 도우미

usage: subtitle-extractor.py [-h] [--framework FRAMEWORK] [--model MODEL] [--device DEVICE] [--language LANGUAGE]
                             [--subtitle_language SUBTITLE_LANGUAGE] [--skip_textlength SKIP_TEXTLENGTH]
                             [--condition_on_previous_text] [--demucs] [--vad] [--vad_threshold VAD_THRESHOLD]
                             [--mel_first]
                             audio

positional arguments:
  audio                 음성추출에 사용할 파일의 전체 경로를 입력합니다.

options:
  -h, --help            show this help message and exit
  --framework FRAMEWORK
                        음성추출에 사용할 방법을 stable-ts와 whisper중에 고릅니다. (default: none)
  --model MODEL         번역 모델을 선택합니다. tiny, base, small, medium, large 등 (default: medium)
  --device DEVICE       cuda 혹은 cpu를 선택합니다. (default: cuda)
  --language LANGUAGE   입력 파일의 언어를 지정합니다. 생략하면 앞쪽 30초 기반으로 자동 판단합니다. (default: None)
  --subtitle_language SUBTITLE_LANGUAGE
                        subtitle target language need only if you plan to use DeepL file translation (default: ko)
  --skip_textlength SKIP_TEXTLENGTH
                        길이가 아주 짧은 자막, 즉 의미없는 자막 삭제에 유용합니다. (default: 1)
  --condition_on_previous_text
                        True를 주면 이전에 사용한 모델 출력을 다음 구간 입력에 활용하며; False일 경우 구간 사이의 문장  불일치는 생기지만, 번역이 루프에 빠지는 오류는 줄어들 수 있습니다. (default: False)
  --demucs              stable-ts 전용이며 사람 음성과 잡음의 분리를 위해 demucs로 전처리 합니다. 추가 설치 필요: pip install demucs PySoundFile
                        https://github.com/facebookresearch/demucs (default: False)
  --vad                 stable-ts 전용, Silero VAD를 사용하여 timestamp 억제를 할 지 선택합니다. 추가 설치 필요: pip install
                        silerohttps://github.com/snakers4/silero-vad (default: False)
  --vad_threshold VAD_THRESHOLD
                        stable-ts 전용, Silero VAD를 적용 시 음성 추출 기준을 설정합니다. 낮은 값은 무음 탐지 시 잘못된 탐지를 줄여줍니다. (default: 0.2)
  --mel_first           stable-ts 전용, log-Mel 스펙트럼을 사용하여 전체 오디오를 처리합니다. whisper보다 음성 추출이 좋지 않다고 판단되면 이용하세요. 오디오/비디오가 긴 경우 GPU메모리가 부족할 수 있습니다. (default: False)
``` 

이제 'sample video.mp4' 비디오의 자막을 추출하려면 다음과 같이 하면 됩니다. 

```
(venv) PS C:\Users\login_id> python .\subtitle-extractor.py --language ja 'D:\videos\sample video.mp4'     
```

(생략할 경우 기본값 설정) --framework None --model medium --device cuda --language None --subtitle_language kr --skip-textlength 1

--skip-textlength 뒤에 있는 숫자 1은 1글자 자막을 무시하겠다는 의미입니다.
--language 입력 비디오/오디오의 언어를 지정합니다. 

기본 값은 None으로 되어 있으므로 만약 비디오의 언어가 영어라면 --language en 을 추가해 주어야 됩니다. 자동 인식의 경우 비디오/오디오 앞 30초 내에 음성이 없으면 인식이 실패합니다. 

DEEPL_API_KEY를 제공하지 않으면 위 명령은 다음과 같이 수동 번역을 하게 되며 아래와 같이 진행합니다. 

```
인공지능 음성추출 및 DeepL 수동 혹은 API번역 도우미


framework: none
model:medium
device:cuda
audio language:ja
subtitle language:ko
igonore n characters:1
audio:D:\videos\DDFF-027_cut_cut.mp4

Python version: 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.1934 64 bit (AMD64)]
Torch version: 2.0.1+cu118

[입력] 음성추출 방법을 선택하세요. stable-ts는 1, Whisper는 2를 입력합니다.
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

DEEPL_API_KEY를 제공한 경우에는 위 과정이 생략되고 아래와 같이 수행이 됩니다. 

```
Saved: D:\sample video.srt
[정보] 전체 자막 길이:  214
[정보] DeepL API 키가 환경변수에 있습니다.
[정보] DeepL API 파일 번역이 시작되었습니다. 완료할 때까지 기다려 주세요.
Character usage: 350000 of 500000
D:\videos\sample video ko.txt 파일이 저장되었습니다.
[정보] DeepL API 파일 번역이 완료되었습니다.
[정보] 새 자막이 저장되었습니다. D:\videos\sample video ko.srt
[정보] 최종 자막이 저장되었습니다.
[정보] 완료하였습니다.
```

참고로, deepl-rapidapi로 구현한 프로그램 추출 및 번역 파이썬 스크립트는  https://github.com/sevengivings/subtitle-xtranslator 를 참조해 주세요. 여러 파일을 배치로 처리하는 기능과 다양한 번역기를 사용하는 기능은 subtitle-xtranslator 에서만 이용 가능합니다.   

그 외 본 스크립트의 사용법은 프로그램에서 출력하는 메시지를 잘 읽어보시기 바랍니다. 

* 실제 사용 동영상 보기(수동 번역) - https://www.youtube.com/watch?v=l8FUgq_4XTE


## [윈도우10/11 기준 준비 작업] 

### 1.파이썬 설치 
 
윈도우11의 명령 프롬프트나 파워쉘 아무데서나 python이라고 치면 실행될 수 있도록 하는 것이 목표입니다. 

https://www.python.org/downloads 
https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe

### 2.CUDA 설치

최신 판을 찾아서 설치합니다. 설치 완료 후 cuda가 설치되어 있는 지 확인하려면 파워쉘(Windows PowerShell 앱)을 띄우고, nvidia-smi 라고 명령을 내려 보면 알 수 있습니다.

https://developer.nvidia.com/cuda-toolkit
https://developer.download.nvidia.com/compute/cuda/12.2.1/local_installers/cuda_12.2.1_536.67_windows.exe

### 3.파워쉘 실행

윈도우키를 누르고 R키를 누르면 좌측에 실행 창이 나타납니다. 이곳에 "powershell"을 입력하고 확인을 누르면 파워쉘을 실행할 수 있습니다(이외에 다양한 방법으로 실행 가능). 
 
파워쉘 창에서 python이라고 치고 [Enter]키를 누르면 다음과 같이 응답이 나와야 합니다. 
```
PS C:\Users\login_id> python

Python 3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
위 >>> 에서 나오기 위해서는 exit() 을 입력합니다. 

### 4.VENV 환경 만들어 주기 및 파이썬 패키지 설치하기 

파이썬은 패키지를 필요할 때마다 설치하게 되는데, 시스템에 설치된 파이썬에 그냥 설치하다보면 가끔 뭔가가 꼬이게 되고 문제가 가끔 생기는데 아주 머리가 아픈 경우가 있습니다. 물론, 이 기능만 이용하겠다하면 상관없지만 그래도 제거가 편하도록 가상의 환경을 만들어 줍니다. 

아래는 사용자 디렉터리에 그냥 설치했는데 다른 드라이브나 폴더에 해도 됩니다(주의: 경로 상에 한글이 없는 곳에서 작업해주세요. 혹시 윈도우 로그인명이 한글이라면 다른 곳에 설치가 필요합니다.)

용량이 4.5GB가량 되므로 적절한 디스크 드라이브에 설치하시면 좋습니다. 

```
PS C:\Users\login_id> python -m venv venv 
PS C:\Users\login_id> .\venv\Scripts\Activate.ps1 
```

만약 .ps1가 실행이 안되면 파워쉘을 관리자 권한으로 실행한 후, 아래 명령을 한번 실행해 줍니다. 

```
PS C:\WINDOWS\system32> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```


위와 같이 해주면, 가상 환경 준비가 끝납니다. 처음에 실행할 때 보안 관련 문의가 나오는데 Always를 선택해 줍니다. venv가 성공적으로 실행되면 프롬프트가 바뀝니다. 

### 5.GPU버전의 pyTorch설치 

GPU버전의 토치를 설치합니다. 
```
(venv) PS C:\Users\login_id> pip install torch==2.0.1+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
```

잘 설치가 되었는 지 확인하기 위해 python을 입력하고 간단한 프로그램을 짭니다. (주의) "__version__" 은 글자의 좌우에 언더바가 2개씩 있습니다. 

```
(venv) PS C:\Users\login_id> python
Python 3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> print(torch.__version__)
2.0.1+cu118
>>> exit()
```

이 상태에서 향후 필요한 패키지들을 설치합니다. 아래의 git+ 명령을 쓰려면 https://git-scm.com/download/win 의 설치가  필요합니다. 

```
(venv) PS C:\Users\login_id> pip install -U git+https://github.com/jianfch/stable-ts.git
(venv) PS C:\Users\login_id> pip install git+https://github.com/openai/whisper.git
(venv) PS C:\Users\login_id> pip install python-docx
```

subtitle-util.py를 사용한다면 pysub-parser가 필요하고, subtitle-translator-google.py에는 google-cloud-translate==2.0.1가 필요합니다. 

```
(venv) PS C:\Users\login_id> pip install pysub-parser
(venv) PS C:\Users\login_id> pip install google-cloud-translate==2.0.1
```

### 6.FFMPEG 설치 및 파이썬 인터프리터 상태에서 영상 자막 만들기 

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

### 7.명령어로 자막 생성해보기 

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

### 8.subtitle-extractor.py 받아서 이용하기  

만약 git를 설치해 두었다면 아래와 같이 받으면 됩니다. 그렇지 않다면 https://github.com/sevengivings/subtitle-extractor 에 접속해서 우측에 "<> CODE"라는 명령버튼이 보입니다. 버튼을 누르면 Download ZIP 메뉴를 통해 압축 파일로 받을 수 있고, 적당한 곳에 압축 해제한 후 이용할 수 있습니다.

```
(venv) C:\Users\login_id> git clone https://github.com/sevengivings/subtitle-extractor
```

(주의) 만약 한글로 된 안내 메시지를 보려면 압축 파일의 locales 디렉토리도 필요합니다. 

## [stable-ts의 옵션 관련] 

stable-ts는 위의 오리지널 Whisper를 조금 더 수정해서 자막 제작에 좀 더 특화되었다고 하는데 깃헙에 써 있는 메모를 번역해 보면, 

- regroup=True를 통해 세그먼트 나눌 때 좀 더 자연스러운 경계로 하고, 
- suppress_silence=True를 통해 시각정보 정확도를 올리고 침묵 구간 처리를 더 잘하고, 
- demucs=True는 원래 음악용인데 음악이 없을 때에도 잘 작동한다고 합니다
- 세그먼트 시각정보 신뢰성을 높이려면 word_timestamp는 false로 하지 말라고 합니다. -> 자막 파일이 너무 커지므로 false로 해야합니다. 
- Whisper보다 못하다고 느껴지면 mel_first=True 등등라고 합니다. 

그외에 demucs와 vad에 대해 잠시 더 언급하자면, 

- demucs 옵션을 사용하기 위해서는 pip install demucs PySoundFile, vad를 위해서는 pip install silero 가 필요합니다.
- demucs 옵션을 켠 경우 긴 파일을 처리하기 위해서는 8GB VRAM이 부족한 것 같습니다.
- vad와 demucs 모두 처리하는 데 몇 분 가량 추가 소요가 되는데 일단은 메모리와 시간 문제로 접어두어야 할 듯합니다.


## [단일 exe로 만들기] 

지금까지는 python .\subtitle-extractor.py로 실행을 했습니다. 다소 불편하므로 exe파일로 만든 후, venv\Scripts에 복사하여 아무 드라이브나 디렉토리에서도 실행할 수 있도록 해보겠습니다. 

```
(venv) C:\Users\login_id> pip install pyinstaller
(venv) C:\Users\login_id> pyinstaller --onefile .\subtitle-extractor.py 
```

위 결과로 나오는 C:\Users\login_id\dist\subtitle-extractor.exe를 환경변수에 경로(PATH)가 잡혀 있는 디렉터리로 복사하면 됩니다. 이제 venv와 관계없이 어느 곳에서나 실행이 가능해집니다. 

위 방식으로 만들면 약 2.4GB의 크기를 가지고 있어서 만들어지는데 오래 걸립니다. 
