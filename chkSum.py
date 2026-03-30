import json
import hashlib

def readData():
    with open('save.json', 'r') as file:
        return json.load(file).pop("chkSum")

def chkSumGen():
    with open('save.json', 'r') as file:
        data = json.load(file)
        data.pop("chkSum", None)
    dataRounded = {k: round(v) if isinstance(v, (int, float)) else v for k, v in data.items()}
    print("generated chkSum")
    jsonStr = json.dumps(dataRounded, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(jsonStr.encode('utf-8')).hexdigest()

def checkCheckSum():
    with open('save.json', 'r') as file:
        data = json.load(file)
    print(f"generated chksum{chkSumGen()} \n old checkSum{data['chkSum']}")
    if chkSumGen() == data["chkSum"]:
        print("checksum     success")
    else:
        print("chkSum error")
