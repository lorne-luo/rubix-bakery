import logging

logger = logging.getLogger(__name__)


class PackBreaker:
    def __init__(self, total_quantity, pack_sizes):
        self.total_quantity = total_quantity
        self.pack_sizes = pack_sizes
        self.pack_sizes.sort(reverse=True)

        # global variable to contain the minimized remainder solution with pack amount minimized
        self.best_remainder = total_quantity
        self.best_remainder_packs = {}

    def remove_zero(self, breakdown):
        """
        remove pack if amount is zero
        {8:0, 5:2} -> {5:2}
        """
        return dict([x for x in breakdown.items() if x[1]])

    def solve(self):
        """
        simply call `pack_breakdown`
        """
        self.pack_breakdown(self.total_quantity, self.pack_sizes)
        result = self.remove_zero(self.best_remainder_packs)
        return result, self.best_remainder

    def pack_breakdown(self, rest_quantity, pack_sizes, filled_pack_amount=()):
        """
        loop possible solution space by the order of packs total amount ascending
        :param rest_quantity:
        :param pack_sizes:
        :return:
        """
        if self.best_remainder == 0:
            # best already found not need continue anymore
            return []
        pack_sizes.sort(reverse=True)

        pack_choice_number = len(pack_sizes)
        current_pack_size = pack_sizes[0]

        if pack_choice_number == 1:  # now we are trying min pack size
            # end of recursion
            pack_amount = int(rest_quantity / current_pack_size)
            packs_amount = filled_pack_amount + (pack_amount,)
            remainder = self.get_remainder(packs_amount)
            if remainder >= 0 and remainder < self.best_remainder:
                self.best_remainder_packs = self.amount_to_breakdown(packs_amount)
                self.best_remainder = remainder
            return [(pack_amount,)]  # dont forget comma to let it as a tuple

        result = []
        possible_pack_amount = (
                int(rest_quantity / current_pack_size) + 1
        )  # make sure the this solution not over rest_quantity quantity

        for j in reversed(range(possible_pack_amount)):
            logger.debug(
                f"{rest_quantity}, {current_pack_size}, {possible_pack_amount}"
            )

            for k in self.pack_breakdown(
                    rest_quantity - j * current_pack_size,
                    pack_sizes[1:],
                    filled_pack_amount,
            ):
                packs_amount = (j,) + k
                remainder = self.get_remainder(packs_amount)
                result.append(packs_amount)

                logger.debug(f"{packs_amount}, {remainder}")
                if remainder >= 0 and remainder < self.best_remainder:
                    self.best_remainder_packs = self.amount_to_breakdown(packs_amount)
                    self.best_remainder = remainder

        return result

    def get_remainder(self, packs_amount):
        """
        return remainder for input packs_amount
        """
        quantity_per_product = [
            self.pack_sizes[i] * packs_amount[i] for i in range(len(packs_amount))
        ]

        total = sum(quantity_per_product)
        remainder = self.total_quantity - total
        return remainder

    def amount_to_breakdown(self, amounts):
        """
        combine amount and pack sizes, return a dict with size as key and amount as value
        :param amounts: amount list
        :return: a dict with size as key and amount as value
        """
        pack_amount_tuple = [
            (self.pack_sizes[i], amounts[i]) for i in range(len(amounts))
        ]
        pack_dict = dict(
            pack_amount_tuple
        )  # convert to dict, pack size is key ,pack amount is value
        return pack_dict
