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
        progress_text.configure(text="Vyber soubor s titulky")
        return
    progress_text.configure(text="Zpracovávám")
    window.update_idletasks()
    try:
        # translate_subtitles(srt_path)
        # progress_text.config(text="Hotovo")
        result = translate_subtitles(srt_path, source_language=in_lang, target_language=out_lang)
        progress_text.configure(text=result)
    except Exception as e:
        progress_text.configure(text=f"Chyba{e}")

# hlavní okno
window = ctk.CTk()
window.title("Převod titulků")
window.minsize(width, height)
window.resizable(width=False, height=False)
window.config(bg=main_color)

# framy
input_frame = ctk.CTkFrame(window, bg_color=main_color, fg_color=main_color)
input_frame.pack()
language_frame = ctk.CTkFrame(window, bg_color=main_color, fg_color=main_color)
language_frame.pack(pady=15)
other_frame = ctk.CTkFrame(window, bg_color=main_color, fg_color=main_color)
other_frame.pack()

# input frame
input_text = ctk.CTkLabel(input_frame,text="Input: ", font=main_font, bg_color=main_color)
input_text.grid(column=0, row=0, padx=5, pady=5)
# vstup od uživatele
srt_input = ctk.CTkEntry(input_frame,width=200, font=main_font)
srt_input.grid(column=1, row=0, padx=5, pady=5)
open_button = ctk.CTkButton(input_frame,text="Open", font=button_font, command=open_file, width=25, fg_color=THEME["button_normal"], hover_color=THEME["button_hover"], text_color=THEME["text"])
open_button.grid(column=2, row=0, padx=10, pady=10)

# language frame
input_language = ctk.CTkLabel(language_frame,text="Input language: ", font=main_font, bg_color=main_color)
input_language.grid(column=0, row=0, padx=5, pady=5)
output_language = ctk.CTkLabel(language_frame,text="Output language: ", font=main_font, bg_color=main_color)
output_language.grid(column=0, row=1, padx=5, pady=5)
input_lang_drop = ctk.StringVar(value=languages[0])
# input_lang_drop.set("AUTO")
input_lang_drop_options = ctk.CTkOptionMenu(master=language_frame, variable=input_lang_drop, values=languages,
                                            fg_color=THEME["dropdown_normal"], button_color=THEME["dropdown_normal"],
                                            button_hover_color=THEME["dropdown_hover"], text_color=THEME["text"],
                                            dropdown_fg_color=THEME["dropdown_normal"],       # pozadí rozbaleného seznamu
                                            dropdown_hover_color=THEME["dropdown_hover"],     # hover nad položkou
                                            dropdown_text_color=THEME["text"])
input_lang_drop_options.grid(column=1, row=0, padx=5, pady=5)
output_lang_drop = StringVar(value=languages[1])
# output_lang_drop.set("CS")
output_lang_drop_options = ctk.CTkOptionMenu(master=language_frame, variable=output_lang_drop, values=languages[1:],
fg_color=THEME["dropdown_normal"], button_color=THEME["dropdown_normal"],
                                            button_hover_color=THEME["dropdown_hover"], text_color=THEME["text"],
                                            dropdown_fg_color=THEME["dropdown_normal"],       # pozadí rozbaleného seznamu
                                            dropdown_hover_color=THEME["dropdown_hover"],     # hover nad položkou
                                            dropdown_text_color=THEME["text"])
output_lang_drop_options.grid(column=1, row=1, padx=5, pady=5)

# other frame
transcribe_button = ctk.CTkButton(other_frame,text="Transcribe", font=main_font, command=transcribe, fg_color=THEME["button_normal"], hover_color=THEME["button_hover"], text_color=THEME["text"])
transcribe_button.pack(padx=5, pady=5)
progress_text = ctk.CTkLabel(other_frame, text="", font=main_font, bg_color=main_color)
progress_text.pack(padx=5, pady=5)
exit_button = ctk.CTkButton(other_frame,text="Exit", font=main_font, command=window.destroy, fg_color=THEME["button_normal"], hover_color=THEME["button_hover"], text_color=THEME["text"])
exit_button.pack(padx=5, pady=5)


window.mainloop()