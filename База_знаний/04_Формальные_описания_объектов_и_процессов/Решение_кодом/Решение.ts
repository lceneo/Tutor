// Граф хранится как список смежности: у каждого пункта перечислены соседи и длины дорог.
// Дороги двусторонние, поэтому каждый участок записан в списках обоих концов.
type Road = { to: string; distance: number };
type Graph = Record<string, Road[]>;
type RouteResult = { cities: string[]; distance: number };

/**
 * Полным перебором DFS ищет кратчайший маршрут без повторного посещения пунктов.
 * `currentCities` хранит путь текущего рекурсивного вызова и не даёт повторно
 * заходить в уже посещённые пункты.
 * Если задан `requiredCity`, учитываются только завершённые маршруты, которые
 * прошли через этот обязательный промежуточный пункт.
 */
function findShortestRoute(
  graph: Graph,
  start: string,
  finish: string,
  requiredCity?: string,
): RouteResult | null {
  let bestDistance = Infinity;
  let bestCities: string[] | null = null;
  const currentCities = [start];

  function visit(current: string, distance: number): void {
    // В финише проверяем условие об обязательном пункте и обновляем лучший ответ.
    if (current === finish) {
      const visitsRequiredCity =
        requiredCity === undefined || currentCities.includes(requiredCity);

      if (visitsRequiredCity && distance < bestDistance) {
        bestDistance = distance;
        bestCities = [...currentCities];
      }
      return;
    }

    // Пробуем все дороги из текущего пункта, кроме ведущих в уже посещённые пункты.
    for (const road of graph[current] ?? []) {
      if (currentCities.includes(road.to)) continue;

      // Углубляемся по выбранной дороге, прибавляя её длину к маршруту.
      currentCities.push(road.to);
      visit(road.to, distance + road.distance);

      // Возвращаемся к предыдущему пункту и пробуем следующую дорогу.
      currentCities.pop();
    }
  }

  visit(start, 0);
  return bestCities === null ? null : { cities: bestCities, distance: bestDistance };
}

// РешуОГЭ, тип 4 № 3: кратчайший путь A → E равен A—B—C—E, 6 км.
const graphProblem3: Graph = {
  A: [{ to: "B", distance: 1 }],
  B: [
    { to: "A", distance: 1 },
    { to: "C", distance: 2 },
    { to: "D", distance: 2 },
    { to: "E", distance: 7 },
  ],
  C: [
    { to: "B", distance: 2 },
    { to: "E", distance: 3 },
  ],
  D: [
    { to: "B", distance: 2 },
    { to: "E", distance: 4 },
  ],
  E: [
    { to: "B", distance: 7 },
    { to: "C", distance: 3 },
    { to: "D", distance: 4 },
  ],
};

// Аналог № 63: кратчайший путь A → E равен A—B—D—E, 7 км.
const graphProblem63: Graph = {
  A: [{ to: "B", distance: 1 }],
  B: [
    { to: "A", distance: 1 },
    { to: "C", distance: 4 },
    { to: "D", distance: 2 },
    { to: "E", distance: 8 },
  ],
  C: [
    { to: "B", distance: 4 },
    { to: "E", distance: 4 },
  ],
  D: [
    { to: "B", distance: 2 },
    { to: "E", distance: 4 },
  ],
  E: [
    { to: "B", distance: 8 },
    { to: "C", distance: 4 },
    { to: "D", distance: 4 },
  ],
};

// РешуОГЭ № 43351: кратчайший путь A → E через C равен A—B—C—D—E, 8 км.
const graphProblem43351: Graph = {
  A: [
    { to: "B", distance: 1 },
    { to: "C", distance: 4 },
    { to: "D", distance: 3 },
    { to: "E", distance: 7 },
  ],
  B: [
    { to: "A", distance: 1 },
    { to: "C", distance: 2 },
    { to: "D", distance: 5 },
  ],
  C: [
    { to: "A", distance: 4 },
    { to: "B", distance: 2 },
    { to: "D", distance: 3 },
  ],
  D: [
    { to: "A", distance: 3 },
    { to: "B", distance: 5 },
    { to: "C", distance: 3 },
    { to: "E", distance: 2 },
  ],
  E: [
    { to: "A", distance: 7 },
    { to: "D", distance: 2 },
  ],
};

console.log(findShortestRoute(graphProblem3, "A", "E"));
console.log(findShortestRoute(graphProblem63, "A", "E"));
console.log(findShortestRoute(graphProblem43351, "A", "E", "C"));
