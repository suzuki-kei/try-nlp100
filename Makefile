
.DEFAULT_GOAL := test

test:
	python -B chapter1.py
	python -B chapter2.py
	python -B chapter3.py

# 実行されたルール名から章番号と課題番号を特定し, 変数に設定する.
run\:%: \
	chapter_no = $(shell expr `echo $@ | sed -E 's/^[^0-9]+|[0-9][^0-9]*$$//g'` + 1)
	chapter_name = chapter$(chapter_no)
	practice_no = $(shell echo $@ | sed -E 's/[^0-9]+//g')
	practice_name = practice$(practice_no)

run\:%.sh:
	@(source $(chapter_name).sh && cd data/chapter2 && $(practice_name))

run\:%:
	python -B run.py --chapter=$(chapter_no) --practice=$(practice_no)

