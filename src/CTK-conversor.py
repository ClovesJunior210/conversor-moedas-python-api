import customtkinter as ctk


# configs iniciais
GUI = ctk.CTk()
GUI.title("Conversor de moedas")
GUI.configure(fg_color="#1e1e1e")
GUI.geometry("480x220")
GUI.maxsize(480, 220)
GUI.minsize(480, 220)

# Funções/Dicionarios&Listas
def convert(event=None):
    valor_resultado.set(f'{valor1.get()}')


moedas = [
    "USD", "EUR", "BRL", "GBP", "JPY", "CNY", "AUD", "CAD", "CHF", "ARS",
    "MXN", "CLP", "SEK", "NOK", "RUB", "INR", "ZAR", "KRW", "TRY", "ILS",
    "AED", "HKD", "SGD", "PLN", "DKK"
] # pegar na API


# Front-end direto na GUI
text1 = ctk.CTkLabel(GUI, text="Escolha um valor!")
text1.grid(row=0, column=0, columnspan=3, pady=10)                     

combo1 = ctk.CTkComboBox(GUI, values=moedas)
combo1.grid(row=1, column=0, padx=10, pady=10)                    
combo1.set(moedas[0])

combo2 = ctk.CTkComboBox(GUI, values=moedas)
combo2.grid(row=1, column=2, padx=10, pady=10)               
combo2.set(moedas[2])

valor1 = ctk.CTkEntry(GUI, placeholder_text="Valor de entrada")
valor1.grid(row=2, column=0, padx=10, pady=10)               
valor1.bind("<Return>", convert)

valor_resultado = ctk.StringVar()
valor2 = ctk.CTkEntry(GUI, textvariable=valor_resultado, state="disabled", placeholder_text="Resultado")
valor2.grid(row=2, column=2, padx=10, pady=10)

botao = ctk.CTkButton(GUI, text="Converter", command=convert)
botao.grid(row=3, column=1, pady=20)

GUI.mainloop()
