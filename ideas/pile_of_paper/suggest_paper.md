This problem is inspired by an old [USACO](http://usaco.org) problem
that had me thinking for a while. A good solution relied on efficient
algorithm choice and data structure choice, due to the large bounds of
the data. Good luck!

----------------

# Problem statement

Have you ever layered colored sticky notes in interesting patterns in
order to make pictures? You can create surprisingly complex pictures
you can make out of square/rectangular pieces of paper. An interesting
question about these pictures, though, is: what area of each color is
actually showing? We will simulate this situation and answer that
question.

Start with a sheet of the base color 0 (colors are represented by
single integers) of some specified size. Let's suppose we have a sheet
of size 20x10, of color 0. This will serve as our "canvas", and first
input:

    20 10

We then place other colored sheets on top of it by specifying their
color (as an integer), the (x, y) coordinates of their top left
corner, and their width/height measurements. For simplicity's sake,
all sheets are oriented in the same orthogonal manner (none of them
are tilted). Some example input:

    1 5 5 10 3
    2 0 0 7 7 

This is interpreted as:

- Sheet of color `1` with top left corner at `(5, 5)`, with a width of `10` and height of `3`.
- Sheet of color `2` with top left corner at `(0,0)`, with a width of
  `7` and height of `7`.

Note that multiple sheets *may* have the same color. Color is not
unique per sheet.

Placing the first sheet would result in a canvas that looks like this:

    00000000000000000000
    00000000000000000000
    00000000000000000000
    00000000000000000000
    00000000000000000000
    00000111111111100000
    00000111111111100000
    00000111111111100000
    00000000000000000000
    00000000000000000000

Layering the second one on top would look like this:

    22222220000000000000
    22222220000000000000
    22222220000000000000
    22222220000000000000
    22222220000000000000
    22222221111111100000
    22222221111111100000
    00000111111111100000
    00000000000000000000
    00000000000000000000

This is the end of the input. The output should answer a single
question: *What area of each color is visible after all the sheets
have been layered, in order?* It should be formatted as an
one-per-line list of colors mapped to their visible areas. In our
example, this would be:

    0 125
    1 26
    2 49

-------------------

# Sample Input:

    20 10
    1 5 5 10 3
    2 0 0 7 7

# Sample Output:

    0 125
    1 26
    2 49

--------------------

# Bonus points

Fulfill any (or all) of the following restrictions for bonus points:

- Your code must work for canvases up to 10,000,000 x 10,000,000 in
  size.
- Your code must work for up to 10,000 input sheets.
- Your code must run in a maximum of 3 seconds.
- Your code may not use over 100 MB of memory.