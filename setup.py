from setuptools import setup

setup(
    name='asr_evaluation',
    version='0.1.0',
    author='Ben Lambert',
    author_email='ben@benjaminlambert.com',
    packages=['asr_evaluation'],
    license='LICENSE.txt',
    description='Evaluating ASR (automatic speech recognitiuon) hypotheses, i.e. computing word error rate.',
    long_description=open('README.md').read(),
    install_requires=['edit_distance'],
)
