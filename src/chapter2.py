#
# 言語処理100本ノック 2020 > 第2章: UNIXコマンド
# https://nlp100.github.io/ja/ch02.html
#

import contextlib
import doctest
import io
import os
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


def head_lines(
        n: int,
        text: str,
    ) -> typing.List[str]:
    """
        テキストの先頭から指定行数を取り出す.

        Arguments
        ---------
        n : int
            取り出す行数.
        text : str
            テキスト.
    """
    lines = text.splitlines()
    return '\n'.join(lines[:n])


class HeadLinesTestCase(unittest.TestCase):
    """
        head_lines() のテストケース.
    """

    def test(self):
        self.assertEqual('', head_lines(0, ''))
        self.assertEqual('', head_lines(1, ''))

        self.assertEqual('', head_lines(0, 'aaa\nbbb\nccc'))
        self.assertEqual('aaa', head_lines(1, 'aaa\nbbb\nccc'))
        self.assertEqual('aaa\nbbb', head_lines(2, 'aaa\nbbb\nccc'))
        self.assertEqual('aaa\nbbb\nccc', head_lines(3, 'aaa\nbbb\nccc'))
        self.assertEqual('aaa\nbbb\nccc', head_lines(4, 'aaa\nbbb\nccc'))


def tail_lines(
        n: int,
        text: str,
    ) -> typing.List[str]:
    """
        テキストの末尾から指定行数を取り出す.

        Arguments
        ---------
        n : int
            取り出す行数.
        text : str
            テキスト.
    """
    if n <= 0:
        return ''
    lines = text.splitlines()
    return '\n'.join(lines[-n:])


class TailLinesTestCase(unittest.TestCase):
    """
        tail_lines() のテストケース.
    """

    def test(self):
        self.assertEqual('', tail_lines(0, ''))
        self.assertEqual('', tail_lines(1, ''))

        self.assertEqual('', tail_lines(0, 'aaa\nbbb\nccc'))
        self.assertEqual('ccc', tail_lines(1, 'aaa\nbbb\nccc'))
        self.assertEqual('bbb\nccc', tail_lines(2, 'aaa\nbbb\nccc'))
        self.assertEqual('aaa\nbbb\nccc', tail_lines(3, 'aaa\nbbb\nccc'))
        self.assertEqual('aaa\nbbb\nccc', tail_lines(4, 'aaa\nbbb\nccc'))


def to_chunks(
        n: int,
        text: str,
    ) -> typing.List[str]:
    """
        テキストを行指向で N 個に分割する.

        Arguments
        ---------
        n : int
            分割数.
        text : str
            分割するテキスト.

        Returns
        -------
        chunks : typing.List[str]
            text を n 個に分割したリスト.
    """
    lines = text.splitlines()
    chunks = [[] for _ in range(n)]

    for i in range(len(lines)):
        chunks[int(i / len(lines) * n)].append(lines[i])
    return list(map('\n'.join, chunks))


class ToChunksTestCase(unittest.TestCase):
    """
        to_chunks() のテストケース.
    """

    def test(self):
        text = '\n'.join('ABCDE')
        self.assertEqual(['A\nB\nC\nD\nE'], to_chunks(1, text))
        self.assertEqual(['A\nB\nC', 'D\nE'], to_chunks(2, text))
        self.assertEqual(['A\nB', 'C\nD', 'E'], to_chunks(3, text))
        self.assertEqual(['A\nB', 'C', 'D', 'E'], to_chunks(4, text))
        self.assertEqual(['A', 'B', 'C', 'D', 'E'], to_chunks(5, text))
        self.assertEqual(['A', 'B', 'C', 'D', 'E', ''], to_chunks(6, text))
        self.assertEqual(['A', 'B', 'C', '', 'D', 'E', ''], to_chunks(7, text))
        self.assertEqual(['A', 'B', '', 'C', 'D', '', 'E', ''], to_chunks(8, text))
        self.assertEqual(['A', 'B', '', 'C', '', 'D', '', 'E', ''], to_chunks(9, text))
        self.assertEqual(['A', '', 'B', '', 'C', '', 'D', '', 'E', ''], to_chunks(10, text))


def practice10():
    """ 10. 行数のカウント

        行数をカウントせよ. 確認には wc コマンドを用いよ.

        Examples
        --------
        >>> practice10()
        2780
    """
    text = text_from_file('data/popular-names.txt')
    print(count_lines(text))


def practice11():
    """
        11. タブをスペースに置換

        タブ 1 文字につきスペース 1 文字に置換せよ. 確認には sed コマンド, tr
        コマンド, もしくは expand コマンドを用いよ.
    """
    text = text_from_file('data/popular-names.txt')
    print(expand_tab(text, 1))


class practice11TestCase(unittest.TestCase):
    """
        practice11() のテストケース.
    """

    def test(self):
        stdout = execute_and_return_stdout(practice11)
        self.assertEqual('Mary F 7065 1880', stdout[0])
        self.assertEqual('Anna F 2604 1880', stdout[1])
        self.assertEqual('Emma F 2003 1880', stdout[2])
        self.assertEqual('Lucas M 12585 2018', stdout[-4])
        self.assertEqual('Mason M 12435 2018', stdout[-3])
        self.assertEqual('Logan M 12352 2018', stdout[-2])
        self.assertEqual('', stdout[-1])


