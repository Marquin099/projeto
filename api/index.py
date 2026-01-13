import requests
import time
from flask import Flask, redirect, make_response, Response, stream_with_context

app = Flask(__name__)

# LISTA INTEGRAL MANTIDA (MESMOS CANAIS)
CANAIS = {
    "cazetv": "http://918197185.com/live/595f428ca7b51f3c37480c96db6e5d8a/d205a045c9c6799d56b9/116845.ts",
    "espn1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/131579.ts",
    "espn2": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/131593.ts",
    "espn3": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/117391.ts",
    "espn4": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/130915.ts",
    "espn5": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/117393.ts",
    "espn6": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/117394.ts",
    "bandsports": "http://918197185.com/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14364.ts",
    "sportv1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14360.ts",
    "sportv2": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14361.ts",
    "sportv3": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14362.ts",
    "sportv1fhd": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/122559.ts",
    "sportv2fhd": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/122560.ts",
    "sportv3fhd": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/122561.ts",
    "sportv4K": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/122065.ts",
    "sportvmosaico": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/130932.ts",
    "sportvmosaico2": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/130930.ts",
    "disneyplus1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116377.ts",
    "disneyplus2": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116378.ts",
    "disney+3": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116379.ts",
    "disney+4": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116380.ts",
    "disney+5": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116381.ts",
    "disney+6": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116382.ts",
    "disney+7": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116383.ts",
    "disney+8": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116384.ts",
    "disney+9": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116385.ts",
    "disney+10": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116386.ts",
    "tnt": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14374.ts",
    "tntseries": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14375.ts",
    "space": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14376.ts",
    "cinemax": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14396.ts",
    "telecineatcion": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14382.ts",
    "telecinepremium": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14383.ts",
    "telecinepipoca": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14384.ts",
    "telecinetouch": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14385.ts",
    "telecinefun": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14386.ts",
    "telecinecult": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14387.ts",
    "hbo": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14388.ts",
    "hbo2": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14389.ts",
    "hbo+": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14390.ts",
    "hbofamily": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14392.ts",
    "hbomundi": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14393.ts",
    "hbopop": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14394.ts",
    "hbosingnature": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14391.ts",
    "hboxtreme": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14395.ts",
    "hbomax": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116903.ts",
    "globospfhd": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/48530.ts",
    "globorj": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/48531.ts",
    "globosp4k": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/90580.ts",
    "globospuhd": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/48530.ts",
    "cnnbrasil": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/48560.ts",
    "recordtvspplayplus": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/122883.ts",
    "recordtvspplayplusuhd": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/14566.ts",
    "premiereclubes1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116837.ts",
    "premiere2": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116838.ts",
    "premiere3": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116839.ts",
    "premiere4": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116840.ts",
    "premiere5": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116841.ts",
    "premiere6": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116842.ts",
    "premiere7": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116843.ts",
    "premiere8": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116844.ts",
    "ufcfightpass1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/117413.ts",
    "appetv1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/116653.ts",
    "xsports1": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/106761.ts",
    "xsports2": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/132276.ts",
    "lesbian": "http://918197185.com:80/live/a1f10d0bca4a5b077a0520250416100028/a75db139b01845e1c314/104888.ts",
}

# Cache ultra rápido de 25 segundos
cache_final = {}

@app.route('/')
def home():
    return "Servidor Estável! Use /nome-do-canal.ts"

@app.route('/<path:canal>')
def get_canal(canal):
    id_canal = canal.replace('.ts', '')
    
    if id_canal not in CANAIS:
        return "Canal não encontrado", 404

    agora = time.time()
    
    # Busca URL real se não tiver em cache ou se expirou (25s)
    if id_canal in cache_final:
        url_cache, tempo = cache_final[id_canal]
        if agora - tempo < 25:
            return redirect(url_cache)

    headers = {"User-Agent": "tvbox-v4.0.0"}
    try:
        # Resolvemos o token dinamicamente
        r = requests.get(CANAIS[id_canal], headers=headers, allow_redirects=False, timeout=5)
        url_real = r.headers.get("Location")
        
        if url_real:
            cache_final[id_canal] = (url_real, agora)
            # Redirecionamento 307 (Temporary Redirect) é melhor para manter a sessão viva
            response = make_response(redirect(url_real, code=307))
            response.headers['Content-Type'] = 'video/mp2t'
            response.headers['Connection'] = 'keep-alive'
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        
        return redirect(CANAIS[id_canal])
    except:
        return redirect(CANAIS[id_canal])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
