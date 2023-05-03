import customtkinter


class Wallet(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window settings:
        self.geometry("500x350")
        self.title("Wallet")

        # Grid layout settings:
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Components:
        self.label = customtkinter.CTkLabel(self, text="User: ", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.label.grid(row=0, column=0, sticky="nsew", padx=10)



class App(customtkinter.CTk):
    # Constructor:
    def __init__(self):
        super().__init__()

        # Window settings:
        self.geometry("1100x580")
        self.title("WalletUI")
        self.wallet_window = None

        # Grid layout settings:
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        # create sidebar frame with widgets:
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, height=580, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=11, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Select Wallet", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="BTC-Mainnet", anchor="n", command=self.useMainnet)
        self.sidebar_button_1.grid(row=1, column=0, padx=5, pady=5)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="BTC-Testnet", anchor="n", command=self.useTestnet)
        self.sidebar_button_2.grid(row=2, column=0, padx=5, pady=5)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode", anchor="w", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.appearance_mode_label.grid(row=3, column=0, padx=10, pady=(20, 10))
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"], command=self.change_appearance)
        self.appearance_mode_optionmenu.grid(row=4, column=0, padx=10, pady=(1, 0))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.scaling_label.grid(row=8, column=0, padx=10, pady=(20, 10))
        self.scaling_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling)
        self.scaling_optionmenu.grid(row=9, column=0, padx=10, pady=(1, 0))

        # Creating main-entry and buttons:
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=30)
        self.login_frame.grid(row=5, column=1)
        self.login_label_1 = customtkinter.CTkLabel(self.login_frame, text="Login to BTC-Mainnet", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.login_label_1.grid(row=2, column=1, columnspan=1, padx=(50, 50), pady=(0, 150), sticky="nsew")
        self.username_input_field = customtkinter.CTkEntry(self.login_frame, width= 240, placeholder_text="Username")
        self.username_input_field.grid(row=2, column=1, columnspan=3, pady=(0, 50))
        self.password_input_field = customtkinter.CTkEntry(self.login_frame, width=240, placeholder_text="Password")
        self.password_input_field.grid(row=2, column=1, columnspan=3, pady=(100, 50))
        self.login_button = customtkinter.CTkButton(self.login_frame, width=240, text="Login", anchor="center", command=self.login)
        self.login_button.grid(row=2, column=1, pady=(200, 50))

        # Setting the default values:
        customtkinter.set_appearance_mode("Dark")
        self.appearance_mode_optionmenu.set("Dark")
        self.scaling_optionmenu.set("100%")


    # Hier Methoden einfügen:
    def useMainnet(self):
        self.login_label_1.configure(True, text="Login to BTC-Mainnet")
        print("Using mainnet!")

    def useTestnet(self):
        self.login_label_1.configure(True, text="Login to BTC-Testnet")
        print("using testnet!")

    def change_appearance(self, new_appearance_mode : str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling(self, new_scaling :str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def login(self):
        self.withdraw()
        if self.wallet_window is None or not self.wallet_window.winfo_exists():
            self.wallet_window = Wallet(self)  # create window if its None or destroyed
        else:
            self.wallet_window.focus()  # if window exists focus it
        print("Logged in!")


def main():
    myInstance = App()
    myInstance.mainloop()


if __name__ == '__main__':
    main()