#
# 言語処理100本ノック 2020 > 第1章: 準備運動
# https://nlp100.github.io/ja/ch01.html
#

import unittest

class Chapter1TestCase(unittest.TestCase):

    def test00(self):
        """
            00. 文字列の逆順

            文字列”stressed”の文字を逆に（末尾から先頭に向かって）並べた文字列を得よ．
        """
        s = 'stressed'
        answer = s[::-1]
        self.assertEqual('desserts', answer)

    def test01(self):
        """
            01. 「パタトクカシーー」

            「パタトクカシーー」という文字列の1,3,5,7文字目を取り出して連結した文字列を得よ．
        """
        s = 'パタトクカシーー'
        answer = ''.join(map(lambda i: s[i - 1], (1, 3, 5, 7)))
        self.assertEqual('パトカー', answer)

    def test02(self):
        """
            02. 「パトカー」＋「タクシー」＝「パタトクカシーー」

            「パトカー」＋「タクシー」の文字を先頭から交互に連結して文字列「パタトクカシーー」を得よ．
        """
        s1 = 'パトカー'
        s2 = 'タクシー'
        answer = ''.join(map(''.join, zip(s1, s2)))
        self.assertEqual('パタトクカシーー', answer)


if __name__ == '__main__':
    unittest.main()

