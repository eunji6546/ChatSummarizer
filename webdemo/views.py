from django.shortcuts import render
from .models import Chat

def chat_summarize(request):
    return render(request, 'webdemo/chat_summarize.html', {})