# Bakery Pack Breakdown

## Requirement Specification
This system will breakdown the packs of client's order by following rules:

1. If perfect breakdown exists, always return the perfect breakdown with minimum packs amount. Perfect breakdown means match the client's quantity with no remainder.
2. If perfect breakdown not exists, consider to minimize the remainder first, then minimum packs amount.
    
    Example: Having pack size 5 and 8, for quantity 11 the expected answer should be 2 packs of 5 instead of 1 pack of 8 due to previous one have the lower remainder.
     
## Install Environment
To make it convenient to run and test, this works is finished within all Python built-in packages, so none extra packages need to be installed. The Python version should be 3.6 or above due to used [f-string formatting](https://docs.python.org/3/reference/lexical_analysis.html#f-strings) which is a new in Python 3.6.
- Python 3.6 or above
- Git

## How to config

Two settings provided, set env vars to make configure:

1. **DEBUG**: for enabling debug log, accept `true`, `false`, `1` and `0`, default is False
2. **PRICE_DECIMAL_PLACES**: to specify price decimal places, accept integer number, default is `2`

## How to install and run
Clone this repo using git then run `main.py`.

 ```
 git clone https://github.com/lorne-luo/rubix-bakery.git
 cd rubix-bakery
 python main.py
 ```
 **Screenshot:**
 
 ![](screenshot.png)
 
## How to test
Simply run `test.py`
```
 cd rubix-bakery
 python test.py
 ```
In this part, I did **super strong random testing** to cover the kernal algorithm function `rank_breakdown` and `pack_breakdown`. 

see [test.py](b.com/lorne-luo/rubix-bakery/blob/master/test.py)

## Algorithm Explaination
### Problem Definition

Problem input: `TOTAL_QUANTITY` (int) and `PACK_SIZES` (int list)

Problem output: 

1. If perfect match exist, find a `PACK_AMOUNTS` let `PACK_AMOUNTS * PACK_SIZES == TOTAL_QUANTITY` and `MINIMISE(SUM(PACK_AMOUNTS))`.

2. If perfect match no exist, find a `PACK_AMOUNTS` meet `MINIMISE(TOTAL_QUANTITY - PACK_AMOUNTS * PACK_SIZES)` first, then `MINIMISE(SUM(PACK_AMOUNTS))`.

### Problem Analysis

Follow the considerations below, we can always find a global best solution for this problem:


For problem inputs `TOTAL_QUANTITY` and `PACK_SIZES`, **always have a divides satisfy**:
```
    # PERFECT_PACKED_QUANTITY could be 0 if PERFECT_PACKED_QUANTITY < MIN(PACK_SIZES)
    # REST_QUANTITY could be 0 then TOTAL_QUANTITY could be perfectly matched 
    TOTAL_QUANTITY = PERFECT_PACKED_QUANTITY + REST_QUANTITY  
    
    # example: [8, 5, 2] = [8] + [5, 2], then MAX_PACK_SIZE = 8, REST_SIZE_LIST = [5, 2]
    PACK_SIZES = [MAX_PACK_SIZE] + REST_SIZE_LIST 
```

Considering function `BEST_BREAKDOWN`, it can be solved **optimally by breaking it into two sub-problems**:
```
    BEST_BREAKDOWN(TOTAL_QUANTITY, PACK_SIZES) = BEST_BREAKDOWN(PERFECT_PACKED_QUANTITY, PACK_SIZES]) + 
                                                 BEST_BREAKDOWN(REST_QUANTITY, PACK_SIZES])
```

To minimize the total pack amount, we just need **priorly use `MAX_PACK_SIZE` to fill the `PERFECT_PACKED_QUANTITY`** as possible as could be, so the formula evolves to below one **without changing the problem's solution space**. 
```
    BEST_BREAKDOWN(TOTAL_QUANTITY, PACK_SIZES) = BEST_BREAKDOWN(PERFECT_PACKED_QUANTITY, [MAX_PACK_SIZE]]) +
                                                 BEST_BREAKDOWN(REST_QUANTITY, REST_SIZE_LIST])
```

For meet this problem's requirement, I have below thought:
1. Loop the formula above **with descending `PERFECT_PACKED_QUANTITY`** can make sure always first test the solutions with minimum packs amount.
2. To make sure priorly return the perfect matched solution, just need check remainder in each loop, **if remainder == 0 return current solution immediately**.
3. For the case of a perfect match not exist, a global variable defined out of the loop is needed to **keep the first occurred solution with the lowest remainder**. If loop ended still can't find a perfect match solution, then give this global variable as the return.

### Algorithm Implementation
My implementation is a typical dynamic programming algorithm using recursion. The core functions is in [helper.py](https://github.com/lorne-luo/rubix-bakery/blob/master/helper.py).

This implementation is not the performance best one. 

1. In `rank_breakdown` function I calculated all edged solutions with packs amount descending(just edged possible solutions, all too much or too less solutions are excluded from the loop) while in total quantity checking step (funcion `pack_breakdown`) not all solutions will be looped.

2. Function `rank_breakdown` is finished by recursion. Recursion can significantly save codes but need extra memory for stack push/pop, and **as input value increasing this cost may explode**.

But my implementation also has significant advantages.

1. Expose all edged possible solutions at once could make implementation **much easier to understand**, and also have **better modularization**.

2. Recursion cloud **avoids too deep nested For loop**, **save lots of codes** and **be easy for understanding**. 

So if not in a performance concerned scenario I'd like to take this implementation due to easier to maintain.
 
If performance has bottleneck, we can still break the recursion into For loop and put the quantity-checking inside to optimize the calculation and memory usage.
 
If in a performance concerned scenario, we can still break the recursion into For loop and bring the quantity-checking inside.

## Development & Tools

1. This project followed TDD development process, test case had been added in the [first commit](https://github.com/lorne-luo/rubix-bakery/commit/63badd3b8767b34ee9204c31cccb988f09be6feb).

2. Implemented by Mac OS and PyCharm 

3. All codes are formatted using [black](https://github.com/python/black) to improve the readability. 