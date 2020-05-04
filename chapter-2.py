#
# 言語処理100本ノック 2020 > 第2章: UNIXコマンド
# https://nlp100.github.io/ja/ch02.html
#

import doctest
import typing
import unittest


def text_from_file(
        file_path: str,
    ) -> str:
    """
        テキストファイルを読み込む.

        Arguments
        ---------
        file_path : str
            テキストファイルのパス.

        Returns
        -------
        text : str
            テキストファイルの内容.
    """
    with open(file_path) as file:
        return file.read()


def count_lines(
        text: str,
    ) -> int:
    """
        テキストの行数を求める.

        Arguments
        ---------
        text : str
            テキスト.

        Returns
        -------
        count : int
            text の行数.
    """
    return len(text.splitlines())


class CountLinesTestCase(unittest.TestCase):
    """
        count_lines() のテストケース.
    """

    def test(self):
        self.assertEqual(0, count_lines(''))
        self.assertEqual(1, count_lines('abc'))
        self.assertEqual(2, count_lines('abc\ndef'))
        self.assertEqual(3, count_lines('abc\ndef\nghi'))
        self.assertEqual(3, count_lines('abc\ndef\nghi\n'))


def test10():
    """
        10. 行数のカウント

        行数をカウントせよ. 確認には wc コマンドを用いよ.

        Examples
        --------
        >>> test10()
        2780
    """
    text = text_from_file('popular-names.txt')
    return count_lines(text)


def main():
    test10()


def test():
    doctest.testmod()
    unittest.main()


if __name__ == '__main__':
    main()
    test()

