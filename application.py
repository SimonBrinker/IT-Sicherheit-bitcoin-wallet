import customtkinter
import database_manager
from wallet import Wallet, Network
from wallet_window import WalletWindow
from register_window import RegisterWindow


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
        self.selected_network = Network.MAINNET
        #region UI
        ##################################################################################
        # Window settings:#

        width = 1100 # Width 
        height = 580 # Height
        
        screen_width = self.winfo_screenwidth()  
        screen_height = self.winfo_screenheight() 
        
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.title("CryptoUI")
        self.wallet_window = None
        self.register_window = None

        ##################################################################################
        # Grid layout settings:
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        ##################################################################################
        # Creating sidebar:
        self.sidebar_frame = customtkinter.CTkFrame(self,
                                                    corner_radius=0)
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
        self.server_mainnet_button = customtkinter.CTkButton(self.sidebar_frame,
                                                             text="BTC-Mainnet",
                                                             command=lambda: self.switch_server(Network.MAINNET))
        self.server_mainnet_button.grid(row=3, column=0, pady=(0, 5))
        self.server_testnet_button = customtkinter.CTkButton(self.sidebar_frame,
                                                             text="BTC-Testnet",
                                                             command=lambda: self.switch_server(Network.TESTNET))
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
        self.ad_bar_frame = customtkinter.CTkFrame(self.sidebar_frame,
                                                   width= 150, height=200)
        self.ad_bar_frame.grid(row=10, column=0)
        self.ad_label = customtkinter.CTkLabel(self.ad_bar_frame,
                                               text="Here could be ur add!",
                                               font=customtkinter.CTkFont(weight="bold"))
        self.ad_label.grid(row=10, column=0, padx=(10, 10), pady=(85, 85))

        ##################################################################################
        # Creating login frame:
        self.login_frame = customtkinter.CTkFrame(self,
                                                  corner_radius=10)
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
                                                    width=145,
                                                    command=self.login)
        self.login_button.grid(row=8, column=2, padx=(150, 0), pady=(10, 30))
        self.register_button = customtkinter.CTkButton(self.login_frame,
                                                       text="Register",
                                                       width=145,
                                                       command=self.create_new_account)
        self.register_button.grid(row=8, column=2, padx=(0, 150), pady=(10, 30))
        ##################################################################################
        # Setting the default values:
        #endregion
        
        customtkinter.set_appearance_mode("Dark")
        self.appearance_mode_optionmenu.set("Dark")
        self.ui_scaling_optionmenu.set("100%")

    def switch_server(self, network:Network):
        if network == Network.MAINNET:
            self.server_mainnet_button.configure(state="disabled")
            self.server_testnet_button.configure(state="normal")
            self.login_label.configure(True, text="Login to Mainnet-Server")
            self.selected_network = Network.MAINNET
        elif network == Network.TESTNET:
            self.server_mainnet_button.configure(state="normal")
            self.server_testnet_button.configure(state="disabled")
            self.login_label.configure(True, text="Login to Testnet-Server")
            self.selected_network = Network.TESTNET

    @staticmethod
    def switch_appearance(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    @staticmethod
    def switch_scaling(new_scaling : str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def login(self):
        print("Entered login-method!")
        login_data = self.get_value()
        print(login_data[0], login_data[1])
        wallet = database_manager.login(login_data[0], login_data[1])
        if wallet:
            # Resetting the colors for wrong input:
            self.username_input_field.configure(fg_color="gray24")
            self.password_input_field.configure(fg_color="gray24")
            print("Login successful!")
            # self.withdraw()
            if self.wallet_window is None or not self.wallet_window.winfo_exists():
                print("Found no open Wallet-Window, creating new one!")
                self.wallet_window = WalletWindow(wallet)  # create window if its None or destroyed
                self.wallet_window.focus_set()
            else:
                print("Found a Wallet-Window-Instance running, focusing it!")
                self.wallet_window.focus()  # if window exists focus it
        else:
            self.username_input_field.configure(fg_color="RED")
            self.password_input_field.configure(fg_color="RED")
            print("Login not successful, 'Username' and 'Password' dont match, or do not exist!")

    def create_new_account(self):
        self.withdraw()
        self.register_window = RegisterWindow(self.selected_network)
        self.register_window.protocol("WM_DELETE_WINDOW", self.on_close_register)


        """
        if self.register_window is None or not self.wallet_window.winfo_exists():
            print("Found no open Register-Window, creating new one!")
            self.register_window = RegisterWindow(self.selected_network)  # create window if its None or destroyed
        else:
            print("Found a Register-Window-Instance running, focusing it!")
            self.register_window_window.focus()  # if window exists focus it
        """

    def on_close_register(self):
        self.register_window.destroy()
        self.deiconify()

    def get_value(self):
        return [self.username_input_field.get(), self.password_input_field.get()]

def main():
    run = Application()


if __name__ == '__main__':
    main()