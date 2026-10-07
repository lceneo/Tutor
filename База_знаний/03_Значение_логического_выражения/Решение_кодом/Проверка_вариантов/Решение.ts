// Проверяем каждый вариант: ложь от ИЛИ получается, когда обе части ложны.
let cityNames: string[] = ["Москва", "Омск", "Дубна", "Новокузнецк"];
let vowelLetters: string = "аеёиоуыэюя";
for (let cityIndex: number = 0; cityIndex < cityNames.length; cityIndex++) {
    let cityName: string = cityNames[cityIndex];
    let hasEvenLetterCount: boolean = cityName.length % 2 === 0;
    let lastLetter: string = cityName[cityName.length - 1].toLowerCase();
    let endsWithVowel: boolean = false;
    for (let vowelIndex: number = 0; vowelIndex < vowelLetters.length; vowelIndex++) {
        if (lastLetter === vowelLetters[vowelIndex]) {
            endsWithVowel = true;
        }
    }
    let expressionIsTrue: boolean = hasEvenLetterCount || endsWithVowel;
    if (!expressionIsTrue) {
        console.log(cityIndex + 1, cityName);
    }
}
