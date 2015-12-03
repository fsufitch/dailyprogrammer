Guess Who(is)?
==============

Wally, a weird friend of yours, has done something mildly
creepy. Using some questionable sources, he has compiled a huge list
of IP address ranges associated with various names (be it the owner of
the IP block, known users, or other things). He has put this data in
one giant text file, but now he's stumped. How is he supposed to look
something up in there?

Help Wally out by writing a lookup system for these IP address ranges.

Formal Input
============

The input comes in two pieces. The first is a text file containing
Wally's IP ranges. These come as one entry per line, with two
space-separated IPs and a name.

The second file is just a list of IPs, one per line, that Wally wants
to look up.

Sample Input IPs
----------------

For the sake of making the problem less creepy, the names we're using
are just random hexadecimal strings. 

	37.19.108.135 41.179.245.88 e5098
	42.177.160.247 56.169.207.111 e5099
	10.79.166.252 61.23.100.14 e509a
	36.215.168.168 36.215.168.217 438ec
	36.215.168.210 36.215.168.212 438ed
	43.244.29.118 48.95.64.225 438ee
	104.26.149.0 104.26.193.186 438ef
	104.26.138.247 104.26.154.8 438f0
	104.26.143.36 104.26.143.42 438f1
	104.26.130.46 104.26.131.61 438f2
	23.211.24.120 23.211.27.247 42582
	23.210.82.244 23.210.124.203 42583
	20.51.111.15 23.123.215.144 42584
	23.162.8.121 23.236.22.68 42585
	23.211.40.182 23.211.47.70 42586

Note that these IP ranges are **not guaranteed to be IPv4
networks**. This means that they may not be accurately represented by
prefix-based
[CIDR blocks](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_blocks). They
may (and probably do) overlap.

Sample Input Lookups
--------------------

	23.211.41.111
	104.26.143.40
	104.26.143.30
	104.26.183.20
	127.0.0.1

Formal Output
=============

You must output each of the requested IPs along with the **smallest IP
range it is a part of**. If an IP is not found, print `<unknown>`
instead of a name.

Sample Output
-------------

	23.211.41.111 e509a
	104.26.143.40 438f1
	104.26.143.30 438f0
	104.26.183.20 438ef
	127.0.0.1 <unknown>

The Catch / The Challenge
=========================

This seems simple, right? Well... Make your program work efficiently
(within a minute or so maximum) for these inputs:

** IP range files: **

* 500 ranges
* 2,500 ranges
* 10,000 ranges
* 300,000 ranges

** Query files: **

* 100 queries
* 1,000 queries
* 10,000 queries

You can mix and match the IP range files and the query files; they are
purely random, not constructed to trip anything in particular up.

**Food for thought**: you may want to split the program into two steps:
one for parsing / recording / organizing the IP ranges into a database
(or something similar), and another for performing lookups against the
database. 
