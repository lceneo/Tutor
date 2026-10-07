// Считаем двузначные числа, которые нечётные и не кратны пяти.
let matchingNumberCount: number = 0;
for (let candidateNumber: number = 10; candidateNumber < 100; candidateNumber++) {
    let isOdd: boolean = candidateNumber % 2 !== 0;
    let isNotMultipleOfFive: boolean = candidateNumber % 5 !== 0;
    if (isOdd && isNotMultipleOfFive) {
        matchingNumberCount = matchingNumberCount + 1;
    }
}
console.log(matchingNumberCount);
