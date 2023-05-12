import customtkinter
import sqlite3
import ecdsa
import base58
import hashlib
import binascii


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
                                                             command=lambda: self.switch_server("mainnet"))
        self.server_mainnet_button.grid(row=3, column=0, pady=(0, 5))
        self.server_testnet_button = customtkinter.CTkButton(self.sidebar_frame,
                                                             text="BTC-Testnet",
                                                             command=lambda: self.switch_server("testnet"))
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
        customtkinter.set_appearance_mode("Dark")
        self.appearance_mode_optionmenu.set("Dark")
        self.ui_scaling_optionmenu.set("100%")

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
        print("Entered login-method!")
        login_data = self.get_value()
        print(login_data[0], login_data[1])
        if login_data[0] == "Cengizhan" and login_data[1] == "Test1234":
            # Resetting the colors for wrong input:
            self.username_input_field.configure(fg_color="gray24")
            self.password_input_field.configure(fg_color="gray24")
            print("Login successful!")
            # self.withdraw()
            if self.wallet_window is None or not self.wallet_window.winfo_exists():
                print("Found no open Wallet-Window, creating new one!")
                self.wallet_window = WalletWindow(login_data[0], login_data[1])  # create window if its None or destroyed
            else:
                print("Found a Wallet-Window-Instance running, focusing it!")
                self.wallet_window.focus()  # if window exists focus it
        else:
            self.username_input_field.configure(fg_color="RED")
            self.password_input_field.configure(fg_color="RED")
            print("Login not successful, 'Username' and 'Password' dont match, or do not exist!")

    def create_new_account(self):
        if self.register_window is None or not self.wallet_window.winfo_exists():
            print("Found no open Register-Window, creating new one!")
            self.register_window = RegisterWindow(str(self.login_label.cget("text")))  # create window if its None or destroyed
        else:
            print("Found a Register-Window-Instance running, focusing it!")
            self.register_window_window.focus()  # if window exists focus it

    def get_value(self):
        return [self.username_input_field.get(), self.password_input_field.get()]


