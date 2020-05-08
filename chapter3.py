#
# 言語処理100本ノック 2020 > 第3章: 正規表現
# https://nlp100.github.io/ja/ch01.html
#

from chapter2 import text_from_file
import doctest
import itertools
import json
import parameterized
import re
import regex
import typing
import unittest


def _load_documents() -> typing.List[dict]:
    """
        本章で扱うドキュメントをロードする.

        Returns
        -------
        typing.List[dict]
            本性で扱うドキュメント.
            キーに 'title', 'text' を持つ dict のリスト.

        Examples
        --------
        >>> documents = _load_documents()
        >>> documents[0]['title']
        'エジプト'
        >>> documents[0]['text'][:40]
        '{{otheruses|主に現代のエジプト・アラブ共和国|古代|古代エジプト}}'
    """
    text = text_from_file('jawiki-country.json')
    documents = map(json.loads, text.splitlines())
    return list(documents)


def text_from_document(
        document: dict,
    ) -> str:
    """
        ドキュメントから本文を取り出す.

        Arguments
        ---------
        document: dict
            ドキュメント.

        Returns
        -------
        text : str
            ドキュメントの本文.
    """
    return document['text']


def texts_from_documents(
        documents: typing.List[dict],
    ) -> typing.List[str]:
    """
        ドキュメントのリストを本文のリストに変換する.

        Arguments
        ---------
        documents : typing.List[dict]
            ドキュメントのリスト.

        Returns
        -------
        texts : typing.List[str]
            本文のリスト.
    """
    return list(map(text_from_document, documents))


def lines_from_documents(
        documents: typing.List[dict],
    ) -> typing.List[str]:
    """
        ドキュメントのリストを本文の行リストに変換する.

        Arguments
        ---------
        documents: typing.List[dict]
            ドキュメントのリスト.

        Returns
        -------
        lines : typing.List[str]
        各ドキュメントの本文を行リストに変換し,
        それをフラットに連結した 1 次元のリスト.
    """
    texts = texts_from_documents(documents)
    lines = itertools.chain(*map(str.splitlines, texts))
    return list(lines)


def match_category_line(
        line: str,
    ) -> typing.Optional[re.Match]:
    """
        カテゴリ行としてマッチさせる.

        Arguments
        ---------
        line : str
            行データ.

        Returns
        -------
        typing.Optional[re.Match]
            line がカテゴリ行の場合はマッチ結果.
            マッチしなかった場合は None.
    """
    pattern = re.compile('\[\[Category:(.+?)(:?\|.+)?\]\]')
    return pattern.fullmatch(line)


def match_section_line(
        line: str,
    ) -> typing.Optional[re.Match]:
    """
        セクション行としてマッチさせる.

        Arguments
        ---------
        line : str
            行データ.

        Returns
        -------
        typing.Optional[re.Match]
            line がセクション行の場合はマッチ結果.
            マッチしなかった場合は None.
    """
    pattern = re.compile(r'(?P<mark>=+) (.*) (?P=mark)')
    return pattern.fullmatch(line)


# '|key=value' にマッチするパターン.
PROPERTIES_TEXT_PATTERN = \
    re.compile(r'^ *\| *([^=]+?) *= *(.*) *', re.M)


class PropertiesTextPatternTestCase(unittest.TestCase):
    """
        PROPERTIES_TEXT_PATTERN のテストケース.
    """

    @parameterized.parameterized.expand([
        ('_イラク.txt', 44),
        ('_カンボジア.txt', 44),
        ('_マレーシア.txt', 46),
        ('_セントクリストファー・ネイビス.txt', 43),
    ])
    def test(self, file_path, property_count):
        text = text_from_file(file_path)
        matches = BASIC_INFORMATION_PATTERN.findall(text)
        basic_information_text = matches[0][1]
        pattern = re.compile(r'\A{{基礎情報 .+\n|}}\Z')

        properties_text = pattern.sub('', basic_information_text)
        properties = dict(PROPERTIES_TEXT_PATTERN.findall(properties_text))
        self.assertEqual(property_count, len(properties))


# '{{基礎情報 <name> ...}}' にマッチするパターン.
# NOTE: 再帰的マッチを行うため re ではなく regex を使用する.
BASIC_INFORMATION_PATTERN = \
    regex.compile(r'(?={{基礎情報 (.+)\n)(?P<_>{(?:[^{}]+|(?&_))*})')


