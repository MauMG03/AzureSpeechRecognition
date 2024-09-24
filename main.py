import os
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from text_to_speech import text_to_speech
from speech_traduction import recognize_from_microphone as translate_speech
from speech_to_text import speech_to_microphone as recognize_speech

# Load environment variables
load_dotenv()
api_key = os.getenv('api_key')
region = os.getenv('region')

def open_speech_to_text():
    stt_window = tk.Toplevel(root)
    stt_window.title("Speech to Text")
    stt_window.configure(bg='#FFCCCC')
    stt_label = tk.Label(stt_window, text="Recognized Text will appear here", bg='#FFCCCC', fg='#660000', font=('Arial', 14))
    stt_label.pack(pady=20, padx=32)
    recognize_speech(api_key, region, stt_label, stt_window)

def open_text_to_speech():
    tts_window = tk.Toplevel(root)
    tts_window.title("Text to Speech")
    tts_window.configure(bg='#FFCCCC')
    tts_label = tk.Label(tts_window, text="Enter text to convert to speech:", bg='#FFCCCC', fg='#660000', font=('Arial', 14))
    tts_label.pack(pady=10, padx=32)
    tts_entry = tk.Entry(tts_window, width=50, font=('Arial', 14))
    tts_entry.pack(pady=10, padx=32)
    tts_button = tk.Button(tts_window, text="Submit", command=lambda: text_to_speech(api_key, region, tts_entry.get()), bg='#FF6666', fg='#FFFFFF', font=('Arial', 14))
    tts_button.pack(pady=10, padx=32)

def open_speech_translation():
    st_window = tk.Toplevel(root)
    st_window.title("Speech Translation")
    st_window.configure(bg='#FFCCCC')
    st_label = tk.Label(st_window, text="Translated Text will appear here", bg='#FFCCCC', fg='#660000', font=('Arial', 14))
    st_label.pack(pady=20, padx=32)
    translate_speech(api_key, region, st_label, st_window)

root = tk.Tk()
root.title("Speech Processing Options")
root.configure(bg='#FFCCCC')

btn_stt = tk.Button(root, text="Speech to Text", command=open_speech_to_text, bg='#FF6666', fg='#FFFFFF', font=('Arial', 14))
btn_stt.pack(pady=10, padx=32)

btn_tts = tk.Button(root, text="Text to Speech", command=open_text_to_speech, bg='#FF6666', fg='#FFFFFF', font=('Arial', 14))
btn_tts.pack(pady=10, padx=32)

btn_st = tk.Button(root, text="Speech Translation", command=open_speech_translation, bg='#FF6666', fg='#FFFFFF', font=('Arial', 14))
btn_st.pack(pady=10, padx=32)

root.mainloop()