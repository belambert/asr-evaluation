from setuptools import setup
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

version='1.2.2'

setup(
    name='asr_evaluation',
    version=version,
    author='Ben Lambert',
    author_email='ben@benjaminlambert.com',
    packages=['asr_evaluation'],
    license='LICENSE.txt',
    description='Evaluating ASR (automatic speech recognition) hypotheses, i.e. computing word error rate.',
    long_description=long_description,
    install_requires=['edit_distance', 'termcolor'],
    test_suite='test.test.TestASREvaluation',
    entry_points={
        'console_scripts': [
            'evaluate.py = asr_evaluation.__main__:main'
        ]
    }
)
