from distutils.core import setup

setup(
    name='asr_evaluation',
    version='0.1.0',
    author='Benjamin Lambert',
    author_email='ben@benjaminlambert.com',
    packages=['asr_evaluation'],
    license='LICENSE.txt',
    description='Evaluating ASR (automatic speech recognitiuon) hypotheses, i.e. computing word error rate.',
    long_description=open('README.txt').read(),
    install_requires=['editdistance'],
)
