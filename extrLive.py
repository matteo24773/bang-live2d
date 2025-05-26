import utility.requestIntercept as req

baseLink = "https://bestdori.com/tool/explorer/asset/jp/live2d/chara"

print("codice del personaggio da estrarre:")
target = input().strip()

response = req.request(f"{baseLink}/{target}.json")
