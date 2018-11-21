import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import ChatSummarize

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('summarize.html')


@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if request.method == 'POST':  # POST request
        chat = request.form['chatField']
        chatSummarizer = ChatSummarize.ChatSummarizer(chat)
        chatSummarizer.preprocess()
        summary = chatSummarizer.summarize(4)
        return render_template('summarize.html', summary=summary)

    else: # GET request
        return render_template('summarize.html')


@app.route('/highlight', methods=['GET', 'POST'])
def highlight():
    if request.method == 'POST':  # POST request
        chat = request.form['chatField']
        chatSummarizer = ChatSummarize.ChatSummarizer(chat)
        chatSummarizer.preprocess()
        highlight = chatSummarizer.highlight()
        return render_template('highlight.html', highlight=highlight)

    else: # GET request
        return render_template('highlight.html')


if __name__ == '__main__':
    app.run()