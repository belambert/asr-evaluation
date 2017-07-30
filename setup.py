from setuptools import setup

version='2.0.1'

setup(
    name='asr_evaluation',
    version=version,
    author='Ben Lambert',
    author_email='ben@benjaminlambert.com',
    packages=['asr_evaluation'],
    license='LICENSE.txt',
    description='Evaluating ASR (automatic speech recognition) hypotheses, i.e. computing word error rate.',
    install_requires=['edit_distance', 'termcolor'],
    test_suite='test.test.TestASREvaluation',
    entry_points={
        'console_scripts': [
            'wer = asr_evaluation.__main__:main'
        ]
    }
)
