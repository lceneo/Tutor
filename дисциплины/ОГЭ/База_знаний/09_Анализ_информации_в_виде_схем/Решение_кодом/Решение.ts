// Для каждого города храним число путей, ведущих туда из начального города.
let cityNames: string[] = ["А", "Б", "В", "Д", "Г", "Е", "Ж", "З", "И", "К", "Л"];
let outgoingRoadsByCity: string[][] = [
    ["Б", "В", "Д", "Г"], ["В", "Е"], ["Е", "З"], ["З"], ["Г", "Ж"],
    ["З", "И", "Л"], ["З", "К", "Л"], ["Л"], ["Л"], ["Л"], []
];
let pathCountByCity: number[] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

// Каждому городу передаём число путей через все его исходящие дороги.
for (let cityIndex: number = 0; cityIndex < cityNames.length; cityIndex++) {
    for (let roadIndex: number = 0; roadIndex < outgoingRoadsByCity[cityIndex].length; roadIndex++) {
        let nextCityName: string = outgoingRoadsByCity[cityIndex][roadIndex];
        for (let nextCityIndex: number = 0; nextCityIndex < cityNames.length; nextCityIndex++) {
            if (cityNames[nextCityIndex] === nextCityName) {
                pathCountByCity[nextCityIndex] = pathCountByCity[nextCityIndex] + pathCountByCity[cityIndex];
            }
        }
    }
}

let destinationCityIndex: number = 0;
for (let cityIndex: number = 0; cityIndex < cityNames.length; cityIndex++) {
    if (cityNames[cityIndex] === "Л") {
        destinationCityIndex = cityIndex;
    }
}
console.log(pathCountByCity[destinationCityIndex]);
