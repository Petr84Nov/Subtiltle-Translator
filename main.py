from tkinter import *
from tkinter import filedialog
from transcriber import translate_subtitles
from config import *
import customtkinter as ctk

def open_file():
    file_path = filedialog.askopenfilename(
        title="Vyber soubor s titulky",
        filetypes=[("SRT titulky", "*.srt"),
                   ("Všechny soubory", "*.*")],
    )
    if file_path:
        srt_input.delete(0, END)
        srt_input.insert(0, file_path)

def transcribe():
    srt_path = srt_input.get()
    in_lang = input_lang_drop.get().lower()
    out_lang = output_lang_drop.get().lower()
    if not srt_path:
        progress_text.config(text="Vyber soubor s titulky")
        return
    progress_text.config(text="Zpracovávám")
    window.update_idletasks()
    try:
        # translate_subtitles(srt_path)
        # progress_text.config(text="Hotovo")
        result = translate_subtitles(srt_path, source_language=in_lang, target_language=out_lang)
        progress_text.config(text=result)
    except Exception as e:
        progress_text.config(text=f"Chyba{e}")


# hlavní okno
window = Tk()
window.title("Převod titulků")
window.minsize(width, height)
window.resizable(width=False, height=False)
window.config(bg=main_color)

# framy
input_frame = Frame(window, bg=main_color)
input_frame.pack()
language_frame = Frame(window, bg=main_color)
language_frame.pack(pady=15)
other_frame = Frame(window, bg=main_color)
other_frame.pack()

# input frame
input_text = Label(input_frame,text="Input: ", font=main_font, bg=main_color, fg="black")
input_text.grid(column=0, row=0, padx=5, pady=5)
# vstup od uživatele
srt_input = Entry(input_frame,width=20, font=main_font)
srt_input.grid(column=1, row=0, padx=5, pady=5)
open_button = Button(input_frame,text="Open", font=button_font, command=open_file)
open_button.grid(column=2, row=0, padx=10, pady=10)

# language frame
input_language = Label(language_frame,text="Input language: ", font=main_font, bg=main_color, fg="black")
input_language.grid(column=0, row=0, padx=5, pady=5)
output_language = Label(language_frame,text="Output language: ", font=main_font, bg=main_color, fg="black")
output_language.grid(column=0, row=1, padx=5, pady=5)
input_lang_drop = StringVar(window)
input_lang_drop.set("AUTO")
input_lang_drop_options = OptionMenu(language_frame, input_lang_drop, *languages)
input_lang_drop_options.grid(column=1, row=0, padx=5, pady=5)
output_lang_drop = StringVar(window)
output_lang_drop.set("CS")
output_lang_drop_options = OptionMenu(language_frame, output_lang_drop, *languages[1:])
output_lang_drop_options.grid(column=1, row=1, padx=5, pady=5)

# other frame
transcribe_button = Button(other_frame,text="Transcribe", font=main_font, command=transcribe)
transcribe_button.pack(padx=5, pady=5)
progress_text = Label(text="", font=main_font, bg=main_color, fg="black")
progress_text.pack(padx=5, pady=5)
exit_button = Button(text="Exit", font=main_font, command=window.destroy)
exit_button.pack(padx=5, pady=5)


window.mainloop()