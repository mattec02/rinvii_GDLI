import os
import glob
import re

def process_xml(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    # Inizializza i contatori per ogni regex
    counters = {
        'pattern_deriv': 0,
        'pattern_multiple_words': 0,
        'pattern_words': 0,
        'pattern_comma_number': 0,
        'pattern_colon_words': 0,
        'pattern_with_number': 0,
        'pattern_with_parenthesis': 0,
        'pattern_multiple_words_cfr': 0,
    }


#1 Regex per trovare il pattern con "e deriv."
    pattern_deriv = re.compile(r'(<ref type="entry">v\.\s+)([A-Za-zÀ-Úà-ú]+(?:\s+[A-Za-zÀ-Úà-ú]+)*)(?=\s*(?:\s+e\s+deriv\.))(\s+e\s+deriv\.)(</ref>)')

    # Funzione per codificare casi con "e deriv."
    def replace_deriv(match):
        counters['pattern_deriv'] += 1 # Incrementa il contatore
        part1 = match.group(1) # "v. " (con spazio)
        word = match.group(2) # La parola o le parole (senza "e deriv.")
        part3 = match.group(3) # "e deriv."
        part4 = match.group(4) # "</ref>"

        return f"{part1}@RR@{word}@_@{part3}{part4}"

    # Sostituzione nel file
    modified_xml = pattern_deriv.sub(replace_deriv, xml_content)


#2 Regex per trovare parole singole o più parole all'interno di <ref>
    pattern_words = re.compile(r'(<ref type="entry">v\.\s+)(?!.*\s+e\s+)([A-Za-zÀ-Úà-ú]+(?:\s+[A-Za-zÀ-Úà-ú]+)*)(\.)?(</ref>)')
    # Funzione per codificare parole singole o multiple
    def replace_words(match):
        counters['pattern_words'] += 1 # Incrementa il contatore
        part1 = match.group(1) # "v. " con spazio
        words = match.group(2) # Parola/i
        point = match.group(3) # Punto finale
        part3 = match.group(4) # </ref>

        return f"{part1}@RR@{words}@_@{point}{part3}"

    modified_xml = pattern_words.sub(replace_words, modified_xml)


#3 Regex per parole con numeri alla fine (es. Accantonare1)
    pattern_with_number = re.compile(r'(<ref type="entry">v\.\s+)([A-Za-zÀ-Úà-ú]+[\d]+)(\.)?(</ref>)')

    # Funzione per sostituire parole seguite da numeri (es. Accantonare1)
    def replace_with_number(match):
        counters['pattern_with_number'] += 1 # Incrementa il contatore
        part1 = match.group(1) # "v. " con spazio
        word = match.group(2) # La parola seguita dal numero
        point = match.group(3) # Punto finale
        part3 = match.group(4) # </ref>

        return f"{part1}@RR@{word}@_@{point}{part3}"

    modified_xml = pattern_with_number.sub(replace_with_number, modified_xml)


#4 Regex per parole separate da "e" o ", "
    pattern_multiple_words = re.compile(r'(<ref type="entry">v\.\s+)([A-Za-zÀ-Úà-ú\d\s,]+)(\.)?(</ref>)')

    def replace_multiple_words(match):
        counters['pattern_multiple_words'] += 1 # Incrementa il contatore
        part1 = match.group(1) # "v. " con spazio
        words_block = match.group(2) # Parole e separatori
        point = match.group(3) if match.group(3) else "" # Punto finale, se presente
        part4 = match.group(4) # "</ref>"

        # Suddivide le parole mantenendo i separatori (e, ", ")
        words = re.split(r'(\s+e\s+|,\s*)', words_block)

        # Codifica ogni parola individualmente, mantenendo i separatori
        coded_words = "".join([
            f"@RR@{word.strip()}@_@" if word.strip() and not re.fullmatch(r'\s*e\s*|,\s*', word) else word
            for word in words
        ])

        return f"{part1}{coded_words}{point}{part4}"

    modified_xml = pattern_multiple_words.sub(replace_multiple_words, modified_xml)


#5 Regex per trovare parole seguite da ", n. <numero>."
    pattern_comma_number = re.compile(r'(<ref type="entry">v\.\s+)([A-Za-zÀ-Úà-ú]+)(\d+)?(,\s*n\.\s*\d+)(\.)?(</ref>)')

    def replace_comma_number(match):
        counters['pattern_comma_number'] += 1 # Incrementa il contatore
        part1 = match.group(1)  # "v. " con spazio
        word = match.group(2)  # La parola da sostituire
        word_number = match.group(3)  # Eventuale numero dopo la parola
        number_part = match.group(4)  # ", n. <numero>"
        point = match.group(5)  # Punto finale
        part6 = match.group(6)  # "</ref>"

        # Se word_number è None non aggiunge nulla
        if word_number is None:
            return f"{part1}@RR@{word}@_@{number_part}{point}{part6}"
        else:
            return f"{part1}@RR@{word}{word_number}@_@{number_part}{point}{part6}"

    modified_xml = pattern_comma_number.sub(replace_comma_number, modified_xml)


#6 Regex per trovare il caso con ", n. <numero>: <altre parole>"
    pattern_colon_words = re.compile(r'(<ref type="entry">v\.\s+)([A-Za-zÀ-Úà-ú]+)(,\s*n\.\s*\d+:\s*)(.*)(</ref>)')

    # Funzione per sostituire parole seguite da ", n. <numero>: <altre parole>"
    def replace_colon_words(match):
        counters['pattern_colon_words'] += 1 # Incrementa il contatore
        part1 = match.group(1) # "v. " con spazio
        word = match.group(2) # La parola da sostituire
        number_part = match.group(3) # ", n. <numero>:"
        part4 = match.group(4) # Qualsiasi contenuto
        part5 = match.group(5) # "</ref>"

        # Mantiene invariata la parte dopo i due punti (parte4) e aggiunge solo il tag alla parola
        return f"{part1}@RR@{word}@_@{number_part}{part4}{part5}"

    modified_xml = pattern_colon_words.sub(replace_colon_words, modified_xml)


#7 Regex per parole seguite da una variante tra parentesi (es. Arreto (arretro))
    pattern_with_parenthesis = re.compile(r'(<ref type="entry">v\.\s+)([A-Za-zÀ-Úà-ú]+)(\s*\([A-Za-zÀ-Úà-ú]+)(\)\.)?(</ref>)')

    # Funzione per sostituire parole seguite da una variante tra parentesi
    def replace_with_parenthesis(match):
        counters['pattern_with_parenthesis'] += 1 # Incrementa il contatore
        part1 = match.group(1) # "v. " con spazio
        word = match.group(2) # La parola principale
        variant = match.group(3) # La variante tra parentesi
        point = match.group(4) # Punto finale
        part5 = match.group(5) # </ref>

        return f"{part1}@RR@{word}@_@{variant}{point}{part5}"

    modified_xml = pattern_with_parenthesis.sub(replace_with_parenthesis, modified_xml)


#8 Regex per trovare i "cfr." con possibili numeri
    pattern_multiple_words_cfr = re.compile(r'(<ref type="entry">.*?cfr\.\s+)([A-Za-zÀ-Úà-ú\s,]+\d?)(, n. \d)?(.*?)(</ref>)')

    def replace_multiple_words_cfr(match):
        counters['pattern_multiple_words_cfr'] += 1 # Incrementa il contatore
        part1 = match.group(1) # Parte iniziale (fino a "cfr. ")
        words_block = match.group(2) # Le parole e eventuali numeri "attaccati"
        number = match.group(3) if match.group(3) else "" # Numero separato se presente
        part4 = match.group(4) # Il resto della frase
        part5 = match.group(5) # Chiusura del tag </ref>

        # Suddivide le parole mantenendo i separatori (e, ", ")
        words = re.split(r'(\s+e\s+|,\s*)', words_block)

        # Codifica ogni parola individualmente, mantenendo i separatori
        coded_words = "".join([
            f"@RR@{word.strip()}@_@" if word.strip() and not re.fullmatch(r'\s*e\s*|,\s*', word) else word
            for word in words
        ])

        return f"{part1}{coded_words}{number}{part4}{part5}"

    modified_xml = pattern_multiple_words_cfr.sub(replace_multiple_words_cfr, modified_xml)


# Restituisce il contenuto modificato e i contatori
    return modified_xml, counters


def process_multiple_files(input_dir, output_dir):
    # Raccoglie tutti i file XML nella directory
    xml_files = glob.glob(os.path.join(input_dir, "*.xml"))

    # Inizializza un dizionario per sommare i contatori di tutti i file
    total_counters = {
        'pattern_deriv': 0,
        'pattern_words': 0,
        'pattern_with_number': 0,
        'pattern_multiple_words': 0,
        'pattern_comma_number': 0,
        'pattern_colon_words': 0,
        'pattern_with_parenthesis': 0,
        'pattern_multiple_words_cfr': 0,
    }

    # Per ogni file, elabora e salva il risultato
    for file_path in xml_files:
        print(f"Elaborando il file: {file_path}")
        modified_xml, counters = process_xml(file_path)

        # Somma i contatori del file corrente ai totali
        for key in total_counters:
            total_counters[key] += counters[key]

        # Salvo il risultato modificato in una nuova cartella (output_dir)
        output_file = os.path.join(output_dir, os.path.basename(file_path))
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(modified_xml)

        print(f"File salvato come: {output_file}")

    # Stampa i totali dei match per ogni regex
    print("\nStatistiche dei match:")
    total = 0
    for key, value in total_counters.items():
        print(f"{key}: {value} match")
        total = total + value
    print(f"Totale match: {total}")


# Eseguo il codice su tutti i file nella cartella di input e salvo i risultati in una cartella di output
input_directory = '/Users/matteochiaramonte/Git/rinvii_GDLI/VOL III'
output_directory = '/Users/matteochiaramonte/Git/rinvii_GDLI/vol3_codificaVociRinvio'

# Controllo che la cartella di output esista
os.makedirs(output_directory, exist_ok=True)

# Processo tutti i file nella directory
process_multiple_files(input_directory, output_directory)

print("Elaborazione completata su tutti i file!")