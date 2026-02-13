from setuptools import setup, find_packages

setup(
    name="teleport-cli",
    version="0.1.1",
    description="A cross-platform CLI tool for smart directory navigation",
    author="Huseyin Acikgoz",
    author_email="huseyin@huseyinacikgoz.com.tr",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "typer>=0.9.0",
        "questionary>=2.0.0",
        "rapidfuzz>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "teleport-core=teleport.cli:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
