if values["-EAN-"]:
    search_type = "gtins"
    search_term = values["-SEARCH-"]
elif values["-DESC-"]:
    search_type = "products"
    search_term = values['-SEARCH-']
else:
    continue

url = f"https://api.cosmos.bluesoft.com.br/{search_type}/{search_term}.json"
headers = {"X-Cosmos-Token": "l5XSvKMx3dKizYndt_WBLg"}

response = requests.get(url, headers=headers)

if response.status_code == 404:
    window["-OUTPUT-"].update("Produto não encontrado.")
elif response.status_code == 200:
    data = response.json()
    if search_type == "gtins":
        descricao = data.get("description")
        ncm = data.get("ncm")
        codigo = data.get("gtin")
    else:
        descricao = data[0].get("description")
        ncm = data[0].get("ncm")
        codigo = data[0].get("gtin")
    if not descricao or not ncm:
        window["-OUTPUT-"].update("Informações do produto não disponíveis.")
    else:
        window["-OUTPUT-"].update(
            f"Código EAN: {codigo}\nDescrição: {descricao}\nNCM: {ncm}")
else:
    window["-OUTPUT-"].update(f"Erro na consulta: {response.status_code}")

if event == '-INSTAGRAM-':
    webbrowser.open_new_tab(
        'https://www.instagram.com/RAFAELMOREIRAFERNANDES/')