class BasicInformationPatternTestCase(unittest.TestCase):
    """
        BASIC_INFORMATION_PATTERN のテストケース.
    """

    @parameterized.parameterized.expand([
        '_イラク.txt',
        '_カンボジア.txt',
        '_マレーシア.txt',
        '_セントクリストファー・ネイビス.txt',
    ])
    def test(self, file_path):
        text = text_from_file(file_path)
        matches = BASIC_INFORMATION_PATTERN.findall(text)
        self.assertEqual(1, len(matches))
        match = matches[0]
        self.assertEqual(2, len(match))
        self.assertEqual('国', match[0])
        self.assertTrue(match[1].startswith('{{基礎情報'))
        self.assertTrue(match[1].endswith('}}'))


def basic_information_from_text(
        text: str,
    ) -> typing.Dict[str, typing.Dict[str, str]]:
    """
        テキストから基礎情報を抽出する.

        Arguments
        ---------
        text : str
            テキスト.

        Returns
        -------
        basic_information : typing.Dict[str, typing.Dict[str, str]]
            キーに基礎情報の名称, 値に基礎情報のプロパティ情報.
            プロパティ情報はキーがプロパティ名, 値がプロパティ値である辞書.
    """
    def properties_from_basic_information_text(basic_information_text):
        pattern = re.compile(r'\A{{基礎情報 .+\n|}}\Z')
        properties_text = pattern.sub('', basic_information_text)
        return dict(PROPERTIES_TEXT_PATTERN.findall(properties_text))

    return {
        name: properties_from_basic_information_text(basic_information_text)
        for name, basic_information_text
        in BASIC_INFORMATION_PATTERN.findall(text)
    }


def practice20():
    """
        20. JSONデータの読み込み

        Wikipedia 記事の JSON ファイルを読み込み, 「イギリス」に関する記事本文
        を表示せよ. 問題 21-29 では, ここで抽出した記事本文に対して実行せよ.
    """
    documents = _load_documents()
    is_england = lambda document: 'イギリス' in document['title']

    for document in filter(is_england, documents):
        print(document['text'])


def practice21():
    """
        21. カテゴリ名を含む行を抽出

        記事中でカテゴリ名を宣言している行を抽出せよ.
    """
    documents = _load_documents()
    lines = lines_from_documents(documents)
    category_lines = filter(match_category_line, lines)
    print('\n'.join(sorted(set(category_lines))))


def practice22():
    """
        22. カテゴリ名の抽出

        記事のカテゴリ名を (行単位ではなく名前で) 抽出せよ.
    """
    documents = _load_documents()
    lines = lines_from_documents(documents)
    category_line_matches = filter(None, map(match_category_line, lines))
    category_names = map(lambda matched: matched[1], category_line_matches)
    print('\n'.join(sorted(set(category_names))))


def practice23():
    """
        23. セクション構造

        記事中に含まれるセクション名とそのレベル (例えば "== セクション名 =="
        なら 1) を表示せよ.
    """
    documents = _load_documents()
    lines = lines_from_documents(documents)
    section_line_matches = filter(None, map(match_section_line, lines))
    section_level_name_pairs = {
        (len(match[1]), match[2])
        for match in section_line_matches
    }
    sorted_section_level_name_pairs = sorted(
        map(list, section_level_name_pairs), reverse=True)
    for level, name in sorted_section_level_name_pairs:
        print('{}) {}'.format(level, name))


def practice24():
    """
        24. ファイル参照の抽出

        記事から参照されているメディアファイルをすべて抜き出せ.
    """
    documents = _load_documents()
    text = ''.join(texts_from_documents(documents))
    pattern = re.compile(r'\[\[ファイル:(.+?)(:?\|.+)\]\]')

    for name, _ in pattern.findall(text):
        print(name)


def practice25():
    """
        25. テンプレートの抽出

        記事中に含まれる「基礎情報」テンプレートのフィールド名と値を抽出し,
        辞書オブジェクトとして格納せよ.
    """
    documents = _load_documents()

    for document in documents:
        basic_information = basic_information_from_text(document['text'])
        print('==== {}'.format(document['title']))
        print(basic_information)


def test():
    doctest.testmod()
    unittest.main()


if __name__ == '__main__':
    test()

