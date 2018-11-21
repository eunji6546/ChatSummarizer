import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import ChatSummarize

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('chat_summarizer.html')

@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if request.method == 'POST':  # POST request
        chat = request.form['chatField']
        # chat = post_params['chatField']
        chatSummarizer = ChatSummarize.ChatSummarizer(chat)
        chatSummarizer.preprocess()
        summary = chatSummarizer.summarize(4)
        return render_template('summarize.html', summary=summary)

    else: # GET request
        return render_template('chat_summarizer.html')

if __name__ == '__main__':
    app.run()