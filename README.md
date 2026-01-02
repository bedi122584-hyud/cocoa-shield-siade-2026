# 🛡️ Cocoa-Shield: Souveraineté Numérique du Cacao Ivoirien
> Projet candidat au Hackathon SIADE 2026 - Thème : Agriculture Intelligente & Souveraineté.

## 💡 Le Concept
**Cocoa-Shield** est une infrastructure de traçabilité "Offline-First" conçue pour répondre aux exigences du règlement européen **RDUE (EUDR)** sans compromettre la souveraineté des données géographiques ivoiriennes.

Contrairement aux solutions SaaS étrangères, Cocoa-Shield permet de vérifier la conformité (Non-Déforestation) localement et de générer une **Preuve à Divulgation Nulle de Connaissance (Zero-Knowledge Proof)** pour l'export.

## 🏗️ Architecture Technique
Le projet repose sur une stack Open Source robuste et déployable en souveraineté (Intranet/Datacenter Local).

* **📱 Mobile (Pisteurs) :** Flutter (Mode 100% Offline pour zones blanches).
* **🧠 Backend (Souverain) :** Python (FastAPI).
* **🗺️ Core SIG :** PostgreSQL + PostGIS (Moteur spatial).
* **🔒 Sécurité :** Chiffrement AES-256 des polygones parcellaires.
* **📦 Déploiement :** Docker / Docker Compose.

## 🚀 Roadmap (Hackathon)
- [x] Initialisation de l'environnement Docker (PostGIS).
- [ ] Ingestion des données cartographiques (Forêts Classées / Zones Protégées).
- [ ] Développement de l'API de validation spatiale (Python).
- [ ] Prototype Mobile de collecte terrain.
- [ ] Démo finale : Génération du Certificat de Conformité.

---
*Développé par la Team Cocoa-Shield.*
