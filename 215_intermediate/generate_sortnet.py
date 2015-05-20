def oddeven_merge(lo, hi, r):
    step = r * 2
    if step < hi - lo:
        yield from oddeven_merge(lo, hi, step)
        yield from oddeven_merge(lo + r, hi, step)
        yield from [(i, i + r) for i in range(lo + r, hi - r, step)]
    else:
        yield (lo, lo + r)
 
def oddeven_merge_sort_range(lo, hi):
    """ sort the part of x with indices between lo and hi.
 
    Note: endpoints (lo and hi) are included.
    """
    if (hi - lo) >= 1:
        # if there is more than one element, split the input
        # down the middle and first sort the first and second
        # half, followed by merging them.
        mid = lo + ((hi - lo) // 2)
        yield from oddeven_merge_sort_range(lo, mid)
        yield from oddeven_merge_sort_range(mid + 1, hi)
        yield from oddeven_merge(lo, hi, 1)
 
def oddeven_merge_sort(length):
    """ "length" is the length of the list to be sorted.
    Returns a list of pairs of indices starting with 0 """
    yield from oddeven_merge_sort_range(0, length - 1)
 
def compare_and_swap(x, a, b):
    if x[a] > x[b]:
        x[a], x[b] = x[b], x[a]

########### Above is from https://en.wikipedia.org/wiki/Batcher_odd%E2%80%93even_mergesort

import sys
def main():
    length = int(sys.argv[1])
    pairs = list(oddeven_merge_sort(length))
    print(length, len(pairs))
    for p1, p2 in pairs:
        print(p1, p2)

if __name__ == '__main__': main()
