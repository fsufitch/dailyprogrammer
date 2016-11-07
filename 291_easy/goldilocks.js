"use strict";
var Rx_1 = require("rxjs/Rx");
var readline_1 = require("readline");
var tty = readline_1.createInterface(process.stdin, process.stdout);
var inputLines = new Rx_1.Observable(function (observer) {
    tty.on("line", function (line) { return observer.next(line); });
    tty.on("close", function () { return observer.complete(); });
})
    .filter(function (line) { return !!line.trim(); })
    .map(function (line) { return line.split(/\s/).slice(0, 2); })
    .map(function (_a) {
    var weight = _a[0], temp = _a[1];
    return ({ weight: parseInt(weight), temp: parseInt(temp) });
});
var goldilocks = inputLines.first();
var tableId = 0;
var tables = inputLines.skip(1).map(function (_a) {
    var weight = _a.weight, temp = _a.temp;
    return ({ weight: weight, temp: temp, id: ++tableId });
});
goldilocks.combineLatest(tables)
    .filter(function (_a) {
    var goldilocks = _a[0], table = _a[1];
    return goldilocks.weight <= table.weight && goldilocks.temp >= table.temp;
})
    .map(function (_a) {
    var goldilocks = _a[0], table = _a[1];
    return table.id;
})
    .reduce(function (output, val) { return "" + output + val + " "; }, "")
    .subscribe(console.log);
