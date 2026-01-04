from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import databases
import qrcode # Pour générer le QR
import os
from datetime import datetime

# Configuration Base de Données
DATABASE_URL = "postgresql://admin_cocoa:secure_password_2026@db:5432/cocoa_shield_db"
database = databases.Database(DATABASE_URL)

app = FastAPI(title="Cocoa-Shield API", version="1.2")

class ChampCheck(BaseModel):
    proprietaire: str
    coordinates: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/check-compliance/")
async def check_compliance(champ: ChampCheck):
    # 1. Nettoyage des coordonnées
    try:
        polygon_wkt = f"POLYGON(({champ.coordinates}))"
    except Exception:
        raise HTTPException(status_code=400, detail="Format invalide")

    # 2. Vérification (SELECT)
    query_check = """
        SELECT f.nom FROM forets_classees f
        WHERE ST_Intersects(ST_MakeValid(ST_GeomFromText(:wkt, 4326)), f.geometrie)
        LIMIT 1;
    """
    result_check = await database.fetch_one(query=query_check, values={"wkt": polygon_wkt})
    
    is_compliant = True
    status_message = "CONFORME"
    message_detail = "Validé pour export UE."
    
    if result_check:
        is_compliant = False
        status_message = "NON_CONFORME"
        message_detail = f"Alerte : Intrusion {result_check['nom']}"

    # 3. Sauvegarde (INSERT)
    query_save = """
        INSERT INTO champs_cacao (proprietaire, geometrie, est_conforme)
        VALUES (:prop, ST_MakeValid(ST_GeomFromText(:wkt, 4326)), :conf)
    """
    try:
        await database.execute(query=query_save, values={
            "prop": champ.proprietaire, "wkt": polygon_wkt, "conf": is_compliant
        })
    except Exception as e:
        print(f"Erreur save: {e}")

    # --- ETAPE 4 : GÉNÉRATION DU QR CODE (NOUVEAU !) ---
    qr_filename = ""
    if is_compliant:
        # On crée le contenu du QR Code (La "Preuve")
        date_jour = datetime.now().strftime("%Y-%m-%d %H:%M")
        data_preuve = f"CERTIFICAT RDUE-2026\nProducteur: {champ.proprietaire}\nDate: {date_jour}\nStatut: VALIDE\nSignature: COCOA-SHIELD-SECURE"
        
        # On génère l'image
        qr = qrcode.make(data_preuve)
        
        # On sauvegarde l'image dans le dossier du serveur
        clean_name = champ.proprietaire.replace(" ", "_")
        qr_filename = f"certificat_{clean_name}.png"
        qr.save(qr_filename)
        print(f"🎟️ QR Code généré : {qr_filename}")

    return {
        "status": status_message,
        "message": message_detail,
        "compliant": is_compliant,
        "qr_file": qr_filename # On dit au téléphone comment s'appelle l'image
    }