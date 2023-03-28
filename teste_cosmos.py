import requests
import PySimpleGUI as sg
import webbrowser
import csv

# Define a janela da GUI
sg.theme('LightGreen')
layout = [
    [sg.Text("Escolha o tipo de pesquisa:"), sg.Radio('Código de barras', 'RADIO1',
                                                      default=True, key="-EAN-"), sg.Radio('Descrição', 'RADIO1', key="-DESC-")],
    [sg.Text("Insira o código EAN ou descrição do produto:"),
     sg.Input(key="-SEARCH-"), sg.Button("Buscar", key="-SEARCHBUTTON-")],
    [sg.Text(size=(50, 3), key="-OUTPUT-")],
    [sg.Text("Desenvolvido por Rafael Fernandes, Rurópolis-Pará"), sg.Text("  "),
     sg.Button('Instagram', font=('Helvetica', 10, 'underline'), button_color=('white', 'purple'), key='-INSTAGRAM-')],
    [sg.Text("Histórico de produtos pesquisados", font=("Helvetica", 12), justification="center")],
    [sg.Listbox(values=[], size=(80, 6), key="-HISTORY-")],
    [sg.Button("Limpar histórico"), sg.Button("Salvar histórico")]
]

window = sg.Window("Consulta de Produto", layout, size=(800, 500))

history = []

# Loop para ler os eventos da janela
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "Limpar histórico":
        history.clear()
        window["-HISTORY-"].update(values=history)
    elif event == "Salvar histórico":
        with open("historico.csv", mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Código EAN", "Descrição", "NCM"])
            writer.writerows(history)
        window["-OUTPUT-"].update("Histórico salvo com sucesso!")
    elif event == "-SEARCHBUTTON-":
        if values["-SEARCH-"]:
            if values["-EAN-"]:
                search_type = "gtins"
            else:
                search_type = "products"

            search_term = values["-SEARCH-"]
            url = f"https://api.cosmos.bluesoft.com.br/{search_type}/{search_term}"
            headers = {"X-Cosmos-Token": "UJTBhybMZx96n33FzUfp2w"}

            response = requests.get(url, headers=headers)

            if response.status_code == 429:
                window["-OUTPUT-"].update(
                    "Erro na consulta: muitas requisições. Tente novamente mais tarde.")
            elif response.status_code == 404:
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
                    window["-OUTPUT-"].update
