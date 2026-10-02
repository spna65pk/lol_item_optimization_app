from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

# Konfiguracja Selenium i przeglądarki
options = Options()
options.headless = True  # Uruchomić bez okna przeglądarki (headless mode)

service = Service("C:\Piotr.K\AGH_STUDIA\semV\Badania_Operacyjne2\projekt\pobieranie_danych\chromedriver-win64\chromedriver.exe")  # Zmienna chromedriver
driver = webdriver.Chrome(service=service, options=options)

# Lista postaci
champions_all = [
    "Aatrox", "Ahri", "Akali","Akshan", "Alistar", "Amumu", "Anivia","annie","Aphelios", "Ashe", "aurelionsol","Aurora", "Azir", #annie z malej; aurelionsol
    "Bard","belveth", "Blitzcrank", "Brand", "Braum","Briar", "Caitlyn", "Camille", "Cassiopeia", "Chogath", #belveth
    "Corki", "Darius", "Diana", "DrMundo", "Draven", "Ekko", "Elise","Evelynn", "Ezreal","Fiddlesticks", "Fiora", 
    "Fizz", "galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves","Gwen", "Hecarim", "Heimerdinger", "Hwei", #galio
    "Illaoi", "Irelia", "janna", "JarvanIV", "Jax", "Jayce", "Jhin", "Jinx", "Kaisa", "Kalista", "Karma", "Karthus",  #janna
    "Kassadin", "Katarina", "Kayle","Kayn", "Kennen", "Khazix", "Kindred", "Kled","KogMaw","KSante", "LeBlanc", #khazix na male z
    "LeeSin", "Leona", "Lillia", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", 
    "Maokai", "MasterYi", "milio", "MissFortune", "MonkeyKing", "Mordekaiser", "Morgana",  #milio
    "Naafiri", "Nami", "nasus", "Nautilus", "Neeko", "Nidalee", "Nilah", "Nocturne", "Nunu",  #nasus
    "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana", "quinn", "Rakan", "Rammus", #quinn
    "RekSai", "Rell", "Renata", "Renekton", "Rengar", "Riven", "Rumble", "Ryze", "Samira", 
    "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana", "Singed", "Sion", 
    "Sivir", "Skarner", "Smolder", "Sona", "Soraka", "Swain", "Sylas", "Syndra", "TahmKench", 
    "Taliyah", "Talon", "Taric", "Teemo", "thresh", "Tristana", "Trundle", "Tryndamere", #thresh
    "TwistedFate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Velkoz", "Vex", 
    "Vi", "Viego", "Viktor", "Vladimir", "volibear", "Warwick", "Xayah", "Xerath", "XinZhao", #volibear
    "Yasuo", "Yone", "Yorick", "Yuumi", "Zac", "Zed", "Zeri", "Ziggs", "Zilean", "zoe", "Zyra" #zoe
]

nie_znalazlo = []
champions_data_suggested_items = {}

for champ in champions_all:
    url = f"https://mobalytics.gg/lol/champions/{champ}/build"
    driver.get(url)
    
    # Czekaj aż strona się załaduje
    time.sleep(3)  # Czas w sekundach, aby strona się wczytała
    
    try:
        image1 = driver.find_element(By.CSS_SELECTOR, '#container > div > main > div.m-o88682 > div > div.m-179t5g5 > div > div > div.m-5ob2ly > div.m-5648tp > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div.m-l9l2ov > div:nth-child(3) > div > div.m-yhe5ws > div > div.m-y4zi7x > div > img')
        image2 = driver.find_element(By.CSS_SELECTOR, "#container > div > main > div.m-o88682 > div > div.m-179t5g5 > div > div > div.m-5ob2ly > div.m-5648tp > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div.m-l9l2ov > div:nth-child(3) > div > div.m-yhe5ws > div > div.m-1k0bl65 > div > img")
        item1 = {"name": image1.get_attribute("alt"), "src": image1.get_attribute("src")}
        item2 = {"name": image2.get_attribute("alt"), "src": image2.get_attribute("src")}
        if (champ == 'Cassiopeia' or champ == 'Yuumi'):

                    # Dodaj dane do słownika
            champions_data_suggested_items[champ] = [item1, item2]
            print(f"Obrazek dla {champ}: {item1}, {item2}")
        else:
            image3 = driver.find_element(By.CSS_SELECTOR, '#container > div > main > div.m-o88682 > div > div.m-179t5g5 > div > div > div.m-5ob2ly > div.m-5648tp > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div.m-l9l2ov > div:nth-child(3) > div > div.m-yhe5ws > div > div.m-1v7ybmd > div > img')
            # Pobieranie zarówno alt jak i src dla każdego obrazka
            item3 = {"name": image3.get_attribute("alt"), "src": image3.get_attribute("src")}

            # Dodaj dane do słownika
            champions_data_suggested_items[champ] = [item1, item2, item3]
            print(f"Obrazek dla {champ}: {item1}, {item2}, {item3}")
 
    except Exception as e:
        print(f"Nie znaleziono obrazka dla {champ}: {e}")
        nie_znalazlo.append(champ)

driver.quit()  # Zamknij przeglądarkę po zakończeniu

# Zapisz dane do pliku JSON
with open("champs_suggested_items.json", "w", encoding="utf-8") as file:
    json.dump(champions_data_suggested_items, file, ensure_ascii=False, indent=4)

print("Nie znaleziono dla:", nie_znalazlo)
