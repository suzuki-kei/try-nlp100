#
# 言語処理100本ノック 2020 > 第2章: UNIXコマンド
# https://nlp100.github.io/ja/ch02.html
#

import contextlib
import doctest
import io
import typing
import unittest


def execute_and_return_stdout(
        target: callable,
    ) -> typing.List[str]:
    """
        指定された処理を実行し, 標準出力の値を取得する.

        Arguments
        ---------
        target : callable
            引数無しで呼び出し可能なオブジェクト.

        Returns
        -------
        stdout : typing.List[str]
            target の実行中に標準出力に出力された内容.
    """
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        target()
    return stdout.getvalue().splitlines()


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

        タブ 1 文字につきスペース 1 文字に置換せよ. 確認には sed コマンド, tr
        コマンド, もしくは expand コマンドを用いよ.
    """
    text = text_from_file('popular-names.txt')
    print(expand_tab(text, 1))


class Test11TestCase(unittest.TestCase):
    """
        test11() のテストケース.
    """

    def test(self):
        stdout = execute_and_return_stdout(test11)
        self.assertEqual('Mary F 7065 1880', stdout[0])
        self.assertEqual('Anna F 2604 1880', stdout[1])
        self.assertEqual('Emma F 2003 1880', stdout[2])
        self.assertEqual('Lucas M 12585 2018', stdout[-4])
        self.assertEqual('Mason M 12435 2018', stdout[-3])
        self.assertEqual('Logan M 12352 2018', stdout[-2])
        self.assertEqual('', stdout[-1])


def test12():
    """
        12. 1 列目を col1.txt に, 2 列目を col2.txt に保存

        各行の 1 列目だけを抜き出したものを col1.txt に, 2 列目だけを抜き出した
        ものを col2.txt としてファイルに保存せよ. 確認には cut コマンドを用いよ.
    """
    text = text_from_file('popular-names.txt')
    lines = text.splitlines()

    with open('col1.txt', 'w') as col1_file, \
         open('col2.txt', 'w') as col2_file:
        for line in lines:
            columns = line.split('\t')
            col1_file.write(columns[0] + '\n')
            col2_file.write(columns[1] + '\n')


class Test12TestCase(unittest.TestCase):
    """
        test12() のテストケース.
    """

    def test(self):
        test12()

        col1_lines = text_from_file('col1.txt').splitlines()
        self.assertEqual('Mary', col1_lines[0])
        self.assertEqual('Anna', col1_lines[1])
        self.assertEqual('Emma', col1_lines[2])
        self.assertEqual('Lucas', col1_lines[-3])
        self.assertEqual('Mason', col1_lines[-2])
        self.assertEqual('Logan', col1_lines[-1])

        col2_lines = text_from_file('col2.txt').splitlines()
        self.assertEqual('F', col2_lines[0])
        self.assertEqual('F', col2_lines[1])
        self.assertEqual('F', col2_lines[2])
        self.assertEqual('M', col2_lines[-3])
        self.assertEqual('M', col2_lines[-2])
        self.assertEqual('M', col2_lines[-1])


def test13():
    """
        13. col1.txt と col2.txt をマージ

        12 で作った col1.txt と col2.txt を結合し, 元のファイルの 1 列目と 2 列
        目をタブ区切りで並べたテキストファイルを作成せよ. 確認には paste コマン
        ドを用いよ.
    """
    col1_lines = text_from_file('col1.txt').splitlines()
    col2_lines = text_from_file('col2.txt').splitlines()

    for values in zip(col1_lines, col2_lines):
        print('\t'.join(values))


class Test13TestCase(unittest.TestCase):
    """
        test13() のテストケース.
    """

    def test(self):
        stdout = execute_and_return_stdout(test13)
        self.assertEqual('Mary\tF', stdout[0])
        self.assertEqual('Anna\tF', stdout[1])
        self.assertEqual('Emma\tF', stdout[2])
        self.assertEqual('Lucas\tM', stdout[-3])
        self.assertEqual('Mason\tM', stdout[-2])
        self.assertEqual('Logan\tM', stdout[-1])


def main():
    test10()
    test11()
    test12()
    test13()


def test():
    doctest.testmod()
    unittest.main()


if __name__ == '__main__':
    main()
    test()

