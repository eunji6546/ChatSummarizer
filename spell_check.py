from bs4 import BeautifulSoup
import requests

url = "http://speller.cs.pusan.ac.kr/PnuWebSpeller/lib/check.asp"

def check(text):
    data = {"text1": text.encode('utf-8')}
    response = requests.post(url=url, data=data)

    soup = BeautifulSoup(response.text, 'html.parser')
    wrong = soup.find_all(class_='tdErrWord')
    replace = soup.find_all(class_='tdReplace')

    for w, r in zip(wrong, replace):
        if r.get_text() == "대치어 없음":
            continue
        r_text = str(r).split("<br/>")[0].split(">")[1].strip(".")
        text = text.replace(w.get_text(), r_text)

    return text