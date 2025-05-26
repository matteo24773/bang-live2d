import requests
from bs4 import BeautifulSoup as bs
import jsbeautifier
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import json
import os
import time
import base64


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# Configurazione Chrome
# options = Options()
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless")

# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# try:
#     driver.get("https://bestdori.com/tool/explorer/asset/jp/live2d/chara")  # Sostituisci con l'URL reale

#     # Attendi che un elemento specifico sia visibile
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, "body"))
#     )

#     # Estrai l'HTML del body
#     html = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
#     print(html)

# finally:
#     driver.quit()
# r = requests.get(general+"/js/app.b174a641.js", headers=headers)
# first = requests.get(baseLink, headers=headers)
# vendor=requests.get(general+"/js/chunk-vendors.9309a223.js", headers=headers)
# cloud=requests.get("https://static.cloudflareinsights.com/beacon.min.js/vcd15cbe7772f49c399c6a5babf22c1241717689176015", headers=headers)
# soup = bs(r.text, "html.parser")
# with open("beautified.js", "w",encoding="utf-8") as f:
#     f.write(jsbeautifier.beautify(r.text))
# with open("vendor.js", "w",encoding="utf-8") as f:
#     f.write(jsbeautifier.beautify(vendor.text))
# with open("cloud.js", "w",encoding="utf-8") as f:
#     f.write(jsbeautifier.beautify(cloud.text))
# print(bs(first.text, "html.parser").find_all("script"))

# funzione quando si fa una richiesta POST
# def log_post_requests(request):
#     if request.method == "POST":
#         print(f"POST Request to: {request.url}")
#         try:
#             post_data = request.post_data
#             print("POST data:", post_data)
#             print("POST data:", request.response)
#         except:
#             print("No POST data available")

# with open("dati.json", "w",encoding="utf-8") as js:
#         f.write(page.content())

    # 🔽 Ora stampa il DOM completo (con la tabella)
#     html=page.content()
#     browser.close()
    
# html=bs( html,"html.parser").prettify()
# print(html)


def log_post_responses(response):
    try:
        request = response.request
        print(f"Response for POST to {request.url}:")
        # prova a stampare il corpo della risposta come testo
        if ".json" in response.url:
            with open(f"{urlparse(response.url).path}.json".strip().replace("/","_"), "w",encoding="utf-8") as f:
                f.write( jsbeautifier.beautify(response.text))
    except:
        print("No response body available")

map={}
baseLink = "https://bestdori.com/tool/explorer/asset/jp/live2d/chara"
general="https://bestdori.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe")
    page = browser.new_page()
    page.goto(baseLink)
    # page.on("request",log_post_requests )
    page.on("response", log_post_responses)
    # page.wait_for_selector("table")  # oppure un altro selettore
    
# with open("_api_explorer_jp_assets__info.json.json", "r",encoding="utf-8") as f:
#     data=json.load(f)
#     for key in data["live2d"]["chara"]:
#         if "general" in key:
#             time.sleep(30)
#             r=requests.get(f"{baseLink}/{key}", headers=headers)
#             text=bs(r.text, "html.parser")
#             print(text.text)
        
