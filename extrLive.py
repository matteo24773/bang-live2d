import playwright
import utility.fileWriter as writer
import json
import utility.requestIntercept as req
import os
import time

# init
rq = req.request()
rq.page()
target=""
# links
baselink="https://bestdori.com/assets/jp/live2d/chara"
infoLink="https://bestdori.com/api/explorer/jp/assets"

# funzioni
def makeDir(path):
    os.makedirs(path, exist_ok=True)

def targetResourceExtract(key,responseTarget):
    makeDir(f"resources/{target}/{key}")
    model={"version":3, "textures": [], "model": "", "physics": "", "expressions": [],"motions": {}}
    for resource in responseTarget:
        if"png"in resource and "texture" in resource:
            pngResponse=rq.pag.request.get(f"{baselink}/{key}_rip/{resource}")
            writer.write_binary(pngResponse.body(), f"resources/{target}/{key}/{resource}")
            model["textures"].append(resource)
        elif "moc" in resource:
            mocResponse=rq.pag.request.get(f"{baselink}/{key}_rip/{resource}")
            writer.write_binary(mocResponse.body(), f"resources/{target}/{key}/{resource}3")
            model["model"] = f"{resource}3"
        elif "physics.json" in resource:
            physicsResponse=rq.pag.request.get(f"{baselink}/{key}_rip/{resource}")
            writer.write_json(physicsResponse.json(), f"resources/{target}/{key}/{resource}")
            model["physics"] = resource
        elif "json" in resource:
            makeDir(f"resources/{target}/{key}/expressions")
            jsonResponse=rq.pag.request.get(f"{baselink}/{key}_rip/{resource}")
            writer.write_json(jsonResponse.json(), f"resources/{target}/{key}/expressions/{resource}")
            model["expressions"].append({"name":resource.split(".json")[0],"file":"expressions/"+resource})
        elif "mtn" in resource:
            makeDir(f"resources/{target}/{key}/expressions")
            mtnResponse=rq.pag.request.get(f"{baselink}/{key}_rip/{resource}")
            writer.write_binary(mtnResponse.body(), f"resources/{target}/{key}/expressions/{resource}")
            model["motions"][resource.split(".mtn")[0]] = {"file": f"expressions/{resource}", "fade_in": 1000, "fade_out": 1000}
        else:
            print(f"Risorsa non gestita: {resource}")
        time.sleep(0.3)  # Aggiungi un breve ritardo per evitare di sovraccaricare il server
    writer.write_json(model, f"resources/{target}/{key}/model.json")

            
# main

infoResponse = rq.pag.goto(infoLink+"/_info.json")
live2dinfo= infoResponse.json()["live2d"]["chara"]
while target != "exit":
    target = input("Inserisci il nome del personaggio (o 'exit' per uscire): ").strip()
    if target == "exit":
        break
    if target.isnumeric() is False:
        print("Codice non valido, reinserire")
        continue
    for x in live2dinfo.keys():
        if target in x:
            print(f"{baselink}/{x}.json")
            responseTarget= rq.pag.request.get(f"{infoLink}/live2d/chara/{x}.json").json()
            targetResourceExtract(x,responseTarget)
            
    print(f"Elaborazione delle risorse per {target}...")
    
