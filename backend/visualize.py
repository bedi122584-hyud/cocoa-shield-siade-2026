import folium
import psycopg2
import os

# Connexion à la base de données
# "db" est le nom du service Docker, "admin_cocoa" l'utilisateur
DB_URL = "postgresql://admin_cocoa:secure_password_2026@db:5432/cocoa_shield_db"

def generer_carte():
    print("🌍 Connexion à la base de données...")
    try:
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        return

    # 1. Création de la carte (Centrée sur la Côte d'Ivoire)
    # Coordonnées : Yamoussoukro [6.82, -5.27] ou Centre Géo [7.54, -5.55]
    print("🗺️  Initialisation de la carte sur la Côte d'Ivoire...")
    m = folium.Map(location=[7.54, -5.55], zoom_start=7)

    # 2. Récupérer et dessiner les Forêts (En VERT)
    print("🌲 Récupération des forêts...")
    cursor.execute("SELECT nom, ST_AsGeoJSON(geometrie) FROM forets_classees;")
    for nom, geojson in cursor.fetchall():
        if geojson:
            folium.GeoJson(
                geojson,
                style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'weight': 2, 'fillOpacity': 0.4},
                tooltip=f"Zone Protégée: {nom}"
            ).add_to(m)

    # 3. Récupérer et dessiner les Champs (En ROUGE si illégal, BLEU si OK)
    print("🍫 Récupération des champs...")
    # Requête pour vérifier l'intersection
    query = """
    SELECT c.proprietaire, ST_AsGeoJSON(c.geometrie),
           EXISTS(SELECT 1 FROM forets_classees f WHERE ST_Intersects(c.geometrie, f.geometrie)) as is_illegal
    FROM champs_cacao c;
    """
    cursor.execute(query)
    
    compteur = 0
    for nom, geojson, is_illegal in cursor.fetchall():
        if geojson:
            compteur += 1
            # Logique de couleur
            color = 'red' if is_illegal else 'blue'
            fill_color = 'red' if is_illegal else '#3388ff' # Bleu joli
            statut = "ILLEGAL 🚨" if is_illegal else "CONFORME ✅"
            
            folium.GeoJson(
                geojson,
                style_function=lambda x, col=color, fill=fill_color: {
                    'fillColor': fill, 
                    'color': col, 
                    'weight': 2, 
                    'fillOpacity': 0.6
                },
                tooltip=f"Paysan: {nom} ({statut})"
            ).add_to(m)

    print(f"📊 {compteur} champs trouvés et dessinés.")

    # 4. Sauvegarder
    output_file = "carte_demo.html"
    m.save(output_file)
    print(f"✅ Carte générée avec succès : {output_file}")

    conn.close()

if __name__ == "__main__":
    generer_carte()