// Из объединения двух пересечений находим общее пересечение всех трёх.
let mathAndInformaticsPageCountThousands: number = 330;
let mathAndPhysicsPageCountThousands: number = 270;
let mathAndInformaticsOrPhysicsPageCountThousands: number = 520;
let allThreePageCountThousands: number = mathAndInformaticsPageCountThousands + mathAndPhysicsPageCountThousands - mathAndInformaticsOrPhysicsPageCountThousands;
console.log(allThreePageCountThousands);