def practice12():
    """
        12. 1 列目を col1.txt に, 2 列目を col2.txt に保存

        各行の 1 列目だけを抜き出したものを col1.txt に, 2 列目だけを抜き出した
        ものを col2.txt としてファイルに保存せよ. 確認には cut コマンドを用いよ.
    """
    text = text_from_file('data/popular-names.txt')
    lines = text.splitlines()

    with open('data/col1.txt', 'w') as col1_file, \
         open('data/col2.txt', 'w') as col2_file:
        for line in lines:
            columns = line.split('\t')
            col1_file.write(columns[0] + '\n')
            col2_file.write(columns[1] + '\n')


class practice12TestCase(unittest.TestCase):
    """
        practice12() のテストケース.
    """

    def test(self):
        practice12()

        col1_lines = text_from_file('data/col1.txt').splitlines()
        self.assertEqual('Mary', col1_lines[0])
        self.assertEqual('Anna', col1_lines[1])
        self.assertEqual('Emma', col1_lines[2])
        self.assertEqual('Lucas', col1_lines[-3])
        self.assertEqual('Mason', col1_lines[-2])
        self.assertEqual('Logan', col1_lines[-1])

        col2_lines = text_from_file('data/col2.txt').splitlines()
        self.assertEqual('F', col2_lines[0])
        self.assertEqual('F', col2_lines[1])
        self.assertEqual('F', col2_lines[2])
        self.assertEqual('M', col2_lines[-3])
        self.assertEqual('M', col2_lines[-2])
        self.assertEqual('M', col2_lines[-1])


def practice13():
    """
        13. col1.txt と col2.txt をマージ

        12 で作った col1.txt と col2.txt を結合し, 元のファイルの 1 列目と 2 列
        目をタブ区切りで並べたテキストファイルを作成せよ. 確認には paste コマン
        ドを用いよ.
    """
    col1_lines = text_from_file('data/col1.txt').splitlines()
    col2_lines = text_from_file('data/col2.txt').splitlines()

    for values in zip(col1_lines, col2_lines):
        print('\t'.join(values))


class practice13TestCase(unittest.TestCase):
    """
        practice13() のテストケース.
    """

    def test(self):
        stdout = execute_and_return_stdout(practice13)
        self.assertEqual('Mary\tF', stdout[0])
        self.assertEqual('Anna\tF', stdout[1])
        self.assertEqual('Emma\tF', stdout[2])
        self.assertEqual('Lucas\tM', stdout[-3])
        self.assertEqual('Mason\tM', stdout[-2])
        self.assertEqual('Logan\tM', stdout[-1])


def practice14():
    """
        14. 先頭からN行を出力

        自然数 N をコマンドライン引数などの手段で受け取り, 入力のうち先頭の N
        行だけを表示せよ. 確認には head コマンドを用いよ.
    """
    print('N = ', end='')
    N = int(input())
    text = text_from_file('data/col1.txt')
    print(head_lines(N, text))


def practice15():
    """
        15. 末尾のN行を出力

        自然数 N をコマンドライン引数などの手段で受け取り,
        入力のうち末尾の N 行だけを表示せよ.
        確認には tail コマンドを用いよ.
    """
    print('N = ', end='')
    N = int(input())
    text = text_from_file('data/col1.txt')
    print(tail_lines(N, text))


def practice16():
    """
        16. ファイルを N 分割する

        自然数 N をコマンドライン引数などの手段で受け取り,
        入力のファイルを行単位で N 分割せよ.
        同様の処理を split コマンドで実現せよ.
    """
    print('N = ', end='')
    N = int(input())
    input_file_path = 'data/popular-names.txt'
    text = text_from_file(input_file_path)
    chunks = to_chunks(N, text)

    def to_output_file_path(input_file_path, chunks, chunk_index):
        suffix_length = len(str(max(1, len(chunks) - 1)))
        suffix = '{:0={}}'.format(chunk_index, suffix_length)
        root, ext = os.path.splitext(os.path.abspath(input_file_path))
        return '{}.{}{}'.format(root, suffix, ext)

    for i in range(len(chunks)):
        output_file_path = to_output_file_path(input_file_path, chunks, i)
        with open(output_file_path, 'w') as file:
            print('write to {}'.format(output_file_path))
            file.write(chunks[i])


def practice17():
    """
        17. 1 列目の文字列の異なり

        1 列目の文字列の種類 (異なる文字列の集合) を求めよ.
        確認には cut, sort, uniq コマンドを用いよ.

        Examples
        --------
        >>> practice17()
        136
    """
    text = text_from_file('data/popular-names.txt')
    lines = text.splitlines()
    names = [line.split()[0] for line in lines]
    print(len(set(names)))


def practice18():
    """
        18. 各行を 3 コラム目の数値の降順にソート

        各行を 3 コラム目の数値の逆順で整列せよ (注意: 各行の内容は変更せずに並
        び替えよ). 確認には sort コマンドを用いよ (この問題はコマンドで実行した
        時の結果と合わなくてもよい).
    """
    text = text_from_file('data/popular-names.txt')
    lines = text.splitlines()
    to_key = lambda line: int(line.split()[2])
    sorted_lines = sorted(lines, key=to_key, reverse=True)
    print('\n'.join(sorted_lines))


def practice19():
    """
        19. 各行の 1 コラム目の文字列の出現頻度を求め, 出現頻度の高い順に並べる.
    """
    text = text_from_file('data/popular-names.txt')
    lines = text.splitlines()
    values = [line.split()[0] for line in lines]
    histogram = to_histogram(values)

    for value, count in sorted(histogram.items(), key=lambda pair: pair[1], reverse=True):
        print(count, value)


def to_histogram(values):
    histogram = {}
    for value in values:
        histogram[value] = histogram.get(value, 0) + 1
    return histogram


def test():
    doctest.testmod()
    unittest.main()


if __name__ == '__main__':
    test()

