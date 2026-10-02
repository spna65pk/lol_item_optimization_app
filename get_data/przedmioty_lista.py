import json

# Wczytywanie pliku JSON
with open("filtered_items.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Tworzenie listy kluczy z głównego słownika
item_names = set((data.keys()))

#print(item_names)



# Wczytywanie pliku JSON
with open("champs_suggested_items.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Zbiór do przechowywania unikalnych nazw przedmiotów
unique_items = set()

# Przechodzenie przez postaci i ich przedmioty
for champion, items in data.items():
    for item in items:
        unique_items.add(item["name"])  # Dodawanie nazw przedmiotów do zbioru

# Konwersja zbioru na listę, aby uzyskać ostateczną listę unikalnych wartości
unique_items_list = list(unique_items)

# Wyświetlenie unikalnych nazw przedmiotów
print(unique_items_list)


only_s2 = unique_items - item_names
#print('RÓŻNICA2:',only_s2)
#{'Blade of The Ruined King', 'Hollow Radiance'}
#'Blade of the Ruined King' w bazie danych all items 
#'Hollow 