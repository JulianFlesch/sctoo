#!/usr/bin/env python3

from collections import OrderedDict
from HTSeq import GenomicInterval


class GenomicBin(GenomicInterval):

    def __init__(self, name, count, chrom, start, end, *args, **kwargs):
        super().__init__(chrom, start, end)
        self.name = name
        self.count = count

    def __str__(self):
        return "GenomicBin({}:{}-{} {})".format(self.chrom, self.start,
                                                self.end, self.count)

    def as_csv_line(self, fields=["ID", "CHR", "START", "END", "COUNT"],
                    sep="\t"):

        fields = [f.upper() for f in fields]

        line = ("{}" + sep) * 4 + "{}"
        content = ["", "", "", "", ""]

        content[fields.index("ID")] = self.name
        content[fields.index("CHR")] = self.chrom
        content[fields.index("START")] = self.start
        content[fields.index("END")] = self.end
        content[fields.index("COUNT")] = self.count

        return line.format(*content)

    def as_bed_line(self):
        bed_template = "{}\t{}\t{}\t{}\t{}"
        return bed_template.format( self.chrom, self.start, self.end,
                                    self.name, self.count)

    @classmethod
    def bins_from_gene_intervals(cls, variants, gene_intervals):
        """
        Bin a list of variants with position and chromosome information,
        by a list of gene intervals with chromosome, start and end positions.

        Note: It is assumed that both the variants and intervals are ordered by
        Chromosome and (start-) position.
        """
        bins = []
        bin_idx = 0

        # we assume that variants are sorted, therefor we need to check every
        # element only once and can skip increasing parts of variants
        variants_idx = 0
        for gene_iv in gene_intervals:

            # default count value for every listed gene
            bins.append(cls(gene_iv.name, 0, gene_iv.chrom,
                            gene_iv.start, gene_iv.end))

            # count how many variants are in the current inteval
            for i in range(variants_idx, len(variants)):
                var_pos = variants[i]
                if gene_iv.contains(var_pos):
                    bins[bin_idx].count += 1
                else:
                    bin_idx += 1
                    variants_idx = i
                    break

        return bins
