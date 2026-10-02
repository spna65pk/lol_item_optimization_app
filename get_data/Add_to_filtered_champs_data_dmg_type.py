import json

i = 0
# Ścieżki do plików JSON
first_file_path = "dmg_type.json"  # Plik z wartościami typu
second_file_path = "filtered_champions_data.json"  # Plik z danymi postaci
output_file_path = "updated_file2.json"  # Plik wynikowy

# Wczytanie plików JSON
with open(first_file_path, "r", encoding="utf-8") as file1:
    type_data = json.load(file1)

with open(second_file_path, "r", encoding="utf-8") as file2:
    champions_data = json.load(file2)

# Dodawanie parametru "type" do każdego bohatera
for champion_name, champion_info in champions_data.items():
    if champion_name in type_data:
        champion_info["attributes"]["type"] = type_data[champion_name]
        i += 1
    else:
         print(champion_name)

# Zapisanie zaktualizowanych danych do pliku wynikowego
with open(output_file_path, "w", encoding="utf-8") as output_file:
    json.dump(champions_data, output_file, indent=4, ensure_ascii=False)

print(f"Zaktualizowane dane zostały zapisane do pliku {output_file_path}")
print(i)