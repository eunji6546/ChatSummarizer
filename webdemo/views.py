import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from django.shortcuts import render
from .models import Chat
from .forms import ChatForm
import ChatSummarize

def chat_summarize(request):
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            text = form.save(commit=False)
            chatSummarizer = ChatSummarize.ChatSummarizer(text.chat)
            chatSummarizer.preprocess()
            summary = chatSummarizer.summarize(4)
            return render(request, 'webdemo/chat_summarize.html', {'form': form, 'summary': summary})
    else:
        form = ChatForm()
    return render(request, 'webdemo/chat_summarize.html', {'form': form})
