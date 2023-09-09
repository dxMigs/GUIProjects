import tkinter as tk
import pytube
from PIL import Image, ImageTk
from urllib.request import urlopen
from tkinter import filedialog
from tkinter.messagebox import showinfo, showerror, askokcancel
from tkinter import ttk
import io
import threading
import time
import os



class VideoDownloader:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Video Downloader")
        self.window_width, self.window_height = 650, 520
        self.window.geometry(f"{self.window_width}x{self.window_height}")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        self.link_label = tk.Label(self.window, text="Link zu deinem Youtube Video eingeben:", fg="black", font=("OCR A Extended", 18))
        self.link_label.place(x=40, y=self.window_height - 210)

        self.link_text_box = tk.Entry(self.window, fg="blue",width=51, font=("Arial", 14))
        self.link_text_box.place(x=40, y=self.window_height - 180)

        self.download_video_button = tk.Button(self.window, text="Download Video", font=("OCR A Extended", 18), command=self.download_video)
        self.download_mp3_button = tk.Button(self.window, text="Download Mp3", font=("OCR A Extended", 18), command=self.download_audio)

        self.initilial_logo = Image.open("youtube.png")
        self.logo_image = self.initilial_logo.resize((450, 280))
        self.logo = ImageTk.PhotoImage(image=self.logo_image)
        self.logo_label = tk.Label(image=self.logo)
        self.logo_label.place(x=-35, y=-20)

        #self.label_image = tk.Label()

        self.logo_text_label = tk.Label(self.window, text="Downloader", fg="black", font=("OCR A Extended", 32))
        self.logo_text_label.place(x=355, y=118)
       
        self.waiting = True
        
        threading.Thread(target=self.link_entry).start()

    def link_entry(self):
        while self.waiting:
            self.link = self.link_text_box.get()
            time.sleep(0.25)
            if self.link.startswith("https://www.youtube.com/watch?v="):
                try:
                    self.thumbnail_url = pytube.YouTube(self.link).thumbnail_url
                except:
                    self.label_image.destroy()
                    self.clear()
                else:
                    self.logo_label.destroy()
                    self.logo_text_label.destroy()
                    self.url = urlopen(self.thumbnail_url)
                    self.raw_data = self.url.read()
                    self.url.close()
                    
                    self.initial_thumbnail_image = Image.open(io.BytesIO(self.raw_data))
                    self.resized_thumbnail_image = self.initial_thumbnail_image.resize((460, 258))
                    self.thumbnail_image = ImageTk.PhotoImage(image=self.resized_thumbnail_image)
                    self.label_image = tk.Label(image=self.thumbnail_image)
                    #self.label_image.image = self.thumbnail_image
                    self.label_image.place(x=93, y=30)
                    self.show_download_buttons()
        

                    
            else:
                try:
                    self.label_image.destroy()
                except:
                    pass
                self.clear()
                self.logo_label = tk.Label(image=self.logo)
                self.logo_text_label = tk.Label(self.window, text="Downloader", fg="black", font=("OCR A Extended", 32))
                self.logo_label.place(x=-35, y=-20)
                self.logo_text_label.place(x=355, y=118)

                
                    
            self.window.update()
    
    def download_audio(self):
        self.file_path = filedialog.askdirectory()
        try:
            self.yt = pytube.YouTube(self.link)
            self.output = self.yt.streams.get_audio_only().download(self.file_path)
            self.base, self.ext = os.path.splitext(self.output)
            self.new_file = self.base + '.mp3'
            os.rename(self.output, self.new_file)
            showinfo(title="Download erfolgreich", message="Deine MP3 Datei wurde erfolgreich gedownloadet.")
        except:
            showerror(title="Download fehlgeschlagen", message="Ein Fehler ist beim downloaden der Datei aufgetreten.\nBitte überprüfe deine Internetverbindung")


    def download_video(self):
        try:
            self.file_path = filedialog.askdirectory()
            self.yt = pytube.YouTube(self.link)
            self.output = self.yt.streams.get_highest_resolution().download(self.file_path)
            showinfo(title="Download erfolgreich", message="Deine Video Datei wurde erfolgreich gedownloadet.")
        except:
            showerror(title="Download fehlgeschlagen", message="Ein Fehler ist beim downloaden der Datei aufgetreten.\nBitte überprüfe deine Internetverbindung")

    def clear_logo(self):
        self.logo_label.destroy()
        self.logo_text_label.destroy()
        
    def show_logo(self):
        self.logo_label = tk.Label(image=self.logo)
        self.logo_text_label = tk.Label(self.window, text="Downloader", fg="black", font=("OCR A Extended", 32))
        self.logo_label.place(x=-35, y=-20)
        self.logo_text_label.place(x=355, y=118)
    
    def clear(self):
        self.download_video_button.place_forget()
        self.download_mp3_button.place_forget()

    def show_download_buttons(self):
        self.download_video_button.place(x=40, y= 400)
        self.download_mp3_button.place(x=416, y= 400)
        

    def close_window(self):
        if askokcancel(title="Schließen", message="Willst du wirklich den Youtube Downloader schließen?"):
            self.window.destroy()
                
if __name__ == '__main__':
    VD = VideoDownloader()
    VD.window.mainloop()