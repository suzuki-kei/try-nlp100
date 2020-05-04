#
# 言語処理100本ノック 2020 > 第1章: 準備運動
# https://nlp100.github.io/ja/ch01.html
#

import doctest
import random
import re
import typing
import unittest


def to_words(
        text: str,
    ) -> typing.List[str]:
    """
        テキストを単語に分割する.

        Arguments
        ---------
        text : str
            分割するテキスト.

        Returns
        -------
        words : typing.List[str]
            text に含まれる単語からなるリスト.
    """
    pattern = re.compile(r'[0-9a-zA-Z]+')
    return pattern.findall(text)


class ToWordsTestCase(unittest.TestCase):
    """
        to_words() のテストケース.
    """

    def test_when_empty_string_passed(self):
        """
            空文字列が渡された場合のテスト.
        """
        self.assertEqual([], to_words(''))

    def test_when_non_empty_string_passed(self):
        """
            非空文字列が渡された場合のテスト.
        """
        self.assertEqual(
            ['It', 's', 'a', 'fine', 'day'],
            to_words("It's a fine day!"))


def to_word_ngram(
        n: int,
        text: str,
    ) -> typing.List[str]:
    """
        テキストを単語 N-gram に分割する.

        Arguments
        ---------
        n : int
            分割数.
        text : str
            分割するテキスト.

        Returns
        -------
        word_ngram : typing.List[str]
            text の単語 N-gram.
    """
    words = to_words(text)
    return [''.join(words[i:i+n]) for i in range(len(words) - n + 1)]


class ToWordNgram(unittest.TestCase):
    """
        to_word_ngram() のテストケース.
    """

    def test_empty_string_to_word_unigram(self):
        """
            空文字列を単語 uni-gram に分割する場合のテスト.
        """
        self.assertEqual([], to_word_ngram(1, ''))

    def test_non_empty_string_to_word_unigram(self):
        """
            非空文字列を単語 uni-gram に分割する場合のテスト.
        """
        self.assertEqual(
            ['It', 's', 'a', 'fine', 'day'],
            to_word_ngram(1, "It's a fine day!"))

    def test_empty_string_to_word_bigram(self):
        """
            空文字列を単語 bi-gram に分割する場合のテスト.
        """
        self.assertEqual([], to_word_ngram(2, ''))

    def test_non_empty_string_to_word_bigram(self):
        """
            非空文字列を単語 bi-gram に分割する場合のテスト.
        """
        self.assertEqual(
            ['Its', 'sa', 'afine', 'fineday'],
            to_word_ngram(2, "It's a fine day!"))

    def test_empty_string_to_word_trigram(self):
        """
            空文字列を単語 tri-gram に分割する場合のテスト.
        """
        self.assertEqual([], to_word_ngram(3, ''))

    def test_non_empty_string_to_word_trigram(self):
        """
            非空文字列を単語 tri-gram に分割する場合のテスト.
        """
        self.assertEqual(
            ['Itsa', 'safine', 'afineday'],
            to_word_ngram(3, "It's a fine day!"))


def to_char_ngram(
        n: int,
        text: str,
    ) -> typing.List[str]:
    """
        テキストを文字 N-gram に分割する.

        Arguments
        ---------
        n : int
            分割数.
        text : str
            分割するテキスト.

        Returns
        -------
        char_ngram : typing.List[str]
            text の文字 N-gram.
    """
    text = ''.join(to_words(text))
    return [text[i:i+n] for i in range(len(text) - n + 1)]


