import base64
import io

import requests
import json
from PIL import Image

if __name__ == "__main__":
    desc = input("What image would you like? ")
    resp = requests.post("https://backend.craiyon.com/generate",
                         json={"prompt": desc+"<br>"})

    #print(resp.content)
    images = json.loads(resp.content)["images"]
    a = Image.open(io.BytesIO(base64.b64decode(images[0])))
    a.show()
