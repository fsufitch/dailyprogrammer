/// <reference path="./typings/index.d.ts" />

((tw:(num:number)=>string)=>{((start:number,f:(i:number,s:any)=>number[]):
number[]=>{return f(start,f)})(99,((i:number,self:(i:number,s:any)=>number[]):
number[]=>{return i?[i].concat(self(i-1,self)):[]})).map((i:number)=>{console.
log(((s:string)=>{return s[0].toUpperCase()+s.slice(1);})(('XXX bottleAAA of \
beer on the wall, XXX bottleAAA of beer,\n  Take one down, pass it around, YYY \
bottleBBB of beer on the wall.'.replace(/XXX/g,tw(i)).replace(/AAA/g,i>1?'s':'')
.replace(/YYY/g,i>1?tw(i-1):'no more').replace(/BBB/g,i-1!=1?'s':''))));})})(
require('number-to-words').toWords);
