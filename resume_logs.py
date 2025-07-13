import requests
import json

# Remplace par ta clé Gemini personnelle
API_KEY = "AIzaSyBQv8D4vQMijV5e4LClGSkAbQW_Xq23zSE"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"


# Lire les logs Jenkins depuis le fichier (avec encodage compatible Windows)
with open("logs.txt", "r", encoding="latin1") as f:
    logs = f.read()

# Préparer le prompt pour Gemini
prompt = f"Résume ces logs Jenkins en quelques lignes lisibles pour un développeur :\n{logs}"

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

# Appel API Gemini
response = requests.post(f"{GEMINI_URL}?key={API_KEY}", headers=headers, data=json.dumps(body))

# Gérer la réponse
if response.status_code == 200:
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
    with open("resume_logs.txt", "w", encoding="utf-8") as out:
        out.write(summary)

else:
    print(f"Erreur API Gemini : {response.status_code}")
    print(response.text)
