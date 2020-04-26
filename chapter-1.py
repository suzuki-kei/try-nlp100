#
# 言語処理100本ノック 2020 > 第1章: 準備運動
# https://nlp100.github.io/ja/ch01.html
#

import re
import unittest


def _to_words(text):
    pattern = re.compile(r'[a-zA-Z]+')
    return pattern.findall(text)


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


if __name__ == '__main__':
    unittest.main()

