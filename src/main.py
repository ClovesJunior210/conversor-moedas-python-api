import os
import customtkinter as ctk
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def obter_moedas():
    """Função que obtém a lista de moedas disponíveis na API."""

    url = f"https://api.exchangerate.host/list?access_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return list(data['currencies'].keys())

def value_verify(v_from, label1, combo_moeda_destino, combo_moeda_origem):
    """Função que verifica a validade do valor inserido."""

    # Verfica se o valor possui algo
    if not v_from.get():
        logging.warning('From= Null')
        label1.configure(text="Digite Algo!")
        return False
    
    # verifica se o user digitou uma moeda que existe na lista
    elif combo_moeda_origem.get() not in obter_moedas() or combo_moeda_destino.get() not in obter_moedas():
        logging.warning('Uma das moedas selecionadas não está disponível')
        label1.configure(text="Uma das moedas selecionadas não está disponível!")
        return False

    # Substitui vírgula por ponto
    elif "," in v_from.get():
        logging.warning('","-detectada')
        updated_value = v_from.get().replace(",", ".")
        v_from.delete(0, ctk.END)
        v_from.insert(0, updated_value)

    # Verifica se o valor é numérico
    try:
        float(v_from.get())
    except ValueError:
        logging.warning('Valor não numérico detectado')
        label1.configure(text="Apenas números!")
        v_from.delete(0, ctk.END)
        return False
    
    return True

def convert(v_from, label1, combo_moeda_origem, combo_moeda_destino, result_value):
    """Função para realizar a conversão de moedas."""

    if not value_verify(v_from, label1, combo_moeda_destino, combo_moeda_origem):
        return  
    
    from_currency = combo_moeda_origem.get()
    to_currency = combo_moeda_destino.get()
    amount = float(v_from.get())

    url_convert = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}&access_key={API_KEY}"
    response_convert = requests.get(url_convert)
    data_convert = response_convert.json()

    logging.info(f'Conversão bem-sucedida: {data_convert}')

    # Exibe o valor convertido
    value_result = round(data_convert["result"], 2)
    label1.configure(text="Convertido!")
    result_value.set(f'{value_result}')

def interface_grafica():
    """Função que inicializa a interface gráfica."""

    # Configuração da GUI
    GUI = ctk.CTk()
    GUI.title("Conversor de Moedas - v1.0")
    GUI.configure(fg_color="#1e1e1e")
    GUI.geometry("480x220")
    GUI.maxsize(480, 220)
    GUI.minsize(480, 220)

    moedas = obter_moedas()

    # Front-End
    label1 = ctk.CTkLabel(GUI, text="Escolha um valor!")
    label1.grid(row=0, column=0, columnspan=3, pady=10)

    combo_moeda_origem = ctk.CTkComboBox(GUI, values=moedas)
    combo_moeda_origem.grid(row=1, column=0, padx=10, pady=10)
    combo_moeda_origem.set('BRL')

    combo_moeda_destino = ctk.CTkComboBox(GUI, values=moedas)
    combo_moeda_destino.grid(row=1, column=2, padx=10, pady=10)
    combo_moeda_destino.set('USD')

    v_from = ctk.CTkEntry(GUI, placeholder_text="Valor de entrada")
    v_from.grid(row=2, column=0, padx=10, pady=10)
    v_from.bind("<Return>", lambda event: convert(v_from, label1, combo_moeda_origem, combo_moeda_destino, result_value))

    result_value = ctk.StringVar()
    v_to = ctk.CTkEntry(GUI, textvariable=result_value, state="disabled", placeholder_text="Resultado")
    v_to.grid(row=2, column=2, padx=10, pady=10)

    button_convert = ctk.CTkButton(GUI, text="Converter", command=lambda: convert(v_from, label1, combo_moeda_origem, combo_moeda_destino, result_value))
    button_convert.grid(row=3, column=1, pady=20)

    GUI.mainloop()
    
def gui_erro():
    """Função que inicializa a interface gráfica de erro."""

    Erro = ctk.CTk()
    Erro.title("Err")
    Erro.configure(fg_color="#1e1e1e")
    Erro.geometry("480x220")
    Erro.resizable(False, False)

    Erro.grid_columnconfigure(0, weight=1)
    Erro.grid_columnconfigure(1, weight=1)
    Erro.grid_columnconfigure(2, weight=1)
    Erro.grid_rowconfigure(0, weight=1)
    Erro.grid_rowconfigure(1, weight=1)
    Erro.grid_rowconfigure(2, weight=1)
    Erro.grid_rowconfigure(3, weight=1)

    label_erro = ctk.CTkLabel(Erro, text="API fora do ar!", text_color="white", font=("Arial", 16))
    label_erro.grid(row=1, column=1, pady=10, sticky="n")

    sub_label_erro = ctk.CTkLabel(Erro, text="Tente novamente mais tarde!", text_color="white", font=("Arial", 14))
    sub_label_erro.grid(row=2, column=1, pady=10, sticky="n")

    Erro.mainloop()

def api_verify():
    """Verifica se a API esta online."""

    url = f"https://api.exchangerate.host/latest?access_key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        logging.info('API-ON')
        return interface_grafica()  
        
    else:
        logging.warning('API-OFF')
        return gui_erro() 


api_verify() #chama verificação
