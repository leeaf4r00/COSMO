import requests
import PySimpleGUI as sg
import webbrowser

# Define a janela da GUI
sg.theme('LightGreen')
layout = [
    [sg.Text("Escolha o tipo de pesquisa:"), sg.Radio('Código de barras', 'RADIO1',
                                                      default=True, key="-EAN-"), sg.Radio('Descrição', 'RADIO1', key="-DESC-")],
    [sg.Text("Insira o código EAN ou descrição do produto:"),
     sg.Input(key="-SEARCH-"), sg.Button("Buscar", bind_return_key=True)],
    [sg.Text(size=(50, 3), key="-OUTPUT-")],
    [sg.Text("Desenvolvido por Rafael Fernandes, Rurópolis-Pará"), sg.Text("  "),
     sg.Button('Instagram', font=('Helvetica', 10, 'underline'), button_color=('white', 'purple'), key='-INSTAGRAM-')],
    [sg.Text("Histórico de pesquisas", font=('Helvetica', 12, 'bold'),
             justification='center', size=(50, 1))],
    [sg.Multiline(key='-HISTORY-', size=(50, 6))],
    [sg.Button("Listar Produtos Pesquisados", key="-LIST-")]
]

window = sg.Window("Consulta de Produto", layout, size=(600, 500))

# Variáveis para armazenar o histórico e a lista de produtos pesquisados
history = []
products_list = []

# Loop para ler os eventos da janela
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "Buscar" or event == "-SEARCH-" and values["-SEARCH-"]:
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
                "Número de requisições excedido. Tente novamente mais tarde.")
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
                window["-OUTPUT-"].update(
                    f"Código EAN: {codigo}\nDescrição: {descricao}\nNCM: {ncm}")

                # Adiciona a pesquisa ao histórico e à lista de produtos pesquisados
                search_result = f"Código EAN: {codigo}\nDescrição: {descricao}\nNCM: {ncm}"
                history.append(search_result)
                products_list.append(search_result)

        else:
            window["-OUTPUT-"].update(
                f"Erro na consulta: {response.status_code}")

    if event == '-INSTAGRAM-':
        webbrowser.open_new_tab(
            'https://www.instagram.com/RAFAELMOREIRAFERNANDES/')

window.close()
