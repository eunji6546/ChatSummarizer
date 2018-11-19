import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from django.shortcuts import render
from .models import Chat
from .forms import ChatForm
import ChatSummarize

from konlpy import jvm
from konlpy.tag import Twitter
import jpype

def chat_summarize(request):
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            text = form.save(commit=False)
            if jpype.isJVMStarted():
	            jpype.attachThreadToJVM()
            konl = Twitter()
            test_string = [
                u'konlpy 사용시 주의 사항',
                u'자바 설치 및 세팅 필요',
                u'JAVA_HOME 세팅이 필요합니다.',
                u'export JAVA_HOME=$(/usr/libexec/java_home)',
            ]
            for row in test_string:
                r = konl.pos(row, norm=True, stem=True)
                print('=' * 20)
                for txt, post in r:
                    print(txt, post)
                print('=' * 20)
            # chatSummarizer = ChatSummarize.ChatSummarizer(text.chat)
            # chatSummarizer.preprocess()
            # summary = chatSummarizer.summarize(4)
            return render(request, 'webdemo/chat_summarize.html', {'form': form, 'summary': summary})
    else:
        form = ChatForm()
    return render(request, 'webdemo/chat_summarize.html', {'form': form})
