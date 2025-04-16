import os
import customtkinter as ctk
import requests
from dotenv import load_dotenv

load_dotenv()

# configs iniciais
GUI = ctk.CTk()
GUI.title("Conversor de moedas")
GUI.configure(fg_color="#1e1e1e")
GUI.geometry("480x220")
GUI.maxsize(480, 220)
GUI.minsize(480, 220)

# API
key = os.getenv('API_KEY')
url = f"https://api.exchangerate.host/list?access_key={key}"
response = requests.get(url)
data = response.json()
currencies = data['currencies']

# Funções/Dicionarios&Listas
def convert(event=None):
    valor_resultado.set(f'{valor1.get()}')

moedas = list(currencies.keys())

# Front-end direto na GUI
text1 = ctk.CTkLabel(GUI, text="Escolha um valor!")
text1.grid(row=0, column=0, columnspan=3, pady=10)                     

combo1 = ctk.CTkComboBox(GUI, values=moedas)
combo1.grid(row=1, column=0, padx=10, pady=10)                    
combo1.set('BRL')

combo2 = ctk.CTkComboBox(GUI, values=moedas)
combo2.grid(row=1, column=2, padx=10, pady=10)               
combo2.set('USD')

valor1 = ctk.CTkEntry(GUI, placeholder_text="Valor de entrada")
valor1.grid(row=2, column=0, padx=10, pady=10)               
valor1.bind("<Return>", convert)

valor_resultado = ctk.StringVar()
valor2 = ctk.CTkEntry(GUI, textvariable=valor_resultado, state="disabled", placeholder_text="Resultado")
valor2.grid(row=2, column=2, padx=10, pady=10)

botao = ctk.CTkButton(GUI, text="Converter", command=convert)
botao.grid(row=3, column=1, pady=20)

GUI.mainloop()
