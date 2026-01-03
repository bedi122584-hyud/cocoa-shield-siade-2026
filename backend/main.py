from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import databases

# Configuration de la base de données (Note: "db" est le nom du service dans Docker)
DATABASE_URL = "postgresql://admin_cocoa:secure_password_2026@db:5432/cocoa_shield_db"

database = databases.Database(DATABASE_URL)

app = FastAPI(title="Cocoa-Shield API", version="1.0")

# Modèle de données (Ce que l'application mobile envoie)
class ChampCheck(BaseModel):
    proprietaire: str
    coordinates: str  # Format attendu : "LONG LAT, LONG LAT, ..." (WKT simplifie)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"message": "Cocoa-Shield API est en ligne 🚀"}

@app.post("/check-compliance/")
async def check_compliance(champ: ChampCheck):
    """
    Vérifie si un champ chevauche une forêt classée.
    """
    # 1. On construit le polygone à partir des coordonnées reçues
    polygon_wkt = f"POLYGON(({champ.coordinates}))"
    
    # 2. La requête SQL magique (la même que tu as testée !)
    query = """
        SELECT f.nom 
        FROM forets_classees f
        WHERE ST_Intersects(
            ST_GeomFromText(:wkt, 4326),
            f.geometrie
        )
        LIMIT 1;
    """
    
    # 3. Exécution
    result = await database.fetch_one(query=query, values={"wkt": polygon_wkt})
    
    # 4. Réponse
    if result:
        return {
            "status": "NON_CONFORME",
            "message": f"Alerte : Chevauchement détecté avec {result['nom']}",
            "compliant": False
        }
    else:
        return {
            "status": "CONFORME",
            "message": "Aucun chevauchement détecté. Cacao validé.",
            "compliant": True
        }