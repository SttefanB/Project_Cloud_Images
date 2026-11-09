import pydicom
import os
import base64
import requests # Adăugăm librăria pentru rețea
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def anonimizeaza_imagine(cale_intrare, cale_iesire): # Citim imaginea 
    print(f"[1] Se citește imaginea: {cale_intrare}")
    # Citim fișierul DICOM
    dataset = pydicom.dcmread(cale_intrare)

    # Ștergem/înlocuim datele sensibile (Anonimizare)
    dataset.PatientName = "ANONIM"
    dataset.PatientID = "000000"
    if 'PatientBirthDate' in dataset:
        del dataset.PatientBirthDate # Ștergem data nașterii complet
        
    dataset.save_as(cale_iesire)
    print(f"[2] Imaginea a fost anonimizată și salvată ca: {cale_iesire}")

def cripteaza_fisier(cale_fisier, parola):
    print("[3] Se generează cheia AES pe baza parolei tale...")
    
    # "Salt-ul" face ca două parole identice să genereze chei diferite. 
    # În producție, acesta se generează aleatoriu per fișier.
    salt = b"sare_secreta_pentru_imagistica" 
    
    # PBKDF2: Transformă o parolă umană (ex: "parola123") într-o cheie de 32 bytes (AES)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000, # Rulează algoritmul de 480.000 de ori pentru a bloca atacurile de tip brute-force
    )
    cheie = base64.urlsafe_b64encode(kdf.derive(parola.encode()))
    sistem_criptare = Fernet(cheie)
    
    # Citim imaginea deja anonimizată
    with open(cale_fisier, "rb") as f_in:
        date_originale = f_in.read()
        
    # O criptăm
    date_criptate = sistem_criptare.encrypt(date_originale)
    
    # O salvăm cu extensia .enc (Encrypted)
    cale_criptata = cale_fisier + ".enc"
    with open(cale_criptata, "wb") as f_out:
        f_out.write(date_criptate)
        
    print(f"[4] Fișierul a fost criptat cu succes: {cale_criptata}")
    return cale_criptata

# === NOU: Funcția de rețea ===
def trimite_la_server(cale_fisier_criptat, url_server="http://34.235.89.155:8000/upload"):
    print(f"[5] Se inițiază conexiunea HTTP POST către: {url_server}")
    
    # Deschidem fișierul criptat în mod citire binară ("rb")
    with open(cale_fisier_criptat, "rb") as f:
        # Structurăm pachetul exact cum se așteaptă FastAPI (sub cheia "file")
        pachet_date = {"file": (os.path.basename(cale_fisier_criptat), f)}
        
        # Trimiterea efectivă a request-ului
        raspuns = requests.post(url_server, files=pachet_date)
        
    if raspuns.status_code == 200:
        print("[SUCCES] Răspuns de la Server:", raspuns.json())
    else:
        print(f"[EROARE] Serverul a respins conexiunea. Cod HTTP: {raspuns.status_code}")

#ZONA DE TESTARE ACTUALIZATĂ
if __name__ == "__main__":
    fisier_original = "test.dcm"
    fisier_anonim = "anonimizat.dcm"
    parola_mea = "ParolaSuperSecreta"
    
    if os.path.exists(fisier_original):
        anonimizeaza_imagine(fisier_original, fisier_anonim)
        fisier_final_criptat = cripteaza_fisier(fisier_anonim, parola_mea)
        
        # Apelăm funcția de rețea!
        trimite_la_server(fisier_final_criptat)
    else:
        print(f"[EROARE] Nu am găsit fișierul '{fisier_original}'.")