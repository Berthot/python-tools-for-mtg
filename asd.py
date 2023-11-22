def first_fit(items: [int], bin_capacity: int):
    bins = []                                   # O(1)
    for item in items:                             # O(n)
        allocated = False                       # O(1)
        for i in range(len(bins)):                 # O(m)
            if bins[i] + item <= bin_capacity:  # O(1)
                bins[i] += item                 # O(1)
                allocated = True                # O(1)
                break                           # O(1)
        if not allocated:                       # O(1)
            bins.append(item)                   # O(1)
    return bins


itemsList = [4, 2, 6, 8, 3]
bin_capacity_count = 10

# 9 [ 4 + 2 + 3 ]
# 6 [ 6 ]
# 8 [ 8 ]

# result = first_fit(itemsList, bin_capacity_count)
# print(result)