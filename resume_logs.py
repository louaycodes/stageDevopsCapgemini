import requests
import json

# Ta clé Gemini personnelle
API_KEY = "AIzaSyBQv8D4vQMijV5e4LClGSkAbQW_Xq23zSE"
# URL avec f-string pour injecter la clé
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Lire les logs Jenkins depuis le fichier (encodage latin1 pour éviter erreurs)
with open("logs.txt", "r", encoding="latin1") as f:
    logs = f.read()

# Préparer le prompt pour Gemini
prompt = f"""Aide a comprendre l'erreur si elle existe dans les logs suivants. si il n a pas d'erreur, mentionne que tous vas bien
Dans les 2 cas fais un résumé des logs Tres important : Propose une solution au erreurs rencontrés.
Voici les logs :
{logs}
"""


headers = {
    "Content-Type": "application/json"
}

body = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ]
}

try:
    # Appel API Gemini
    response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(body))
    response.raise_for_status()  # Pour lever une erreur HTTP si status != 200
except requests.exceptions.RequestException as e:
    print(f"Erreur lors de la requête API Gemini : {e}")
    exit(1)

# Gérer la réponse
data = response.json()
try:
    summary = data["candidates"][0]["content"]["parts"][0]["text"]
except (KeyError, IndexError):
    summary = "Erreur lors de l'analyse de la réponse Gemini."

# Afficher dans Jenkins console
print("\n===== Résumé des logs par Gemini =====\n")
print(summary)
print("\n======================================\n")

# Sauvegarder dans un fichier
with open("resume_logs.txt", "w", encoding="cp1252", errors="replace") as out:
    out.write(summary)

    
#modiffication du url de gemini