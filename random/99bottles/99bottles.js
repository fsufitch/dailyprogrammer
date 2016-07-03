(function (tw) {
    (function (start, f) { return f(start, f); })(99, (function (i, self) { return i ? [i].concat(self(i - 1, self)) : []; })).map(function (i) {
        console.
            log((function (s) { return s[0].toUpperCase() + s.slice(1); })(('XXX bottleAAA of \
beer on the wall, XXX bottleAAA of beer,\n  Take one down, pass it around, YYY \
bottleBBB of beer on the wall.'.replace(/XXX/g, tw(i)).replace(/AAA/g, i > 1 ? 's' : '')
            .replace(/YYY/g, i > 1 ? tw(i - 1) : 'no more').replace(/BBB/g, i - 1 != 1 ? 's' : ''))));
    });
})(require('number-to-words').toWords);