class ToCharNgramTestCase(unittest.TestCase):
    """
        to_char_ngram() のテストケース.
    """

    def test_empty_string_to_char_unigram(self):
        """
            空文字列を単語 uni-gram に分割する場合のテスト.
        """
        self.assertEqual([], to_char_ngram(1, ''))

    def test_non_empty_string_to_char_unigram(self):
        """
            非空文字列を文字 uni-gram に分割する場合のテスト.
        """
        self.assertEqual(
            ['I', 't', 's', 'a', 'f', 'i', 'n', 'e', 'd', 'a', 'y'],
            to_char_ngram(1, "It's a fine day!"))

    def test_empty_string_to_char_bigram(self):
        """
            空文字列を単語 bi-gram に分割する場合のテスト.
        """
        self.assertEqual([], to_char_ngram(2, ''))

    def test_non_empty_string_to_char_bigram(self):
        """
            非空文字列を文字 bi-gram に分割する場合のテスト.
        """
        self.assertEqual(
            ['It', 'ts', 'sa', 'af', 'fi', 'in', 'ne', 'ed', 'da', 'ay'],
            to_char_ngram(2, "It's a fine day!"))

    def test_empty_string_to_char_trigram(self):
        """
            空文字列を文字 tri-gram に分割する場合のテスト.
        """
        self.assertEqual([], to_char_ngram(3, ''))

    def test_non_empty_string_to_char_trigram(self):
        """
            非空文字列を文字 tri-gram に分割する場合のテスト.
        """
        self.assertEqual(
            ['Its', 'tsa', 'saf', 'afi', 'fin', 'ine', 'ned', 'eda', 'day'],
            to_char_ngram(3, "It's a fine day!"))


def cipher(
        text: str,
    ) -> str:
    """
        テキストを暗号化する.

        暗号化はテキストの各文字を以下の条件で変換することによって行う.

         * 英小文字ならば (219 - 文字コード) の文字に変換する.
         * その他の文字は変換しない.

        Arguments
        ---------
        text : str
            暗号化するテキスト.

        Returns
        -------
        cipher_text : str
            text を暗号化した文字列.
    """
    def convert(c):
        return chr(219 - ord(c)) if c.islower() else c
    return ''.join(map(convert, list(text)))


class CipherTestCase(unittest.TestCase):
    """
        cipher() のテストケース.
    """

    def test_when_empty_string_passed(self):
        """
            空文字列を渡した場合のテスト.
        """
        self.assertEqual('', cipher(''))

    def test_when_ascii_string_passed(self):
        """
            ASCII 文字を含む文字列を渡した場合のテスト.
        """
        self.assertEqual('I zn zm NLPvi', cipher('I am an NLPer'))

    def test_when_multibyte_string_passed(self):
        """
            マルチバイト文字を含む文字列を渡した場合のテスト.
        """
        self.assertEqual('c時のbはa', cipher('x時のyはz'))


def to_typoglycemia(
        text: str,
    ) -> str:
    """
        テキストをスペースで区切り, それぞれについて以下の規則で変換する.

         * 先頭と末尾の文字はそのまま残し, それ以外をランダムに並び替える.
         * ただし長さが 4 以下の場合は変換しない.

        Arguments
        ---------
        text : str
            変換するテキスト.

        Returns
        -------
        typoglycemia : str
            変換したテキスト.
    """
    def shuffle(text):
        chars = list(text)
        random.shuffle(chars)
        return ''.join(chars)
    def convert(word):
        if len(word) <= 4:
            return word
        else:
            return word[0] + shuffle(word[1:-1]) + word[-1]
    words = text.split(' ')
    return ' '.join(map(convert, words))


