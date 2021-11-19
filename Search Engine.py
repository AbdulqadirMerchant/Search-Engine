from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import PIL.Image
import wikipedia
import pyttsx3
import urllib.request
import os
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty("rate", 180)
previous_query = {}


def search(event = None):
    if not search_box.get():
        messagebox.showerror("Error", "Please enter something to search for!!")
        return
    query = search_box.get()
    try:
        search_result = wikipedia.summary(query, sentences = 2)
        pages = wikipedia.page(query)
        for index, value in enumerate(pages.images):
            if value[-4:] in [".jpg", ".png", ".gif"]:
                urllib.request.urlretrieve(value, query+value[-4:])
                image = PIL.Image.open(query + value[-4:])
                image = image.resize((150, 150), PIL.Image.ANTIALIAS)
                image = ImageTk.PhotoImage(image)
                previous_query[query] = value[-4:]
                search_image.config(image=image)
                search_image.image = image
                break
        else:
            messagebox.showinfo("Error", "Failed to load image!")
        search_label.config(text=search_result)

    except wikipedia.exceptions.PageError:
        messagebox.showerror("Error", "Sorry! We couldn't find what you are looking for!!")


def close_and_delete(event = None):
    for query, extension in previous_query.items():
        os.remove(query + extension)
    root.destroy()


def speak(event = None):
    if len(search_label["text"]) != 0:
        engine.say(search_label["text"])
        engine.runAndWait()
    else:
        messagebox.showerror("Error", "Please search for something first!!")


def audio_search(event = None):
    if search_box.get():
        search_box.delete(0, END)
    try:
        recording = sr.Recognizer()
        with sr.Microphone() as source:
            recording.adjust_for_ambient_noise(source)
            print("Listening now!")
            audio_input = recording.listen(source)
            text = recording.recognize_google(audio_input)
            search_box.insert(0, text)
            search()
    except:
        engine.say("Looks like something went wrong! Please try again....")
        engine.runAndWait()


root = Tk()
root.configure(bg = "cyan")
root.protocol("WM_DELETE_WINDOW", close_and_delete)
root.bind("alt-f4", close_and_delete)
root.title("Search Engine")

microphone = PIL.Image.open("Microphone.png")
microphone = microphone.resize((50, 50), PIL.Image.ANTIALIAS)
microphone = ImageTk.PhotoImage(microphone)

search_box = Entry(root, font = ("Verdana", 20), bg = "blue",)
search_box.pack(pady = 10)

microphone_button = Button(root, image = microphone, command = audio_search)
microphone_button.bind("<Return>", audio_search)
microphone_button.pack(side = TOP)

search_button = Button(root, text = "Search", font = ("Verdana", 10), command = search)
search_button.bind("<Return>", search)
search_button.pack(pady = 10, side = TOP)
search_box.focus()

search_image = Label(root)
search_image.pack()

search_label = Label(root, font = ("Comic Sans MS", 15), relief = SUNKEN, wraplength = 800)
search_label.pack(pady = 10, side = TOP)

audio = PIL.Image.open("audio.jpg")
audio = audio.resize((50, 50), PIL.Image.ANTIALIAS)
audio = ImageTk.PhotoImage(audio)

audio_button = Button(root, image = audio, command = speak)
audio_button.bind("<Return>", speak)
audio_button.pack(side = TOP, pady = 10)

root.mainloop()
