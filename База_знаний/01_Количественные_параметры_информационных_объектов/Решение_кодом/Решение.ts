// Размер уменьшения в байтах и число бит на один символ.
let sizeReductionBytes: number = 8;
let bitsPerSymbol: number = 8;

// Находим число удалённых символов, затем убираем запятую и пробел.
let bytesPerSymbol: number = bitsPerSymbol / 8;
let targetNameLength: number = sizeReductionBytes / bytesPerSymbol - 2;

// Ищем название нужной длины среди вариантов из условия.
let candidateNames: string[] = ["Обь", "Лена", "Волга", "Москва", "Макензи", "Амазонка"];
for (let nameIndex: number = 0; nameIndex < candidateNames.length; nameIndex++) {
    if (candidateNames[nameIndex].length === targetNameLength) {
        console.log(candidateNames[nameIndex]);
    }
}
