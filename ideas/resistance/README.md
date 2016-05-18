Vive la resistance!
===================

Description
-----------

It's midnight. You're tired after a night of partying (or gaming, or whatever
else you like to do when procrastinating), and are about ready to go to sleep
when you remember: you have a whole load of homework for your Electronics 101
course. The topic is resistance, and calculating the total resistance of various
circuits.

Someone who is not you might do something sensible, like sighing and getting the
work done, or even going to sleep and letting it go. But you are a *programmer*!
Obviously, the only thing to do here is to write a program to do your homework
for you!

Today's challenge is to write a program that calculates the resistance between
two points in a circuit. For the necessary background maths, check the bottom
of the problem.

Formal Input
------------

The input consists of two parts. First, a line that lists a series of IDs for
circuit "nodes". These are strings of uppercase characters. The first and last
node are to be the start and end point of the circuit.

Next, there will be some number of lines that identify two nodes and specify the resistance between
them (in Ohms, for simplicity). This will be a positive number.

**Sample input:**

    A B C
    A B 10
    A B 20
    B C 30

The above input can be interpreted as the circuit:

         +--(10)--+
         |        |
    [A]--+        +--[B]--(50)--[C]
         |        |
         +--(30)--+

> Note: resistance is bi-directional. `A B 10` means the same thing as `B A 10`.

 Formal Output
 -------------

 The output consists of a single number: the resistance between the first and
 last node, in Ohms. Round to the 3rd decimal place, if necessary.

 **Sample output:**

    57.5

**Explanation:** The theory is explained in the last section of this problem,
but the calculation to achieve `57.5` is:

    1 / (1/10 + 1/30) + 50

Challenge 1
-----------

**Input:**

    A B C D E F
    A C 5
    A B 10
    D A 5
    D E 10
    C E 10
    E F 15
    B F 20

**Output:**

    12.857

Challenge 2
-----------

This is a 20x20 grid of 10,000 Ohm resistors. As the input is too large to paste
here, you can find it here instead: https://github.com/fsufitch/dailyprogrammer/raw/master/ideas/resistance/challenge.txt

Maths Background
----------------

Circuit resistance is calculated in two ways depending on the circuit's
structure. That is, whether the circuit is serial or parallel. Here's what that
means:

**Serial circuit.** This is a circuit in which everything is in a row. There is
no branching. It might look something like this:

    [A]--(x)--[B]--(y)--[C]

In the case of a serial circuit, resistances are simply added. Since resistance
measures the "effort" electricity has to overcome to get from one place to
another, it makes sense that successive obstacles would sum up their difficulty.
In the above example, the resistance between A and C would simply be `x + y`.

**Parallel circuit.** This is an instance where there are multiple paths from
one node to the next. We only need two nodes to demonstrate this, so let's show
a case with three routes:

         +--(x)--+
         |       |
    [A]--+--(y)--+--[B]
         |       |
         +--(z)--+

When there are multiple routes for electricity to take, the overall resistance
goes down. However, it does so in a funny way: the total resistance is the
inverse of the sum of the inverses of the involved resistances. Stated
differently, you must take all the component resistances, invert them (divide 1
by them), add them, then invert that sum. That means the resistance for the
above example is:

    1 / (1/x + 1/y + 1/z)

**Putting them together.**

When solving a more complex circuit, you can use the two calculations from above
to simplify the circuit in steps. Take the circuit in the sample input:

         +--(10)--+
         |        |
    [A]--+        +--[B]--(50)--[C]
         |        |
         +--(30)--+

There is a parallel circuit between A and B, which means we can apply the second
calculation. `1 / (1/10 + 1/30) = 7.5`, so we simplify the problem to:

    [A]--(7.5)--[B]--(50)--[C]

This is now a serial circuit, which means we can simplify it with the first
rule. `7.5 + 50 = 57.5`, so:

    [A]--(57.5)--[C]

This leaves us with 57.5 as the answer to the problem.

Finally...
----------

Have your own ~~boring homework~~ fascinating challenge to suggest? Drop by
/r/dailyprogrammer_ideas and post it!
