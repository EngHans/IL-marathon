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

const tickLogic = (currentInput: input, previousInput: input ) => {
  const delta = 5;
  let direction = 0;

  const ballDirectedTo = getPlayerTheBallIsGoingTo(previousInput.bx, currentInput.bx);
  
  if (Number(currentInput.py) - delta > Number(currentInput.by)) {
    direction = -1
  }
  if (Number(currentInput.py) + delta < Number(currentInput.by)) {
    direction = 1
  }
  console.log({direction, ballDirectedTo})
  console.log(outputFile)
  fs.writeFileSync(outputFile, `${direction}`, { "encoding": "utf-8" })
}

(async () => {
  console.log({ inputFile, outputFile })
  while (true) {
    const input = fs.readFileSync(inputFile, { encoding: "utf-8" })
    const [px, py, e, bx, by] = input.split(",").map(s => { return s.trim() });
    if(player === 0)
      player = getPlayer(px);
    console.log({ px, py, e, bx, by, player })
    if (previousInput[0] < 0 || Number(e) < 20) {
      console.log(Number(e) < 20)
      fs.writeFileSync(outputFile, "0", { "encoding": "utf-8" })
    } else {
      tickLogic({px, py, e, bx, by}, previousInput);
    }
    await delay(50)
    previousInput = {px, py, e, bx, by};
  }
})();
