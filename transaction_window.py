import customtkinter  # Importiere das Modul customtkinter

class TransactionWindow(customtkinter.CTkToplevel):
    def __init__(self, transaction):
        super().__init__()

        self.resizable(width=False, height=False)


        width = 750  # Breite des Fensters
        height = 400  # Höhe des Fensters
        
        screen_width = self.winfo_screenwidth()  # Breite des Bildschirms
        screen_height = self.winfo_screenheight()  # Höhe des Bildschirms
        
        x = (screen_width/2) - (width/2)  # X-Koordinate der Fensterposition
        y = (screen_height/2) - (height/2)  # Y-Koordinate der Fensterposition

        self.geometry('%dx%d+%d+%d' % (width, height, x, y))  # Setze die Fenstergeometrie
        self.title("Transaktion")  # Setze den Fenstertitel

        self.columnconfigure((0,1), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        transaction_frame = customtkinter.CTkFrame(self, width=710, height=360, corner_radius=20)
        transaction_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), rowspan=8 ,columnspan=2, sticky="nsew")

        header_label = customtkinter.CTkLabel(transaction_frame, width=710, text="Transaktionsdetails", font=customtkinter.CTkFont(size=20, weight="bold"))
        header_label.grid(row=0, column=0, columnspan=2,  padx=(10, 10), pady=(10, 10))

        confirmation_label = customtkinter.CTkLabel(transaction_frame , width=480, anchor=customtkinter.W, justify=customtkinter.LEFT, text="Bestätigungen:", font=customtkinter.CTkFont(size=13))
        confirmation_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))

        confirmation_label_in = customtkinter.CTkLabel(transaction_frame , width=230,text=transaction['confirmations'], font=customtkinter.CTkFont(size=13))
        confirmation_label_in.grid(row=1, column=1,  padx=(10, 0), pady=(10, 10))

        in_label = customtkinter.CTkLabel(transaction_frame , width=480,text="Eingehende Transaktionen:", anchor=customtkinter.W, justify=customtkinter.LEFT, font=customtkinter.CTkFont(size=13))
        in_label.grid(row=2, column=0, padx=(10, 10), pady=(10, 10))

        inputs = ""
        inputs_value = ""
        for inputs_tx in transaction['inputs']:
            print(inputs_tx['addresses'])
            inputs = inputs + f"{inputs_tx['addresses'][0]}\n"
            inputs_value = inputs_value + f"Wert: {inputs_tx['output_value']/10**8} BTC\n"

        inputs_label = customtkinter.CTkLabel(transaction_frame,text=inputs,  width=480,anchor=customtkinter.W, justify=customtkinter.LEFT, font=customtkinter.CTkFont(size=13))
        inputs_label.grid(row=3, column=0, padx=(10, 10), pady=(10, 10))

        inputs_value_label_in = customtkinter.CTkLabel(transaction_frame,  width=230, text=inputs_value,font=customtkinter.CTkFont(size=13))
        inputs_value_label_in.grid(row=3, column=1,  padx=(10, 10), pady=(10, 10))

        out_label = customtkinter.CTkLabel(transaction_frame , width=480,text="Ausgehende Transaktionen:" ,anchor=customtkinter.W, justify=customtkinter.LEFT, font=customtkinter.CTkFont(size=13))
        out_label.grid(row=4, column=0, padx=(10, 10), pady=(10, 10))

        outputs = ""
        outputs_value = ""
        for output_tx in transaction['outputs']:
            print(output_tx['addresses'])
            if(not output_tx['addresses']):
                break
            outputs = outputs + f"{output_tx['addresses'][0]}\n"
            outputs_value = outputs_value + f"Wert: {output_tx['value']/10**8} BTC\n"

        outputs_label = customtkinter.CTkLabel(transaction_frame,text=outputs, width=480, anchor=customtkinter.W, justify=customtkinter.LEFT, font=customtkinter.CTkFont(size=13))
        outputs_label.grid(row=5, column=0,padx=(10, 10), pady=(10, 10))

        outputs_value_label = customtkinter.CTkLabel(transaction_frame, width=230,text=outputs_value, font=customtkinter.CTkFont(size=13))
        outputs_value_label.grid(row=5, column=1,  padx=(10, 10), pady=(10, 10))