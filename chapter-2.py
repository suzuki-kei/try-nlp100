#
# 言語処理100本ノック 2020 > 第2章: UNIXコマンド
# https://nlp100.github.io/ja/ch02.html
#

import doctest
import typing
import unittest


def test10():
    """
        10. 行数のカウント

        行数をカウントせよ. 確認には wc コマンドを用いよ.

        Examples
        --------
        >>> test10()
        2780
    """
    with open('popular-names.txt') as file:
        lines = list(map(str.strip, file.readlines()))
        print(len(lines))


def main():
    test10()


def test():
    doctest.testmod()
    unittest.main()


if __name__ == '__main__':
    main()
    test()

