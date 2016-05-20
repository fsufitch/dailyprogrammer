IDDQD
=====

Description
-----------

You are trapped in a room full of evil zombies. Some people might resign
themselves to their doom in this situation, but not you. You're a badass space
marine! No, not the kind with the [big armor](http://vignette1.wikia.nocookie.net/warhammer40k/images/1/13/Ultramarines_Artificer_Armour2.jpg);
the kind with a [BFG-9000](http://vignette2.wikia.nocookie.net/doom/images/d/d6/BFG9000-HellRevealed-map04.png).

Unfortunately though, this Big F'in Gun only has one shot remaining, so you have
to make it count. The BFG will blow away anything it hits, of course, but it
will also destroy anything it grazes. The zombies in the room are slow, so you
have ample time to position yourself for the perfect shot. How many zombies can
you take out at once?

For the sake of simplicity, the room is represented by a flat 2D grid. The BFG
can be fired from any empty spot in any direction along a row, column, or
diagonal of the grid. Any zombie that it meets in its path gets destroyed, and stops
the BFG beam. Additionally, any zombie that is adjacent (horizontally, vertically
or diagonally) to the beam is also destroyed.

Formal input
------------

The first line of input will be two numbers denoting the size (height, width) of the
two-dimensional room. The remaining lines will contain the coordinates at which
there is a zombie. These coordinates are zero-indexed.

**Sample input:**

    6 10
    2 4
    4 6
    5 5
    0 0
    0 6

This corresponds to the following map:

    X.....X...
    ..........
    ....X.....
    ..........
    ......X...
    .....X....

Formal output
-------------

The output is a single number: the maximum number of zombies you can blast with
one single shot of the BFG.

**Sample output:**

    4

Because there are many possible ways to achieve the maximum, an actual output of
what the shot *is* is not necessary. You might want to do it for debug purposes,
but in big rooms it is fairly meaningless.

**Sample explanation:** One way to achieve the 4-zombie blast is:

    X....#X...
    .....#....
    ....X#....
    .....#....
    .....#X...
    .....X....

Another one is:

    X#....X...
    ..#.......
    ...#X.....
    ....#.....
    .....#X...
    .....X#...

As might be evident, "your" position doesn't matter. All that matters is the
line that the BFG beam draws, and the things adjacent to it.

Challenge input
---------------

    20 20
    11 16
    5 19
    12 5
    8 9
    0 10
    17 16
    14 9
    10 8
    19 7
    17 11
    6 10
    0 4
    10 9
    11 13
    19 6
    17 10
    8 11
    6 0
    18 17
    2 10
    12 11
    4 2
    1 0
    2 17
    10 5
    8 3
    13 14
    10 14
    4 3
    5 2

Bonus points
------------

Modify the challenge to feature walls or other non-zombie obstacles.

Finally...
----------

Have your own challenge idea that is totally not a reference to a recently
released video game? Come by /r/dailyprogrammer_ideas and share it!
