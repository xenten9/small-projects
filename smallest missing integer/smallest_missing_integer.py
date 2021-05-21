# Standard Library
import random
from time import time
from typing import List


# Generator of list
def random_list(len: int) -> List[int]:
    return [random.randint(0, 500) for _ in range(len)]


# Methods
def smallest_missing_int0(nums: List[int]) -> int:
    a = set(range(1, len(nums) + 1))
    for num in nums:
        a.discard(num)
    if len(a) == 0:
        return len(nums) + 1
    return min(a)

def smallest_missing_int1(nums: List[int]) -> int:
    a = set(range(1, len(nums) + 1))
    for num in a:
        if num not in nums:
            return num
    return len(nums) + 1


# Main
def main():
    b: List[List[int]] = []
    for _ in range(500):
        b.append(random_list(10))

    c: List[float] = []
    t = time()
    for _ in range(100):
        for n, _ in enumerate(b):
            b[n] += random_list(10)
        for a in range(len(b)):
            smallest_missing_int0(b[a])
        c.append(round(time()-t, 2))
        t = time()
    print(c)
    print(sum(c))

if __name__ == '__main__':
    main()

