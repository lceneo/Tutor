// Перебираем целые A и считаем, сколько раз программа выдаёт YES.
let inputSValues: number[] = [13, 11, -12, 2, -10, 6, 2, 9, 1];
let inputTValues: number[] = [2, 12, 12, -2, -10, -5, 8, 10, 13];
let matchingParameterCount: number = 0;

// Все границы изменения результата лежат между -13 и 14.
for (let parameterA: number = -20; parameterA <= 20; parameterA++) {
    let yesOutputCount: number = 0;
    for (let pairIndex: number = 0; pairIndex < inputSValues.length; pairIndex++) {
        if (inputSValues[pairIndex] > parameterA || inputTValues[pairIndex] > 12) {
            yesOutputCount = yesOutputCount + 1;
        }
    }
    if (yesOutputCount === 5) {
        matchingParameterCount = matchingParameterCount + 1;
        console.log("Подходит A:", parameterA);
    }
}

console.log("Число значений A:", matchingParameterCount);
