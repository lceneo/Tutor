const encodedMessage: string = "#~#~#++~#";

const codeToLetter: Record<string, string> = {
    "+#": "А",
    "#+": "Е",
    "~": "Л",
    "#": "П",
    "+~#": "Т",
    "~#": "О"
};

interface DecodeState {
    pointer: number;
    decodedText: string;
    usedLetters: Set<string>;
}

const stack: DecodeState[] = [
    { pointer: 0, decodedText: "", usedLetters: new Set() }
];

let finalResult: string = "";

while (stack.length > 0) {
    const currentState = stack.pop()!;
    const { pointer, decodedText, usedLetters } = currentState;

    if (pointer === encodedMessage.length) {
        finalResult = decodedText;
        break;
    }

    for (const [code, letter] of Object.entries(codeToLetter)) {
        if (!usedLetters.has(letter) && encodedMessage.startsWith(code, pointer)) {
            const nextUsed = new Set(usedLetters);
            nextUsed.add(letter);

            stack.push({
                pointer: pointer + code.length,
                decodedText: decodedText + letter,
                usedLetters: nextUsed
            });
        }
    }
}

console.log(finalResult); // ПОЛЕТ
