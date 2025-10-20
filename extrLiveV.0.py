import utility.requestIntercept as req
import utility.fileWriter as writer
import json
import time
import os
from bs4 import BeautifulSoup as bs
import asyncio
import threading
estrazione_completata = threading.Event()
targetResource=""
baseLink = "https://bestdori.com/tool/explorer/asset/jp/live2d/chara"
resource_baseLink = "https://bestdori.com/assets/jp/live2d/chara"
rq = req.request()
rq.page()
with open("nomi.json","r", encoding="utf-8") as characters_file:
    characters= json.load(characters_file)

model= {"version":3}

# Funzione per estrarre le risorse dalla risposta
def resourceExtract(response):
        print(f"Elaborazione della risposta per {response.url}...")
    # try:
        if not characters.get(target) :
            resourcePath=f"resources/{target}/{targetResource}"
        else:
            resourcePath=f"resources/{characters.get(target)}/{targetResource}"
        request = response.request
        url=request.url
        if f"{targetResource}.json" in url:
            rq.pag.once("response", resourceExtract)
            print(f"Elaborazione della risposta per {url}...")
            resourcesIndex=response.json()
            print(f"Risorse trovate: {len(resourcesIndex)}")
            for resource in resourcesIndex:

                print(f"{resource_baseLink}/{targetResource}_rip/{resource}")
                if resource.endswith(".png")and "texture" in resource:
                    print(f"Scaricamento della texture: {resource}")
                    resourceResponse= rq.pag.request.get(f"{resource_baseLink}/{targetResource}_rip/{resource}")
                    os.makedirs(resourcePath, exist_ok=True)
                    writer.write_binary(resourceResponse.body(),resourcePath+"/"+resource)
                    if not model.get("textures"):
                        model["textures"] = []
                    model["textures"].append(resource)
                    writer.scrittura_completata.wait()
                elif resource.endswith(".moc"):
                    # Usa fetch invece di goto per i file binari che vengono scaricati automaticamente
                    fetch_response =  rq.pag.request.get(f"{resource_baseLink}/{targetResource}_rip/{resource}")
                    moc_data = fetch_response.body()
                    os.makedirs(resourcePath, exist_ok=True)
                    writer.write_binary(moc_data, f"{resourcePath}/{resource}3")
                    model["model"] = f"{resource}3"
                    print(f"File MOC scaricato: {resource}")
                    writer.scrittura_completata.wait()
                elif resource.endswith(".physics.json"):
                    resourceResponse= rq.pag.request.get( f"{resource_baseLink}/{targetResource}_rip/{resource}")
                    os.makedirs(resourcePath, exist_ok=True)
                    writer.write_json(resourceResponse.json(),resourcePath+"/"+resource)
                    model["physics"] = resource
                elif resource.endswith(".json"):
                    resourceResponse= rq.pag.request.get(f"{resource_baseLink}/{targetResource}_rip/{resource}")
                    os.makedirs(resourcePath+"/expressions", exist_ok=True)
                    writer.write_json(resourceResponse.body(),resourcePath+"/expressions/"+resource)
                    if not model.get("expressions"):
                        model["expressions"] = []
                    model["expressions"].append({"name":resource.split(".json")[0], "file": "expressions/"+resource})
                    writer.scrittura_completata.wait()
                elif resource.endswith(".mtn"):
                    resourceResponse= rq.pag.request.get(f"{resource_baseLink}/{targetResource}_rip/{resource}")
                    os.makedirs(resourcePath+"/expressions", exist_ok=True)
                    writer.write_binary(resourceResponse.body(),resourcePath+"/expressions/"+resource)
                    if not model.get("motions"):
                        model["motions"] = {}
                    model["motions"][resource.split(".mtn")[0]]=[{"file": "expressions/"+resource,"fade_in": 1000, "fade_out": 1000}]
                    writer.scrittura_completata.wait()
                if resourcesIndex[-1] is resource:
                    writer.write_json(model, f"{resourcePath}/model.json")
                    model.clear()
                    model["version"] = 3
                    estrazione_completata.set()
        # if url.endswith(".json"):
    # except Exception as e:
    #     print(f"Error processing response: {e.args.count}")
rq.pag.on("response", req.response)
rq.goto(baseLink)
while True:
    print("codice del personaggio da estrarre:")
    target = input().strip()
    if target == "exit":
        
        break
    if target.isnumeric() is False:
        print("codice non valido, reinserire")
        continue
    if target not in characters:
        print("codice non trovato, reinserire")
        continue
    character= characters.get(target)
    
    chara = req.json_data["api_explorer_jp_assets__info.json"]["live2d"]["chara"]
    for x in chara.keys():

        targetResource = x
        if target in x:
            estrazione_completata.clear()
            print(f"{baseLink}/{x}")
            rq.pag.on("response", resourceExtract)
            print(f"Attendere il completamento dell'estrazione per {character}...")
            rq.goto(f"{baseLink}/{x}")
            estrazione_completata.wait(timeout=60)
            print(f"Estrazione completata per {character}!")