class WalletWindow(customtkinter.CTkToplevel):
    def __init__(self, username: str, password: str):
        super().__init__()

        ##################################################################################
        # User information:
        self.username = username
        self.password = password

        ##################################################################################
        # Window settings:
        self.geometry("1100x580")
        self.title("Wallet")

        ##################################################################################
        # Grid layout settings:
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
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

        ##################################################################################
        # Profile frame with widgets:
        self.profile_frame = customtkinter.CTkFrame(self, width=600, height=300, corner_radius=10)
        self.profile_frame.grid(row=0, column=1, columnspan=3, rowspan=3, padx=(10, 650), pady=(15, 10), sticky="nsew")
        self.profile_label = customtkinter.CTkLabel(self.profile_frame,
                                                    text="Profile",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.profile_label.grid(row=0, column=1, columnspan=2, padx=(15, 650), pady=(5, 15))
        self.username_label = customtkinter.CTkLabel(self.profile_frame,
                                                     text="Username:",
                                                     font=customtkinter.CTkFont(size=16, weight="bold"))
        self.username_label.grid(row=1, column=1, padx=(0, 575), pady=(0, 5))
        self.username_from_user_label = customtkinter.CTkLabel(self.profile_frame,
                                                               text="Placeholder",
                                                               font=customtkinter.CTkFont(size=16, weight="bold"))
        self.username_from_user_label.grid(row=1, column=1, padx=(0, 350), pady=(0, 5))
        self.bitcoin_address_label = customtkinter.CTkLabel(self.profile_frame,
                                                            text="Address:",
                                                            font=customtkinter.CTkFont(size=16, weight="bold"))
        self.bitcoin_address_label.grid(row=1, column=1, padx=(15, 575), pady=(50, 5))
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
        self.destroy()


class RegisterWindow(customtkinter.CTkToplevel):
    def __init__(self, login_label):
        super().__init__()

        ##################################################################################
        # Window settings:
        self.geometry("450x400")
        self.title("Wallet")
        self.login_label = login_label

        ##################################################################################
        # Creating grid layout:
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        ##################################################################################
        # Creating Frame for the register form:
        register_frame = customtkinter.CTkFrame(self,
                                                width=350,
                                                height=400,
                                                corner_radius=20)
        register_frame.grid(row=0, column=0, padx=(50, 50), pady=(50, 50), rowspan=6, sticky="nsew")
        # Creating widgets:
        register_label = customtkinter.CTkLabel(register_frame,
                                                text="Register as a User",
                                                font=customtkinter.CTkFont(size=20, weight="bold"))
        register_label.grid(row=1, column=0, padx=(85, 85), pady=(20, 15))
        self.username_entry = customtkinter.CTkEntry(register_frame,
                                                width=300,
                                                placeholder_text="Username")
        self.username_entry.grid(row=2, column=0, padx=(25, 25), pady=(0, 15))
        self.password_entry = customtkinter.CTkEntry(register_frame,
                                                width=300,
                                                placeholder_text="Password")
        self.password_entry.grid(row=3, column=0, padx=(25, 25), pady=(0, 15))
        password_2_entry = customtkinter.CTkEntry(register_frame,
                                                  width=300,
                                                  placeholder_text="Repeat Password")
        password_2_entry.grid(row=4, column=0, padx=(25, 25), pady=(0, 15))
        self.create_btc_address = customtkinter.CTkCheckBox(register_frame,
                                                            text="Create new BTC-Address?",
                                                            onvalue="on",
                                                            offvalue="off")
        self.create_btc_address.grid(row=5, column=0, padx=(25, 25), pady=(0, 15))
        self.register_button = customtkinter.CTkButton(register_frame,
                                                       text="Register!",
                                                       width=300,
                                                       command=self.register_account)
        self.register_button.grid(row=6, column=0, padx=(25, 25), pady=(0, 0))
        ##################################################################################
    # Methods:

    def register_account(self):
        print("Entered register_account-Method!")
        # Variables for the userinput:
        username = self.username_entry.get()
        password = self.password_entry.get()
        create_new_address = self.create_btc_address.get()

        # Establishing a connection to the Databank:
        connection = sqlite3.connect("Accounts.db")
        cursor = connection.cursor()
        print("Connected to Databank at register_account-Method!")

        # Checking if a new address is wanted:
        if self.login_label == "Login to Mainnet-Server" and create_new_address == "on":
            print("Creating a new User with given input: " + username, " " + password + " on Mainnet-Server!")
            new_address = Address("00")
            # Saving the new_address to the databank:
            cursor.execute(
                "INSERT INTO Accounts (name, password, address, privatekey, publickey) VALUES (?, ?, ?, ?, ?)",
                (username, password, str(new_address.bitcoinAddress), str(new_address.ecdsaPrivateKey.to_string().hex()),
                 str(new_address.ecdsaPublicKey)))
        elif self.login_label == "Login to Testnet-Server" and create_new_address == "on":
            print("Creating a new User with given input: " + username, " " + password + " on Testnet-Server!")
            new_address = Address("6f")
            # Saving the new_address to the databank:
            cursor.execute(
                "INSERT INTO Accounts (name, password, address, privatekey, publickey) VALUES (?, ?, ?, ?, ?)",
                (username, password, str(new_address.bitcoinAddress), str(new_address.ecdsaPrivateKey.to_string().hex()),
                 str(new_address.ecdsaPublicKey)))
        # Creating a new account without btc_address:
        elif create_new_address == "off":
            print("Creating a new User with given input: " + username, " " + password + " without new_address!")
            # Saving the new_address to the databank:
            cursor.execute(
                "INSERT INTO Accounts (name, password) VALUES (?, ?)", (username, password))

        # Committing the changes to the Databank:
        print("Committing changes to the Databank!")
        connection.commit()
        connection.close()

        # Closing the window:
        print("Closing the Register-Window!")
        self.destroy()


class Address(object):
    def __init__(self, prefix):
        self.ecdsaPrivateKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.ecdsaPublicKey = '04' + self.ecdsaPrivateKey.get_verifying_key().to_string().hex()
        hash256FromECDSAPublicKey = hashlib.sha256(binascii.unhexlify(self.ecdsaPublicKey)).hexdigest()
        ridemp160FromHash256 = hashlib.new('ripemd160', binascii.unhexlify(hash256FromECDSAPublicKey))
        prependNetworkByte = str(prefix) + ridemp160FromHash256.hexdigest()
        hash = prependNetworkByte
        for x in range(1, 3):
            hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
        cheksum = hash[:8]
        appendChecksum = prependNetworkByte + cheksum
        self.bitcoinAddress = base58.b58encode(binascii.unhexlify(appendChecksum))
        print("BTC-Private-Key: ", self.ecdsaPrivateKey.to_string().hex())
        print("BTC-Public-Key: ", self.ecdsaPublicKey)
        print("BITCOIN PUBLIC ADDRESS: ", self.bitcoinAddress.decode('utf8'))

    def get_private_key(self):
        return self.ecdsaPrivateKey.to_string().hex()

    def get_public_key(self):
        return self.ecdsaPublicKey

    def get_bitcoin_address(self):
        return self.bitcoinAddress.decode('utf8')


def main():
    run = Application()


if __name__ == '__main__':
    main()