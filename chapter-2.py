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


def expand_tab(
        text: str,
        tab_size: int,
    ) -> str:
    """
        テキストに含まれるタブをスペースに置換する.

        Arguments
        ---------
        text : str
            テキスト.
        tab_size : int
            1 つのタブを tab_size 個の ' ' に置換する.

        Returns
        -------
        text : str
            text に含まれる各タブを tab_size 個の ' ' に置換したテキスト.
    """
    return text.replace('\t', ' ' * tab_size)


class ExpandTabTestCase(unittest.TestCase):

    def test(self):
        self.assertEqual('', expand_tab('', 1))
        self.assertEqual('ABC', expand_tab('ABC', 1))
        self.assertEqual('A B C', expand_tab('A B C', 1))
        self.assertEqual('A B C', expand_tab('A\tB\tC', 1))
        self.assertEqual('A  B  C', expand_tab('A\tB\tC', 2))
        self.assertEqual('A    B    C', expand_tab('A\t\tB\t\tC', 2))


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
    print(count_lines(text))


def test11():
    """
        11. タブをスペースに置換

        タブ 1 文字につきスペース 1 文字に置換せよ.
        確認には sed コマンド, tr コマンド, もしくは expand コマンドを用いよ.
    """
    text = text_from_file('popular-names.txt')
    print(expand_tab(text, 1))


def main():
    test10()
    test11()


def test():
    doctest.testmod()
    unittest.main()


if __name__ == '__main__':
    main()
    test()

