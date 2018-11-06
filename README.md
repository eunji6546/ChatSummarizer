
# MOSP document 
[MOSP google docs](https://docs.google.com/document/d/13Y9vXj0-o8YUrPARlkWuKreQxLOW5cpRHh8oMSqnMd4/edit)

# 구성 
### Token-Sentence Converter
채팅의 특성상 여러 토막으로 나뉘어 있는 대화 내용을 온전한 문장으로 이어준다. 시간 및 화자의 고려가 필요 
### Coined-Word Converter
위키피디아의 ‘대한민국의 인터넷 신조어 목록’ 문서를 파싱하여 문장 내에 있는 인터넷 신조어를 적절한 사전에 있는 어휘로 대체시킴 
### Noise Detector
대화 내용의 요약에 필요 없는 의미 없는 노이즈들을 제거하여 Spelling Checker로 넘겨준다. 노이즈에는 초성어(ㅋㅋ, ㅠㅠ 등)와 사진, 동영상, 이모티콘 등이 포함된다. 이런 노이즈들은 내용의 요약 자체에는 의미를 가지지 않지만 초성어의 빈도수와 같은 특성은 이전 대화 내용의 중요도 지표로 활용될 수 있기 때문에 따로 저장하여 Additional Feature Generator로 넘겨준다.
### Spelling Checker
형태소 분리를 하기 위한 전처리 단계로 대화 내용의 맞춤법을 교정한다. 네이버 맞춤법 검사기를 활용한 파이썬 한글 맞춤법 검사 라이브러리인 py-hanspell을 활용한다.-> 부산대 맞춤법 교정기를 사용한다. 
### KoNLPy
한국어 자연어 처리를 할 수 있는 파이썬 패키지, KoNLPy를 이용해 맞춤법이 교정된 문장을 형태소로 분리해 LexRank Algorithm과 Additional feature Generator에 넘겨준다. 
### LexRank Algorithm
LexRank 기반 한국어 다중 문서 요약 라이브러리인 lexrankr를 사용해서 각 문장을 scoring 한다. lexrankr 라이브러리의 경우에 대화 text 전체를 한번에 input으로 받은 뒤, 요약된 결과만을 출력해준다. 따라서 해당 라이브러리를 수정하여 우리가 대화의 형태소 분석을 한 결과를  input으로 주고 이를 이용해 계산을 할 수 있도록 한다. 또한 계산 결과를 각각의 문장에 대한 score 배열로 받아올 수 있도록 한다.

# Done

# TODO

# Plans 
- 11/6 : 데이터 만들기 
