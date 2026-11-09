from fastapi import FastAPI, UploadFile, File
import uvicorn
import os
# Test final deployment CI/CD
# 1. Inițializăm aplicația
app = FastAPI(title="API Seif Securizat")

# Creăm un folder local care va simula stocarea din cloud (S3)
FOLDER_STOCARE = "stocare_cloud"
os.makedirs(FOLDER_STOCARE, exist_ok=True)

# 2. Definim ruta (punctul de frontieră unde așteptăm datele)
@app.post("/upload")
async def upload_encrypted_file(
    # Pydantic/FastAPI forțează clientul să trimită exact un fișier
    file: UploadFile = File(...)
):
    print(f"[SERVER] Primesc fișierul: {file.filename}")

    # Citim biții (zgomotul alb)
    continut_criptat = await file.read()
    
    # Salvăm fișierul pe "server"
    cale_salvare = os.path.join(FOLDER_STOCARE, file.filename)
    with open(cale_salvare, "wb") as buffer:
        buffer.write(continut_criptat)
        
    print(f"[SERVER] Fișier salvat cu succes în: {cale_salvare}")
    
    # 3. Răspundem clientului cu un mesaj JSON
    return {
        "status": "succes",
        "mesaj": "Fișier recepționat și izolat în siguranță!",
        "nume_fisier": file.filename,
        "dimensiune_bytes": len(continut_criptat)
    }

# Pornim serverul asincron
if __name__ == "__main__":
    print("Pornim serverul. Așteptăm conexiuni pe portul 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)