import customtkinter as ctk
import tkinter as tk

import requests


class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Erstellung des "Coin Balance"-Frames:
        self.coin_balance_frame = ctk.CTkFrame(self, corner_radius=10)
        self.coin_balance_frame.grid(row=1, column=1, rowspan=1)
        self.coin_balance_frame.place(x=570, y=20)

        # Erstellung der "Coin Balance"-Widgets:
        self.coin_balance_label = ctk.CTkLabel(self.coin_balance_frame,
                                                text="Balance",
                                                font=ctk.CTkFont(size=20, weight="bold"))
        self.coin_balance_label.grid(row=0, column=0, padx=(25, 25), pady=(30, 15))

        self.coin_balance_value = ctk.CTkLabel(self.coin_balance_frame,
                                                text="0 BTC",
                                                font=ctk.CTkFont(size=20))
        self.coin_balance_value.grid(row=1, column=0, padx=(25, 25), pady=(10, 10))

        # Fetch coin balance and update every minute
        self.fetch_coin_balance()
        self.update_coin_balance()
        self.after(60000, self.update_coin_balance)

    def fetch_coin_balance(self):
        # Adresse der API von blockcyper, nicht wundern, ist nur Text, wenn man es im Browser öffnet
        address = 'mfjZWvFYpkV6tybneaKCBi2CS2bdVdpUAA'
        url = f'https://api.blockcypher.com/v1/btc/test3/addrs/{address}/balance'

        response = requests.get(url)
        if response.status_code == 200:
            balance = response.json()['balance']
            print(f'Balance: {balance} Satoshi')
            self.coin_balance_value.configure(text=f"{balance} BTC")

        else:
            print('Fehler beim Abrufen der Balance / Coins.')

    def update_coin_balance(self):
        # Abrufen des aktuellen Kontostands vom Server und updated in der App
        self.fetch_coin_balance()

if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    app.pack()
    root.mainloop()
