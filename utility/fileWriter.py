import json
import os
import threading



def write_json(data, filePath):
    print(f"Writing JSON to {filePath}")
    try:
        with open(filePath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing JSON to {filePath}: {e}")

def write_text(data, filePath):
    print(f"Writing file to {filePath}")
    try:
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(data)   
    except Exception as e:
        print(f"Error writing text to {filePath}: {e}")

def write_binary(data, filePath):
    print(f"Writing binary data to {filePath} ({len(data)} bytes)")
    try:
        # Crea la directory se non esiste
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        with open(filePath, 'wb') as f:  # Nota la 'b' per modalità binaria
            f.write(data)
        # Verifica che il file sia stato creato correttamente
        if os.path.exists(filePath) and os.path.getsize(filePath) > 0:
            print(f"File scritto correttamente: {filePath} ({os.path.getsize(filePath)} bytes)")
        else:
            print(f"Attenzione: il file è stato creato ma sembra vuoto: {filePath}")
    except Exception as e:
        print(f"Error writing binary data to {filePath}: {e}")