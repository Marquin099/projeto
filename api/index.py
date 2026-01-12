import requests
import time
from flask import Flask, Response, stream_with_context

app = Flask(__name__)

# LISTA INTEGRAL DE CANAIS - TODOS OS 35 MANTIDOS
CANAIS = {
    "cazetv": "http://918197185.com/live/595f428ca7b51f3c37480c96db6e5d8a/d205a045c9c6799d56b9/116845.ts",
    "espn1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/117389.ts",
    "bandsports": "http://918197185.com/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14364.ts",
    "getv": "http://918197185.com/live/595f428ca7b51f3c37480c96db6e5d8a/d205a045c9c6799d56b9/130945.ts",
    "disneyplus1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116377.ts",
    "espn3": "http://918197185.com/live/595f428ca7b51f3c37480c96db6e5d8a/d205a045c9c6799d56b9/116378.ts",
    "hbomax": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116903.ts",
    "acampanheacasa": "http://918197185.com/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/104817.ts",
    "quartomagia": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/104819.ts",
    "mosaico": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/104820.ts",
    "fada": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/105390.ts",
    "gnomo": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/105391.ts",
    "banheiro": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/105392.ts",
    "cozinhadelicia": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/105393.ts",
    "quarto4": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/105394.ts",
    "sala": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/105395.ts",
    "pscina": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/105396.ts",
    "academiarexona": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/105397.ts",
    "recordtvspplayplus": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/122883.ts",
    "recordtvspplayplusuhd": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14566.ts",
    "globospfhd": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/48530.ts",
    "globorj": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/48531.ts",
    "premiereclubes1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116837.ts",
    "premiere2": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116838.ts",
    "premiere3": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116839.ts",
    "premiere4": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116840.ts",
    "premiere5": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116841.ts",
    "premiere6": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116842.ts",
    "premiere7": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116843.ts",
    "premiere8": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116844.ts",
    "disneyplus2": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116378.ts",
    "ufcfightpass1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/117413.ts",
    "appetv1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116653.ts",
    "cnnbrasil": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/48560.ts",
    "xsports2": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/132276.ts",
}

def stream_canal(url_base):
    headers = {
        "User-Agent": "tvbox-v4.0.0",
        "Icy-MetaData": "1",
        "Connection": "keep-alive"
    }
    
    # 1. Resolver token/redirecionamento silenciosamente no servidor
    try:
        r_token = requests.get(url_base, headers=headers, allow_redirects=False, timeout=10)
        url_final = r_token.headers.get("Location") or url_base
    except:
        url_final = url_base

    # 2. Abrir conexão estável e repassar dados
    try:
        with requests.get(url_final, headers=headers, stream=True, timeout=15) as r:
            for chunk in r.iter_content(chunk_size=256*1024): # Buffer de 256KB
                if chunk:
                    yield chunk
    except Exception as e:
        print(f"Erro no stream: {e}")

@app.route('/')
def home():
    return "Servidor Online! Use /nome-do-canal"

@app.route('/<canal>')
def serve_canal(canal):
    if canal not in CANAIS:
        return "Canal não encontrado", 404
    
    # Inicia a ponte de dados sem redirecionar o player
    return Response(
        stream_with_context(stream_canal(CANAIS[canal])),
        mimetype='video/mp2t',
        headers={"Content-Disposition": "attachment; filename=canal.ts"}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
