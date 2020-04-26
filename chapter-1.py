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


if __name__ == '__main__':
    unittest.main()

