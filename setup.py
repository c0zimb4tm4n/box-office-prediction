import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="box-office-prediction",
    version="1.0",
    author="Rohit Chandiramani",
    author_email="rohitch@uw.edu",
    description="Tool aiming to predict box office of hypothetical movie based on cast & crew",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/c0zimb4tm4n/box-office-prediction",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
