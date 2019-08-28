#!/usr/bin/python3
#==================================================================================================
# Created by    : LGE
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



def GoogleTrans(text):
    translator = Translator();
    trans_text = translator.translate(text, dest='ko').text;
    return trans_text;
    


if __name__ == "__main__":
        
    prv_text="";
    window = tkinter.Tk();
    window.minsize(500, 80);
    window.resizable(False, False);
    window.title("Google Translate - BBOMI KIM");
    
    while(1):        
        text = clipboard.paste();
        if(prv_text!=text) :
            # print(text);
            trans_text = GoogleTrans(text);
            try: 
                LABEL.pack_forget();
            except:
                pass;


            LABEL = tkinter.Label(window, text=trans_text, padx=20, pady=20);
            LABEL.pack();
            window.update()

            prv_text = text;

        time.sleep(0.5);

