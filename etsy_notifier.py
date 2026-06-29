import os
import requests
from datetime import datetime, timedelta

# --- VOS IDENTIFIANTS SÉCURISÉS ---
# Le script va chercher ces infos dans les variables d'environnement de GitHub
ETSY_SHOP_ID = os.environ.get("ETSY_SHOP_ID")
ETSY_ACCESS_TOKEN = os.environ.get("ETSY_ACCESS_TOKEN")
ETSY_API_KEY = os.environ.get("ETSY_API_KEY")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def get_recent_etsy_orders():
    # Calculer le timestamp d'il y a 12 heures
    past_12_hours = int((datetime.now() - timedelta(hours=12)).timestamp())
    
    url = f"https://openapi.etsy.com/v3/application/shops/{ETSY_SHOP_ID}/receipts"
    
    headers = {
        "x-api-key": ETSY_API_KEY,
        "Authorization": f"Bearer {ETSY_ACCESS_TOKEN}"
    }
    
    params = {
        "min_created": past_12_hours,
        "was_paid": True
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Erreur API Etsy: {response.status_code} - {response.text}")
        return []

def send_discord_notification(order):
    # Vous pouvez personnaliser ce message !
    # message = f"🎉 **Nouvelle Commande Etsy !**\n" \
              # f"Montant : {order['grandtotal']['amount']} {order['grandtotal']['currency_code']}\n" \
              # f"Acheteur : {order['name']}"
              
    # payload = {"content": message}
    # requests.post(DISCORD_WEBHOOK_URL, json=payload)

# --- EXECUTION DU SCRIPT ---
if __name__ == "__main__":
    if not all([ETSY_SHOP_ID, ETSY_ACCESS_TOKEN, ETSY_API_KEY, DISCORD_WEBHOOK_URL]):
        print("Erreur : Il manque des clés API dans les secrets GitHub.")
    else:
        orders = get_recent_etsy_orders()
        if orders:
            for order in orders:
                send_discord_notification(order)
            print(f"{len(orders)} commande(s) trouvée(s) et notifiée(s).")
        else:
            print("Aucune nouvelle commande ces 12 dernières heures.")
