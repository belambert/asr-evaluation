.PHONY: test

clean:
	python setup.py clean
	rm -f MANIFEST
	rm -rf dist
	rm -rf asr_evaluation.egg-info
	rm -rf build

test:
	python -m unittest discover test
