import requests
import PySimpleGUI as sg
import webbrowser

# Define a janela da GUI
sg.theme('LightGreen')
layout = [
    [sg.Text("Escolha o tipo de pesquisa:"), sg.Radio('Código de barras', 'RADIO1',
                                                      default=True, key="-EAN-"), sg.Radio('Descrição', 'RADIO1', key="-DESC-")],
    [sg.Text("Insira o código EAN ou descrição do produto:"),
     sg.Input(key="-SEARCH-", enable_events=True)],
    [sg.Button("Buscar"), sg.Button("Sair")],
    [sg.Text(size=(50, 3), key="-OUTPUT-")],
    [sg.Text("Desenvolvido por Rafael Fernandes, Rurópolis-Pará"), sg.Text("  "),
     sg.Button('Instagram', font=('Helvetica', 10, 'underline'), button_color=('white', 'purple'), key='-INSTAGRAM-')],
    [sg.Listbox([], size=(50, 6), key="-HISTORY-")],
]

window = sg.Window("Consulta de Produto", layout, size=(600, 400))

# Lista para armazenar histórico de pesquisas
search_history = []

# Loop para ler os eventos da janela
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Sair":
        break

    if event == "-SEARCH-":
        # Se o usuário pressionar Enter, inicia a busca automaticamente
        if len(values["-SEARCH-"]) == 13:  # EAN tem 13 dígitos
            window["Buscar"].click()

    if event == "Buscar":
        if values["-EAN-"]:
            search_type = "gtins"
        else:
            search_type = "products"

        search_term = values["-SEARCH-"]
        url = f"https://api.cosmos.bluesoft.com.br/{search_type}/{search_term}"
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
                window["-OUTPUT-"].update(
                    "Informações do produto não disponíveis.")
            else:
                output_text = f"Código EAN: {codigo}\nDescrição: {descricao}\nNCM: {ncm}"
                window["-OUTPUT-"].update(output_text)
                search_history.append(output_text)
                window["-HISTORY-"].update(search_history)
        else:
            window["-OUTPUT-"].update(
                f"Erro na consulta: {response.status_code}")

    if event == '-INSTAGRAM-':
        webbrowser.open_new_tab(
            'https://www.instagram.com/RAFAELMOREIRAFERNANDES/')

window.close()