class TypoglycemiaTestCase(unittest.TestCase):
    """
        to_typoglycemia() のテストケース.
    """

    def test(self):
        text = "I couldn't believe that I could actually understand " \
               "what I was reading : the phenomenal power of the human mind ."
        words = to_typoglycemia(text).split(' ')

        self.assertEqual(sorted("I"), sorted(words[0]))
        self.assertEqual(sorted("couldn't"), sorted(words[1]))
        self.assertEqual(sorted("believe"), sorted(words[2]))
        self.assertEqual(sorted("that"), sorted(words[3]))
        self.assertEqual(sorted("I"), sorted(words[4]))
        self.assertEqual(sorted("cloud"), sorted(words[5]))
        self.assertEqual(sorted("actually"), sorted(words[6]))
        self.assertEqual(sorted("understand"), sorted(words[7]))
        self.assertEqual(sorted("what"), sorted(words[8]))
        self.assertEqual(sorted("I"), sorted(words[9]))
        self.assertEqual(sorted("was"), sorted(words[10]))
        self.assertEqual(sorted("reading"), sorted(words[11]))
        self.assertEqual(sorted(":"), sorted(words[12]))
        self.assertEqual(sorted("the"), sorted(words[13]))
        self.assertEqual(sorted("phenomenal"), sorted(words[14]))
        self.assertEqual(sorted("power"), sorted(words[15]))
        self.assertEqual(sorted("of"), sorted(words[16]))
        self.assertEqual(sorted("the"), sorted(words[17]))
        self.assertEqual(sorted("human"), sorted(words[18]))
        self.assertEqual(sorted("mind"), sorted(words[19]))
        self.assertEqual(sorted("."), sorted(words[20]))

        self.assertEqual(['I', 'I'], [words[0][0], words[0][-1]])
        self.assertEqual(['c', 't'], [words[1][0], words[1][-1]])
        self.assertEqual(['b', 'e'], [words[2][0], words[2][-1]])
        self.assertEqual(['t', 't'], [words[3][0], words[3][-1]])
        self.assertEqual(['I', 'I'], [words[4][0], words[4][-1]])
        self.assertEqual(['c', 'd'], [words[5][0], words[5][-1]])
        self.assertEqual(['a', 'y'], [words[6][0], words[6][-1]])
        self.assertEqual(['u', 'd'], [words[7][0], words[7][-1]])
        self.assertEqual(['w', 't'], [words[8][0], words[8][-1]])
        self.assertEqual(['I', 'I'], [words[9][0], words[9][-1]])
        self.assertEqual(['w', 's'], [words[10][0], words[10][-1]])
        self.assertEqual(['r', 'g'], [words[11][0], words[11][-1]])
        self.assertEqual([':', ':'], [words[12][0], words[12][-1]])
        self.assertEqual(['t', 'e'], [words[13][0], words[13][-1]])
        self.assertEqual(['p', 'l'], [words[14][0], words[14][-1]])
        self.assertEqual(['p', 'r'], [words[15][0], words[15][-1]])
        self.assertEqual(['o', 'f'], [words[16][0], words[16][-1]])
        self.assertEqual(['t', 'e'], [words[17][0], words[17][-1]])
        self.assertEqual(['h', 'n'], [words[18][0], words[18][-1]])
        self.assertEqual(['m', 'd'], [words[19][0], words[19][-1]])
        self.assertEqual(['.', '.'], [words[20][0], words[20][-1]])


def test00():
    """
        00. 文字列の逆順

        文字列 "stressed" の文字を逆に (末尾から先頭に向かって) 並べた文字列を
        得よ.

        Examples
        --------
        >>> test00()
        desserts
    """
    text = 'stressed'
    print(text[::-1])


def test01():
    """
        01. 「パタトクカシーー」

        「パタトクカシーー」という文字列の1,3,5,7文字目を取り出して連結した文字
        列を得よ.

        Examples
        --------
        >>> test01()
        パトカー
    """
    text = 'パタトクカシーー'
    print(''.join(map(lambda n: text[n - 1], [1, 3, 5 ,7])))


def test02():
    """
        02. 「パトカー」＋「タクシー」＝「パタトクカシーー」

        「パトカー」＋「タクシー」の文字を先頭から交互に連結して文字列「パタト
        クカシーー」を得よ．

        Examples
        --------
        >>> test02()
        パタトクカシーー
    """
    text1 = 'パトカー'
    text2 = 'タクシー'
    print(''.join(map(''.join, zip(text1, text2))))


def test03():
    """
        03. 円周率

        "Now I need a drink, alcoholic of course, after the heavy lectures
        involving quantum mechanics." という文を単語に分解し, 各単語の (アルフ
        ァベットの) 文字数を先頭から出現順に並べたリストを作成せよ.

        Examples
        --------
        >>> test03()
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9]
    """
    text = 'Now I need a drink, alcoholic of course, ' \
           'after the heavy lectures involving quantum mechanics.'
    words = to_words(text)
    print(list(map(lambda word: len(word), words)))


def test04():
    """
        04. 元素記号

        "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might
        Also Sign Peace Security Clause. Arthur King Can." という文を単語に分解
        し, 1, 5, 6, 7, 8, 9, 15, 16, 19 番目の単語は先頭の 1 文字, それ以外の
        単語は先頭に2文字を取り出し, 取り出した文字列から単語の位置 (先頭から何
        番目の単語か) への連想配列 (辞書型もしくはマップ型) を作成せよ.

        Examples
        --------
        >>> test04()
        {1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mi', 13: 'Al', 14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca'}
    """
    text = 'Hi He Lied Because Boron Could Not Oxidize Fluorine. ' \
           'New Nations Might Also Sign Peace Security Clause. ' \
           'Arthur King Can.'
    indices = [1, 5, 6, 7, 8, 9, 15, 16, 19]
    words = to_words(text)
    print({
        i + 1: words[i][:1 if i + 1 in indices else 2]
        for i in range(len(words))
    })


