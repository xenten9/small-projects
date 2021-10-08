# Standard Library
import random
from time import time
from typing import List


# Generator of list
def random_list(len: int) -> List[int]:
    return [random.randint(0, 101) for _ in range(len)]


# Method 0
def smallest_missing_int0(nums: List[int]) -> int:
    a = set(range(1, len(nums) + 1))
    for num in nums:
        a.discard(num)
    if len(a) == 0:
        return len(nums) + 1
    return min(a)


# Method 1
def smallest_missing_int1(nums: List[int]) -> int:
    a = set(range(1, len(nums) + 1))
    for num in a:
        if num not in nums:
            return num
    return len(nums) + 1


# Main
def main():
    # Generate list of random lists
    random_list_list: List[List[int]] = []
    for _ in range(500):
        random_list_list.append(random_list(100))

    # Method 0
    time_total: float = 0.0
    t = time()
    for _ in range(100):
        t = time()
        for list_index in range(len(random_list_list)):
            smallest_missing_int0(random_list_list[list_index])
        time_total += time() - t
    print(f"Total time for method 0: {time_total}")

    # Method 1
    time_total = 0.0
    for _ in range(100):
        t = time()
        for list_index in range(len(random_list_list)):
            smallest_missing_int1(random_list_list[list_index])
        time_total += time() - t
    print(f"Total time for method 1: {time_total}")


if __name__ == "__main__":
    main()
