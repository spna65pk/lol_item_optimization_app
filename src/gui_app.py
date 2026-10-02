import customtkinter as ctk
from tkinter import messagebox
from random import sample
from optimizer_logic import Algorithm, SolutionHandler
from typing import Union
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import requests
from io import BytesIO
import os
import sys

class SharedObject():
    def __init__(self,number):
        if isinstance(number,int) and number in [4,5,6]:
            self.no_of_items = number
        else:
            print("Błąd: no_of_items zły typ danych lub no_of_items nie należy do [4,5,6]")
    
    def get(self):
        return self.no_of_items
    
    def set(self,number):
        if isinstance(number,int) and number in [4,5,6]:
            self.no_of_items = number
        else:
            print("Błąd: zły typ danych lub no_of_items nie należy do [4,5,6]")

class MyRadiobuttonFrame(ctk.CTkFrame):
    def __init__(self, master, title, values,no_of_items):
        super().__init__(master,corner_radius=8)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.values = values
        self.no_of_items = no_of_items
        self.radiobuttons = []
        self.variable = ctk.IntVar(value=4)

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6,)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = ctk.CTkRadioButton(self, text=f'{value}', value=value, variable=self.variable,command=self._set_no_of_items)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def _set_no_of_items(self):
        self.no_of_items.set(self.variable.get())

