#
# 言語処理100本ノック 2020 > 第3章: 正規表現
# https://nlp100.github.io/ja/ch01.html
#

from chapter2 import text_from_file
import doctest
import functools
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
    text = text_from_file('data/chapter3/jawiki-country.json')
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
        ('data/chapter3/jawiki-country.イラク.txt', 44),
        ('data/chapter3/jawiki-country.カンボジア.txt', 44),
        ('data/chapter3/jawiki-country.マレーシア.txt', 46),
        ('data/chapter3/jawiki-country.セントクリストファー・ネイビス.txt', 43),
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
        'data/chapter3/jawiki-country.イラク.txt',
        'data/chapter3/jawiki-country.カンボジア.txt',
        'data/chapter3/jawiki-country.マレーシア.txt',
        'data/chapter3/jawiki-country.セントクリストファー・ネイビス.txt',
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


def print_basic_information(
        basic_information: typing.Dict[str, typing.Dict[str, str]],
        indent: str='    ',
    ) -> None:
    """
        基礎情報を含む辞書を表示する.

        Arguments
        ---------
        basic_information : typing.Dict[str, typing.Dict[str, str]
            基礎情報を含む辞書.
        indent: str
            インデントに使用する文字列.
    """
    print('基礎情報')

    if not basic_information:
        print('{}{}'.format(indent * 1, 'None'))
        return

    for name, properties in basic_information.items():
        print('{}{}'.format(indent * 1, name))
        for key, value in properties.items():
            print('{}{} = {}'.format(indent * 2, key, value))


def markdown_enphasis(
        text: str,
    ) -> str:
    """
        MediaWiki の強調マークアップを通常テキストに置換する.

        Arguments
        ---------
        text : str
            テキスト.

        Returns
        -------
        str
            強調マークアップを通常テキストに置換した文字列.

        Examples
        --------
        >>> markdown_enphasis('aaa "bbb" ccc')
        'aaa bbb ccc'
        >>> markdown_enphasis('aaa ""bbb"" ccc')
        'aaa bbb ccc'
        >>> markdown_enphasis('aaa \"\"\"bbb\"\"\" ccc')
        'aaa bbb ccc'
    """
    pattern = re.compile(r'(<[^>]+>|{[^}]+})|(?P<mark>"{1,3})([^"]+)(?P=mark)')
    return pattern.sub('\\1\\3', text)


class MarkdownEnphasisTestCase(unittest.TestCase):
    """
        markdown_enphasis() のテストケース.
    """

    def test(self):
        # 空文字列を渡した場合.
        text = ''
        expected = text
        self.assertEqual(expected, markdown_enphasis(text))

        # マークアップを含まない場合.
        text = 'abc'
        expected = text
        self.assertEqual(expected, markdown_enphasis(text))

        # 強調マークアップを含む場合.
        text = '0: zero, 1: "one", 2: ""two"", 3: """three"""'
        expected = '0: zero, 1: one, 2: two, 3: three'
        self.assertEqual(expected, markdown_enphasis(text))

        # 内部リンクを含む場合.
        text = 'aaa [[記事名]] bbb [[記事名#節名]] ccc [[記事名|表示文字]] ddd [[記事名#節名|表示文字]] eee'
        expected = text
        self.assertEqual(expected, markdown_enphasis(text))

        # 外部リンクを含む場合.
        text = '[http://www.example.com 外部リンク]'
        expected = text
        self.assertEqual(expected, markdown_enphasis(text))

        # タグを含む場合.
        text = '注記 = <references group="注"/>註1: 人口、及び各種GDPの数値'
        expected = text
        self.assertEqual(expected, markdown_enphasis(text))

        # テンプレートを含む場合.
        text = '注記 = {{Reflist|group="注釈"}}'
        expected = text
        self.assertEqual(expected, markdown_enphasis(text))

        # ファイルを含む場合.
        text = '[[ファイル:Wikipedia-logo-v2-ja.png|thumb|説明文]]'
        expected = text
        self.assertEqual(expected, markdown_enphasis(text))

        # ファイルを含む場合.
        text = '[[File:Wikipedia-logo-v2-ja.png|thumb|説明文]]'
        expected = text
        self.assertEqual(expected, markdown_enphasis(text))

        # カテゴリを含む場合.
        text = '[[Category:ヘルプ|はやみひよう]]'
        expected = text
        self.assertEqual(expected, markdown_enphasis(text))


def markdown_internal_links(
        text: str,
    ) -> str:
    """
        MediaWiki の内部リンクを通常テキストに置換する.

        Arguments
        ---------
        text : str
            テキスト.

        Returns
        -------
        str
            内部リンクを通常テキストに置換した文字列.

        Examples
        --------
        >>> markdown_internal_links('[[記事名]]')
        '記事名'
        >>> markdown_internal_links('[[記事名|表示テキスト]]')
        '表示テキスト'
    """
    pattern = re.compile(r'\[\[(?!ファイル:|File:|Category:|]])(?:[^|\]]+\|([^\]]+?)|([^\]]+?))]]')
    return pattern.sub('\\1\\2', text)


