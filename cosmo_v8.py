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
     sg.Input(key="-SEARCH-")],
    [sg.Button("Buscar"), sg.Button("Sair")],
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

# Loop para ler os eventos da janela
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Sair":
        break

    if values["-EAN-"]:
        search_type = "gtins"
    else:
        search_type = "products"

    search_term = values["-SEARCH-"]
    url = f"https://api.cosmos.bluesoft.com.br/{search_type}?query={search_term}"
    headers = {"X-Cosmos-Token": "NATS-jewDl9Y3gCluv5Sgw"}

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
            window["-OUTPUT-"].update("Informações do produto não disponíveis.")
        else:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            search_history.insert(0, [now, descricao, ncm])
            # Limita o histórico em 20 pesquisas
            search_history = search_history[:20]
            window["-HISTORY-"].update(values=search_history)
            window["-OUTPUT-"].update(
                f"Código EAN: {codigo}\nDescrição: {descricao}\nNCM: {ncm}")
    else:
        error_msg = f"Erro na consulta: {response.status_code}"
        window["-OUTPUT-"].update(error_msg)
        if sg.popup_yes_no("Deseja copiar o erro?", title="Erro na consulta"):
            pyperclip.copy(error_msg)

    if event == '-INSTAGRAM-':
        webbrowser.open_new_tab(
            'https://www.instagram.com/RAFAELMOREIRAFERNANDES/')

window.close()