class MyCheckboxFrame(ctk.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master,corner_radius=8)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = ctk.CTkCheckBox(self, text=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

class MyScrollableRadiobuttonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title,corner_radius=8)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.radiobuttons = []
        self.variable = ctk.StringVar(value="")

        for i, value in enumerate(self.values):
            radiobutton = ctk.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()
    
    def set(self, value):
        self.variable.set(value)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        # self.grid_rowconfigure(0, weight=1)

        # dane
        self.list_of_champions = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Aurora', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 'Briar', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'DrMundo', 'Draven', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Hwei', 'Illaoi', 'Irelia', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'KSante', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'Milio', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Naafiri', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Smolder', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']
        self.list_of_items = ['Abyssal Mask', 'Aether Wisp', 'Amplifying Tome', 'Anti-Tower Socks', "Archangel's Staff", 'Ardent Censer', 'Axiom Arc', 'B. F. Sword', "Bami's Cinder", 'Bandleglass Mirror', "Banshee's Veil", 'Base Turret Reinforced Armor (Turret Item)', "Berserker's Greaves", 'Black Cleaver', 'Black Spear', 'Blackfire Torch', 'Blade of the Ruined King', 'Blasting Wand', 'Blighting Jewel', 'Bloodsong', 'Bloodthirster', 'Boots', 'Boots of Swiftness', 'Bounty of Worlds', 'Bramble Vest', 'Cappa Juice', 'Catalyst of Aeons', "Caulfield's Warhammer", 'Celestial Opposition', 'Chain Vest', 'Chempunk Chainsword', 'Cloak of Agility', 'Cloth Armor', 'Control Ward', 'Cosmic Drive', 'Cryptbloom', 'Crystalline Bracer', 'Cull', 'Dagger', 'Dark Seal', 'Dawncore', "Dead Man's Plate", "Death's Dance", "Death's Daughter", "Doran's Blade", "Doran's Ring", "Doran's Shield", 'Dream Maker', 'Echoes of Helia', 'Eclipse', 'Edge of Night', 'Elixir of Avarice', 'Elixir of Force', 'Elixir of Iron', 'Elixir of Skill', 'Elixir of Sorcery', 'Elixir of Wrath', 'Essence Reaver', "Executioner's Calling", 'Experimental Hexplate', 'Eye of the Herald', 'Faerie Charm', 'Farsight Alteration', 'Fated Ashes', 'Fiendish Codex', 'Fimbulwinter', 'Fire at Will', 'Forbidden Idol', 'Force of Nature', 'Fortification', 'Frozen Heart', "Giant's Belt", 'Glacial Buckler', 'Glowing Mote', 'Guardian Angel', "Guardian's Blade", "Guardian's Hammer", "Guardian's Horn", "Guardian's Orb", "Guinsoo's Rageblade", 'Gusto', 'Gustwalker Hatchling', 'Haunting Guise', 'Health Potion', 'Hearthbound Axe', 'Heartsteel', 'Hexdrinker', 'Hextech Alternator', 'Hextech Rocketbelt', 'Hollow Radiance', 'Horizon Focus', 'Hubris', 'Hullbreaker', 'Iceborn Gauntlet', 'Immortal Shieldbow', 'Imperial Mandate', 'Infinity Edge', 'Ionian Boots of Lucidity', "Jak'Sho, The Protean", 'Kaenic Rookern', 'Kindlegem', "Knight's Vow", 'Kraken Slayer', 'Last Whisper', "Liandry's Torment", 'Lich Bane', 'Locket of the Iron Solari', 'Long Sword', "Lord Dominik's Regards", 'Lost Chapter', "Luden's Companion", 'Malignance', 'Manamune', 'Maw of Malmortius', "Mejai's Soulstealer", 'Mercurial Scimitar', "Mercury's Treads", "Mikael's Blessing", 'Moonstone Renewer', 'Morellonomicon', 'Mortal Reminder', 'Mosstomper Seedling', 'Muramana', "Nashor's Tooth", 'Navori Flickerblade', 'Needlessly Large Rod', 'Negatron Cloak', 'Noonquiver', 'Null-Magic Mantle', 'Oblivion Orb', 'Ohmwrecker (Turret Item)', 'Opportunity', 'Oracle Lens', 'Overcharged', "Overlord's Bloodmail", 'Phage', 'Phantom Dancer', 'Phreakish Gusto', 'Pickaxe', 'Plated Steelcaps', 'Poro-Snax', 'Profane Hydra', 'Quicksilver Sash', "Rabadon's Deathcap", 'Raise Morale', "Randuin's Omen", 'Rapid Firecannon', 'Ravenous Hydra', 'Rectrix', 'Recurve Bow', 'Redemption', 'Refillable Potion', 'Reinforced Armor (Turret Item)', 'Rejuvenation Bead', 'Riftmaker', 'Rod of Ages', 'Ruby Crystal', "Runaan's Hurricane", 'Runic Compass', "Rylai's Crystal Scepter", 'Sapphire Crystal', 'Scarecrow Effigy', 'Scorchclaw Pup', "Scout's Slingshot", "Seeker's Armguard", "Seraph's Embrace", "Serpent's Fang", 'Serrated Dirk', "Serylda's Grudge", 'Shadowflame', 'Shattered Armguard', 'Sheen', "Shurelya's Battlesong", 'Slightly Magical Boots', 'Solstice Sleigh', "Sorcerer's Shoes", 'Spear of Shojin', "Spectre's Cowl", 'Spirit Visage', 'Staff of Flowing Water', 'Statikk Shiv', 'Stealth Ward', 'Steel Sigil', "Sterak's Gage", 'Stormsurge', 'Stridebreaker', 'Sundered Sky', 'Sunfire Aegis', 'Super Mech Armor', 'Super Mech Power Field', 'Symbiotic Soles', 'Synchronized Souls', 'Tear of the Goddess', 'Terminus', 'The Brutalizer', 'The Collector', 'Thornmail', 'Tiamat', 'Titanic Hydra', 'Total Biscuit of Everlasting Will', 'Trailblazer', 'Trinity Force', 'Tunneler', 'Turret Plating', 'Umbral Glaive', 'Unending Despair', 'Vampiric Scepter', 'Verdant Barrier', 'Vigilant Wardstone', 'Void Staff', 'Voltaic Cyclosword', "Warden's Eye", "Warden's Mail", "Warmog's Armor", 'Watchful Wardstone', 'Winged Moonplate', "Winter's Approach", "Wit's End", 'World Atlas', "Youmuu's Ghostblade", 'Your Cut', 'Yun Tal Wildarrows', "Zaz'Zak's Realmspike", 'Zeal', "Zeke's Convergence", 'Zephyr', "Zhonya's Hourglass"]
        self.no_of_items = SharedObject(4)
        self.choosen_items = []
        self.choosen_champs = []
        self.main_champ = ""
        self.how_to_neighbour = []
        self.T_init = None
        self.T_final = None
        self.alfa = None
        self.alg = Algorithm()  # algorytm
        self.handler = None
        self.gold_limit = None
        self.toplevel_window = None

        # inicjalizacja widżetów
        # kolumna pierwsza (0)
        self.scrollable_radiobutton_frame_champs_1 = MyScrollableRadiobuttonFrame(self,title="Wybierz Championa",values=self.list_of_champions)
        self.scrollable_radiobutton_frame_champs_2 = MyScrollableRadiobuttonFrame(self,title="Wybierz wrogich Championów",values=self.list_of_champions)
        self.frame1 = ctk.CTkFrame(self,corner_radius=8)
        self.frame1.grid_columnconfigure(1,weight=1)
        self.button_add_champion = ctk.CTkButton(self.frame1,text="Wybierz Championa",command=self.add_champs_to_choosen)
        self.button_random_champ = ctk.CTkButton(self.frame1,text="Wylosuj Championów",command=self.choose_champs_randomly)
        self.combox_choosen_champs = ctk.CTkComboBox(self.frame1,values=self.choosen_champs)
        self.button_remove_champ = ctk.CTkButton(self.frame1,text="Usuń Championa",command=self.delete_champ_form_choosen)
        self.textbox_champs = ctk.CTkTextbox(self,width=200,height=200,state="disabled",corner_radius=8)

        # kolumna druga (1)
        self.radiobutton_frame_no_of_items = MyRadiobuttonFrame(self,title="Wybierz ilość przedmiotów",values=[4,5,6],no_of_items=self.no_of_items)
        self.scrollable_radiobutton_frame_items = MyScrollableRadiobuttonFrame(self,title="Przedmioty",values=self.list_of_items)
        self.frame2 = ctk.CTkFrame(self,corner_radius=8)
        self.frame2.grid_columnconfigure(1,weight=1)
        self.button_add_item = ctk.CTkButton(self.frame2,text="Wybierz przedmiot",command=self.add_item_to_choosen)
        self.button_random_items = ctk.CTkButton(self.frame2,text="Wylosuj przedmioty",command=self.choose_items_randomly)
        self.combox_choosen_item = ctk.CTkComboBox(self.frame2,values=self.choosen_items)
        self.button_remove_item = ctk.CTkButton(self.frame2,text="Usuń przedmiot",command=self.delete_item_form_choosen)
        self.textbox_items = ctk.CTkTextbox(self,width=200,height=200,corner_radius=8,state="disabled")

        # kolumna trzecia (2)
        self.frame3 = ctk.CTkFrame(self,corner_radius=8)    # początek frame 3
        self.label_text = ctk.CTkLabel(self.frame3,text="Wprowadź parametry")
        self.label_Tinit = ctk.CTkLabel(self.frame3,text="T_init:")
        self.label_Tfinal = ctk.CTkLabel(self.frame3,text="T_final:")
        self.label_alfa = ctk.CTkLabel(self.frame3,text="alfa:")
        self.label_gold_limit = ctk.CTkLabel(self.frame3,text="Ograniczenie złota:")
        self.entry_Tinit = ctk.CTkEntry(self.frame3)
        self.entry_Tfinal = ctk.CTkEntry(self.frame3)
        self.entry_alfa = ctk.CTkEntry(self.frame3)
        self.entry_gold_limt = ctk.CTkEntry(self.frame3)         # koniec frame 3
        self.frame4 = ctk.CTkFrame(self,corner_radius=8)    # początek frame 4
        self.label_text2 = ctk.CTkLabel(self.frame4,text="Wybierz sposób tworzenie sąsiedztwa:")
        self.checkbox_frame_noghbourhood = MyCheckboxFrame(self.frame4,values=["s1","s2","s3","s4","s5","s6"])
        self.start_button = ctk.CTkButton(self,text="Start",command=self.start)


        # wywołanie głownego okna
        self.setup_main_window()

    def setup_main_window(self):

        self.title("Dobór przedmiotów w grze League of Legends")
        self.geometry("900x1000")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    
        # budowanie okna z istniejących widzetów zainicjalizowanych w __init__
        # kolumna pierwsza (0)
        self.scrollable_radiobutton_frame_champs_1.grid(row=0,column=0,padx=10,pady=10)
        self.scrollable_radiobutton_frame_champs_2.grid(row=1,column=0,padx=10,pady=10)
        self.frame1.grid(row=2,column=0,padx=10,pady=10) #,sticky="ew")
        self.button_add_champion.grid(row=0,column=0,padx=10,pady=(10,0),sticky="ew")   # początek frame1
        self.button_random_champ.grid(row=1,column=0,padx=10,pady=(10,0),sticky="ew")
        self.combox_choosen_champs.grid(row=2,column=0,padx=10,pady=(10,0),sticky="ew")
        self.button_remove_champ.grid(row=3,column=0,padx=10,pady=(10,10),sticky="ew")  # koniec frame1
        self.textbox_champs.grid(row=3,column=0,padx=10,pady=10)

        # kolumna druga (1)
        self.radiobutton_frame_no_of_items.grid(row=0,column=1,padx=10,pady=10)
        self.scrollable_radiobutton_frame_items.grid(row=1,column=1,padx=10,pady=10)
        self.frame2.grid(row=2,column=1,padx=10,pady=10) #,sticky="ew")
        self.button_add_item.grid(row=0,column=0,padx=10,pady=(10,0),sticky="ew")       # początek frame2
        self.button_random_items.grid(row=1,column=0,padx=10,pady=(10,0),sticky="ew")
        self.combox_choosen_item.grid(row=2,column=0,padx=10,pady=(10,0),sticky="ew")
        self.button_remove_item.grid(row=3,column=0,padx=10,pady=(10,10),sticky="ew")    # koniec frame2
        self.textbox_items.grid(row=3,column=1,padx=10,pady=10)

        # kolumna trzecia (2)
        self.frame3.grid(row=0,column=2,padx=10,pady=10)
        self.label_text.grid(row=0,column=0,padx=10,pady=10,columnspan=2)
        self.label_Tinit.grid(row=1,column=0,padx=10,pady=(10,0))
        self.label_Tfinal.grid(row=2,column=0,padx=10,pady=(10,0))
        self.label_alfa.grid(row=3,column=0,padx=10,pady=(10,0))
        self.label_gold_limit.grid(row=4,column=0,padx=10,pady=(10,10))
        self.entry_Tinit.grid(row=1,column=1,padx=10,pady=(10,0))
        self.entry_Tfinal.grid(row=2,column=1,padx=10,pady=(10,0))
        self.entry_alfa.grid(row=3,column=1,padx=10,pady=(10,0))
        self.entry_gold_limt.grid(row=4,column=1,padx=10,pady=(10,10))
        self.frame4.grid(row=1,column=2,padx=10,pady=10) #,rowspan=2)
        self.label_text2.grid(row=0,column=0,padx=10,pady=10)
        self.checkbox_frame_noghbourhood.grid(row=1,column=0,padx=10,pady=10)
        self.start_button.grid(row=2,column=2,padx=10,pady=10, rowspan=2)

    def setup_result_window(self):
        frame1 = ctk.CTkFrame(self)
        frame2 = ctk.CTkFrame(self)
        back_button = ctk.CTkButton(frame2,text="Powrót",command=self.back_to_main_window)
        label_result = ctk.CTkLabel(frame1,text=self.handler.get_string_solution())

        canvas = FigureCanvasTkAgg(self.handler.obj_func_fig(), master=self)
        canvas_widget_obj_func = canvas.get_tk_widget()

        canvas = FigureCanvasTkAgg(self.handler.temperature_fig(), master=self)
        canvas_widget_temp = canvas.get_tk_widget()

        # place
        frame1.grid(row=0,column=0,padx=10,pady=10)
        label_result.grid(row=0,column=0,padx=10,pady=10)
        frame2.grid(row=1,column=0,padx=10,pady=10)
        back_button.grid(row=1,column=1,padx=10,pady=10)
        canvas_widget_temp.grid(row=0,column=1,padx=10,pady=10)
        canvas_widget_obj_func.grid(row=1,column=1,padx=10,pady=10)

    def clear_window(self):
        # czyszeczenie okna z widżetów
        for widget in self.winfo_children():
            widget.destroy()

    def add_item_to_choosen(self):
        item = self.scrollable_radiobutton_frame_items.get()
        if item == "":
            return
        if item not in self.choosen_items:
            if len(self.choosen_items) < self.no_of_items.get():
                self.choosen_items.append(item)
                self.update_textbox_items()
                self.combox_choosen_item.configure(values=self.choosen_items)
            else:
                if self.no_of_items.get() == 4:
                    messagebox.showerror("Błąd","Należy wybrać dokładnie 4 przedmioty")
                else:
                    messagebox.showerror("Błąd",f"Należy wybrać dokładnie {self.no_of_items.get()} przedmiotów")
        else:
            messagebox.showerror("Błąd","Nie można dwa razy wybrać tego samego przedmiotu")

    def choose_items_randomly(self):
        choosen_items = sample(self.list_of_items,self.no_of_items.get())
        self.choosen_items = choosen_items
        self.update_textbox_items()
        self.combox_choosen_item.configure(values=self.choosen_items)

    def delete_item_form_choosen(self):
        item = self.combox_choosen_item.get()
        if item not in self.choosen_items:
            return
        self.choosen_items.remove(item)
        self.combox_choosen_item.configure(values=self.choosen_items)
        self.update_textbox_items()
     
    def update_textbox_items(self):
        self.textbox_items.configure(state="normal")
        self.textbox_items.delete("1.0", "end")
        for item in self.choosen_items:
            self.textbox_items.insert("end", f"{item}\n")
        self.textbox_items.configure(state="disabled")

    def add_champs_to_choosen(self):
        champ = self.scrollable_radiobutton_frame_champs_2.get()
        if champ == "":
            return
        if champ not in self.choosen_champs:
            if len(self.choosen_champs) < 5:
                self.choosen_champs.append(champ)
                self.update_textbox_champs()
                self.combox_choosen_champs.configure(values=self.choosen_champs)
            else:
                messagebox.showerror("Błąd",f"Należy wybrać dokładnie 5 championów")
        else:
            messagebox.showerror("Błąd","Nie można dwa razy wybrać tego samego championa")

    def choose_champs_randomly(self):
        choosen_champs = sample(self.list_of_champions,5)
        self.choosen_champs = choosen_champs
        self.update_textbox_champs()
        self.combox_choosen_champs.configure(values=self.choosen_champs)
    
    def delete_champ_form_choosen(self):
        champ = self.combox_choosen_champs.get()
        if champ not in self.choosen_champs:
            return
        self.choosen_champs.remove(champ)
        self.combox_choosen_champs.configure(values=self.choosen_champs)
        self.update_textbox_champs()

    def update_textbox_champs(self):
        self.textbox_champs.configure(state="normal")
        self.textbox_champs.delete("1.0", "end")
        for champ in self.choosen_champs:
            self.textbox_champs.insert("end", f"{champ}\n")
        self.textbox_champs.configure(state="disabled")

    def get_neighbourhood(self):
        neigh = self.checkbox_frame_noghbourhood.get()
        neighbourhood_numbers = []
        d = {
            "s1" : 1,
            "s2" : 2,
            "s3" : 3,
            "s4" : 4,
            "s5" : 5,
            "s6" : 6
        }
        for e in neigh:
            neighbourhood_numbers.append(d[e])
        return neighbourhood_numbers

    def set_T_init(self,value):
        try:
            value = float(value)
            if value > 0 or value < 10000000:
                self.T_init = value
            else:
                messagebox.showerror("Błąd","T_init musi być z przedziału [0,10^7]")
        except ValueError:
            messagebox.showerror("Błąd","T_init musi być typu int lub float")
            
    def set_T_final(self,value):
        try:
            value = float(value)
            if value > 0 or value < 10000000:
                self.T_final = value
            else:
                messagebox.showerror("Błąd","T_fianl musi być z przedziału [0,10^7] oraz być większa od T_init")
        except ValueError:
            messagebox.showerror("Błąd","T_fianl musi być typu int lub float")

    def set_alfa(self,value):
        try:
            value = float(value)
            if value > 0 and value < 1:
                self.alfa = value
            else:
                messagebox.showerror("Błąd","alfa musi być z przedziału [0,1]")
        except ValueError:
            messagebox.showerror("Błąd","alfa musi być typu int lub float")

    def set_gold_limit(self,g):
        try:
            g = int(g)
            if g > 0:
                self.gold_limit = g
            else:
                messagebox.showerror("Błąd","Gold musi być liczbą większą od zera")
        except ValueError:
            messagebox.showerror("Błąd","Gold musi być typu int")

    def start(self):
        self.set_T_init(self.entry_Tinit.get())
        self.set_T_final(self.entry_Tfinal.get())
        self.set_alfa(self.entry_alfa.get())
        self.set_gold_limit(self.entry_gold_limt.get())
        self.main_champ = self.scrollable_radiobutton_frame_champs_1.get()



        if self.T_init is not None and self.T_final is not None and self.alfa is not None and len(self.choosen_champs) == 5\
                and self.main_champ != "" and len(self.choosen_items) == self.no_of_items.get() and\
                    self.gold_limit is not None and len(self.checkbox_frame_noghbourhood.get()) >= 1:
            
            if self.T_init < self.T_final:
                messagebox.showerror("Błąd","T_fianl musi być większe od T_init")
                return None
            
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                # ustawienie parametrów i wywołanie algorytmu
                self.alg.set_no_of_items(self.no_of_items.get())
                self.alg.gold_setting(self.gold_limit)
                self.alg.starting_enemy_parameters(self.choosen_champs)
                self.handler = self.alg.simulated_annealing(self.main_champ,self.choosen_items,self.get_neighbourhood(),self.T_init,self.T_final,self.alfa,self.choosen_champs)
                images_of_items = []
                for e in self.handler.best_solution:
                    if e is not None:
                        im = self.download_image(self.alg.items_data[e]["icon"])
                        images_of_items.append(im)
                # utworzenie okna wynikowego
                self.toplevel_window = ToplevelWindow(self.handler,images_of_items)  # Przekazujemy self.eooe
                self.toplevel_window.attributes("-topmost", True)
                self.toplevel_window.focus_force()
                # self.toplevel_window.attributes("-topmost", False)
            else:
                self.toplevel_window.focus()  # Jeśli okno istnieje, ustawiamy na nim fokus

    def download_image(self, url):
        try:
            # Pobierz obraz z URL
            response = requests.get(url)
            response.raise_for_status()  # Sprawdzenie błędów HTTP

            # Konwersja do obiektu PIL.Image
            pil_image = Image.open(BytesIO(response.content))

            # Konwersja obrazu PIL na CTkImage
            ctk_image = ctk.CTkImage(pil_image, size=(100, 100))  # Rozmiar obrazu (100x100)
            return ctk_image
        except Exception as e:
            print(f"Nie udało się pobrać obrazu: {e}")
            return None
        

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self,handler: SolutionHandler, images_of_items: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.geometry("900x1000")
        self.title("Wyniki działania algorytmu")

        # frame 1
        frame1 = ctk.CTkFrame(self)
        label_result = ctk.CTkLabel(frame1,text=handler.get_string_solution(),anchor="w",justify="left")
        # frame 2
        frame2 = ctk.CTkFrame(self)
        list_of_labelimages = []
        for e in images_of_items:
            label = ctk.CTkLabel(frame2,text="",image=e)
            list_of_labelimages.append(label)

        # wykresy z algorytmu
        canvas = FigureCanvasTkAgg(handler.obj_func_fig(), master=self)
        canvas_widget_obj_func = canvas.get_tk_widget()
        canvas = FigureCanvasTkAgg(handler.temperature_fig(), master=self)
        canvas_widget_temp = canvas.get_tk_widget()

        # place
        # frame 1
        frame1.grid(row=0,column=0,padx=10,pady=10)
        label_result.grid(row=0,column=0,padx=10,pady=10)
        # frame 2
        frame2.grid(row=1,column=0,padx=10,pady=10)
        row = 0
        column = 0
        for e in list_of_labelimages:
            if column == 3:
                row = 1
                column = 0
            e.grid(row=row,column=column,padx=5,pady=10)
            column += 1

        # wykresy z algorytmu
        canvas_widget_temp.grid(row=0,column=1,padx=10,pady=10)
        canvas_widget_obj_func.grid(row=1,column=1,padx=10,pady=10)

def resource_path(relative_path):
    """ Uzyskuje absolutną ścieżkę do zasobu, działa zarówno dla .py, jak i .exe """
    if getattr(sys, 'frozen', False):  # Sprawdza, czy aplikacja działa jako .exe
        base_path = sys._MEIPASS  # Ścieżka tymczasowa dla zasobów w PyInstaller
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()