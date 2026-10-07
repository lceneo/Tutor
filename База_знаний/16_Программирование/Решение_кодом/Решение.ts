// Читаем количество чисел, затем ищем наибольшее из кратных пяти.
let inputText: string = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (incomingTextChunk: string) => {
    inputText = inputText + incomingTextChunk;
});
process.stdin.on("end", () => {
    let inputValues: string[] = inputText.trim().split(/\s+/);
    let numberCount: number = Number(inputValues[0]);
    let largestMultipleOfFive: number = 0;
    for (let valueIndex: number = 1; valueIndex <= numberCount; valueIndex++) {
        let currentNumber: number = Number(inputValues[valueIndex]);
        // Обновляем максимум только для подходящих чисел.
        if (currentNumber % 5 === 0 && currentNumber > largestMultipleOfFive) {
            largestMultipleOfFive = currentNumber;
        }
    }
    console.log(largestMultipleOfFive);
});
