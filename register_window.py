import customtkinter
import database_manager
from wallet import Wallet,Network

class RegisterWindow(customtkinter.CTkToplevel):
    def __init__(self, network:Network):
        super().__init__()

        #region UI

        ##################################################################################
        # Window settings:
        self.geometry("450x400")
        self.title("Wallet")
        self.network = network

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
    
        #endregion

    # Methods:

    def register_account(self):
        print("Entered register_account-Method!")
        # Variables for the userinput:
        username = self.username_entry.get()
        password = self.password_entry.get()
        #create_new_address = self.create_btc_address.get()

        print(f"Creating a new User with given input: {username} {password} on {self.network.value}!")
        wallte = database_manager.register(username, password, self.network)


        # Committing the changes to the Databank:
        print("Committing changes to the Database and close the connection!")
        database_manager.close()

        # Closing the window:
        print("Closing the Register-Window!")
        self.destroy()