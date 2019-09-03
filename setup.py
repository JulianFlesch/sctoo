import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sctoo",
    version="0.1",
    author="Julian Flesch",
    author_email="julianflesch@gmail.com",
    keywords="bioinformatics vcf binning type-of-origin",
    description="Single Cell Type of Origin Experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JulianFlesch/sctoo",
    project_urls={
        "Documentation": "https://github.com/JulianFlesch/sctoo",
        "Source": "https://github.com/JulianFlesch/sctoo"
        },
    packages=["sctoo"],
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "HTSeq"
        ],
    scripts=[
        "bin/sctoo"],
    classifiers=[
        "Topics :: Bioinformatics ::  Variant Binning and Modelling",
        ""
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI APPROVED :: MIT License",
        "Operating System :: LINUX",
    ],
)
