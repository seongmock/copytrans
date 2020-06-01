#!/usr/bin/python3
# ==================================================================================================
# Filename      : CopyTrans.py
# Author        : seongmock
# Created On    : 2019-08-28 14:39
# Last Modified : 2019-08-28 14:39 (seongmock)
#
# Description:
#
#
# ==================================================================================================
#
#
# import sys
import re
import pyperclip
import time
import tkinter as tk
from html import escape
from pypapago import Translator
# from googletrans import Translator
from requests import get
from bs4 import BeautifulSoup
import webbrowser

def callback(url):
    webbrowser.open_new(url)

def my_search(event=None):
    pyperclip.copy(search_entry.get())


def CutLongString(text, mylen=100):
    cnt = 0
    new_line = ""
    for char in text:
        if(char == '\n'):
            cnt = 0
        elif(cnt == mylen):
            cnt = 0
            new_line = new_line + '\n'
        else:
            cnt += 1
        new_line = new_line + char

    return new_line


# def GoogleTrans2(text, dest):
#     return "none"

def papago(text, dest):
    # translator = pypapago.Translator()
    translator = Translator()
    result = translator.translate(text, source='en', target=dest)
    return result

# def GoogleTrans(text, dest):
#     translator = Translator(service_urls=['translate.google.com'])
#     trans_text = translator.translate(text, dest=dest).text
#     return trans_text


def search_daum_dic(query_keyword):
    dic_url = """http://dic.daum.net/search.do?q={0}"""
    r = get(dic_url.format(query_keyword))
    soup = BeautifulSoup(r.text, "html.parser")
    result_means = soup.find_all(attrs={'class': 'list_search'})
    text = result_means[0].get_text().strip()
    return text


def set_trans(text):
    # trans_text = GoogleTrans(text, 'ja')
    # trans_text = GoogleTrans(text, 'ko')
    # trans_text = GoogleTrans2(text, 'ko')
    trans_text = papago(text, 'ko')
    trans_text = CutLongString(trans_text, 50)

    search_entry.delete(0, 'end')
    search_entry.insert(0, text)
    org_txt.set(CutLongString(re.sub('\\\"', '\"', text)))
    trans_txt.set(trans_text)


def set_dict(text):
    trans_text = search_daum_dic(text)
    search_entry.delete(0, 'end')
    search_entry.insert(0, text)
    org_txt.set(text)
    trans_txt.set(trans_text)


window    = tk.Tk()
org_txt   = tk.StringVar(value="Google Translate")
trans_txt = tk.StringVar(value="Google Translate")

top_frame    = tk.Frame(window, pady=10)
bottom_frame = tk.Frame(window)
link_frame   = tk.Frame(window)

#TOP Frame Entity
tk.Label(top_frame, text="Seach :").pack(side='left')

search_entry = tk.Entry(top_frame, width=30)
search_entry.pack(side='left')
search_entry.bind('<Return>', my_search)

search_bt = tk.Button(top_frame, text="search", padx=3,
                      pady=0, command=my_search)
search_bt.pack(side='right')

top_frame.pack(side="top")

#Link Frame Entity
g_link = tk.Label(link_frame, text="Google Translate", fg="blue", cursor="hand2")
g_link.pack(side="right", anchor="e", padx=20)
g_link.bind("<Button-1>", lambda e: callback("https://translate.google.com/?tl=ko&q=%s"%prv_text))

p_link = tk.Label(link_frame, text="Papago", fg="blue", cursor="hand2")
p_link.pack(side="right", anchor="e", padx=20)
p_link.bind("<Button-1>", lambda e: callback("https://papago.naver.com/?sk=auto&tk=ko&st=%s"%prv_text))
link_frame.pack(side="bottom", anchor="e")


#Bottom Frame Entity
org_label = tk.Label(bottom_frame, textvariable=org_txt, padx=20, pady=15)
org_label.pack()
trans_label = tk.Label(bottom_frame, textvariable=trans_txt, padx=20, pady=15,
                       font='굴림 11 bold')
trans_label.pack(side="bottom")

bottom_frame.pack(side="bottom")



prv_text = ""

myre= re.compile(r'[^A-Za-z0-9가-힣\'\"\(\)\[\]\{\}\,\.\/\:\?\!\~\`\*\&\^\%\$\#\@\-\_\=\+\<\>\\\| \t]')

def GetClip():
    global window, prv_text, trans_txt
    text = pyperclip.paste()
    if(prv_text != text):
        prv_text = text
        try:
            text = text.strip()
            text = re.sub('\n', ' ', text)
            text = re.sub('\"', '\\\"', text)
            text = myre.sub('', text)
            if re.search(r"\s", text):
                set_trans(text)
            else:
                set_dict(text)

            window.update()
            window.deiconify()
            window.attributes("-topmost", True)
            window.attributes("-topmost", False)

        except:
            # print("Unexpected error:", sys.exc_info()[0])
            print("Error")
            # raise

        
    window.after(500, GetClip)


if __name__ == "__main__":
    window.minsize(500, 80)
    window.resizable(False, False)
    window.title("Google Translate - BBOMI KIM")

    window.after(500, GetClip)
    window.mainloop()
