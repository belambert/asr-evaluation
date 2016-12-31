from setuptools import setup

setup(
    name='asr_evaluation',
    version='0.2.3',
    author='Ben Lambert',
    author_email='ben@benjaminlambert.com',
    packages=['asr_evaluation'],
    license='LICENSE.txt',
    description='Evaluating ASR (automatic speech recognition) hypotheses, i.e. computing word error rate.',
    install_requires=['edit_distance', 'termcolor', 'matplotlib'],
    scripts=['bin/evaluate.py']
)
