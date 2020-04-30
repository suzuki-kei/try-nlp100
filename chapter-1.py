#
# 言語処理100本ノック 2020 > 第1章: 準備運動
# https://nlp100.github.io/ja/ch01.html
#

import re
import unittest


def _to_words(text):
    pattern = re.compile(r'[a-zA-Z]+')
    return pattern.findall(text)


class ToWordsTestCase(unittest.TestCase):

    def test(self):
        self.assertEqual([], _to_words(''))
        self.assertEqual(['a'], _to_words('a'))
        self.assertEqual(['a'], _to_words(' a '))
        self.assertEqual(
            ['It', 's', 'a', 'fine', 'day'],
            _to_words("It's a fine day!"))
        self.assertEqual(
            ['My', 'name', 'is', 'Jane', 'Due'],
            _to_words('My name is Jane Due.'))


def _generate_ngram_from_word(n, word):
    if len(word) < n:
        return
    for i in range(len(word) - n + 1):
        yield word[i : i + n]


def _generate_ngram_from_words(n, words):
    for word in words:
        yield from _generate_ngram_from_word(n, word)


def _generate_ngram_from_text(n, text):
    s = ''.join(_to_words(text))
    yield from _generate_ngram_from_word(n, s)


class Chapter1TestCase(unittest.TestCase):

    def test00(self):
        """
            00. 文字列の逆順

            文字列 "stressed" の文字を逆に（末尾から先頭に向かって）並べた文字列
            を得よ．
        """
        s = 'stressed'
        answer = s[::-1]
        self.assertEqual('desserts', answer)

    def test01(self):
        """
            01. 「パタトクカシーー」

            「パタトクカシーー」という文字列の1,3,5,7文字目を取り出して連結した
            文字列を得よ．
        """
        s = 'パタトクカシーー'
        answer = ''.join(map(lambda i: s[i - 1], (1, 3, 5, 7)))
        self.assertEqual('パトカー', answer)

    def test02(self):
        """
            02. 「パトカー」＋「タクシー」＝「パタトクカシーー」

            「パトカー」＋「タクシー」の文字を先頭から交互に連結して文字列「パタ
            トクカシーー」を得よ．
        """
        s1 = 'パトカー'
        s2 = 'タクシー'
        answer = ''.join(map(''.join, zip(s1, s2)))
        self.assertEqual('パタトクカシーー', answer)

    def test03(self):
        """
            03. 円周率

            "Now I need a drink, alcoholic of course, after the heavy lectures 
            involving quantum mechanics." という文を単語に分解し，各単語の（アル
            ファベットの）文字数を先頭から出現順に並べたリストを作成せよ．
        """
        s = 'Now I need a drink, alcoholic of course, ' \
            'after the heavy lectures involving quantum mechanics.'
        words = _to_words(s)
        answer = list(map(len, words))
        self.assertEqual([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9], answer)

    def test04(self):
        """
            04. 元素記号

            "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations 
            Might Also Sign Peace Security Clause. Arthur King Can." という文を
            単語に分解し，1, 5, 6, 7, 8, 9, 15, 16, 19番目の単語は先頭の1文字，
            それ以外の単語は先頭に2文字を取り出し，取り出した文字列から単語の位
            置（先頭から何番目の単語か）への連想配列（辞書型もしくはマップ型）を
            作成せよ．
        """
        def index_to_chars(index):
            if index in [1, 5, 6, 7, 8, 9, 15, 16, 19]:
                return 1
            else:
                return 2

        s = 'Hi He Lied Because Boron Could Not Oxidize Fluorine. ' \
            'New Nations Might Also Sign Peace Security Clause. Arthur King Can.'
        words = _to_words(s)
        answer = {
            i: words[i - 1][:index_to_chars(i)]
            for i in range(1, len(words) + 1)
        }
        expected = {
            1: 'H',
            2: 'He',
            3: 'Li',
            4: 'Be',
            5: 'B',
            6: 'C',
            7: 'N',
            8: 'O',
            9: 'F',
            10: 'Ne',
            11: 'Na',
            12: 'Mi',
            13: 'Al',
            14: 'Si',
            15: 'P',
            16: 'S',
            17: 'Cl',
            18: 'Ar',
            19: 'K',
            20: 'Ca',
        }
        self.assertEqual(expected, answer)

    def test05(self):
        """
            05. n-gram

            与えられたシーケンス（文字列やリストなど）からn-gramを作る関数を作成
            せよ．この関数を用い，"I am an NLPer" という文から単語bi-gram，文字
            bi-gramを得よ．
        """
        s = 'I am an NLPer'

        word_2gram = list(_generate_ngram_from_words(2, _to_words(s)))
        self.assertEqual(
            ['am', 'an', 'NL', 'LP', 'Pe', 'er'],
            word_2gram)

        text_2gram = list(_generate_ngram_from_text(2, s))
        self.assertEqual(
            ['Ia', 'am', 'ma', 'an', 'nN', 'NL', 'LP', 'Pe', 'er'],
            text_2gram)

    def test06(self):
        """
            06. 集合

            "paraparaparadise" と "paragraph" に含まれる文字bi-gramの集合を，
            それぞれ, XとYとして求め，XとYの和集合，積集合，差集合を求めよ．
            さらに，'se' というbi-gramがXおよびYに含まれるかどうかを調べよ．
        """
        x = set(_generate_ngram_from_text(2, 'paraparaparadise'))
        self.assertSetEqual({'pa', 'ar', 'ra', 'ap', 'ad', 'di', 'is', 'se'}, x)

        y = set(_generate_ngram_from_text(2, 'paragraph'))
        self.assertSetEqual({'pa', 'ar', 'ra', 'ag', 'gr', 'ap', 'ph'}, y)

        # 和集合
        self.assertSetEqual(
            {'pa', 'ar', 'ra', 'ap', 'ad', 'di', 'is', 'se', 'ag', 'gr', 'ph'},
            x | y)

        # 積集合
        self.assertSetEqual({'pa', 'ar', 'ra', 'ap'}, x & y)

        # 差集合 (x - y)
        self.assertSetEqual({'ad', 'di', 'is', 'se'}, x - y)

    def test07(self):
        """
            07. テンプレートによる文生成

            引数x, y, zを受け取り「x時のyはz」という文字列を返す関数を実装せよ．
            さらに，x=12, y=”気温”, z=22.4として，実行結果を確認せよ．
        """
        def f(x, y, z):
            return '{}時の{}は{}'.format(x, y, z)

        self.assertEqual('12時の気温は22.4', f(12, '気温', 22.4))

    def test08(self):
        """
            08. 暗号文

            与えられた文字列の各文字を，以下の仕様で変換する関数cipherを実装せ
            よ．

             * 英小文字ならば(219 - 文字コード)の文字に置換
             * その他の文字はそのまま出力

            この関数を用い，英語のメッセージを暗号化・復号化せよ．
        """
        def cipher(text):
            def convert(c):
                if c in range(ord('a'), ord('z') + 1):
                    return 219 - c
                else:
                    return c
            return ''.join(map(chr, map(convert, map(ord, text))))

        # empty string
        self.assertEqual('', cipher(''))

        # ASCII only
        self.assertEqual(
            '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10' \
            '\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !' \
            '"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]' \
            '^_`zyxwvutsrqponmlkjihgfedcba{|}~\x7f',
            cipher(
                '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f' \
                '\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e' \
                '\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUV' \
                'WXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'))

        # both ASCII and multibyte
        self.assertEqual(
            'zyxDEFｇｈｉＪＫＬ',
            cipher('abcDEFｇｈｉＪＫＬ'))


if __name__ == '__main__':
    unittest.main()

