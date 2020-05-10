#!/bin/bash

set -eu

DATA_DIR=./data
mkdir -p "${DATA_DIR}"

function prepare_chapter2_data {
    if [[ ! -f "${DATA_DIR}/popular-names.txt" ]]; then
        curl -o "${DATA_DIR}/popular-names.txt" \
            'https://nlp100.github.io/data/popular-names.txt'
    fi
}
prepare_chapter2_data

function prepare_chapter3_data {
    if [[ ! -f "${DATA_DIR}/jawiki-country.json" ]]; then
        curl 'https://nlp100.github.io/data/jawiki-country.json.gz' \
            | gunzip \
            > "${DATA_DIR}/jawiki-country.json"
    fi

    names=(
        'イラク'
        'カンボジア'
        'マレーシア'
        'セントクリストファー・ネイビス'
    )
    for name in "${names[@]}"; do
        cat "${DATA_DIR}/jawiki-country.json" \
            | jq -r "select(.title == \"$name\") | .text" \
            > "${DATA_DIR}/jawiki-country.${name}.txt"
    done
}
prepare_chapter3_data

