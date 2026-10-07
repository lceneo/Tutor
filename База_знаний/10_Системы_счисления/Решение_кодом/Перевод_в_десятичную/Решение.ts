// Переводим двоичное число в десятичное разряд за разрядом.
let binaryNumberText: string = "1100110";
let decimalValue: number = 0;
for (let digitIndex: number = 0; digitIndex < binaryNumberText.length; digitIndex++) {
    let binaryDigit: number = Number(binaryNumberText[digitIndex]);
    decimalValue = decimalValue * 2 + binaryDigit;
}
console.log(decimalValue);
