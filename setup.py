from setuptools import setup

setup(
    name="dfm",
    version="0.1",
    py_modules=["dfm"],
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        dfm=dfm:dfm
    """,
)