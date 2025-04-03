import sqlite3
import re
import unicodedata

def init_db():
    conn = sqlite3.connect("definitions_en.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS definitions (
            mot TEXT PRIMARY KEY,
            definition TEXT,
            source TEXT
        )
    """)
    conn.commit()
    conn.close()

def enlever_accents(texte):
    """Delete all accents of a string"""
    return ''.join(c for c in unicodedata.normalize('NFD', texte) if unicodedata.category(c) != 'Mn')

def chercher_mot(fichier, mot):
    try:
        mot_normalise = enlever_accents(mot.lower())  
        with open(fichier, 'r', encoding='utf-8') as f:
            for i, ligne in enumerate(f, start=1):
                ligne_normalisee = enlever_accents(ligne.strip().lower())  
                if ligne_normalisee == mot_normalise:
                    return i, ligne.strip()
    except FileNotFoundError:
        print("File not found.")
    return None, None

def chercher_ligne(fichier, numero_ligne):
    """Search a specific line in the file."""
    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            lignes = f.readlines()
            if 1 <= numero_ligne <= len(lignes):  
                return lignes[numero_ligne - 1].strip()  
    except FileNotFoundError:
        print("File not found.")
    return None

def retirer_chiffres(phrase):
    return ''.join([c for c in phrase if not c.isdigit()])

def analyser_commande(command):
    """Analyse if the command is '/do search !line_nb:true && !word:false"""
    match = re.search(r"~/§\[line:(\d+)", command)
    if match:
        return int(match.group(1))
    return None  

def main():
    init_db()
    fichier = "english.txt"  
    mot = input("Enter a word, a sentence or a command.\nCommand list: \n1. /do stop\nStoping the program\n2. /do search !line_nb:true && !word:false\nDon't search the word, but the line (BUGGY, BUT, REALLY BUGGY)\n$ ").strip()
    
    # Verification if the special command is used
    numero_ligne = analyser_commande(mot)
    if numero_ligne:
        ligne_trouvee = chercher_ligne(fichier, numero_ligne)
        if ligne_trouvee:
            print(f"Ligne {numero_ligne} : {ligne_trouvee}")
        else:
            print(f"Zero lines found for the number: {numero_ligne}.")
        return main()  

    elif mot == "/do stop":
        return 0
    # Normal Treating (sorry for the translation T_T)
    phrase_sans_chiffres = retirer_chiffres(mot)
    mots = phrase_sans_chiffres.split()
    
    resultats = []
    numeros_ligne = []
    mots_trouves = []
    
    for mot in mots:
        ligne, mot_trouve = chercher_mot(fichier, mot)
        if mot_trouve:
            numeros_ligne.append(str(ligne))
            mots_trouves.append(mot_trouve)
            resultats.append(f"{ligne} | {mot_trouve}.")  
        else:
            resultats.append(f"Sorry, but I didn't find {mot} in the file.")
    
    if numeros_ligne and mots_trouves:
        print(" ".join(numeros_ligne))
        print(" ".join(mots_trouves))
    
    return main()

if __name__ == "__main__":
    main()
