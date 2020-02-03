#!/usr/bin/python3
#==================================================================================================
# Filename      : CopyTrans.py
# Author        : seongmock
# Created On    : 2019-08-28 14:39
# Last Modified : 2019-08-28 14:39 (seongmock)
#
# Description:
#
#
#==================================================================================================
#
#
import re
import clipboard;
import time;
import tkinter as tk;
from googletrans import Translator;
import requests
from bs4 import BeautifulSoup




window    = tk.Tk();


org_txt   = tk.StringVar();
trans_txt = tk.StringVar();
org_txt.set("Google Translate");
trans_txt.set("Google Translate");

org_label   = tk.Label(window, textvariable=org_txt, padx=20, pady=15);
org_label.pack()
trans_label = tk.Label(window, textvariable=trans_txt, padx=20, pady=15,
                        font='굴림 11 bold');
trans_label.pack(side="bottom");
prv_text="";


def CutLongString(text):
    cnt = 0;
    new_line = ""
    for char in text:
        if(char=='\n'):
            cnt = 0;
        elif(cnt==100):
            cnt = 0;
            new_line = new_line + '\n';
        else:
            cnt += 1;
        new_line = new_line + char;

    return new_line;

def GoogleTrans(text, dest):
    translator = Translator();
    trans_text = translator.translate(text, dest=dest).text;
    return trans_text;

def search_daum_dic(query_keyword):
    dic_url = """http://dic.daum.net/search.do?q={0}"""
    r = requests.get(dic_url.format(query_keyword))
    soup = BeautifulSoup(r.text, "html.parser")
    result_means = soup.find_all(attrs={'class':'list_search'})
    text = result_means[0].get_text().strip()
    return text

def set_google_trans(text):
    trans_text = GoogleTrans(text, 'ja');
    trans_text = GoogleTrans(text, 'ko');
    trans_text = CutLongString(trans_text);
    org_txt.set(CutLongString(text));
    trans_txt.set(trans_text);

def set_dict(text):
    trans_text = search_daum_dic(text);
    org_txt.set(text);
    trans_txt.set(trans_text);
    
def GetClip():
    global window, prv_text,trans_txt;
    text = clipboard.paste();
    if(prv_text!=text) :
        try:
            text=text.strip()
            if( re.search("\s",text) ):
                set_google_trans(text);
            else:
                set_dict(text)
            
            window.attributes("-topmost", True)
            window.attributes("-topmost", False)
            window.update() 
            window.deiconify()
        except:
            print("Error ");

        prv_text = text;
    window.after(500, GetClip);




if __name__ == "__main__":
    window.minsize(500, 80);
    window.resizable(False, False);
    window.title("Google Translate - BBOMI KIM");
    
    window.after(500, GetClip);
    window.mainloop();

