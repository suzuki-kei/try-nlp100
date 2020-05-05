# 言語処理100本ノック 2020

## 概要

以下に取り組む.

 * 言語処理100本ノック 2020 (https://nlp100.github.io/ja/)

## 事前準備

    # 第 2 章で使用するファイルをダウンロードする.
    curl -o popular-names.txt https://nlp100.github.io/data/popular-names.txt

    # 第 3 章で使用するファイルをダウンロードする.
    curl https://nlp100.github.io/data/jawiki-country.json.gz | gunzip > jawiki-country.json

## 実行方法

テストを実行するには `make test` とします.

    # テストを実行する.
    make test

各課題を実行するには `make run:<課題番号>` とします.

    # 課題 00 を実行する.
    make run:00

