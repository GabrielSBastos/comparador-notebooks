import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def coletar_preco_notebooks():
    headers = {"User-Agent": "Mozilla/5.0"}
    produtos = []

    for pagina in range(1, 4):  # 3 páginas
        url = f"https://lista.mercadolivre.com.br/notebook_Pagina_{pagina}"
        resposta = requests.get(url, headers=headers)
        soup = BeautifulSoup(resposta.text, "html.parser")

        for item in soup.select(".ui-search-result"):
            try:
                nome = item.select_one("h2").text.strip()
                preco = item.select_one(".ui-search-price__second-line span").text.strip()
                link = item.select_one("a")["href"]
                imagem = item.select_one("img")["data-src"] if item.select_one("img") else ""

                # Acessa a página do produto para buscar detalhes e avaliação
                detalhes = "Detalhes não encontrados"
                avaliacao = "Sem avaliação"
                try:
                    detalhe_resp = requests.get(link, headers=headers)
                    detalhe_soup = BeautifulSoup(detalhe_resp.text, "html.parser")

                    # Descrição principal
                    desc_tag = detalhe_soup.select_one("p.ui-pdp-description__content")
                    if desc_tag:
                        detalhes = desc_tag.text.strip()[:250]

                    # Avaliação média
                    nota_tag = detalhe_soup.select_one("span.ui-review-capability__rating")
                    if nota_tag:
                        avaliacao = nota_tag.text.strip()
                except Exception:
                    pass  # Ignora erro no detalhe

                # Data da coleta (hoje)
                data_hoje = datetime.now().strftime("%d/%m/%Y")

                produtos.append({
                    "nome": nome,
                    "valor": preco,
                    "link": link,
                    "imagem": imagem,
                    "detalhes": detalhes,
                    "avaliacao": avaliacao,
                    "historico": [
                        {
                            "data": data_hoje,
                            "valor": preco
                        }
                    ]
                })

            except Exception:
                continue  # ignora produtos com dados quebrados

    # Salva todos os produtos coletados
    with open("dados.json", "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    coletar_preco_notebooks()