# Для каждого города храним число путей, ведущих туда из начального города.
outgoing_roads_by_city = {
    "А": ["Б", "В", "Д", "Г"],
    "Б": ["В", "Е"],
    "В": ["Е", "З"],
    "Г": ["З"],
    "Д": ["Г", "Ж"],
    "Е": ["З", "И", "Л"],
    "Ж": ["З", "К", "Л"],
    "З": ["Л"],
    "И": ["Л"],
    "К": ["Л"],
    "Л": []
}
city_processing_order = ["А", "Б", "В", "Д", "Г", "Е", "Ж", "З", "И", "К", "Л"]
path_count_by_city = {"А": 1}

# Каждому городу передаём число путей через все его исходящие дороги.
for current_city in city_processing_order:
    if current_city not in path_count_by_city:
        path_count_by_city[current_city] = 0
    for next_city in outgoing_roads_by_city[current_city]:
        if next_city not in path_count_by_city:
            path_count_by_city[next_city] = 0
        path_count_by_city[next_city] = path_count_by_city[next_city] + path_count_by_city[current_city]

print(path_count_by_city["Л"])
