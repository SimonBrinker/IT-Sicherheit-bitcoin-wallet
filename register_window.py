import customtkinter
import database_manager
from wallet import Wallet,Network

class RegisterWindow(customtkinter.CTkToplevel):
    def __init__(self, network:Network):
        super().__init__()

        #region UI

        ##################################################################################
        # Window settings:

        width = 450 # Width 
        height = 400 # Height
        
        screen_width = self.winfo_screenwidth()  
        screen_height = self.winfo_screenheight() 
        
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.title("Wallet")
        self.network = network

        ##################################################################################
        # Creating grid layout:
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        ##################################################################################
        # Creating Frame for the register form:
        register_frame = customtkinter.CTkFrame(self,
                                                width=350,
                                                height=400,
                                                corner_radius=20)
        register_frame.grid(row=0, column=0, padx=(50, 50), pady=(20, 20), rowspan=7, sticky="nsew")
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
        self.password_2_entry = customtkinter.CTkEntry(register_frame,
                                                  width=300,
                                                  placeholder_text="Repeat Password")
        self.password_2_entry.grid(row=4, column=0, padx=(25, 25), pady=(0, 15))
        self.private_key_entry = customtkinter.CTkEntry(register_frame,
                                                  width=300,
                                                  placeholder_text="Enter Private Key")
        self.private_key_entry.grid(row=5, column=0, padx=(25, 25), pady=(0, 15))
        self.create_btc_address = customtkinter.CTkCheckBox(register_frame,
                                                            text="Create new BTC-Address?",
                                                            onvalue="on",
                                                            offvalue="off",
                                                            command=self.toggle_Private_Key_Entry)
        self.create_btc_address.grid(row=6, column=0, padx=(25, 25), pady=(0, 15))
        self.register_button = customtkinter.CTkButton(register_frame,
                                                       text="Register!",
                                                       width=300,
                                                       command=self.register_account)
        self.register_button.grid(row=7, column=0, padx=(25, 25), pady=(0, 0))
        self.error_Label = customtkinter.CTkLabel(register_frame,
                                                text="",
                                                font=customtkinter.CTkFont(size=13, weight="bold"))
        self.error_Label.grid(row=8, column=0, padx=(0, 0), pady=(0, 0))
        ##################################################################################
    
        #endregion

    # Methods:

    def toggle_Private_Key_Entry(self):

        if customtkinter.get_appearance_mode() == "Dark":
            if self.create_btc_address.get() == "on":
                
                self.private_key_entry.configure(state="disabled", fg_color=['gray75', 'gray18'], border_color=['gray60', 'gray24'], placeholder_text="disabled")
            else:
                self.private_key_entry.configure(state="normal", fg_color=['#F9F9FA', '#343638'], border_color=['#979DA2', '#565B5E'], placeholder_text="Enter Private Key")

        elif customtkinter.get_appearance_mode() == "Light":
            if self.create_btc_address.get() == "on":
                self.private_key_entry.configure(state="disabled", fg_color=['gray75', 'gray18'], border_color=['gray60', 'gray24'], placeholder_text="disabled")
            else:
                self.private_key_entry.configure(state="normal", fg_color=['#F9F9FA', '#343638'], border_color=['#979DA2', '#565B5E'], placeholder_text="Enter Private Key")
        

        

    def register_account(self):
        print("Entered register_account-Method!")
        # Variables for the userinput:
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_2 = self.password_2_entry.get()

        if len(username) < 5 or len(username) > 15:
            self.error_Label.configure(text="\nFehler: Der Username muss länger als 4\n und kürzer als 16 Zeichen sein!")
            
        elif len(password) < 5:
            self.error_Label.configure(text="\nFehler: Das Passwort muss länger als 5\n Zeichen sein!")

        elif password_2 != password:
            self.error_Label.configure(text="\nFehler: Die Passwörter")

        else:
            createNew = False

            if self.create_btc_address.get() == "on":
                createNew = True
            
            print(f"Creating a new User with given input: {username} {password} on {self.network.value}!")
            wallet = database_manager.register(username, password, self.network, createNew, self.private_key_entry.get())


            # Committing the changes to the Databank:
            print("Committing changes to the Database and close the connection!")
            database_manager.close()

            # Closing the window:
            print("Closing the Register-Window!")
            self.destroy()