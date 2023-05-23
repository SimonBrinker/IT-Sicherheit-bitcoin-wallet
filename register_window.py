import customtkinter  # Importiere das Modul customtkinter
import database_manager  # Importiere das Modul database_manager
from wallet import Wallet, Network  # Importiere die Klassen Wallet und Network aus dem Modul wallet
import re

class RegisterWindow(customtkinter.CTkToplevel):
    def __init__(self, network:Network, application):
        super().__init__()

        # Speichern des MainWindows für die login_on_register Methode
        self.application = application

        # Fenster soll nicht resizable sein
        self.resizable(width=False, height=False)

        #region UI

        width = 450  # Breite des Fensters
        height = 400  # Höhe des Fensters
        
        screen_width = self.winfo_screenwidth()  # Breite des Bildschirms
        screen_height = self.winfo_screenheight()  # Höhe des Bildschirms
        
        x = (screen_width/2) - (width/2)  # X-Koordinate der Fensterposition
        y = (screen_height/2) - (height/2)  # Y-Koordinate der Fensterposition

        self.geometry('%dx%d+%d+%d' % (width, height, x, y))  # Setze die Fenstergeometrie
        self.title("Wallet")  # Setze den Fenstertitel
        self.network = network  # Setze das Netzwerk

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        # Erstelle ein Rahmen-Widget für die Registrierung
        register_frame = customtkinter.CTkFrame(self, width=350, height=400, corner_radius=20)
        register_frame.grid(row=0, column=0, padx=(50, 50), pady=(20, 20), rowspan=7, sticky="nsew")

        # Erstelle ein Label-Widget für die Registrierung
        register_label = customtkinter.CTkLabel(register_frame, text="Registrieren", font=customtkinter.CTkFont(size=20, weight="bold"))
        register_label.grid(row=1, column=0, padx=(85, 85), pady=(20, 15))

        # Erstelle ein Entry-Widget für den Benutzernamen
        self.username_entry = customtkinter.CTkEntry(register_frame, width=300, placeholder_text="Benutzername")
        self.username_entry.grid(row=2, column=0, padx=(25, 25), pady=(0, 15))

        # Erstelle ein Entry-Widget für das Passwort
        self.password_entry = customtkinter.CTkEntry(register_frame, width=300, placeholder_text="Passwort", show="*")
        self.password_entry.grid(row=3, column=0, padx=(25, 25), pady=(0, 15))

        # Erstelle ein Entry-Widget für die Passwortbestätigung
        self.password_2_entry = customtkinter.CTkEntry(register_frame, width=300, placeholder_text="Passwort wiederhohlen", show="*")
        self.password_2_entry.grid(row=4, column=0, padx=(25, 25), pady=(0, 15))

        # Erstelle ein Entry-Widget für den privaten Schlüssel
        self.private_key_entry = customtkinter.CTkEntry(register_frame, width=300, placeholder_text="Privater Schlüssel")
        self.private_key_entry.grid(row=5, column=0, padx=(25, 25), pady=(0, 15))

        # Erstelle ein CheckBox-Widget für die Option zum Erstellen einer neuen BTC-Adresse
        self.create_btc_address = customtkinter.CTkCheckBox(register_frame, text="Neue BTC-Adresse?", onvalue="on", offvalue="off", command=self.toggle_Private_Key_Entry)
        self.create_btc_address.grid(row=6, column=0, padx=(25, 25), pady=(0, 15))

        # Erstelle ein Button-Widget zum Registrieren
        self.register_button = customtkinter.CTkButton(register_frame, text="Registrieren!", width=300, command=self.register_account)
        self.register_button.grid(row=7, column=0, padx=(25, 25), pady=(0, 0))

        # Erstelle ein Label-Widget für Fehlermeldungen
        self.error_Label = customtkinter.CTkLabel(register_frame, text="", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.error_Label.grid(row=8, column=0, padx=(0, 0), pady=(0, 0))
    
        #endregion

    def toggle_Private_Key_Entry(self):
        # Methode zum Aktivieren/Deaktivieren des privaten Schlüsseleingabe-Widgets basierend auf dem Zustand der CheckBox

        if self.create_btc_address.get() == "on":
                # Deaktiviere das Eingabefeld für den privaten Schlüssel
            self.private_key_entry.configure(state="disabled", fg_color=['gray75', 'gray18'], border_color=['gray60', 'gray24'], placeholder_text="disabled")
        else:
                # Aktiviere das Eingabefeld für den privaten Schlüssel
            self.private_key_entry.configure(state="normal", fg_color=['#F9F9FA', '#343638'], border_color=['#979DA2', '#565B5E'], placeholder_text="Enter Private Key")

    def register_account(self):
        # Methode zum Registrieren eines Benutzerkontos

        username = self.username_entry.get() # Abrufen des Benutzernamens aus der Eingabe
        password = self.password_entry.get() # Abrufen des Passworts aus der Eingabe
        password_2 = self.password_2_entry.get() # Abrufen des wiederholten Passworts aus der Eingabe

        # Validierung des Usernames
        if len(username) < 5 or len(username) > 15:
            self.error_Label.configure(text="\nFehler: Der Username muss länger als 4\n und kürzer als 16 Zeichen sein!")
        
        #Validierung des Passworts
        elif len(password) < 8:
            self.error_Label.configure(text="\nFehler: Das Passwort muss länger als 8\n Zeichen sein!")

        elif re.search(r"\d", password) is None and re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None:
            self.error_Label.configure(text="\nFehler: Das Passwort muss mindestens \nein Sonderzeichen oder eine Zahl\n enthalten!")

        elif re.search(r"[a-z]", password) is None or re.search(r"[A-Z]", password) is None:
            self.error_Label.configure(text="\nFehler: Das Passwort muss mindestens \neinen Großbuchstaben oder einen Kleinbuchstaben\n enthalten!")

        #Validierung der Passwortbestätigung
        elif password_2 != password:
            self.error_Label.configure(text="\nFehler: Die Passwörter")

        else:
            createNew = False

            if self.create_btc_address.get() == "on":
                createNew = True
            
            # Registrierung des Benutzers in der Datenbank und erstellung/speicherung der Wallet
            wallet = database_manager.register(username, password, self.network, createNew, self.private_key_entry.get())

            database_manager.close() # Schließen der Datenbankverbindung

            # login nach einem erfolgreichen Registrierungsversuch
            self.application.login_on_register(wallet)

            self.destroy() # Schließen des aktuellen Fensters