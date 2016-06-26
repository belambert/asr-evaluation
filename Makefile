.PHONY: test

clean:
	python setup.py clean
	rm -f MANIFEST
	rm -rf dist
	rm -rf asr_evaluation.egg-info
	rm -rf build
	find . -name *.pyc -exec rm -rf '{}' \;

doc:
	pydoc -w `find asr_evaluation -name '*.py'`

showdoc:
	pydoc asr_evaluation/*

# test:
# 	python -m unittest discover test
