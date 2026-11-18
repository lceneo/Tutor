// Считаем запуски, в которых исходное условие программы не выполняется.
let inputSValues: number[] = [12, 5, -4, 2, 5, 10, 18, 3, 2];
let inputTValues: number[] = [5, 3, 1, -5, -7, 3, 6, 0, 5];
let notOutputCount: number = 0;
for (let pairIndex: number = 0; pairIndex < inputSValues.length; pairIndex++) {
    let yesCondition: boolean = inputSValues[pairIndex] >= 2 && inputTValues[pairIndex] < 5;
    if (!yesCondition) {
        notOutputCount = notOutputCount + 1;
    }
}
console.log(notOutputCount);
