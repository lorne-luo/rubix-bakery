import logging

logger = logging.getLogger(__name__)


def pack_breakdown(total_quantity, pack_sizes):
    # if can't find perfect match, below vars will keep the minimized remainder solution with pack amount minimized
    best_remainder = total_quantity
    best_remainder_packs = {}

    solution_space = rank_breakdown(total_quantity, pack_sizes)  # whole possible solution space
    for solution in solution_space:
        quantity_per_product = [pack_sizes[i] * solution[i] for i in range(len(solution))]
        total = sum(quantity_per_product)
        remainder = total_quantity - total

        if remainder == 0:
            # perfect breakdown, return directly
            logger.debug(f'{solution}, {remainder}')
            pack_amount_tuple = [(pack_sizes[i], solution[i]) for i in range(len(solution))]
            pack_dict = dict(pack_amount_tuple)  # convert to dict, pack size is key ,pack amount is value
            return pack_dict, 0
        else:
            logger.debug(f'{solution}, {remainder}')
            if remainder > 0 and remainder < best_remainder:
                pack_amount_tuple = [(pack_sizes[i], solution[i]) for i in range(len(solution))]
                best_remainder_packs = dict(
                    pack_amount_tuple)  # convert to dict, pack size is key ,pack amount is value
                best_remainder = remainder

    # cant find perfect breakdown, return the minimized remainder solution with pack amount minimized
    return best_remainder_packs, best_remainder


def rank_breakdown(rest_quantity, pack_sizes):
    """
    Generate a possible solution space of pack breakdown which ranking by ascending packs total amount
    
    This is a recursive function follow below logic: 
    
    Assume that:
        total_quantity = PACKED_QUANTITY + REST_QUANTITY
        pack_sizes = [MAX_PACK_SIZE] + REST_SIZE_LIST
            
    then always have:
        rank_breakdown(total_quantity, pack_sizes) = rank_breakdown(PACKED_QUANTITY, [MAX_PACK_SIZE]) + rank_breakdown(REST_QUANTITY, [REST_SIZE_LIST])
    
    To minimise the total packs amount, just need simply make sure in this function always try MAX_PACK_SIZE first
    
    :param rest_quantity: total quantity, sum up of each combination should be equal this number
    :param pack_sizes: all available pack sizes
    :return: break down result, will be a tuple having same dimension with pack_size
    """

    # pack_sizes should be descending to make sure the result rank the solution with minimized packs amount first
    pack_sizes.sort(reverse=True)

    pack_choice_number = len(pack_sizes)
    current_pack_size = pack_sizes[0]
    if pack_choice_number == 1:
        # end of recursion
        pack_amount = int(rest_quantity / current_pack_size)
        return [(pack_amount,)]  # dont forget comma to let it as a tuple

    result = []
    possible_pack_amount = int(
        rest_quantity / current_pack_size) + 1  # make sure the this solution not over rest_quantity quantity
    for j in reversed(range(possible_pack_amount)):
        # print('####################', rest_quantity, current_pack_size, possible_pack_amount)

        for k in rank_breakdown(rest_quantity - j * current_pack_size, pack_sizes[1:]):
            # print('     ####################', (j,), k, '=', (j,) + k)
            result.append((j,) + k)

    return result
