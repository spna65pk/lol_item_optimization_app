import json

# Ścieżka do pliku tekstowego
txt_file_path = 'dodac parametry.txt'  # Zamień na ścieżkę do swojego pliku
json_file_path = 'dmg_type.json'  # Ścieżka do pliku wynikowego

# Przetwarzanie pliku
data_dict = {}

with open(txt_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        if ':' in line:
            key, value = line.split(':', 1)  # Rozdzielenie po pierwszym ':'
            key = key.strip()
            value = value.strip()
            data_dict[key] = value

# Zapisz do JSON
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data_dict, json_file, indent=4, ensure_ascii=False)

print(f"Dane zostały zapisane do pliku {json_file_path}")
