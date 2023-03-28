import requests
import PySimpleGUI as sg
import webbrowser

# Define a janela da GUI
sg.theme('Reddit')
layout = [
    [sg.Text("Escolha o tipo de pesquisa:"), sg.Radio('Código de barras', 'RADIO1',
                                                      default=True, key="-EAN-"), sg.Radio('Descrição', 'RADIO1', key="-DESC-")],
    [sg.Text("Insira o código EAN ou descrição do produto:"),
     sg.Input(key="-SEARCH-")],
    [sg.Button("Buscar"), sg.Button("Sair")],
    [sg.Text(size=(50, 3), key="-OUTPUT-")],
    [sg.Text("Desenvolvido por Rafael Fernandes, Rurópolis-Pará"), sg.Text("  "),
     sg.Button('Instagram', font=('Helvetica', 10, 'underline'), key='-INSTAGRAM-')]
]

window = sg.Window("Consulta de Produto", layout, size=(600, 300))

# Variáveis para controlar o limite de consultas
requests_count = 0
limit = 5

# Loop para ler os eventos da janela
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Sair":
        break

    if values["-EAN-"]:
        search_type = "gtins"
        search_term = values["-SEARCH-"]
    else:
        search_type = "products"
        search_term = f"?query={values['-SEARCH-']}"

    if requests_count >= limit:
        window["-OUTPUT-"].update(
            f"Limite de {limit} consultas atingido. Tente novamente em alguns minutos.")
        continue

    url = f"https://api.cosmos.bluesoft.com.br/{search_type}/{search_term}.json"
    headers = {"X-Cosmos-Token": "k9wmJau-n3jaYFYriECRwA"}

    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        window["-OUTPUT-"].update(
            "Erro na autenticação. Verifique se o token está correto.")
    elif response.status_code == 404:
        window["-OUTPUT-"].update("Produto não encontrado.")
    elif response.status_code == 200:
        requests_count += 1
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

window.close()