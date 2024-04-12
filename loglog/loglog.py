"""
Algorthm LOGLOG (m: Multiset of hashed value: m = 2^k)
Initialize M1, ..., Mm to 0;
let p(y) be the rank of first 1-bit from the left in y;
    for x =b1b2... in m do:
        set j := <b1...bk>2 (value of first k bits in base 2)
        set M(j) := max(Mj, p(bk+1, bk+2, ...))
return E := alpha(m)*m*2^(1/m * sum(Mj)
"""
try:
    from bitarray import bitarray
except ImportError:
    raise ImportError("require bitarray >= 0.3.4")
from Interface.Interface import Interface
from math import log, pow, ceil
from hashlib import sha1


def _word_size_calculator(max_cardinality):
    """
    Estimates the size of the memory Units, using the maximum cardinality as an argument
    Arguments:
    :param max_cardinality: Maximum Cardinality
    :return: size of the memory units
    """
    return int(ceil(log(log(max_cardinality, 2), 2)))


def get_sha1_bin(word: str) -> str:
    """Calculates the SHA1 hash of a word and returns its binary representation.

    Args:
        word: The word to be hashed.

    Returns:
        A 160-character binary string representing the SHA1 hash.
    """
    hash_s = sha1()
    hash_s.update(word.encode('utf-8'))
    return bin(int(hash_s.hexdigest(), 16))[2:].zfill(160)


def getindex(bin_string: str, end_index=160) -> int:
    """Calculates the position of the first 1-bit

    Args:
        bin_string: string to be compared
        end_index: Maximum index to use in the lookup for the 1-bit

    Returns:
        The position of the first 1-bit

    """
    res = -1
    try:
        res = bin_string.index('1') + 1
    except ValueError:
        res = end_index
    return res


class LogLog(Interface):
    """
    Implement a LogLog Sketch
    """

    def __init__(self, max_cardinality, error_rate):
        """
        Implementes a LogLog Sketch
        :param max_cardinality: this sketch able to count cardinalities up to cardinality 
        :param error_rate: the error rate of the sketch when calculating the cardinality of the set
        """
        if not (0 < error_rate < 1):
            raise ValueError("Error rate must be between 0 and 1.")
        if not max_cardinality > 0:
            raise ValueError("max cardinality must be > 0")
        self._max_cardinality = max_cardinality
        # k
        self._k = int(round(log(pow(1.30 / error_rate, 2), 2)))
        # m = 2**k
        self._bucket_number = 1 << self._k
        # Bucket size = loglog(max_cardinality) bits
        self._bucket_size = _word_size_calculator(self._max_cardinality)

        # M(1)...M(m) = 0
        self._bucket_list = [bitarray(self._bucket_size) for _ in range(self._bucket_number)]
        for barray in self._bucket_list:
            barray.setall(False)

        self.__name = "LogLogSketch"

    def add(self, item):
        """
        Adds the item to the LogLog Sketch
        :param item: Item to be added the loglog sketch
        :return: 
        """
        sha_string = get_sha1_bin(item)
        print(item)
        position = int(sha_string[:self._k], 2)
        # Retries the position of leftmost 1
        aux = getindex(sha_string[self._k], 160 - self._k)
        # The position cannot be bigger than the maximum number that can be fitted in word size bits
        index = min(aux, (1 << self._bucket_size) - 1)
        new_value = max(int(self._bucket_list[position].to01(), 2), index)
        print(index, " ", new_value)
        self._bucket_list[position] = bitarray(bin(new_value)[2:])
        # Perhaps it would be faster if operations were done in binary only

    def get_number_estimate(self):
        """Returns the estimate of the cardinality
        """
        # E = am * m * 2**(1/2 * sum M(j))
        m = self._bucket_number
        e = 0.39701 * m * 2 ** ((1.0 / m) * sum([int(x.to01(), 2) for x in self._bucket_list]))
        return e

    def join(self, *args):
        raise NotImplementedError("Method is not implemented for class" + str(type(self))[17:-2])

    def get_name(self):
        return self.__name

    def __sizeof__(self):
        # return get sizeof(self._max_cardinality) + get-sizeof(self._k) + get-sizeof(self._bucket_number) +
        # get-sizeof(self._bucket_list)
        return self._bucket_number * self._bucket_size
