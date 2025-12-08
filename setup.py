from setuptools import setup, find_packages

setup(
    name="rrs",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "lark",
        "litemapy"
    ],
    entry_points={
        "console_scripts": [
            "rrs=rrs.cli:main",
        ],
    },
)
