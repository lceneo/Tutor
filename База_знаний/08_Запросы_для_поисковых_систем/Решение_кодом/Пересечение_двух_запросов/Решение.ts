// Из суммы размеров запросов вычитаем размер объединения.
let wordAPageCountThousands: number = 60;
let wordBPageCountThousands: number = 140;
let unionPageCountThousands: number = 180;
let intersectionPageCountThousands: number = wordAPageCountThousands + wordBPageCountThousands - unionPageCountThousands;
console.log(intersectionPageCountThousands);