def test05():
    """
        05. n-gram

        与えられたシーケンス (文字列やリストなど) から n-gram を作る関数を作成せ
        よ. この関数を用い, "I am an NLPer" という文から単語 bi-gram, 文字
        bi-gram を得よ.

        Examples
        --------
        >>> test05()
        ['Iam', 'aman', 'anNLPer']
        ['Ia', 'am', 'ma', 'an', 'nN', 'NL', 'LP', 'Pe', 'er']
    """
    text = 'I am an NLPer'
    print(to_word_ngram(2, text))
    print(to_char_ngram(2, text))


def test06():
    """
        06. 集合

        "paraparaparadise" と "paragraph" に含まれる文字 bi-gram の集合を, それ
        ぞれ,  X と Y として求め, X と Y の和集合, 積集合, 差集合を求めよ. さら
        に, 'se' という bi-gram が X および Y に含まれるかどうかを調べよ.

        Examples
        --------
        >>> test06()
        X = ['ad', 'ap', 'ar', 'di', 'is', 'pa', 'ra', 'se']
        Y = ['ag', 'ap', 'ar', 'gr', 'pa', 'ph', 'ra']
        X | Y = ['ad', 'ag', 'ap', 'ar', 'di', 'gr', 'is', 'pa', 'ph', 'ra', 'se']
        X & Y = ['ap', 'ar', 'pa', 'ra']
        X - Y = ['ad', 'di', 'is', 'se']
    """
    text1 = 'paraparaparadise'
    X = set(to_char_ngram(2, text1))
    print('X = {}'.format(sorted(X)))

    text2 = 'paragraph'
    Y = set(to_char_ngram(2, text2))
    print('Y = {}'.format(sorted(Y)))

    print('X | Y = {}'.format(sorted(X | Y)))
    print('X & Y = {}'.format(sorted(X & Y)))
    print('X - Y = {}'.format(sorted(X - Y)))


def test07():
    """
        07. テンプレートによる文生成

        引数 x, y, z を受け取り「x時のyはz」という文字列を返す関数を実装せよ.
        さらに, x=12, y="気温", z=22.4 として, 実行結果を確認せよ.

        Examples
        --------
        >>> test07()
        12時の気温は22.4
    """
    def format(x, y, z):
        template = '{x}時の{y}は{z}'
        return template.format(x=x, y=y, z=z)
    print(format(12, '気温', 22.4))


def test08():
    """
        08. 暗号文

        与えられた文字列の各文字を, 以下の仕様で変換する関数cipherを実装せよ.

         * 英小文字ならば (219 - 文字コード) の文字に置換
         * その他の文字はそのまま出力

        この関数を用い, 英語のメッセージを暗号化・復号化せよ.

        Examples
        --------
        >>> test08()
        I zn zm NLPvi
    """
    print(cipher('I am an NLPer'))


def test09():
    """
        09. Typoglycemia

        スペースで区切られた単語列に対して, 各単語の先頭と末尾の文字は残し, そ
        れ以外の文字の順序をランダムに並び替えるプログラムを作成せよ. ただし,
        長さが 4 以下の単語は並び替えないこととする. 適当な英語の文 (例えば "I
        couldn't believe that I could actually understand what I was reading :
        the phenomenal power of the human mind .") を与え, その実行結果を確認せ
        よ.

        Examples
        --------
        乱数によって結果が変わるため省略.
    """
    text = "I couldn't believe that I could actually understand " \
           "what I was reading : the phenomenal power of the human mind ."
    print(to_typoglycemia(text))


def main():
    test00()
    test01()
    test02()
    test03()
    test04()
    test05()
    test06()
    test07()
    test08()
    test09()


def test():
    doctest.testmod()
    unittest.main()


if __name__ == '__main__':
    main()
    test()

