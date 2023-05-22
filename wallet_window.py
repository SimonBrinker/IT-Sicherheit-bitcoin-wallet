import customtkinter
from wallet import Wallet, Network
import database_manager
import wallet_api

class WalletWindow(customtkinter.CTk):
    def __init__(self, wallet: Wallet, old_root:customtkinter.CTk):
        super().__init__()

        # User information:
        self.wallet = wallet

        #region UI

        
        # Window settings:
        self.geometry("1100x580")
        self.title("Wallet")

        
        # Grid layout settings:
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        
        #region Sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self,
                                                    corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=11, sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                 text="CryptoUI",
                                                 font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=35, pady=(20, 15))

        # Appearance setting widgets:
        self.appearance_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                       text="Appearance Settings",
                                                       font=customtkinter.CTkFont(size=18, weight="bold"))
        self.appearance_label.grid(row=1, column=0)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                            text="Mode",
                                                            font=customtkinter.CTkFont(size=16, weight="bold"))
        self.appearance_mode_label.grid(row=2, column=0, pady=(0, 5))
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                      values=["Dark", "Light", "System"],
                                                                      command=self.switch_appearance)
        self.appearance_mode_optionmenu.grid(row=3, column=0, pady=(0, 15))
        self.ui_scaling_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                       text="UI-Scaling",
                                                       font=customtkinter.CTkFont(size=18, weight="bold"))
        self.ui_scaling_label.grid(row=4, column=0, pady=(0, 5))
        self.ui_scaling_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                 values=["80%", "90%", "100%", "110%", "120%"],
                                                                 command=self.switch_scaling)
        self.ui_scaling_optionmenu.grid(row=5, column=0, pady=(0, 15))

        # Using the blank space:
        self.ad_bar_frame = customtkinter.CTkFrame(self.sidebar_frame, width=150, height=200)
        self.ad_bar_frame.grid(row=6, column=0)
        self.ad_label = customtkinter.CTkLabel(self.ad_bar_frame,
                                               text="Here could be ur ad!",
                                               font=customtkinter.CTkFont(weight="bold"))
        self.ad_label.grid(row=6, column=0, padx=(10, 10), pady=(85, 85))

        # Creating logout widgets:
        self.logout_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                   text="Switch User",
                                                   font=customtkinter.CTkFont(size=18, weight="bold"))
        self.logout_label.grid(row=7, column=0, pady=(25, 5))
        self.logout_button = customtkinter.CTkButton(self.sidebar_frame,
                                                     text="Logout!",
                                                     command=self.logout)
        self.logout_button.grid(row=8, column=0, sticky="s")

        #endregion

        
        #region Profile frame

        self.content = customtkinter.CTkFrame(self, corner_radius=0)

        self.content.grid_columnconfigure((0, 1, 2), weight=1)
        self.content.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.content.grid(column=1, row = 0, rowspan=11, columnspan=3, sticky="nesw")

        self.profile_frame = customtkinter.CTkFrame(self.content, corner_radius=10)
        self.profile_frame.grid_rowconfigure((0,1,2,3), weight=1)
        self.profile_frame.grid_columnconfigure((0), weight=1)
        self.profile_frame.grid(row=0, column=0, columnspan = 3, stick="ewn", padx=(15,15))
        
        self.profile_label = customtkinter.CTkLabel(self.profile_frame,
                                                    text="Profile",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.profile_label.grid(row=0, column=0, columnspan=1, sticky ="ew")
        
        self.username_label = customtkinter.CTkLabel(self.profile_frame,
                                                     text=f"Username: {wallet.username}",
                                                     font=customtkinter.CTkFont(size=16, weight="bold"))
        self.username_label.grid(row=1, column=0, pady=5, padx=5)
        
        self.bitcoin_address_label = customtkinter.CTkLabel(self.profile_frame,
                                                            text=f"Address: {wallet.get_address_string()}",
                                                            font=customtkinter.CTkFont(size=16, weight="bold"))
        self.bitcoin_address_label.grid(row=2, column=0, pady=5, padx=5)

        self.balance_lable = customtkinter.CTkLabel(self.profile_frame,
                                                     text=f"Balance: ...",
                                                     font=customtkinter.CTkFont(size=16, weight="bold"))
        self.balance_lable.grid(row=3, column=0, pady=5, padx=5)

        #endregion Profile

        #region Transaction

        self.transacton_frame = customtkinter.CTkFrame(self.content, corner_radius=10)
        self.transacton_frame.grid_rowconfigure((0,1,2,3), weight=1)
        self.transacton_frame.grid_columnconfigure(0, weight=1)
        self.transacton_frame.grid_columnconfigure(1, weight=4)
        self.transacton_frame.grid(row=1, column=0, columnspan = 3, stick="ewn", padx=(15,15))

        self.transaction_title_lable = customtkinter.CTkLabel(self.transacton_frame,
                                                    text="Transaktion",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.transaction_title_lable.grid(row=0, column = 0, columnspan = 2, pady = (5,5))
        # Inputfeld für die Zieladdresse

        self.transaction_target_address_lable = customtkinter.CTkLabel(self.transacton_frame,
                                                                       text = "Zieladresse:",
                                                                       font=customtkinter.CTkFont(weight="bold"))
        self.transaction_target_address_lable.grid(row=1, column = 0, pady = (5,5))

        self.transaction_target_address = customtkinter.CTkEntry(self.transacton_frame,
                                                                width=300,
                                                                placeholder_text = "Zieladresse")
        self.transaction_target_address.grid(row=1, column = 1, pady = (5,5), sticky = "we", padx=(0,5))

        #Inputfeld für die Anzahl der Bitcoin die überwiesen werden sollen
        #Lable
        self.transaction_amount_lable = customtkinter.CTkLabel(self.transacton_frame,
                                                                       text = "Anzahl:",
                                                                       font=customtkinter.CTkFont(weight="bold"))
        self.transaction_amount_lable.grid(row=2, column = 0, pady = (5,5))
        #Input
        self.transaction_amount = customtkinter.CTkEntry(self.transacton_frame,
                                                                width=150,
                                                                placeholder_text = "Anzahl Bitcoin")
        self.transaction_amount.grid(row=2, column = 1, pady = (5,5), sticky="ew", padx=(0,5))

        #Button zum senden der Transaktion
        self.transaction_btn_send_transaction = customtkinter.CTkButton(self.transacton_frame,
                                                                        width=150,
                                                                        text = "Senden",
                                                                        command=self.send_transaction)
        self.transaction_btn_send_transaction.grid(row=3, column = 0, columnspan = 2, pady = (5,15), padx =(50,50), sticky="ew")

        #endregion

        #endregion UI

        self.update_balance()

        # Setting the default values:
        customtkinter.set_appearance_mode("Dark")
        self.appearance_mode_optionmenu.set("Dark")
        self.ui_scaling_optionmenu.set("100%")
        self.mainloop()
        

    ##################################################################################

    @staticmethod
    def switch_appearance(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    @staticmethod
    def switch_scaling(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def logout(self):
        self.destroy()

    def update_balance(self):
        balance = wallet_api.get_wallet_balance(self.wallet)
        self.balance_lable.configure(text=f"Balance: {balance} BTC")

    def send_transaction(self):
        target_address = self.transaction_target_address.get()
        amount_in_btc = self.transaction_amount.get()
        valid = True
        if target_address == "":
            self.transaction_target_address.configure(fg_color=['#F9F9FA', '#343638'])
            valid = False
        else:
            self.transaction_target_address.configure(fg_color=['gray75', 'gray18'])
        if amount_in_btc == "":
            self.transaction_amount.configure(fg_color=['#F9F9FA', '#343638'])
            valid = False
        else:
            self.transaction_amount.configure(fg_color=['gray75', 'gray18'])
        self.update()
        if not valid:
            return
        
        success = self.wallet.send_transaction(target_address, amount_in_btc)
        if success:
            pass
            #self.transacton_frame.

def main():
    wallet = database_manager.login("Simon", "12345")
    #wallet_to = database_manager.login("SimonTarget", "12345")
    print(wallet)
    #print(wallet_to)
    run = WalletWindow(wallet, None)
    run.mainloop()

if __name__ == '__main__':
    main()