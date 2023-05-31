"""Crude implementation of SuperMemo 2, simplifying it for the usecase I had

   Algorithm SM-2, (C) Copyright SuperMemo World, 1991.

   https://www.supermemo.com
   https://www.supermemo.eu
"""

import math


def answered(q, memo):
    n = memo.get("n", 1)
    i_n_1 = memo.get("i_n_1", 1)
    old_ef = memo.get("ef", 2.5)
    i_n = interval(q, n, i_n_1, old_ef)
    ef_p = ef(q, old_ef)
    return {"n": n + 1, "i_n": i_n, "ef": ef_p}


def interval(q, n, i_n_1, old_ef):
    if q < 3:
        return 1
    if n == 1:
        return 1
    if n == 2:
        return 6
    return int(math.ceil(i_n_1 * old_ef))


def ef(q, old_ef):
    """Calculate the new e-factor. Note that I will be only using
    response qualities (q) 2 and 4.5 (quite incorrect and almost perfect).
    When ef is unknown, ef is 2.5
    """
    ef_p = old_ef - 0.8 + 0.28 * q - 0.02 * q * q
    if ef_p < 1.3:
        ef_p = 1.3
    return ef_p
