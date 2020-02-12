# **copytrans**

CopyTrans는 간단한 파이썬 스크립트로 수행되고 있는 도중에 클립보드의 텍스트 변화를

감지하여 구글 번역기로 변역해 표시해 주는 역할을 합니다.

클리앙의 stargen님 프로그램을 사용하다가 사용가능한 단어길이가 짧아 만들어 보았습니다.

<https://www.clien.net/service/board/pds/9071993>

## **Requirement**

### **Windows**

- Output 폴더내의 exe파일을 그대로 수행하시면 됩니다.

### **Others**

- python3
- pip module: pyperclip, googletrans, beautifulsoup4, requests
- **MAC**: pbcopy, pbpaste 명령어 사용
- **LINUX**: xclip or xel, qtk or pyqt4

## **사용방법**

1. 스크립트 or exe를 실행한다.
2. 번역하고자 하는 Text를 복사한다.
3. 복사한 Text가 문장일 경우 Google 번역을 진행
4. 복사한 Text가 단어일 경우 Daum Dict 검색을 진행

## **History**

- Search Box Added
- Daum Dictionary Search Added
- Initaial Upload

# TODO

- [x]  Search 가능하도록 수정