import { Observable, Observer } from "rxjs/Rx";
import { createInterface } from "readline";

let tty = createInterface(process.stdin, process.stdout);

let inputLines = new Observable<string>(observer => {
  tty.on("line", line => observer.next(line));
  tty.on("close", () => observer.complete());
})
  .filter(line => !!line.trim())
  .map(line => <[string, string]>line.split(/\s/).slice(0, 2))
  .map(([weight, temp]) => ({weight: parseInt(weight), temp: parseInt(temp)}));

let goldilocks = inputLines.first();

let tableId = 0;
let tables = inputLines.skip(1).map(({weight, temp}) => ({weight, temp, id: ++tableId}));

goldilocks.combineLatest(tables)
  .filter(([goldilocks, table]) => goldilocks.weight <= table.weight && goldilocks.temp >= table.temp)
  .map(([goldilocks, table]) => table.id)
  .reduce((output, val) => `${output}${val} `, "")
  .subscribe(console.log);