class MarkdownInternalLinksTestCase(unittest.TestCase):
    """
        markdown_internal_links() のテストケース.
    """

    def test(self):
        # 空文字列を渡した場合.
        text = ''
        expected = text
        self.assertEqual(expected, markdown_internal_links(text))

        # マークアップを含まない場合.
        text = 'abc'
        expected = text
        self.assertEqual(expected, markdown_internal_links(text))

        # 強調マークアップを含む場合.
        text = '0: zero, 1: "one", 2: ""two"", 3: """three"""'
        expected = text
        self.assertEqual(expected, markdown_internal_links(text))

        # 内部リンクを含む場合.
        text = 'aaa [[記事名]] bbb [[記事名#節名]] ccc [[記事名|表示文字]] ddd [[記事名#節名|表示文字]] eee'
        expected = 'aaa 記事名 bbb 記事名#節名 ccc 表示文字 ddd 表示文字 eee'
        self.assertEqual(expected, markdown_internal_links(text))

        # 外部リンクを含む場合.
        text = '[http://www.example.com 外部リンク]'
        expected = text
        self.assertEqual(expected, markdown_internal_links(text))

        # タグを含む場合.
        text = '注記 = <references group="注"/>註1: 人口、及び各種GDPの数値'
        expected = text
        self.assertEqual(expected, markdown_internal_links(text))

        # テンプレートを含む場合.
        text = '注記 = {{Reflist|group="注釈"}}'
        expected = text
        self.assertEqual(expected, markdown_internal_links(text))

        # ファイルを含む場合.
        text = '[[ファイル:Wikipedia-logo-v2-ja.png|thumb|説明文]]'
        expected = text
        self.assertEqual(expected, markdown_internal_links(text))

        # ファイルを含む場合.
        text = '[[File:Wikipedia-logo-v2-ja.png|thumb|説明文]]'
        expected = text
        self.assertEqual(expected, markdown_internal_links(text))

        # カテゴリを含む場合.
        text = '[[Category:ヘルプ|はやみひよう]]'
        expected = text
        self.assertEqual(expected, markdown_internal_links(text))


def markdown_file(
        text: str,
    ) -> str:
    """
        MediaWiki のファイルのマークアップを通常テキストに置換する.

        Arguments
        ---------
        text : str
            テキスト.

        Returns
        -------
        str
            ファイルのマークアップを通常テキストに置換した文字列.

        Examples
        --------
        >>> markdown_file('[[File:a.png]]')
        'a.png'
        >>> markdown_file('[[ファイル:a.png]]')
        'a.png'
    """
    pattern = re.compile(r'\[\[(?:File|ファイル):([^|\]+)(?:[^\]]*?)]]')
    return pattern.sub('\\1', text)


class MarkdownFileTestCase(unittest.TestCase):
    """
        markdown_file() のテストケース.
    """
    # TODO テストを書く.


def markdown_category(
        text: str,
    ) -> str:
    """
        MediaWiki のカテゴリのマークアップを通常テキストに置換する.

        Arguments
        ---------
        text : str
            テキスト.

        Returns
        -------
        str
            カテゴリのマークアップを通常テキストに置換した文字列.

        Examples
        --------
        >>> markdown_category('[[Category:ヘルプ|はやみひよう]]')
        'はやみひよう'
    """
    pattern = re.compile(r'\[\[Category:[^|\]]+\|([^\]]+?)]]')
    return pattern.sub('\\1', text)


class MarkdownCategoryTestCase(unittest.TestCase):
    """
        markdown_category() のテストケース.
    """
    # TODO テストを書く.


def markdown(
        text: str,
    ) -> str:
    """
        MediaWiki のマークアップを通常テキストに置換する.

        Arguments
        ---------
        text : str
            テキスト.

        Returns
        -------
        str
            マークアップを通常テキストに置換した文字列.
    """
    markdown_functions = [
        markdown_enphasis,
        markdown_internal_links,
        markdown_file,
        markdown_category,
    ]

    def reducer(text, markdown_function):
        return markdown_function(text)

    return functools.reduce(reducer, markdown_functions, text)


class MarkdownTestCase(unittest.TestCase):
    """
        markdown() のテストケース.
    """
    # TODO テストを書く.


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
        title, text = document['title'], document['text']
        print('==== {}'.format(title))
        basic_information = basic_information_from_text(text)
        print_basic_information(basic_information)


def practice26():
    """
        26. 強調マークアップの除去

        25 の処理時に, テンプレートの値から MediaWiki の強調マークアップ (弱い
        強調, 強調, 強い強調のすべて) を除去してテキストに変換せよ (参考: マー
        クアップ早見表).

         * マークアップ早見表
           https://ja.wikipedia.org/wiki/Help:%E6%97%A9%E8%A6%8B%E8%A1%A8
    """
    documents = _load_documents()

    for document in documents:
        title, text = document['title'], document['text']
        print('==== {}'.format(title))
        text = markdown_enphasis(text)
        basic_information = basic_information_from_text(text)
        print_basic_information(basic_information)


def practice27():
    """
        27. 内部リンクの除去

        26 の処理に加えて, テンプレートの値から MediaWiki の内部リンクマークア
        ップを除去し, テキストに変換せよ (参考: マークアップ早見表).

         * マークアップ早見表
           https://ja.wikipedia.org/wiki/Help:%E6%97%A9%E8%A6%8B%E8%A1%A8
    """
    documents = _load_documents()

    for document in documents:
        title, text = document['title'], document['text']
        print('==== {}'.format(title))
        text = markdown_enphasis(text)
        text = markdown_internal_links(text)
        basic_information = basic_information_from_text(text)
        print_basic_information(basic_information)


def practice28():
    """
        28. MediaWiki マークアップの除去

        27 の処理に加えて, テンプレートの値から MediaWiki マークアップを可能な
        限り除去し, 国の基本情報を整形せよ.
    """
    documents = _load_documents()

    for document in documents:
        title, text = document['title'], document['text']
        print('==== {}'.format(title))
        text = markdown(text)
        basic_information = basic_information_from_text(text)
        print_basic_information(basic_information)


def test():
    doctest.testmod()
    unittest.main()


if __name__ == '__main__':
    test()

