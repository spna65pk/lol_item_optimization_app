import requests
import json

# URL do dużego pliku JSON
url = "https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/items.json"

# Funkcja do pobierania danych JSON
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()  # sprawdź, czy zapytanie się powiodło
    return response.json()



# Pobierz dane
data = fetch_data(url)
print('DŁUGOŚĆ: ', len(data))
# Stworzenie słownika, w którym będziemy przechowywać przefiltrowane dane
filtered_items = {}
names = []
def get_item_data(item_num):
    # Jeśli bohater istnieje w danych, zwróć jego dane
    if item_num in data:
        item = data[item_num]
        # Możesz teraz uzyskać interesujące cię dane, np. tytul, zdrowie, itp.
        item_name = item.get("name", "Brak tytułu")
        item_rank = item.get("rank", "No rank")
        param = item["stats"]
        item_passive = item['passives']
        item_active = item['active']
        item_shop_stats = item['shop']
        item_icon = item['icon']
        print(f"{item_name}: {item_rank}")
        names.append(item_name)
        
        filtered_items[item_name] = {
            "name": item_name,
            "rank": item_rank,
            "param": param,
            "passives": item_passive,
            "active": item_active,
            "shop": item_shop_stats,
            "icon": item_icon
        }
for el in data:
   get_item_data(el)

# Zapisz przefiltrowane dane do lokalnego pliku JSON
with open("filtered_items.json", "w", encoding="utf-8") as f:
    json.dump(filtered_items, f, ensure_ascii=False, indent=4)

print("Dane zostały zapisane do 'filtered_items.json'")
    
print('wynik_dlg: ',len(filtered_items))
print(names)