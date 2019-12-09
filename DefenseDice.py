import random
import multiprocessing as mp


class DefenseDice():
    parallel = False

    def __init__(self, parallel=False):
        self.parallel = parallel

    @staticmethod
    def __red():
        return random.sample(('b', 'b', 'b', 's', 'n', 'n'), 1)[0]

    @staticmethod
    def __white():
        return random.sample(('b', 's', 'n', 'n', 'n', 'n'), 1)[0]

    @staticmethod
    def __roll(red_dice=0, white_dice=0):
        dice = []
        dice += [DefenseDice.__red() for _ in range(red_dice)]
        dice += [DefenseDice.__white() for _ in range(white_dice)]
        result = ''.join(dice)
        return {
            'b': result.count('b'),
            's': result.count('s'),
            'n': result.count('n'),
        }

    def result(self, red_dice=0, white_dice=0, has_surge=False):
        result = DefenseDice.__roll(red_dice, white_dice)
        val = result['b']
        val += result['s'] if has_surge else 0
        return val

    def __test_async(self, red_dice=0, white_dice=0, rolls=10000, has_surge=False):
        pool = mp.Pool(mp.cpu_count())
        results = []
        while rolls > 0:
            pool.apply_async(
                self.result,
                args=(red_dice, white_dice, has_surge),
                callback=lambda r: results.append(r)
            )
            rolls -= 1
        pool.close()
        pool.join()
        return sum(results) / len(results) if len(results) > 0 else 0

    def __test_sync(self, red_dice=0, white_dice=0, rolls=10000, has_surge=False):
        results = []
        while rolls > 0:
            results.append(self.result(red_dice, white_dice, has_surge))
            rolls -= 1
        return sum(results) / len(results) if len(results) > 0 else 0

    def test(self, red_dice=0, white_dice=0, rolls=10000, has_surge=False):
        if self.parallel:
            return self.__test_async(red_dice, white_dice, rolls, has_surge)
        else:
            return self.__test_sync(red_dice, white_dice, rolls, has_surge)
