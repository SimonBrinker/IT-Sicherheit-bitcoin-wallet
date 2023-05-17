
import customtkinter
from wallet import Wallet, Network

class WalletWindow(customtkinter.CTkToplevel):
    def __init__(self, wallet: Wallet):
        super().__init__()

        ##################################################################################
        # User information:
        self.wallet = wallet

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
                                                     text=f"Username",
                                                     font=customtkinter.CTkFont(size=16, weight="bold"))
        self.username_label.grid(row=1, column=1, padx=(0, 575), pady=(0, 5))
        self.username_from_user_label = customtkinter.CTkLabel(self.profile_frame,
                                                               text="Placeholder",
                                                               font=customtkinter.CTkFont(size=16, weight="bold"))
        self.username_from_user_label.grid(row=1, column=1, padx=(0, 350), pady=(0, 5))
        self.bitcoin_address_label = customtkinter.CTkLabel(self.profile_frame,
                                                            text=f"Address",
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
