#
# 言語処理100本ノック 2020 > 第3章: 正規表現
# https://nlp100.github.io/ja/ch01.html
#

from chapter2 import text_from_file
import doctest
import itertools
import json
import re
import typing
import unittest


def _load_documents():
    """
        本章で扱うドキュメントをロードする.

        Returns
        -------
        typing.List[dict]
            本性で扱うドキュメント.
            キーに 'title', 'text' を持つ dict のリスト.
    """
    text = text_from_file('jawiki-country.json')
    documents = map(json.loads, text.splitlines())
    return list(documents)


def match_category_line(line):
    pattern = re.compile('\[\[Category:(.+?)(:?\|.+)?\]\]')
    return pattern.fullmatch(line)


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
    text_from_document = lambda document: document['text']
    texts = map(text_from_document, documents)
    lines = itertools.chain(*map(str.splitlines, texts))
    category_lines = filter(match_category_line, lines)
    print('\n'.join(sorted(set(category_lines))))


def practice22():
    """
        22. カテゴリ名の抽出

        記事のカテゴリ名を (行単位ではなく名前で) 抽出せよ.
    """
    documents = _load_documents()
    text_from_document = lambda document: document['text']
    texts = map(text_from_document, documents)
    lines = itertools.chain(*map(str.splitlines, texts))
    category_lines = filter(match_category_line, lines)
    to_category_name = lambda line: match_category_line(line)[1]
    category_names = map(to_category_name, category_lines)
    print('\n'.join(sorted(set(category_names))))


def test():
    doctest.testmod()
    unittest.main()


if __name__ == '__main__':
    test()

