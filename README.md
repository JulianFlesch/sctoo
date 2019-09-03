# Single Cell Type of Origin

## Install

This package uses Python3 and a number of third party packages.
It is recommended to set up and activate a virtualenv to contain the
dependencies by running:
```
virtualenv --python=python3 sctoo-venv
source sctoo-venv/bin/activate
```

Installation has to be done manually with the `setup.py` script.
```
python setup.py build sdist
pip install dist/sctoo-0.1.tar.gz
```

## Variant Binning

Example use case 1: Bin all varscan2 annotated somatic variants in
data/varscan.somatic.snp.vcf according to the intervals defined by
data/gene_intervals.bed and print them to the command line in bed format.
```
sctoo binner --variants data/varscan.somatic.snp.vcf --intervals data/gene_intervals.bed --only-somatic
```

Example use case 2: Bin all variants in data/varscan.somatic.snp.vcf according
to the intervals defined in data/gene_intervals.bed and write them to the file
binned_variants.bed.
```
sctoo binner --variants data/varscan.somatic.indel.vcf --intervals data/gene_intervals.bed --out binned_variants.bed
```

# Fitting a Linear Model

No comman line utilities for fitting linear models, yet.
