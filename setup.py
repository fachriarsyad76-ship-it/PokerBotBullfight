from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="poker-bot-bullfight",
    version="0.1.0",
    author="Fachri Arsyad",
    author_email="fachriarsyad76@gmail.com",
    description="Advanced Poker Bot with GTO Strategy, Hand Evaluator & GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fachriarsyad76-ship-it/PokerBotBullfight",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.9",
    install_requires=[
        "phevaluator>=0.3.1",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "PyQt6>=6.5.0",
        "scipy>=1.10.0",
    ],
)
