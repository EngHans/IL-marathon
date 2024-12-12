import fs from "fs";
import config from "@mercadoni/elementals/config";

const inputFile = config.get("input")
const outputFile = config.get("output")

const delay = (ms: number) => {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
  console.log({ inputFile, outputFile })
  while (true) {
    const delta = 5;
    const input = fs.readFileSync(inputFile, { encoding: "utf-8" })
    const [px, py, e, bx, by] = input.split(",").map(s => { return s.trim() });
    console.log({ px, py, e, bx, by })
    if (Number(e) < 20) {
      console.log(Number(e) < 20)
      fs.writeFileSync(outputFile, "0", { "encoding": "utf-8" })
    } else {
      let direction = 0;
      if (Number(py) - delta > Number(by)) {
        direction = -1
      }
      if (Number(py) + delta < Number(by)) {
        direction = 1
      }
      console.log({direction})
      fs.writeFileSync(outputFile, `${direction}`, { "encoding": "utf-8" })
    }
    await delay(50)
  }
})();
