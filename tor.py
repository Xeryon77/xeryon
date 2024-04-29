import os
import hashlib
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def send_pushbullet_notification(title, message, token):
    url = "https://api.pushbullet.com/v2/pushes"
    headers = {
        "Access-Token": token,
        "Content-Type": "application/json"
    }
    data = {
        "type": "note",
        "title": title,
        "body": message
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

url = "https://www.binance.com/en/copy-trading/lead-details/3887627985594221568?timeRange=7D"

# Inicializace webdriveru
driver = webdriver.Firefox()

# Načtení stránky
driver.get(url)

# Čekání 10 vteřin před kliknutím na tlačítko 'trade history'
time.sleep(10)

wait = WebDriverWait(driver, 5)  # čekání 10 sekund
trade_history_button = wait.until(EC.element_to_be_clickable((By.ID, 'tab-tradeHistory')))

# Kliknutí na tlačítko 'trade history'
trade_history_button.click()

# Čekání 10 vteřin na načtení dat
time.sleep(5)

# Získání HTML stránky
html = driver.page_source

# Vytvoření BeautifulSoup objektu
soup = BeautifulSoup(html, 'html.parser')

# Extrahování dat
data = soup.find_all('div', {'class': 'history-content css-lmauh6'})  # Nahraďte 'data-class' skutečnou třídou dat, která vás zajímá

# Vytvoření hash hodnoty z dat
data_hash = hashlib.md5(str(data).encode()).hexdigest()

# Kontrola, zda se data změnila od poslední kontroly
if os.path.exists('last_data_hash.txt'):
    with open('last_data_hash.txt', 'r') as file:
        last_data_hash = file.read()
    if last_data_hash == data_hash:
        print("Data se nezměnila.")
    else:
        print("Data se změnila.")
        send_pushbullet_notification(
            "Data se změnila",
            "Tortoise_Haire".format(url),
            "o.fbXAJ6jk4aw8CMkkuENzv0Z7zN1gPIHQ"  # Nahraďte "váš_pushbullet_api_klíč" skutečným API klíčem
        )
else:
    print("Probíhá první kontrola dat.")

# Uložení hash hodnoty pro další kontrolu
with open('last_data_hash.txt', 'w') as file:
    file.write(data_hash)

# Uzavření prohlížeče
driver.close()
