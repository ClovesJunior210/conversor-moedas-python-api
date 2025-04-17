import os
import customtkinter as ctk
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')  

def obter_moedas():
    url = f"https://api.exchangerate.host/list?access_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return list(data['currencies'].keys())

def interface_grafica():

    def convert(event=None):
        from_currency = combo_moeda_origem.get()
        to_currency = combo_moeda_destino.get()
        amount = float(v_from.get()) 

        url_convert = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}&access_key={API_KEY}"
        response_convert = requests.get(url_convert)
        data_convert = response_convert.json()
        print(f'data convert: {data_convert}')

        value_result = round(data_convert["result"], 2)
        valor_resultado.set(f'{value_result}')

    # configs iniciais
    GUI = ctk.CTk()
    GUI.title("Conversor de moedas")
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
    v_from.bind("<Return>", convert)

    valor_resultado = ctk.StringVar()
    v_to = ctk.CTkEntry(GUI, textvariable=valor_resultado, state="disabled", placeholder_text="Resultado")
    v_to.grid(row=2, column=2, padx=10, pady=10)

    botao = ctk.CTkButton(GUI, text="Converter", command=convert)
    botao.grid(row=3, column=1, pady=20)

    GUI.mainloop()

# chama o GUI
interface_grafica()