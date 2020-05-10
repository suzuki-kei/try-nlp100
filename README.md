# 言語処理100本ノック 2020

## 概要

以下に取り組む.

 * 言語処理100本ノック 2020 (https://nlp100.github.io/ja/)

## 事前準備

    # virtualenv をセットアップする.
    pip install virtualenv
    virtualenv --python=python3 virtualenv
    source virtualenv/bin/activate
    pip install -r requirements.txt

    # データファイルを準備する.
    bash prepare-data.sh

## 実行方法

テストを実行するには `make test` とします.

    # テストを実行する.
    source virtualenv/bin/activate
    make test

各課題を実行するには `make run:<課題番号>` とします.

    # 課題 00 を実行する.
    source virtualenv/bin/activate
    make run:00

