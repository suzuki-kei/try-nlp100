#
# 言語処理100本ノック 2020 > 第2章: UNIXコマンド
# https://nlp100.github.io/ja/ch02.html
#

#
# 10. 行数のカウント
#
# 行数をカウントせよ. 確認には wc コマンドを用いよ.
#
function practice10 {
    if [[ ! -f popular-names.txt ]]; then
        curl -o popular-names.txt https://nlp100.github.io/data/popular-names.txt
    fi
    wc -l popular-names.txt
}

#
# 11. タブをスペースに置換
#
# タブ 1 文字につきスペース 1 文字に置換せよ.
# 確認には sed コマンド, tr コマンド, もしくは expand コマンドを用いよ.
#
function practice11 {
    cat popular-names.txt | tr -s '\t' ' '
}

#
# 12. 1 列目を col1.txt に, 2 列目を col2.txt に保存
#
# 各行の 1 列目だけを抜き出したものを col1.txt に,
# 2 列目だけを抜き出したものを col2.txt としてファイルに保存せよ.
# 確認には cut コマンドを用いよ.
#
function practice12 {
    cat popular-names.txt | cut -f1 > col1.txt
    cat popular-names.txt | cut -f2 > col2.txt
}

#
# 13. col1.txt と col2.txt をマージ
#
# 12 で作った col1.txt と col2.txt を結合し,
# 元のファイルの 1 列目と 2 列目をタブ区切りで並べたテキストファイルを作成せよ.
# 確認には paste コマンドを用いよ.
#
function practice13 {
    paste col1.txt col2.txt
}

#
# 14. 先頭からN行を出力
#
# 自然数 N をコマンドライン引数などの手段で受け取り,
# 入力のうち先頭の N 行だけを表示せよ.
# 確認には head コマンドを用いよ.
#
function practice14 {
    echo -n 'N = '
    read N
    head -n $N popular-names.txt
}

#
# 15. 末尾のN行を出力
#
# 自然数 N をコマンドライン引数などの手段で受け取り,
# 入力のうち末尾の N 行だけを表示せよ.
# 確認には tail コマンドを用いよ.
#
function practice15 {
    echo -n 'N = '
    read N
    tail -n $N popular-names.txt
}

#
# 16. ファイルを N 分割する
#
# 自然数 N をコマンドライン引数などの手段で受け取り,
# 入力のファイルを行単位で N 分割せよ.
# 同様の処理を split コマンドで実現せよ.
#
function practice16 {
    echo -n 'N = '
    read N
    split -n l/$N -d popular-names.txt _popular-names. --additional-suffix=.txt
}

#
# 17. 1 列目の文字列の異なり
#
# 1 列目の文字列の種類 (異なる文字列の集合) を求めよ.
# 確認には cut, sort, uniq コマンドを用いよ.
#
function practice17 {
    cat popular-names.txt | cut -f1 | sort | uniq
}

#
# 18. 各行を 3 コラム目の数値の降順にソート
#
# 各行を 3 コラム目の数値の逆順で整列せよ (注意: 各行の内容は変更せずに並び替えよ).
# 確認には sort コマンドを用いよ (この問題はコマンドで実行した時の結果と合わなくてもよい).
#
function practice18 {
    cat popular-names.txt | sort -k3 -nr
}

#
# 19. 各行の 1 コラム目の文字列の出現頻度を求め, 出現頻度の高い順に並べる.
#
function practice19 {
    cat popular-names.txt | cut -f1 | sort | uniq -c | sort -nr -k1 | awk '{print $2}'
}

