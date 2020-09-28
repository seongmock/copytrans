#!/usr/bin/env python3
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
import re
import time
from sys import exc_info
import tkinter as tk
from html import escape
# from pypapago import Translator
# from googletrans import Translator
from requests import get
from bs4 import BeautifulSoup
import webbrowser
import urllib.request
import json

class CopyTrans(tk.Tk):
    def __init__(self):
        super().__init__()

        #Variable
        self.clip_text  = ""
        self.trans_text = ""
        self.trans_dst  = "ko"
        self.trans_src  = "en"
        self.SV_clip    = tk.StringVar(value="CopyTrans")

        #Main Window
        self.minsize(500, 80)
        self.resizable(False, False)
        self.title("CopyTrans - BBOM & YOO")

        # Frame
        self.frame0 = tk.Frame(self, pady=10)
        self.frame1 = tk.Frame(self)
        self.frame2 = tk.Frame(self)
        self.frame0.pack()
        self.frame1.pack(fill='both')
        self.frame2.pack(fill='both')

        # Frame0
        # Label
        self.L_search = tk.Label(self.frame0, text="Search :")
        self.L_search.pack(side="left")
        # Entry
        self.E_search = tk.Entry(self.frame0, width=40)
        self.E_search.pack(side="left")
        self.E_search.bind('<Return>', self.manual_search)
        # Button
        self.B_search = tk.Button(
            self.frame0, text="Search", padx=3, pady=0, command=self.manual_search)
        self.B_search.pack(side='right')

        # Frame1
        self.L_clip = tk.Label(
            self.frame1, textvariable=self.SV_clip, padx=20, pady=15)
        self.L_clip.pack()
        self.T_trans  = tk.Text(self.frame1, font='굴림 11 bold'
                        , bg=self.frame1.cget("bg"), relief="flat", borderwidth=0)
        self.T_trans.tag_configure('tag-center', justify='center')
        self.T_trans.configure(state="normal", height=5)
        self.T_trans.pack(side="bottom")

        #Frame2
        self.L_google = tk.Label(self.frame2, text="Google Translate", fg="blue", cursor="hand2")
        self.L_google.bind("<Button-1>", self.open_google)
        self.L_google.pack(side="right", anchor="e", padx=20)
        

        self.L_papago = tk.Label(self.frame2, text="Papago", fg="blue", cursor="hand2")
        self.L_papago.bind("<Button-1>", self.open_papago )
        self.L_papago.pack(side="right", anchor="e", padx=20)

        #Check Iteration
        self.after(500, self.check_clip)

    def check_clip(self):
        try:
            new_clip = self.clipboard_get()
            if (self.clip_text != new_clip):
                self.set_clip_text(new_clip)
            
                escaped_text = self.escape_text(self.clip_text)
                if re.search(r'\s', escaped_text):
                    self.translate(escaped_text)
                else:
                    self.dictonray(escaped_text)
                
                self.update()
                self.deiconify()
                self.attributes("-topmost", True)
                self.attributes("-topmost", False)
        except:
            print("Unexpected error:", exc_info()[0]) 


        self.after(500, self.check_clip)

    def set_clip_text(self, text):
        if self.check_ko(text):
            self.trans_dst="en"
            self.trans_src="ko"
        else:
            self.trans_dst="ko"
            self.trans_src="en"
        self.clip_text = text
    def set_E_search(self, text):
        self.E_search.delete(0, 'end')
        self.E_search.insert(0, text)

    def set_T_trans(self, text):
        line_cnt = text.count('\n')
        self.T_trans.configure(state="normal", height=(line_cnt+1), borderwidth=0)
        
        self.T_trans.delete(0.0,'end')
        self.T_trans.insert(1.0, text, 'tag-center')

    def check_ko(self, text):
        regex = re.compile('[가-힣]')
        result = regex.search(text)
        return result
    def escape_text(self, text):
        text = re.sub('\n','\\\\n', text)
        text = re.sub('\"', '\\\"', text)
        regex = re.compile(r'[^A-Za-z0-9가-힣\'\"\(\)\[\]\{\}\,\.\/\:\?\!\~\`\*\&\^\%\$\#\@\-\_\=\+\<\>\\\| \t]')
        text = regex.sub('', text)
        return text
    def unescape_text(self, text):
        text = re.sub(r'\\n',r'\n', text)
        text = re.sub(r'\\"', r'"', text)
        regex = re.compile(r'[^A-Za-z0-9가-힣\'\"\(\)\[\]\{\}\,\.\/\:\?\!\~\`\*\&\^\%\$\#\@\-\_\=\+\<\>\\\| \t]')
        text = regex.sub('', text)
        return text
    
    def CutLongString(self, text, mylen=80):
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


    #Event Function
    def open_google(self, event=None):
        url = "https://translate.google.com/?tl=%s&q=%s"%(self.trans_dst, self.clip_text)
        webbrowser.open_new(url)
    def open_papago(self, event=None):
        url = "https://papago.naver.com/?sk=auto&tk=%s&st=%s"%(self.trans_dst, self.clip_text)
        webbrowser.open_new(url)
    def manual_search(self, event=None):
        self.clipboard_clear()
        self.clipboard_append(self.E_search.get())


    #Web API
    def papago(self, text, src='en', dst='ko'):
        # translator = pypapago.Translator()
        # translator = Translator()
        # result = translator.translate(text, source=src, target=dst)
        client_id = "p1AhtSWDfF_A_ltcjJfm" # 개발자센터에서 발급받은 Client ID 값
        client_secret = "" # 개발자센터에서 발급받은 Client Secret 값
        encText = urllib.parse.quote(text)
        data = "source=%s&target=%s&text="%(src, dst) + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            result = json.loads(response_body)['message']['result']['translatedText']
        else:
            print("Error Code:" + rescode)
        return result

    # def GoogleTrans(text, dst):
    #     translator = Translator(service_urls=['translate.google.com'])
    #     trans_text = translator.translate(text, dst=dst).text
    #     return trans_text

    def search_daum_dic(self, query_keyword):
        dic_url = """http://dic.daum.net/search.do?q={0}"""
        r = get(dic_url.format(query_keyword))
        soup = BeautifulSoup(r.text, "html.parser")
        result_means = soup.find_all(attrs={'class': 'list_search'})
        text = result_means[0].get_text().strip()
        return text


    def translate(self, text):
        self.trans_text = self.papago(text, src=self.trans_src, dst=self.trans_dst)
        self.trans_text = self.CutLongString(self.trans_text, 50)

        self.set_E_search(text)
        self.SV_clip.set(self.CutLongString(self.unescape_text(text)))
        self.set_T_trans(self.trans_text)

    def dictonray(self, text):
        self.trans_text = self.search_daum_dic(text)
        self.set_E_search(text)
        self.SV_clip.set(text)
        self.set_T_trans(self.trans_text)


if __name__ == "__main__":
    app = CopyTrans()
    app.mainloop()
