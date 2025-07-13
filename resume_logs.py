import requests
import json

# Remplace par ta clé Gemini
API_KEY = "AIzaSyBQv8D4vQMijV5e4LClGSkAbQW_Xq23zSE"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

with open("logs.txt", "r", encoding="utf-8") as f:
    logs = f.read()

prompt = f"Résume ces logs Jenkins en quelques lignes lisibles pour un développeur :\n{logs}"

headers = {"Content-Type": "application/json"}

body = {
    "contents": [
        {"parts": [{"text": prompt}]}
    ]
}

response = requests.post(f"{GEMINI_URL}?key={API_KEY}", headers=headers, data=json.dumps(body))

if response.status_code == 200:
    data = response.json()
    summary = data["candidates"][0]["content"]["parts"][0]["text"]
    print("\n===== Résumé des logs par Gemini =====\n")
    print(summary)
    print("\n======================================\n")
    with open('logs.txt', 'r', encoding='latin1') as f:
        out.write(summary)
else:
    print(f"Erreur API Gemini : {response.status_code}")
    print(response.text)

    #Approve mis dans jenkins pour Acceder au RawBuild
