import PySimpleGUI as sg
import subprocess

# define a janela principal
sg.theme("DarkAmber")
layout = [
    [sg.Text("COSMO - Integration with Machine Learning")],
    [sg.Multiline(size=(80, 8), key="-HISTORY-",
                  reroute_stdout=True, reroute_stderr=True)],
    [sg.Button("Run COSMO")],
    [sg.Button("Exit")],
]

window = sg.Window("COSMO Integration", layout, resizable=True, finalize=True)

# loop principal
while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    if event == "Run COSMO":
        # abre uma janela de diálogo para escolher o arquivo de entrada
        input_file = sg.popup_get_file("Select a COSMO input file")

        if input_file:
            # chama o arquivo cosmo_v8.py com o caminho do arquivo de entrada como argumento
            subprocess.call(["python", "cosmo_v8.py", input_file])

            # adiciona o caminho do arquivo ao histórico de busca
            search_history = window["-HISTORY-"].get().split("\n")
            search_history.insert(0, f"Input file: {input_file}")
            window["-HISTORY-"].update(values=search_history)
window.close()
