import requests
import time
from flask import Flask, redirect, make_response

app = Flask(__name__)

# LISTA INTEGRAL DE CANAIS - TODOS OS 39 MANTIDOS
CANAIS = {
    "cazetv": "http://918197185.com/live/595f428ca7b51f3c37480c96db6e5d8a/d205a045c9c6799d56b9/116845.ts",
    "espn1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/131579.ts",
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
    "sportv1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14360.ts",
    "sportv2": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14361.ts",
    "sportv3": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14362.ts",
    "xsports1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/106761.ts",
    "espn2": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/131593.ts",
    "espn3": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/117391.ts",
    "espn4": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/130915.ts",
    "espn5": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/117393.ts",
    "espn6": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/117394.ts",
    "sportvmosaico": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/130932.ts",
    "sportv4K": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/122065.ts",
    "sportv1fhd": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/122559.ts",
    "sportv2fhd": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/122560.ts",
    "sportv3fhd": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/122561.ts",
    "sportvmosaico2": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/130930.ts",
    "disney+3": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116379.ts",
    "disney+4": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116380.ts",
    "disney+5": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116381.ts",
    "disney+6": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116382.ts",
    "disney+7": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116383.ts",
    "disney+8": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116384.ts",
    "disney+9": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116385.ts",
    "disney+10": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116386.ts",
}

# Cache global simples
cache_final = {}

@app.route('/')
def home():
    return "Servidor IPTV Online. Use /nome-do-canal"

@app.route('/<canal>')
def get_canal(canal):
    if canal not in CANAIS:
        return "Canal Inexistente", 404

    agora = time.time()
    
    # Se o canal estiver no cache e tiver menos de 1 minuto, redireciona direto
    # Reduzimos o tempo de cache para evitar que o token expire na mão do player
    if canal in cache_final:
        url_cache, tempo = cache_final[canal]
        if agora - tempo < 60:
            return redirect(url_cache)

    # Caso contrário, busca o link real (resolve o redirecionamento do token)
    headers = {"User-Agent": "tvbox-v4.0.0"}
    try:
        r = requests.get(CANAIS[canal], headers=headers, allow_redirects=False, timeout=5)
        url_real = r.headers.get("Location")
        
        if url_real:
            cache_final[canal] = (url_real, agora)
            # Criamos uma resposta de redirecionamento que proíbe cache no player
            response = make_response(redirect(url_real))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        
        return redirect(CANAIS[canal])
    except:
        return redirect(CANAIS[canal])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
