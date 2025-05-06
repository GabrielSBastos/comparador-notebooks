
import requests
from bs4 import BeautifulSoup
import json

def coletar_preco_notebooks():
    url = "https://lista.mercadolivre.com.br/notebook"
    headers = {"User-Agent": "Mozilla/5.0"}
    resposta = requests.get(url, headers=headers)
    soup = BeautifulSoup(resposta.text, "html.parser")

    produtos = []
    for item in soup.select(".ui-search-result"):
        nome = item.select_one("h2").text.strip()
        preco = item.select_one(".ui-search-price__second-line span").text.strip()
        link = item.select_one("a")["href"]
        produtos.append({
            "nome": nome,
            "valor": preco,
            "link": link
        })

    with open("dados.json", "w", encoding="utf-8") as f:
        json.dump(produtos[:5], f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    coletar_preco_notebooks()
