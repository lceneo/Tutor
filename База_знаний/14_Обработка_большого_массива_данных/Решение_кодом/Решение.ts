// Ввод: число строк, затем для каждой записи четыре значения через пробел:
// округ, фамилия, предмет, балл. Значения не должны содержать пробелов.
let inputText: string = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (incomingTextChunk: string) => {
    inputText = inputText + incomingTextChunk;
});
process.stdin.on("end", () => {
    let inputFields: string[] = inputText.trim().split(/\s+/);
    let recordCount: number = Number(inputFields[0]);
    let nextFieldIndex: number = 1;
    let informaticsExamCount: number = 0;
    let informaticsScoreSum: number = 0;
    let informaticsScoreOver600Count: number = 0;
    let districtVParticipantCount: number = 0;
    let districtZelParticipantCount: number = 0;
    let districtZParticipantCount: number = 0;

    for (let recordIndex: number = 0; recordIndex < recordCount; recordIndex++) {
        let districtCode: string = inputFields[nextFieldIndex];
        let studentSurname: string = inputFields[nextFieldIndex + 1];
        let examSubject: string = inputFields[nextFieldIndex + 2];
        let examScore: number = Number(inputFields[nextFieldIndex + 3]);
        nextFieldIndex = nextFieldIndex + 4;

        // Для информатики считаем количество, сумму и результаты выше 600.
        if (examSubject === "информатика") {
            informaticsExamCount = informaticsExamCount + 1;
            informaticsScoreSum = informaticsScoreSum + examScore;
            if (examScore > 600) {
                informaticsScoreOver600Count = informaticsScoreOver600Count + 1;
            }
        }

        // Отдельно считаем участников трёх округов для диаграммы.
        if (districtCode === "В") {
            districtVParticipantCount = districtVParticipantCount + 1;
        }
        if (districtCode === "Зел") {
            districtZelParticipantCount = districtZelParticipantCount + 1;
        }
        if (districtCode === "З") {
            districtZParticipantCount = districtZParticipantCount + 1;
        }
    }

    console.log("Информатика, больше 600:", informaticsScoreOver600Count);
    if (informaticsExamCount > 0) {
        let averageInformaticsScore: number = informaticsScoreSum / informaticsExamCount;
        console.log("Средний балл по информатике:", averageInformaticsScore);
    }
    console.log("Участники по округам В, Зел, З:", districtVParticipantCount, districtZelParticipantCount, districtZParticipantCount);
});
