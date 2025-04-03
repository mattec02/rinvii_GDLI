import os
import glob
import re

def process_xml(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    # Inizializza i contatori per ogni regex
    counters = {
        'pattern_cfr_anche': 0,
        'pattern_v_anche': 0,
        'pattern_v_anche_numero': 0,
        'pattern_v_numero': 0,
        'pattern_cfr_numero': 0,
        'pattern_coniug': 0,
        'pattern_coniug_parenthesis': 0,
        'pattern_coniugazione': 0,
        'pattern_cfr_multiple_words_1': 0,
        'pattern_cfr_multiple_words_2': 0,
        'pattern_cfr_parenthesis': 0,
        'pattern_v_multiple_words_parenthesis': 0,
        'pattern_v_multiple_words': 0,
        'pattern_cfr': 0,
        'pattern_v_parenthesis': 0,
    }

#1 Regex per trovare il pattern con cfr. anche
    pattern_cfr_anche = re.compile(r'(<def>.*?)(\([Cc]fr\. anche\s*)([A-Za-zÀ-Úà-ú\s]+)(\))(.*)(\.</def>)')
    
    def replace_cfr_anche(match):
        counters['pattern_cfr_anche'] += 1 # Incrementa il contatore
        part1 = match.group(1) # <def> fino a (cfr. anche)
        anche = match.group(2) # cfr. anche
        word = match.group(3) # La parola o le parole (espressione) da codificare
        part4 = match.group(4) # Chiusura parentesi
        part5 = match.group(5) if match.group(4) else "" # Eventuale altro testo dopo il rinvio
        part6 = match.group(6) # Chiusura tag

        return f"{part1}{anche}@RR@{word}@_@{part4}{part5}{part6}"
    
    modified_xml = pattern_cfr_anche.sub(replace_cfr_anche, xml_content)


#2 Regex per trovare il pattern con v. anche
    pattern_v_anche = re.compile(r'(<def>.*?\.?\s)(\(?[Vv]\. anche\s*)([A-Za-zÀ-Úà-ú]+)(\)?\.</def>)')
    
    def replace_v_anche(match):
        counters['pattern_v_anche'] += 1 # Incrementa il contatore
        part1 = match.group(1) # <def> fino a (V. anche)
        anche = match.group(2) # v. anche
        word = match.group(3) # La parola o le parole (espressione) da codificare
        part4 = match.group(4) # Chiusura tag

        return f"{part1}{anche}@RR@{word}@_@{part4}"
    
    modified_xml = pattern_v_anche.sub(replace_v_anche, modified_xml)


#3 Regex per trovare il pattern con v. anche con numero entrata o definizione
    pattern_v_anche_numero = re.compile(r'(<def>.*?)(\([Vv]\.\s*)(anche\s*)([A-Za-zÀ-Úà-ú]+)(\d+)?(,\s*n\.\s*\d+)?(\)\.)(.*?)(</def>)')
  
    def replace_v_anche_numero(match):
        counters['pattern_v_anche_numero'] += 1 # Incrementa il contatore
        part1 = match.group(1) # <def> fino a (v.
        v = match.group(2) # (v.
        anche = match.group(3) if match.group(3) else "" # Eventuale "anche"
        word = match.group(4) # La parola o le parole (espressione) da codificare
        number = match.group(5) if match.group(5) else "" # Eventuale numero indicante il lemma (attaccato al lemma stesso)
        comma_number = match.group(6) if match.group(6) else ""# Numero dopo la virgola indicante il significato
        part6 = match.group(7) if match.group(7) else "" # Chiusura parentesi
        part7 = match.group(8) if match.group(8) else "" # Eventuale testo dopo il rinvio
        part8 = match.group(9) # Chiusura tag


        return f"{part1}{v}{anche}@RR@{word}{number}@_@{comma_number}{part6}{part7}{part8}"

    modified_xml = pattern_v_anche_numero.sub(replace_v_anche_numero, modified_xml)


#4 Regex per trovare il pattern con v. e numero definizione
    pattern_v_numero = re.compile(r'(<def>.*?)(\(?[Vv]\.\s*)([A-Za-zÀ-Úà-ú]+)(\d+)?(,\s*n\.\s*\d+)(\)?\.?)(.*?)(</def>)')
  
    def replace_pattern_v_numero(match):
        counters['pattern_v_numero'] += 1 # Incrementa il contatore
        part1 = match.group(1) # <def> fino a (v.
        v = match.group(2) # (v.
        word = match.group(3) # La parola da codificare
        number = match.group(4) if match.group(4) else "" # Eventuale numero indicante il lemma (attaccato al lemma stesso)
        comma_number = match.group(5) # Numero dopo la virgola indicante il significato
        part5 = match.group(6) if match.group(6) else "" # Chiusura parentesi
        part6 = match.group(7) if match.group(7) else "" # Eventuale testo dopo il rinvio
        part7 = match.group(8) # Chiusura tag

        return f"{part1}{v}@RR@{word}{number}@_@{comma_number}{part5}{part6}{part7}"

    modified_xml = pattern_v_numero.sub(replace_pattern_v_numero, modified_xml)


#5 Regex per trovare il pattern con "(cfr.)" con numero definizione
    pattern_cfr_numero = re.compile(r'(<def>.*?)(\(?[Cc]fr\.\s*)([A-Za-zÀ-Úà-ú]+)(\d+)?(,\s*n\.\s*\d+)(\)?\.?)(.*?)(</def>)')
  
    def replace_pattern_cfr_numero(match):
        counters['pattern_cfr_numero'] += 1 # Incrementa il contatore
        part1 = match.group(1) # <def> fino a (cfr.
        cfr = match.group(2) # (cfr.
        word = match.group(3) # La parola da codificare
        number = match.group(4) if match.group(4) else "" # Eventuale numero indicante il lemma (attaccato al lemma stesso)
        comma_number = match.group(5) # Numero dopo la virgola indicante il significato
        part5 = match.group(6) if match.group(6) else "" # Chiusura parentesi
        part6 = match.group(7) if match.group(7) else "" # Eventuale testo dopo il rinvio
        part7 = match.group(8) # Chiusura tag

        return f"{part1}{cfr}@RR@{word}{number}@_@{comma_number}{part5}{part6}{part7}"

    modified_xml = pattern_cfr_numero.sub(replace_pattern_cfr_numero, modified_xml)    


#6 Regex per trovare i rimandi alla coniugazione
    pattern_coniug = re.compile(r'(<def>.*)(Per la coniug\.?:? [Cc]fr\.:?\s)([A-Za-zÀ-Úà-ú\s]+)(\.)(.*?)(</def>)')
  
    def replace_pattern_coniug(match):
        counters['pattern_coniug'] += 1 # Incrementa il contatore
        part1 = match.group(1) # <def> fino a per la coniug.
        coniug = match.group(2) # Per la coniug.: cfr. o Per la coniug. cfr.:
        word = match.group(3) # La parola da codificare
        part4 = match.group(4) # Punto
        part5 = match.group(5) if match.group(5) else "" # Eventuale testo dopo il rinvio
        part6 = match.group(6)

        return f"{part1}{coniug}@RR@{word}@_@{part4}{part5}{part6}"

    modified_xml = pattern_coniug.sub(replace_pattern_coniug, modified_xml)


#7 Regex per trovare i rimandi alla coniugazione fra parentesi, opzione 1
    pattern_coniug_parenthesis = re.compile(r'(<def>.*)(\(per la coniugaz(ione)?\.?:? [Cc]fr\.:?\s)([A-Za-zÀ-Úà-ú\s]+)(\))(.*?)(</def>)')
  
    def replace_pattern_coniugazione(match):
        counters['pattern_coniug_parenthesis'] += 1 # Incrementa il contatore
        part1 = match.group(1) # <def> fino alla parentesi
        coniug = match.group(2) # (Per la coniug.: cfr. o Per la coniug. cfr.:
        word = match.group(4) # La parola da codificare
        part5 = match.group(5) # Chiusura parentesi
        part6 = match.group(6) if match.group(5) else "" # Eventuale testo dopo il rinvio
        part7 = match.group(7) # Chiusura tag

        return f"{part1}{coniug}@RR@{word}@_@{part5}{part6}{part7}"

    modified_xml = pattern_coniug_parenthesis.sub(replace_pattern_coniugazione, modified_xml)


#8 Regex per trovare i rimandi alla coniugazione fra parentesi, opzione 3
    pattern_coniugazione = re.compile(r'(<def>.*)(\(per la coniugazione\:? [Vv]\.:?\s)([A-Za-zÀ-Úà-ú\s]+)(\).*?)(</def>)')
  
    def replace_pattern_coniugazione(match):
        counters['pattern_coniugazione'] += 1 # Incrementa il contatore
        part1 = match.group(1) # <def> fino alla parentesi
        coniug = match.group(2) # (Per la coniugazione: cfr. o Per la coniugazione cfr.:
        word = match.group(3) # La parola da codificare
        part4 = match.group(4) if match.group(4) else "" # Eventuale testo dopo il rinvio
        part5 = match.group(5) # Chiusura tag


        return f"{part1}{coniug}@RR@{word}@_@{part4}{part5}"

    modified_xml = pattern_coniugazione.sub(replace_pattern_coniugazione, modified_xml)


#9 Regex per trovare il pattern con cfr. senza parentesi e con più rinvii nello stesso campo (separati da e)
    pattern_cfr_multiple_words_1 = re.compile(r'(<def>.*?\. )([Cc]fr\.\s)([A-Za-zÀ-Úà-ú\s]+(?:\s*(?:e|,)\s*[A-Za-zÀ-Úà-ú\s]+)*)(\.</def>)')
    
    def replace_cfr_multiple_words_1(match):
        counters['pattern_cfr_multiple_words_1'] += 1  # Incrementa il contatore
        part1 = match.group(1) # <def> e testo prima di cfr.
        cfr = match.group(2) # cfr.
        words_block = match.group(3) # Parole da codificare separate da "e"
        part4 = match.group(4) # Chiusura tag

        # Suddivide le parole mantenendo i separatori (e, ", ")
        words = re.split(r'(\se\s|,\s*)', words_block)

        # Codifica ogni parola individualmente, mantenendo i separatori
        coded_words = "".join([
            f"@RR@{word.strip()}@_@" if word.strip() and not re.fullmatch(r'\se\s*|\s*,\s*', word) else word
            for word in words
        ])

        return f"{part1}{cfr}{coded_words}{part4}"

    modified_xml = pattern_cfr_multiple_words_1.sub(replace_cfr_multiple_words_1, modified_xml)


#10 Regex per trovare il pattern con cfr. fra parentesi e con più rinvii nello stesso campo (separati da virgola)
    pattern_cfr_multiple_words_2 = re.compile(r'(<def>.*?\()([Cc]fr\.\s)([A-Za-zÀ-Úà-ú]+(?:\d+)?(?:(,\s|;\s|\se\s)[A-Za-zÀ-Úà-ú]+(?:\d+)?)+)(\).*?</def>)')    

    def replace_cfr_multiple_words_2(match):
        counters['pattern_cfr_multiple_words_2'] += 1  # Incrementa il contatore
        part1 = match.group(1) # <def> e testo prima di cfr.
        cfr = match.group(2) # cfr.
        words_block = match.group(3) # Parole da codificare separate da ","
        #Parte 4 è il separatore tra le parole: non serve selezionarlo
        part5 = match.group(5) # Chiusura tag

        # Suddivide le parole mantenendo i separatori (e, ", ")
        words = re.split(r'(,\s|;\s|\se\s)', words_block)

        # Codifica ogni parola individualmente, mantenendo i separatori
        coded_words = "".join([
            f"@RR@{word.strip()}@_@" if word.strip() and not re.fullmatch(r',\s|;\s|\se\s', word) and not re.fullmatch(r'\d*', word) else word
            for word in words
        ])

        return f"{part1}{cfr}{coded_words}{part5}"

    modified_xml = pattern_cfr_multiple_words_2.sub(replace_cfr_multiple_words_2, modified_xml)


#11 Regex per trovare il pattern con " cfr." con parentesi
    pattern_cfr_parenthesis = re.compile(r'(<def>.*?)(\(.*?[Cc]fr\. )([A-Za-zÀ-Úà-ú\s]+(?:\s+[A-Za-zÀ-Úà-ú]+)*)(\d+)?([.?!]?\).|;\s)(.*?)(</def>)')
    
    def replace_cfr_parenthesis(match):
        counters['pattern_cfr_parenthesis'] += 1 # Incrementa il contatore
        part1 = match.group(1) # <def> e eventuale testo nella parentesi prima di cfr.
        cfr = match.group(2) # Cfr.
        word = match.group(3) # La parola o le parole (polirematica) da codificare
        part4 = match.group(4) if match.group(4) else "" # Eventuale numero indicante il lemma (attaccato al lemma stesso)
        part5 = match.group(5) # Chiusura parentesi e punto o punto e virgola e spazio
        part6 = match.group(6) if match.group(6) else "" # Eventuale testo dopo il rinvio
        part7 = match.group(7) # Chiusura tag

        return f"{part1}{cfr}@RR@{word}{part4}@_@{part5}{part6}{part7}"
    
    modified_xml = pattern_cfr_parenthesis.sub(replace_cfr_parenthesis, modified_xml)


#12 Regex per trovare il pattern con v. fra parentesi e con più rinvii nello stesso campo (separati da e)
    pattern_v_multiple_words_parenthesis = re.compile(r'(<def>.*?)(\([Vv]\.\s)([A-Za-zÀ-Úà-ú\s]+(?:\d+)?(?:[\s,;]*[A-Za-zÀ-Úà-ú\s]+(?:\d+)?)*)(\)\.</def>)')
    
    def replace_v_multiple_words_parenthesis(match):
        counters['pattern_v_multiple_words_parenthesis'] += 1  # Incrementa il contatore
        part1 = match.group(1)  # <def> e testo prima di v.
        v = match.group(2)  # v.
        words_block = match.group(3)  # Parole da codificare separate da "e" o ","
        part4 = match.group(4)  # Chiusura tag

        # Suddivide le parole mantenendo i separatori (",", "e", ";")
        words = re.split(r'(\se\s+|,\s*|;\s*)', words_block)

        # Codifica ogni parola individualmente, mantenendo i separatori
        coded_words = "".join([
            f"@RR@{word.strip()}@_@" if word.strip() and not re.fullmatch(r'(\se\s+|,\s*|;\s*)', word) else word
            for word in words
        ])

        return f"{part1}{v}{coded_words}{part4}"

    modified_xml = pattern_v_multiple_words_parenthesis.sub(replace_v_multiple_words_parenthesis, modified_xml)


#13 Regex per trovare il pattern con v. fra parentesi e con più rinvii nello stesso campo (separati da e)
    pattern_v_multiple_words = re.compile(r'(<def>.*?)(\s[Vv]\.\s)([A-Za-zÀ-Úà-ú\s]+\d*?(?:\s?(?:e\s+|,|;)\s*[A-Za-zÀ-Úà-ú\s]+\d*?)*)(\.</def>)')
    
    def replace_v_multiple_words(match):
        counters['pattern_v_multiple_words'] += 1  # Incrementa il contatore
        part1 = match.group(1)  # <def> e testo prima di v.
        v = match.group(2)  # v.
        words_block = match.group(3)  # Parole da codificare separate da "e" o ","
        part4 = match.group(4)  # Chiusura tag

        # Suddivide le parole mantenendo i separatori ("e", ", ")
        words = re.split(r'(\se\s|,\s|;\s)', words_block)

        # Codifica ogni parola individualmente, mantenendo i separatori
        coded_words = "".join([
            f"@RR@{word.strip()}@_@" if word.strip() and not re.fullmatch(r'(\se\s|,\s|;\s)', word) else word
            for word in words
        ])

        return f"{part1}{v}{coded_words}{part4}"

    modified_xml = pattern_v_multiple_words.sub(replace_v_multiple_words, modified_xml)


#14 Regex per trovare il pattern con cfr senza parentesi
    pattern_cfr = re.compile(r'(<def>.*?)(\s[Cc]fr\.\s)([A-Za-zÀ-Úà-ú]+)(\s|\d+)?(\.|\()(.*?)(</def>)')

    def replace_cfr(match):
        if re.fullmatch(r"[A-Za-zÀ-Úà-ú]", match.group(3)) and match.group(4) is None: # Se la parola è un singolo carattere seguito da un punto, non fare nulla (evita la selezione di falsi rinvii come "S. Tommaso" o rinvii ad un'altra definizione interna alla stessa voce)
            return match.group(0)
        else:
            counters['pattern_cfr'] += 1 # Incrementa il contatore
            part1 = match.group(1) # <def> e testo prima di cfr.
            cfr = match.group(2) # Cfr.
            word = match.group(3) # La parola o le parole (espressione) da codificare
            if match.group(4) == " ":
                part4 = match.group(4)
                part4num = ""
            elif match.group(4) == None:
                part4 = ""
                part4num = ""
            else:
                part4num = match.group(4)
                part4 = ""
            part5 = match.group(5) # Punto
            part6 = match.group(6) if match.group(6) else "" # Eventuale testo dopo il rinvio
            part7 = match.group(7) # Chiusura tag
            return f"{part1}{cfr}@RR@{word}{part4num}@_@{part4}{part5}{part6}{part7}"
    
    modified_xml = pattern_cfr.sub(replace_cfr, modified_xml)


#15 Regex per trovare il pattern con v con parentesi
    pattern_v_parenthesis = re.compile(r'(<def>.*?)(\(.*?[Vv]\.\s)([A-Za-zÀ-Úà-ú\s]+)(\d+)?(\)[.;]?.*?)(</def>)')
    
    def replace_v_parenthesis(match):
        counters['pattern_v_parenthesis'] += 1 # Incrementa il contatore
        part1 = match.group(1) # <v> e testo prima di v.
        part2 = match.group(2) # (v.
        word = match.group(3) # La parola o le parole (espressione) da codificare
        part4 = match.group(4) if match.group(4) else "" # Eventuale numero indicante il lemma (attaccato al lemma stesso)
        part5 = match.group(5) # Punto o punto e virgola + eventuale testo
        part6 = match.group(6) # Chiusura tag

        return f"{part1}{part2}@RR@{word}{part4}@_@{part5}{part6}"
    
    modified_xml = pattern_v_parenthesis.sub(replace_v_parenthesis, modified_xml)


# Restituisce il contenuto modificato e i contatori
    return modified_xml, counters


def process_multiple_files(input_dir, output_dir):
    # Raccoglie tutti i file XML nella directory
    xml_files = glob.glob(os.path.join(input_dir, "*.xml"))

    # Inizializza un dizionario per sommare i contatori di tutti i file
    total_counters = {
        'pattern_cfr_anche': 0,
        'pattern_v_anche': 0,
        'pattern_v_anche_numero': 0,
        'pattern_v_numero': 0,
        'pattern_cfr_numero': 0,
        'pattern_coniug': 0,
        'pattern_coniug_parenthesis': 0,
        'pattern_coniugazione': 0,
        'pattern_cfr_multiple_words_1': 0,
        'pattern_cfr_multiple_words_2': 0,
        'pattern_cfr_parenthesis': 0,
        'pattern_v_multiple_words_parenthesis': 0,
        'pattern_v_multiple_words': 0,
        'pattern_cfr': 0,
        'pattern_v_parenthesis': 0,
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
input_directory = '/Users/matteochiaramonte/Git/rinvii_GDLI/vol3_codificaVociRinvio'
output_directory = '/Users/matteochiaramonte/Git/rinvii_GDLI/vol3_codificaCompleta'

# Controllo che la cartella di output esista
os.makedirs(output_directory, exist_ok=True)

# Processo tutti i file nella directory
process_multiple_files(input_directory, output_directory)

print("Elaborazione completata su tutti i file!")