Reverse Fizz Buzz
================

Problem description
-------------------

[Fizz Buzz](http://en.wikipedia.org/wiki/Fizz_buzz) is a simple kids'
game revolving around counting. The basic rules involve counting from
1 to 100, and replacing any multiples of 3 with the word "fizz",
any multiples of 5 with the word "buzz", and any multiples of both
with both words ("fizz buzz").

It is not only useful for teaching kids about division, but is also
used as a litmus test for basic programming skills in job
interviews. What they're usually looking for is some code like this
(C99):

    #include <stdio.h>
    
    int main() {
      int mod3, mod5;
      for (int i=1; i<101; i++) {
        mod3 = i % 3;
        mod5 = i % 5;
        if (!mod3 && !mod5) printf("fizz buzz\n");
        else if (!mod3) printf("fizz\n");
        else if (!mod5) printf("buzz\n");
        else printf("%d\n", i);
      }
    }

Resulting in output like this:

    1
    2
    fizz
    4
    buzz
    fizz
    7
    8
    fizz
    buzz
    11
    fizz
    13
    14
    fizz buzz
    16
    [...]

That's simple, though. Today, let's look at a more interesting
problem: reversing the Fizz Buzz process to find out what the divisors
for a particular "fizz buzz" sequence (in this case, 3 and 5)
were. Better, let's do it from an input that has no numbers; only words.

Input
-----

The input starts by specifying two numbers:

- the number of different words; for example, if we are
using the words "fizz", "buzz" and "qazz", it would be 3
- a number N >= 1

These inputs will be followed by a series of lines containing the Fizz
Buzz words (no numbers) corresponding to playing Fizz Buzz from 1 to N
(which was specified above).

Given the number of words, and the sample "play" of Fizz Buzz, your
program must figure out the divisors corresponding to each word.

Output
------

The output must contain each word used, associated with a divisor that
makes the sequence work.

Sample 1
--------

# Input

    2 20
    fizz
    buzz
    fizz
    fizz
    buzz
    fizz
    fizz buzz
    fizz
    buzz

The intended solution uses "fizz" and "buzz" as words, with 3 and 5 as
the respective divisors. The pattern (ranging 1..20) with the numbers
not excluded would have been: `1, 2, fizz, 4, buzz, fizz, 7, 8, fizz,
buzz, 11, fizz, 13, 14, fizz buzz, 16, 17, fizz, 19, buzz`

# Output

    fizz 3
    buzz 5

The program figured out that "fizz" must correspond to 3, and "buzz"
must correspond to 5.

Sample 2
--------

# Input

    3 30
    red
    red blue
    red
    yellow
    red blue
    red
    red blue
    red yellow
    red blue
    red
    red blue
    yellow
    red
    red blue
    red
    red blue yellow
    red

# Output

    red 2
    blue 4
    yellow 7

Notes
-----

You can find a script for generating inputs for this problem here:

https://github.com/fsufitch/dailyprogrammer/blob/master/ideas/reverse_fizzbuzz/fizzbuzz_inputgen.py