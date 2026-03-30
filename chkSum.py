import json
import hashlib
import os
import sys
from cryptography.fernet import Fernet

disableChecksum = False

key = b'qrPPSTK7n8cMLJaKIWxWkJa9gqOCZfx0VTyKIiJRYr0=' #maybe store in an env var later

def encryptSave(data):
    f = Fernet(key)
    return f.encrypt(json.dumps(data, indent=4).encode()).decode()

def decryptSave(token):
    f = Fernet(key)
    return json.loads(f.decrypt(token.encode()).decode())

def chkSumGen():
    data = decryptSave(open('save.json').read())
    data.pop("chkSum", None)
    dataRounded = {k: round(v, 6) if isinstance(v, float) else v for k, v in data.items()}
    jsonStr = json.dumps(dataRounded, sort_keys=True, ensure_ascii=True)
    result = hashlib.sha256(jsonStr.encode('utf-8')).hexdigest()
    return result

def checkCheckSum():
    if not os.path.exists('save.json'):
        return

    data = decryptSave(open('save.json').read())
    storedSum   = data.get("chkSum", "")
    computedSum = chkSumGen()

    print(f"generated chksum {computedSum} \n old checkSum {storedSum}")

    if computedSum == storedSum:
        print("success")
    else:
        print("mr nagra why are you cheating?????")
        try:
            os.remove('save.json')
        except OSError as e:
            print(f"lucky... {e}")
        os.execv(sys.executable, [sys.executable] + sys.argv)