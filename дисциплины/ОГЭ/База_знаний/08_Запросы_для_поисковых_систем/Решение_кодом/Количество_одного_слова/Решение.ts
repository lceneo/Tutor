// Восстанавливаем размер второго запроса из объединения и пересечения.
let unionPageCountThousands: number = 780;
let knownWordPageCountThousands: number = 260;
let sharedPageCountThousands: number = 50;
let otherWordPageCountThousands: number = unionPageCountThousands - knownWordPageCountThousands + sharedPageCountThousands;
console.log(otherWordPageCountThousands);
