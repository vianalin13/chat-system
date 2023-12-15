#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import json
from tkinter.messagebox import showerror, showinfo
import random
import datetime

emojis = ["😊", "🎉", "🌟", "🐱", "🍕", "🚀", "🎈", "🎸", "🌈", "🍩","😍","🥰","😋",
          "😎","🤩","🥳","😭","😡","😱","🙄","😴","😈","🤡","💩","😻","✌️","🐶","🐰",
          "🐨","🦁","🐷","🐽","🐸","🐣","🦄","🦋","🦕","🦖","🐙","🕊","🎄","☘️","🥀",
          "🌹","🌸","🌻","🌼","🌙","✨","🔥","☀️","☁️","❄️","🍎","🍉","🍓","🍑","🧀","🍔",
          "🍟","🍚","🍰","🍪","🍻","🏀","⚽️","🎾","🩰","🎨","🎤","🎧","🎮","🏖","🏔","🎞","💎"]


# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        # create a Label
        self.pls = Label(self.login, 
                       text = "Please login to continue",
                       justify = CENTER, 
                       font = "Helvetica 14 bold")
          
        self.pls.place(relheight = 0.15,
                       relx = 0.35, 
                       rely = 0.1)
        # create a Label
        self.labelName = Label(self.login,
                               text = "Username: ",
                               font = "Helvetica 12")
          
        self.labelName.place(relheight = 0.2,
                             relx = 0.195, 
                             rely = 0.3)
          
        # create a entry box for 
        # tyoing the message
        self.entryName = Entry(self.login, 
                             font = "Helvetica 14")
          
        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.37,
                             rely = 0.34)
          
        # set the focus of the curser
        self.entryName.focus()

        #password-------- still need to adjust the position
        self.labelPassword = Label(self.login,
                               text = "Password: ",
                               font = "Helvetica 12")
          
        self.labelPassword.place(relheight = 0.2,
                             relx = 0.2, 
                             rely = 0.45)
          
        # create a entry box for 
        # tyoing the message
        self.entryPassword = Entry(self.login, 
                             font = "Helvetica 14")
          
        self.entryPassword.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.37,
                             rely = 0.49)
          
        # set the focus of the curser
        self.entryName.focus()
        
          
        # create a Continue Button 
        # along with action
        self.go = Button(self.login,
                         text = "continue", 
                         font = "Helvetica 14 bold", 
                         command = lambda: self.goAhead(self.entryName.get(), self.entryPassword.get()))
          
        self.go.place(relx = 0.4,
                      rely = 0.74)
        self.Window.mainloop()
  
    def goAhead(self, name, password):
        
        if len(name) > 0 and len(password):
            msg = json.dumps({"action":"login", "name": name, "password": password})
            self.send(msg)
            response = json.loads(self.recv())

            if response["status"] == 'ok':
                
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state = NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")   
                self.textCons.insert(END, menu +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)

            elif response["status"] == 'error':
                showerror(title="Login Error", message="Incorrect password.")
                return
            elif response["status"] == "weak_password":
                error_message = response.get("error", "Invalid password.")
                showerror(title="Sign Up Error", message = "Weak password: "+ error_message)
                return
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()
            self.update_time()
  
    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#66545e")
        self.labelHead = Label(self.Window,
                             bg = "#66545e", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.002)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#a39193",
                             fg = "#EAECEE",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.85,
                            relwidth = 1, 
                            rely = 0.06)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#a39193",
                                 height = 45)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.91)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#66545e",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
          
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.67,
                            relheight = 0.05,
                            rely = 0.007,
                            relx = 0.12)
          
        self.entryMsg.focus()
          
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 5,
                                bg = "#a39193",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx = 0.8,
                             rely = 0.007,
                             relheight = 0.05, 
                             relwidth = 0.18)
        
        ## emoji button
        self.emoji_label = Label(self.Window,
                         bg="#66545e",
                         #fg="#EAECEE",
                         font="Helvetica 20 bold",
                         pady=1)
        
        self.emoji_label.place(relx = 0.01,
                             rely = 0.007,
                             relheight = 0.05, 
                             relwidth = 0.1)

        self.buttonemoji = Button(self.labelBottom,
                                text = "emoji",
                                font = "Helvetica 10 bold", 
                                width = 10,
                                bg = "#a39193",
                                command=self.display_random_emoji)
          
        self.buttonemoji.place(relx = 0.01,
                             rely = 0.007,
                             relheight = 0.05, 
                             relwidth = 0.1)
        ##

        ##display time
        self.time_label = Label(self.Window,
                            bg="#66545e",
                            fg="#EAECEE",
                            font="Helvetica 12 bold",
                            pady=5)
        self.time_label.place(relx=0.87, 
                              rely=0.007,
                              relheight = 0.05, 
                              relwidth = 0.1)
        ##
          
        self.textCons.config(cursor = "arrow")
          
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)

    #random emoji
    def display_random_emoji(self):
        random_emoji = random.choice(emojis)
        self.emoji_label.config(text=random_emoji)

    #time function
    def update_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.time_label.after(1000, self.update_time)

  
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg += self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, self.system_msg +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    g = GUI()