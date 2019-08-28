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

import clipboard;
import time;
import tkinter;
from googletrans import Translator;
import threading

window = tkinter.Tk();
label_txt = tkinter.StringVar();
label_txt.set("Google Translate");
# tkinter.Label(window, text="Maximum 가로길이(글자수)").grid(row=0);
# tkinter.Entry(window).grid(row=0, column=1)l
LABEL = tkinter.Label(window, textvariable=label_txt, padx=20, pady=20);
LABEL.pack();
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

def GoogleTrans(text):
    translator = Translator();
    trans_text = translator.translate(text, dest='ko').text;
    return trans_text;
    
def GetClip():
    # print("Function CAll");
    global window, prv_text,label_txt;
    text = clipboard.paste();
    if(prv_text!=text) :
        # print(text);
        trans_text = GoogleTrans(text);
        trans_text = CutLongString(trans_text);
        label_txt.set(trans_text);
        
        window.attributes("-topmost", True)
        window.attributes("-topmost", False)
        window.update() 
        window.deiconify()

        prv_text = text;
    window.after(500, GetClip);




if __name__ == "__main__":
    window.minsize(500, 80);
    window.resizable(False, False);
    window.title("Google Translate - BBOMI KIM");
    
    window.after(500, GetClip);
    window.mainloop();

