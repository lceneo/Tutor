// Разделяем строку на коды из разбора и заменяем каждый код буквой.
let codeSegments: string[] = ["#", "~#", "~", "#+", "+~#"];
let symbolCodes: string[] = ["+#", "#+", "~", "#", "+~#", "~#"];
let decodedLetters: string[] = ["А", "Е", "Л", "П", "Т", "О"];
let decodedMessage: string = "";

for (let segmentIndex: number = 0; segmentIndex < codeSegments.length; segmentIndex++) {
    for (let symbolIndex: number = 0; symbolIndex < symbolCodes.length; symbolIndex++) {
        if (codeSegments[segmentIndex] === symbolCodes[symbolIndex]) {
            decodedMessage = decodedMessage + decodedLetters[symbolIndex];
        }
    }
}
console.log(decodedMessage);
