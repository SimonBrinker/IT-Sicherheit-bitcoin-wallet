import customtkinter
import requests


class Application(object):
    def __init__(self):
        self.window = Window1()
        self.window.mainloop()

class User(object):
    def __init__(self, username: str, password : str):
        self.username = username
        self.password = password


class Window1(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        ##### KEANU #####

        self.clicked = False


        ##################################################################################
        # Window settings:
        self.geometry("1100x580")
        self.title("CryptoUI")
        self.wallet_window = None

        ##################################################################################
        # Grid layout settings:
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        ##################################################################################
        # Creating sidebar:
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=11, sticky="nsew")

        # Creating Server-switch widgets:
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                 text="CryptoUI",
                                                 font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=35, pady=(20, 15))
        self.server_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                   text="Chose Server",
                                                   font=customtkinter.CTkFont(size=18, weight="bold"))
        self.server_label.grid(row=1, column=0, pady=(0, 5))

        ### KEANU ÄNDERUNG - BITTE LÖSCHEN, WENN GESEHEN #####
        self.server_mainnet_button = customtkinter.CTkButton(self.sidebar_frame,
                                                             text="BTC-Mainnet",
                                                             command=lambda: self.switch_server("mainnet"))
        self.server_mainnet_button.grid(row=3, column=0, pady=(0, 5))

        self.server_testnet_button = customtkinter.CTkButton(self.sidebar_frame,
                                                             text="BTC-Testnet",
                                                             command=lambda: self.switch_server("testnet"))
        self.server_testnet_button.grid(row=4, column=0, pady=(0, 5))

        self.server_testnet_button.grid(row=4, column=0, padx=(10, 10), pady=(0, 15))

        # Appearance setting widgets:
        self.appearance_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                       text="Appearance Settings",
                                                       font=customtkinter.CTkFont(size=18, weight="bold"))
        self.appearance_label.grid(row=5, column=0)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                            text="Mode",
                                                            font=customtkinter.CTkFont(size=16, weight="bold"))
        self.appearance_mode_label.grid(row=6, column=0, pady=(0, 5))
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                      values=["Dark", "Light", "System"],
                                                                      command=self.switch_appearance)
        self.appearance_mode_optionmenu.grid(row=7, column=0, pady=(0, 15))
        self.ui_scaling_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                       text="UI-Scaling",
                                                       font=customtkinter.CTkFont(size=18, weight="bold"))
        self.ui_scaling_label.grid(row=8, column=0, pady=(0, 5))
        self.ui_scaling_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                 values=["80%", "90%", "100%", "110%", "120%"],
                                                                 command=self.switch_scaling)
        self.ui_scaling_optionmenu.grid(row=9, column=0, pady=(0, 15))

        # Using the blank space:
        self.ad_bar_frame = customtkinter.CTkFrame(self.sidebar_frame, width= 150, height=200)
        self.ad_bar_frame.grid(row=10, column=0)
        self.ad_label = customtkinter.CTkLabel(self.ad_bar_frame,
                                               text="Here could be ur add!",
                                               font=customtkinter.CTkFont(weight="bold"))
        self.ad_label.grid(row=10, column=0, padx=(10, 10), pady=(85, 85))

        ##################################################################################
        # Creating login frame:
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.login_frame.grid(row=3, column=2, rowspan=4)

        # Creating login widgets:
        self.login_label = customtkinter.CTkLabel(self.login_frame,
                                                  text="Login to Mainnet-Server",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=5, column=2, padx=(15, 15), pady=(30, 15))
        self.username_input_field = customtkinter.CTkEntry(self.login_frame,
                                                           width=300,
                                                           placeholder_text="Username")
        self.username_input_field.grid(row=6, column=2, padx=(15, 15), pady=(10, 10))
        self.password_input_field = customtkinter.CTkEntry(self.login_frame,
                                                           width=300,
                                                           placeholder_text="Password")
        self.password_input_field.grid(row=7, column=2, padx=(15, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame,
                                                    text="Login",
                                                    width= 300,
                                                    command=self.login)
        self.login_button.grid(row=8, column=2, padx=(30, 30), pady=(10, 30))

        ##################################################################################
        # Setting the default values:
        customtkinter.set_appearance_mode("Dark")
        self.appearance_mode_optionmenu.set("Dark")
        self.ui_scaling_optionmenu.set("100%")

    ### KEANU ÄNDERUNG - BITTE LÖSCHEN, WENN GESEHEN #####

    def switch_server(self, server):
        if server == "mainnet":
            self.server_mainnet_button.configure(state="disabled")
            self.server_testnet_button.configure(state="normal")
            self.login_label.configure(True, text="Login to Mainnet-Server")
        elif server == "testnet":
            self.server_mainnet_button.configure(state="normal")
            self.server_testnet_button.configure(state="disabled")
            self.login_label.configure(True, text="Login to Testnet-Server")


    @staticmethod
    def switch_appearance(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    @staticmethod
    def switch_scaling(new_scaling : str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def login(self):
        # self.withdraw()
        if self.wallet_window is None or not self.wallet_window.winfo_exists():
            self.wallet_window = Window2()  # create window if its None or destroyed
        else:
            self.wallet_window.focus()  # if window exists focus it
        print("Logged in!")


class Window2(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        ##################################################################################
        # Window settings:
        self.geometry("1100x580")
        self.title("Wallet")


        ##################################################################################
        # Grid layout settings:
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        ##################################################################################
        # Creating sidebar:
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=11, sticky="nsew")

        # Creating Server-switch widgets:
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
                                               text="Here could be ur add!",
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

        ####### NEUER CODE ZUR ANBINDUNG DER API ######

        # Erstellung des "Coin Balance"-Frames:
        self.coin_balance_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.coin_balance_frame.grid(row=1, column=1, rowspan=1)
        self.coin_balance_frame.place(x=570, y=20)

        # Erstellung der "Coin Balance"-Widgets:
        self.coin_balance_label = customtkinter.CTkLabel(self.coin_balance_frame,
                                                         text="Balance",
                                                         font=customtkinter.CTkFont(size=20, weight="bold"))
        self.coin_balance_label.grid(row=0, column=0, padx=(25, 25), pady=(30, 15))
        self.coin_balance_value = customtkinter.CTkLabel(self.coin_balance_frame,
                                                         text="0 BTC",
                                                         font=customtkinter.CTkFont(size=20))
        self.coin_balance_value.grid(row=1, column=0, padx=(25, 25), pady=(10, 10))


        ##################################################################################
        # Setting the default values:
        customtkinter.set_appearance_mode("Dark")
        self.appearance_mode_optionmenu.set("Dark")
        self.ui_scaling_optionmenu.set("100%")

    ##################################################################################

    @staticmethod
    def switch_appearance(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    @staticmethod
    def switch_scaling(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def logout(self):
        self.master.destroy()
        Window1()

def main():
    run = Application()


if __name__ == '__main__':
    main()
