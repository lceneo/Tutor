function findFirst(
    start: number,
    stop: number,
    step: number,
    condition: (value: number) => boolean,
): number | undefined {
    for (let value: number = start; step > 0 ? value < stop : value > stop; value += step) {
        if (condition(value)) {
            return value;
        }
    }
    return undefined;
}

const largest = findFirst(100, -101, -1, (x) => !(x <= 15) && x < 20);
const smallest = findFirst(-100, 101, 1, (x) => !(x < 2) && x < 5);
const anyValue = findFirst(-100, 101, 1, (x) => x < 8 && !(x < 7));

console.log("Наибольшее: ", largest);
console.log("Наименьшее: ", smallest);
console.log("Подходящее число: ", anyValue);
