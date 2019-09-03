#!/usr/bin/env python3.7

from .cli import parse_args
from .binner import GenomicBin
from .parser import GeneInterval, VariantPosition, intervals_to_bed
#from models import LinearModel, RandomForest
import pandas as pd


def load_data():

    # input files
    everything_file = "data/DataKinam.dat"
    snp_file = "data/varscan.somatic.snp.vcf"
    gene_intervals_file = "data/gene_intervals.csv"
    expression_levels_file = "data/expression_levels.csv"

    # parse and load the different input files to python representations
    expr_levels = pd.read_csv(expression_levels_file, header=0)
    expr_levels = expr_levels.set_index("gene_name")
    expr_levels = expr_levels.drop(expr_levels.columns[0], axis=1)
    gene_bins = GeneInterval.intervals_from_csv(gene_intervals_file)
    snp_positions = VariantPosition.somatic_variants_from_vcf(snp_file)


def main():
    # parse the command line arguments
    job = parse_args()

    if job.subcommand == "binner":
        intervals = GeneInterval.intervals_from_bed(job.intervals)
        if job.only_somatic:
            variants = VariantPosition.somatic_variants_from_vcf(job.variants)
        else:
            variants = VariantPosition.variants_from_vcf(job.variants)

        bins = GenomicBin.bins_from_gene_intervals( variants=variants,
                                                    gene_intervals=intervals)

        if job.out:
            intervals_to_bed(bins, job.out)
        else:
            for iv in bins:
                print(iv.as_bed_line())

    if job.subcommand == "lin-coeff":
        pass


if __name__ == "__main__":
    main()
