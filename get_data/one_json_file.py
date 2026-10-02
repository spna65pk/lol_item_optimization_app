import requests
import json

# URL do dużego pliku JSON
url = "https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json"

# Funkcja do pobierania danych JSON
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()  # sprawdź, czy zapytanie się powiodło
    return response.json()

champions_all = [
    "Aatrox", "Ahri", "Akali","Akshan", "Alistar", "Amumu", "Anivia","Annie","Aphelios", "Ashe", "AurelionSol","Aurora", "Azir", 
    "Bard","Belveth", "Blitzcrank", "Brand", "Braum","Briar", "Caitlyn", "Camille", "Cassiopeia", "Chogath", 
    "Corki", "Darius", "Diana", "DrMundo", "Draven", "Ekko", "Elise","Evelynn", "Ezreal","Fiddlesticks", "Fiora", 
    "Fizz", "Galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves","Gwen", "Hecarim", "Heimerdinger", "Hwei",
    "Illaoi", "Irelia", "Janna", "JarvanIV", "Jax", "Jayce", "Jhin", "Jinx", "Kaisa", "Kalista", "Karma", "Karthus", 
    "Kassadin", "Katarina", "Kayle","Kayn", "Kennen", "Khazix", "Kindred", "Kled","KogMaw","KSante", "Leblanc", #khazix na male z
    "LeeSin", "Leona", "Lillia", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", 
    "Maokai", "MasterYi", "Milio", "MissFortune", "MonkeyKing", "Mordekaiser", "Morgana", 
    "Naafiri", "Nami", "Nasus", "Nautilus", "Neeko", "Nidalee", "Nilah", "Nocturne", "Nunu", 
    "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana", "Quinn", "Rakan", "Rammus", 
    "RekSai", "Rell", "Renata", "Renekton", "Rengar", "Riven", "Rumble", "Ryze", "Samira", 
    "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana", "Singed", "Sion", 
    "Sivir", "Skarner", "Smolder", "Sona", "Soraka", "Swain", "Sylas", "Syndra", "TahmKench", 
    "Taliyah", "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere", 
    "TwistedFate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Velkoz", "Vex", 
    "Vi", "Viego", "Viktor", "Vladimir", "Volibear", "Warwick", "Xayah", "Xerath", "XinZhao", 
    "Yasuo", "Yone", "Yorick", "Yuumi", "Zac", "Zed", "Zeri", "Ziggs", "Zilean", "Zoe", "Zyra"
]

# Pobierz dane
data = fetch_data(url)
# Przykładowa funkcja do wyciągania danych dla konkretnego bohatera
filtered_champions_data = {}

# Przykładowa funkcja do wyciągania danych dla konkretnego bohatera
def get_champion_data(champion_name):
    # Jeśli bohater istnieje w danych, zwróć jego dane
    if champion_name in data:
        champion = data[champion_name]
        # Możesz teraz uzyskać interesujące cię dane, np. tytul, zdrowie, itp.
        champion_title = champion.get("title", "Brak tytułu")
        health_flat = champion["stats"]["health"]["flat"]
        health_per_level = champion["stats"]["health"]["perLevel"]
        regen_flat = champion["stats"]["healthRegen"]["flat"]
        regen_per_level = champion["stats"]["healthRegen"]["perLevel"]
        mana_flat = champion["stats"]["mana"]["perLevel"]
        mana_per_level = champion["stats"]["mana"]["perLevel"]
        mana_reg_flat = champion["stats"]["manaRegen"]["perLevel"]
        mana_reg_per_level = champion["stats"]["manaRegen"]["perLevel"]
        armor_flat = champion["stats"]["armor"]["flat"]
        armor_per_level = champion["stats"]["armor"]["perLevel"]
        magic_res_flat = champion["stats"]["magicResistance"]["flat"]
        magic_res_per_level = champion["stats"]["magicResistance"]["perLevel"]
        ad_flat = champion["stats"]["attackDamage"]["flat"]
        ad_per_lev = champion["stats"]["attackDamage"]["perLevel"]
        mvs_flat = champion["stats"]["movespeed"]["flat"]
        mvs_per_lev = champion["stats"]["movespeed"]["perLevel"]
        crit_dmg_flat = champion["stats"]["criticalStrikeDamage"]["flat"]
        crit_modifier = champion["stats"]["criticalStrikeDamageModifier"]["flat"]
        as_flat = champion["stats"]["attackSpeed"]["flat"]
        as_per_lev = champion["stats"]["attackSpeed"]["perLevel"]
        as_ratio = champion["stats"]["attackSpeedRatio"]["flat"]
        range_flat = champion["stats"]["attackRange"]["flat"]
        range_per_lev = champion["stats"]["attackRange"]["perLevel"]
        attributes = champion["attributeRatings"] 

        print(f"{champion_name}: {champion_title}")
        
        filtered_champions_data[champion_name] = {
            "name" : champion_name,
            "attributes" : attributes,
            "title": champion_title,
            "health": {
                "flat": health_flat,
                "perLevel": health_per_level,
                "regen flat" : regen_flat,
                "regen per level": regen_per_level},
            "mana" : {
                "flat" : mana_flat,
                "per level" : mana_per_level,
                "regen flat" : mana_reg_flat,
                "regen per level" : mana_reg_per_level
            },

            "armor": {
                "flat": armor_flat,
                "perLevel": armor_per_level
            },
            "magicResistance": {
                "flat": magic_res_flat,
                "perLevel":magic_res_per_level
            },
            "attackDamage": {
                "flat": ad_flat,
                "perLevel": ad_per_lev
            },
            "movespeed": {
                "flat": mvs_flat,
                "perLevel": mvs_per_lev,
            },

            "criticalStrikeDamage": {
                "flat": crit_dmg_flat,
            },
            "criticalStrikeDamageModifier": {
                "flat": crit_modifier,

            },
            "attackSpeed": {
                "flat": as_flat,
                "perLevel": as_per_lev,
            },
            "attackSpeedRatio": {
                "flat": as_ratio,

            },

            "attackRange": {
                "flat": range_flat,
                "perLevel": range_per_lev,
            }

            }
    else:
        print(f"Bohater {champion_name} nie istnieje w danych.")
ile = 0
for champion in champions_all:
    get_champion_data(champion)
    ile += 1

print('tyle mam:', ile)
print('dlg listy', len(champions_all))

# Zapisz przefiltrowane dane bohaterów do pliku JSON
with open("filtered_champions_data.json", "w", encoding="utf-8") as f:
    json.dump(filtered_champions_data, f, ensure_ascii=False, indent=4)

print(f"Liczba przetworzonych bohaterów: {len(filtered_champions_data)}")
print(f"Długość listy champions_all: {len(champions_all)}")
print(set(champions_all) - set(filtered_champions_data))