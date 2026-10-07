// Переводим 100 в двоичную систему и считаем остатки, равные единице.
let decimalValue: number = 100;
let binaryOneCount: number = 0;
while (decimalValue > 0) {
    let binaryRemainder: number = decimalValue % 2;
    if (binaryRemainder === 1) {
        binaryOneCount = binaryOneCount + 1;
    }
    decimalValue = Math.floor(decimalValue / 2);
}
console.log(binaryOneCount);
