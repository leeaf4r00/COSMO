import requests
import PySimpleGUI as sg
import webbrowser
import datetime
import pyperclip

# Define a janela da GUI
sg.theme('Reddit')
layout = [
    [sg.Text("Escolha o tipo de pesquisa:"), sg.Radio('Código de barras', 'RADIO1',
                                                      default=True, key="-EAN-"), sg.Radio('Descrição', 'RADIO1', key="-DESC-")],
    [sg.Text("Insira o código EAN ou descrição do produto:"),
     sg.Input(key="-SEARCH-", focus=True, enable_events=True), sg.Button("Buscar", bind_return_key=True)],
    [sg.Button("Ver histórico"), sg.Button("Sair")],
    [sg.Table(values=[], headings=['Data da pesquisa', 'Descrição', 'NCM'], key='-HISTORY-',
              auto_size_columns=False, col_widths=[15, 40, 10], enable_events=True)],
    [sg.Text(size=(50, 3), key="-OUTPUT-")],
    [sg.Text("Desenvolvido por Rafael Fernandes, Rurópolis-Pará"), sg.Text("  "),
     sg.Button('Instagram', font=('Helvetica', 10, 'underline'), key='-INSTAGRAM-')]
]

window = sg.Window("Consulta de Produto", layout,
                   size=(600, 500), resizable=True)

# Lista de histórico de pesquisa
search_history = []

# Carrega o histórico salvo anteriormente
try:
    with open('search_history.txt', 'r', encoding='utf8') as f:
        search_history = [line.strip().split(',') for line in f.readlines()]
except:
    pass

# Loop para ler os eventos da janela
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Sair":
        # Salva o histórico atual antes de sair
        with open('search_history.txt', 'w', encoding='utf8') as f:
            for line in search_history:
                f.write(','.join(line) + '\n')
        break

    if values["-EAN-"]:
        search_type = "gtins"
    else:
        search_type = "products"

    search_term = values["-SEARCH-"]
    url = f"https://api.cosmos.bluesoft.com.br/{search_type}?query={search_term}"
    headers = {"X-Cosmos-Token": "k9wmJau-n3jaYFYriECRwA"}

    if event == "Buscar" or event == "-SEARCH-":
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
                produto = data[0]
                descricao = produto.get("description")
                ncm = produto.get("ncm")
                codigo = produto.get("gtin")
            if not descricao or not ncm:
                window["-OUTPUT-"].update(
                    "Informações do produto não disponíveis.")
            else:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                search_history.insert(0, [now, descricao, ncm])
                # Limita o histórico em 20
