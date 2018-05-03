from setuptools import setup

setup(
    name='asr_evaluation',
    version='2.0.3',
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
    },
    keywords=['word', 'error', 'rate', 'asr', 'speech', 'recognition'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License"
    ]
)
