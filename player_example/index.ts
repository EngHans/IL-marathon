import fs from "fs";
import config from "@mercadoni/elementals/config";

const inputFile = config.get("input")
const outputFile = config.get("output")
let player = 0;

type input = {
  px: number,
  py: number,
  e: number,
  bx: number,
  by: number
}

let previousInput: input = {
  px: -1,
  py: -1,
  e: -1,
  bx: -1,
  by: -1
};

const delay = (ms: number) => {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const getPlayer = (px: number): number => {
  if(px > 450)
    return 2;
  return 1;
}

const getPlayerTheBallIsGoingTo = (previousX: number, currentX: number) => {
  if(previousX > currentX)
    return 1;
  return 2;
}

const directToDesiredY = (desiredY: number, currentPlayerY: number) => {
  const delta = 20;
  if(currentPlayerY < desiredY + delta && currentPlayerY > desiredY - delta){
    return 0
  }
  else if(currentPlayerY < desiredY){
    return 1
  }
  else
    return -1
}

const calculateYCollision = (currentInput: input, previousInput: input): number => {
  const ballDeltaX = currentInput.bx - previousInput.bx;
  const ballDeltaY = currentInput.by - previousInput.by;
  let expectedPreliminarCollision: number = -1;
  let remainingX: number = -1;
  
  const limit : number = ballDeltaX < 0 ? 55 : 845;

  remainingX = limit - currentInput.bx;
  const stepsForCollision = Math.round(remainingX/ballDeltaX);
  expectedPreliminarCollision = currentInput.by + (stepsForCollision * ballDeltaY);
  console.log({expectedPreliminarCollision})
  if(expectedPreliminarCollision > 600){
    expectedPreliminarCollision = 1200 - expectedPreliminarCollision;
  } else if (expectedPreliminarCollision < 0){
    expectedPreliminarCollision = -expectedPreliminarCollision;
  }
  
  return expectedPreliminarCollision;
}

const tickLogic = (currentInput: input, previousInput: input ) => {
  const delta = 5;
  let direction = 0;

  const ballDirectedTo = getPlayerTheBallIsGoingTo(previousInput.bx, currentInput.bx);
  
  if(ballDirectedTo === player){
    const expectedCollision = calculateYCollision(currentInput, previousInput);
    console.log({expectedCollision})
    direction = directToDesiredY(expectedCollision, currentInput.py);
/*    if (Number(currentInput.py) - delta > Number(currentInput.by)) {
      direction = -1
    }
    if (Number(currentInput.py) + delta < Number(currentInput.by)) {
      direction = 1
    }
*/
  } else {
    direction = directToDesiredY(300, currentInput.py);
  }

//  console.log({direction, ballDirectedTo})
//  console.log(outputFile)
  fs.writeFileSync(outputFile, `${direction}`, { "encoding": "utf-8" })
}

(async () => {
//  console.log({ inputFile, outputFile })
  while (true) {
    const input = fs.readFileSync(inputFile, { encoding: "utf-8" })
    const [px, py, e, bx, by] = input.split(",").map(s => { return Number(s.trim()) });
    if(player === 0)
      player = getPlayer(px);
//    console.log({ px, py, e, bx, by, player })
    if (previousInput.px < 0 || Number(e) < 20) {
      console.log(Number(e) < 20)
      fs.writeFileSync(outputFile, "0", { "encoding": "utf-8" })
    } else {
      tickLogic({px, py, e, bx, by}, previousInput);
    }
    await delay(50)
    previousInput = {px, py, e, bx, by};
  }
})();
