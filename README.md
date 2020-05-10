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

    # 第 2 章で使用するファイルをダウンロードする.
    mkdir -p data/chapter2
    curl -o data/chapter2/popular-names.txt https://nlp100.github.io/data/popular-names.txt

    # 第 3 章で使用するファイルをダウンロードする.
    mkdir -p data/chapter3
    curl https://nlp100.github.io/data/jawiki-country.json.gz | gunzip > data/chapter3/jawiki-country.json

    # テストデータを作成する.
    for name in イラク カンボジア マレーシア セントクリストファー・ネイビス; do
        cat data/chapter3/jawiki-country.json \
            | jq -r "select(.title == \"$name\") | .text" \
            > data/chapter3/jawiki-country.$name.txt
    done

## 実行方法

テストを実行するには `make test` とします.

    # テストを実行する.
    source virtualenv/bin/activate
    make test

各課題を実行するには `make run:<課題番号>` とします.

    # 課題 00 を実行する.
    source virtualenv/bin/activate
    make run:00

