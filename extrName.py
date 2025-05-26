import utility.requestIntercept as req
import time
import os
import json as j

from bs4 import BeautifulSoup as bs
baseLink="https://bestdori.com/tool/explorer/asset/jp"

targetLink = "https://bestdori.com/tool/explorer/asset/jp/live2d/chara"
nomiJson={}
nomiNonTrivati=[]
target=""
def general_date(response):
    codice=target.split("_")[0]
    if  f"{target}.json" in response.url:
        dati=response.json()
        for dato in dati:
            if "asset" in dato and "TransitionData" in dato:
                nome=dato.split("TransitionData")[0]
                nomiJson[codice]=nome
            elif nomiJson.get(codice) is None:
                nomiNonTrivati.append(codice)

rq=req.request(targetLink)
rq.page()
rq.pag.on("response", req.response)
rq.goto()

json = req.json_data


for x in json["api_explorer_jp_assets__info.json"]["live2d"]["chara"]:
    
    if x.endswith("general"):
        target = x
        print(x)
        rq.link = f"{targetLink}/{x}"
        print(rq.link)
        rq.pag.on("response", general_date)
        rq.goto()
        time.sleep(3)
try:
    with open("nomi.json", "w",encoding="utf-8") as f:
        j.dump(nomiJson,f, ensure_ascii=False, indent=4)
except Exception as e:
    print("Errore durante il salvataggio del file nomi.json:", e)


print("Nomi non trovati:", nomiNonTrivati)
rq.close()
