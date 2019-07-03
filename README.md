# Bakery Pack Breakdown

## Requirement Specification
This system will breakdown the packs of client's order by following rules:

1. If perfect breakdown exists, always return the perfect breakdown with minimum packs amount. Perfect breakdown means match client's quantity requirement with no remainder.
2. If perfect breakdown not exists, consider to minimize the remainder first, then minimum packs amount.
    
    Example: Having pack size 5 and 8, for quantity 11 the expected answer should be 2 packs of 5 instead of 1 pack of 8 due to previous one have the lower remainder.
     
## Install Environment
To make it convenient to run and test, this works is finished within all Python built-in packages, so none extra packages need to be installed. The Python version should be 3.6 or above due to used [f-string formatting](https://docs.python.org/3/reference/lexical_analysis.html#f-strings) which is a new feature in Python 3.6.
- Python 3.6 or above
- Git

## How to config

Two settings provided, set env vars to make configure:

1. `DEBUG` for enabling debug log, accept `true`, `false`, `1` and `0`, default is False
2. `PRICE_DECIMAL_PLACES` to specify price decimal places, accept integer number, default is 2

## How to install and run
Simply clone this repo using git then run `main.py.

 ```
 git clone https://github.com/lorne-luo/rubix-bakery.git
 cd rubix-bakery
 python main.py
 ```

### Algorithm Explaination
#### Problem Definition

Problem input: `TOTAL_QUANTITY` and `PACK_SIZES`

Problem output: 

1. If perfect match exist, find a `PACK_AMOUNTS` let `PACK_AMOUNTS * PACK_SIZES == TOTAL_QUANTITY` and `MINIMISE(SUM(PACK_AMOUNTS))`.

2. If perfect match no exist, find a `PACK_AMOUNTS` meet `MINIMISE(TOTAL_QUANTITY - PACK_AMOUNTS * PACK_SIZES)` first, then `MINIMISE(SUM(PACK_AMOUNTS))`.

#### Problem Analysis

Follow the considerations below, we can always find a global best solution for this problem:


For input `TOTAL_QUANTITY` and `PACK_SIZES` we can always find a split satisfy:
```
    # PERFECT_PACKED_QUANTITY could be 0 if PERFECT_PACKED_QUANTITY < MIN(PACK_SIZES)
    # REST_QUANTITY could be 0 then TOTAL_QUANTITY could be perfectly matched 
    TOTAL_QUANTITY = PERFECT_PACKED_QUANTITY + REST_QUANTITY  
    
    # example: [8, 5, 2] = [8] + [5, 2], then MAX_PACK_SIZE = 8, REST_SIZE_LIST = [5, 2]
    PACK_SIZES = [MAX_PACK_SIZE] + REST_SIZE_LIST 
```

Then for problem function `BEST_BREAKDOWN,` it can be solved optimally by breaking it into sub-problems:
```
    BEST_BREAKDOWN(TOTAL_QUANTITY, PACK_SIZES) = BEST_BREAKDOWN(PERFECT_PACKED_QUANTITY, PACK_SIZES]) + BEST_BREAKDOWN(REST_QUANTITY, PACK_SIZES])
```

To minimize the total pack amount, we just need prior to use `MAX_PACK_SIZE` to fill the `PERFECT_PACKED_QUANTITY`  part as possible as could be, so the formula evolves to below but without changing the problem's satisfaction. 
```
    BEST_BREAKDOWN(TOTAL_QUANTITY, PACK_SIZES) = BEST_BREAKDOWN(PERFECT_PACKED_QUANTITY, [MAX_PACK_SIZE]]) + BEST_BREAKDOWN(REST_QUANTITY, REST_SIZE_LIST])
```

For meet this problem's requirement, I have below thought:
1. Loop below's formula with descending `PERFECT_PACKED_QUANTITY` can make sure we first test the solutions with minimum packs amount
2. To make sure priorly give the perfect matched solution, we just need check remainder in each loop, if remainder == 0, return current solution immediately.
3. For the case of a perfect match not exist, just need to set a global variable out of the loop and keep the first solution with the lowest remainder. If loop ended still can't find a perfect match solution, then give this global variable as the return.

#### Algorithm Implementation
My implementation is a typical dynamic programming algorithm using recursion. The core functions is in [helper.py](https://github.com/lorne-luo/rubix-bakery/blob/master/helper.py).

This implementation is not the best performance as in `rank_breakdown` function I used recursion to calculate all edged answers with packs amount descending(just edge answers, all impossible answers are excluded from the loop) while in total quantity checking step (funcion `pack_breakdown`) not all answer will be touched.

But the advantage of my implementation is that it avoided too deep For loop, so it has good modularization and easy to understand. If not in a performance concerned scenario I'd always like take this implementation.
 
 
If in a performance concerned scenario, we can still break the recursion into For loop and bring the quantity-checking inside.

# Development
1. This project followed TDD