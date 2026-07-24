from tkinter import *
from tkinter import filedialog
from transcriber import translate_subtitles
from config import *

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

def exit_app():
    window.destroy()



# hlavní okno
window = Tk()
window.title("Převod titulků")
window.minsize(width, height)
window.resizable(width=False, height=False)
window.config(bg=main_color)

# texty
input_text = Label(text="Input: ", font=main_font, bg=main_color, fg="black")
input_text.grid(column=0, row=0, padx=5, pady=5)
progress_text = Label(text="", font=main_font, bg=main_color, fg="black")
progress_text.grid(column=1, row=4, padx=5, pady=5)
input_language = Label(text="Input language: ", font=main_font, bg=main_color, fg="black")
input_language.grid(column=1, row=1, padx=5, pady=5)
output_language = Label(text="Output language: ", font=main_font, bg=main_color, fg="black")
output_language.grid(column=1, row=2, padx=5, pady=5)

# vstup od uživatele
srt_input = Entry(width=20, font=main_font)
srt_input.grid(column=1, row=0, padx=5, pady=5)


# tlačítka
open_button = Button(text="Open", font=button_font, command=open_file)
open_button.grid(column=2, row=0, padx=5, pady=5)
transcribe_button = Button(text="Transcribe", font=main_font, command=transcribe)
transcribe_button.grid(column=1, row=3, padx=5, pady=5)
exit_button = Button(text="Exit", font=main_font, command=exit_app)
exit_button.grid(column=1, row=5, padx=10, pady=10)

# roletky
input_lang_drop = StringVar(window)
input_lang_drop.set("AUTO")
input_lang_drop_options = OptionMenu(window, input_lang_drop, "AUTO", "EN", "CS", "DE", "FR", "IT", "JA", "KO", "ES", "PT", "RU")
input_lang_drop_options.grid(column=2, row=1, padx=5, pady=5)

output_lang_drop = StringVar(window)
output_lang_drop.set("CS")
output_lang_drop_options = OptionMenu(window, output_lang_drop, "CS", "EN", "DE", "FR", "IT", "JA", "KO", "ES", "PT", "RU")
output_lang_drop_options.grid(column=2, row=2, padx=5, pady=5)



window.mainloop()