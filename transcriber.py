import os
import time
import srt
from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound

# vrátí cestu se stejným názvem, ale příponou nahrazenou za "srt"
def edit_extension(path:str, language:str=None):
    original_path, _ = os.path.splitext(path)
    if language:
        return f"{original_path}_{language}.srt"
    else:
        return f"{original_path}.srt"

# přeloží obsah srt souboru a uloží ho do nového souboru.
#def translate_subtitles(input_file: str, output_file: str, source_language: str="auto", target_language: str="cs", pause: float = 0.3) -> None:
def translate_subtitles(input_file, output_file=None, source_language="auto", target_language="cs", pause=0.3):
    if output_file is None:
        output_file = edit_extension(input_file, language=target_language)

    # načtení a rozparsování vstupního srt souboru
    with open(input_file, encoding="utf-8-sig") as f:
        content = f.read()

    subtitles = list(srt.parse(content))
    print(f"Načteno {len(subtitles)} titulků z '{input_file}'")

    translator = GoogleTranslator(source=source_language, target=target_language)
    number = 1
    for subtitle in subtitles:
        lines = subtitle.content.split("\n")
        transcribe_lines = []
        for line in lines:
            if not line.strip():
                transcribe_lines.append(line)
                continue
            try:
                transcribed = translator.translate(line)
                transcribe_lines.append(transcribed if transcribed else line)
            except TranslationNotFound:
                print(f" [!] Titulek {number}: překlad se nezdařil, ponecháme originál.")
                transcribe_lines.append(line)
            except Exception as e:
                print(f" [!] Titulek {number}: chyba, ponecháme originál.")
                transcribe_lines.append(line)

        subtitle.content = "\n".join(transcribe_lines)
        number += 1

        if number % 10 == 0 or number == len(subtitles):
            print(f" Přeloženo {number}/{len(subtitles)} titulků...")

        time.sleep(pause) # pauza mezi požadavky, aby google nepiskoval

    # uložení přeložených titulků zpět do srt formátu
    output = srt.compose(subtitles)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Hotovo. Přeložené titulky uloženy do '{output_file}'")
    return f"Hotovo. Přeložené titulky uloženy do '{output_file}'"