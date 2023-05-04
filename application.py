import customtkinter


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

        ##################################################################################
        # Window settings:
        self.geometry("1100x580")
        self.title("CryptoUI")

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
        self.server_mainnet_button = customtkinter.CTkButton(self.sidebar_frame,
                                                             text="BTC-Mainnet",
                                                             command=self.switch_server())
        self.server_mainnet_button.grid(row=3, column=0, pady=(0, 5))
        self.server_testnet_button = customtkinter.CTkButton(self.sidebar_frame,
                                                             text="BTC-Testnet",
                                                             command=self.switch_server())
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
        self.login_button.grid(row=8, column=2, padx=(15, 30), pady=(10, 30))

        ##################################################################################
        # Setting the default values:
        customtkinter.set_appearance_mode("Dark")
        self.appearance_mode_optionmenu.set("Dark")
        self.ui_scaling_optionmenu.set("100%")

    def switch_server(self):
        #if self.login_label.cget("text") == "Login to BTC-Mainnet":
            #self.login_label.configure(True, "Login to BTC-Testnet")
        pass

    def switch_appearance(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def switch_scaling(self, new_scaling : str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def login(self):
        pass


def main():
    run = Application()


if __name__ == '__main__':
    main()