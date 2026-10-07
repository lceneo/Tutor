// Считаем суммы цифр в восьмеричных записях и выбираем наименьшую.
let decimalNumbers: number[] = [55, 83, 91];
let octalBase: number = 8;
let smallestOctalDigitSum: number = 1000;
for (let numberIndex: number = 0; numberIndex < decimalNumbers.length; numberIndex++) {
    let remainingValue: number = decimalNumbers[numberIndex];
    let octalDigitSum: number = 0;
    while (remainingValue > 0) {
        let octalDigit: number = remainingValue % octalBase;
        octalDigitSum = octalDigitSum + octalDigit;
        remainingValue = Math.floor(remainingValue / octalBase);
    }
    console.log(decimalNumbers[numberIndex], "сумма цифр:", octalDigitSum);
    if (octalDigitSum < smallestOctalDigitSum) {
        smallestOctalDigitSum = octalDigitSum;
    }
}
console.log("Наименьшая сумма:", smallestOctalDigitSum);
