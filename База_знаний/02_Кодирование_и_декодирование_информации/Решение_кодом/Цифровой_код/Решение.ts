// Перебираем все варианты разбиения каждого сообщения на коды разной длины.
let binaryCodes: string[] = ["01", "011", "100", "111", "010", "001"];
let decodedLetters: string[] = ["А", "В", "Д", "О", "Р", "У"];

function decodeFrom(encodedMessage: string, currentPosition: number): string[] {
    // Конец строки означает, что найдено полное разбиение.
    if (currentPosition === encodedMessage.length) {
        return [""];
    }

    let possibleDecodings: string[] = [];
    for (let codeIndex: number = 0; codeIndex < binaryCodes.length; codeIndex++) {
        let codeFragment: string = binaryCodes[codeIndex];
        if (encodedMessage.substring(currentPosition, currentPosition + codeFragment.length) === codeFragment) {
            let remainingDecodings: string[] = decodeFrom(encodedMessage, currentPosition + codeFragment.length);
            for (let decodingIndex: number = 0; decodingIndex < remainingDecodings.length; decodingIndex++) {
                possibleDecodings[possibleDecodings.length] = decodedLetters[codeIndex] + remainingDecodings[decodingIndex];
            }
        }
    }
    return possibleDecodings;
}

let encodedMessages: string[] = ["01001001", "11101001", "10001010"];
for (let messageIndex: number = 0; messageIndex < encodedMessages.length; messageIndex++) {
    let possibleDecodings: string[] = decodeFrom(encodedMessages[messageIndex], 0);
    console.log(encodedMessages[messageIndex], possibleDecodings);
    console.log("Число разбиений:", possibleDecodings.length);
}
