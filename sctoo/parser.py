#!/usr/bin/env python3.7

import os
import csv
import rpy2.robjects as robjects
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri
from HTSeq import VCF_Reader, BED_Reader, GenomicInterval, GenomicPosition


# Column names used by default in csv and bed files
CSV_FIELDS = ("ID", "CHR", "START", "END")
BED_FIELDS = ("CHR", "START", "END", "ID")


def rdf_to_pandas(rdf_file):
    """
    Load a R Dataframe object file and convert it into a pandas representation

    Parameters
    ----------
    rdf_file : string
        `rdf_file` is interpreted as a path to an R datafile containing a dataframe.

    Returns
    -------
    pandas.DataFrame
        `pandas` representation of the R Dataframe
    """

    if not os.path.exists(rdf_file):
        print("[!] Could not locate file {}".format(rdf_file))
        return None

    rdf = robjects.r.load(rdf_file)

    with localconverter(robjects.default_converter + pandas2ri.converter):
        df = robjects.conversion.rpy2py(robjects.r[rdf[0]])

    return df


def intervals_to_csv(intervals, filename, fields=None):
    fields = CSV_FIELDS if not fields else fields
    with open(filename, "w") as csv_file:
        for iv in intervals:
            csv_file.write(iv.as_csv_line(fields))
            # TODO: make this windows compatible
            csv_file.write("\n")


def intervals_to_bed(intervals, filename, fields=None):
    fields = BED_FIELDS if not fields else fields
    with open(filename, "w") as bed_file:
        for iv in intervals:
            bed_file.write(iv.as_bed_line())
            # TODO: make this windows compatible
            bed_file.write("\n")


class VariantPosition(GenomicPosition):

    def __init__(self, name, ref, alt, chrom, pos, type):
        super().__init__(chrom, pos)
        self.name = name
        self.ref = ref
        self.alt = alt
        self.type = type

    def __str__(self):
        return "VariantPosition({}:{} {}/{})".format(   self.chrom, self.pos,
                                                        self.ref, self.alt)

    @classmethod
    def somatic_variants_from_vcf(cls, vcf_file):

        reader = VCF_Reader(vcf_file)
        reader.parse_meta()
        reader.make_info_dict()

        # filter non-somatic mutations
        def var_filter(var):
            var.unpack_info(reader.infodict)
            return var.info.get("SOMATIC")

        somatic_variants = cls.variants_from_vcf(   vcf_file, reader=reader,
                                                    var_filter=var_filter)
        return somatic_variants

    @classmethod
    def variants_from_vcf(  cls,
                            vcf_file,
                            var_filter=lambda var: var,
                            reader=None):

        if not os.path.exists(vcf_file):
            print("[!] Could not locate VCF file {}".format(vcf_file))
            return []

        if not reader:
            reader = VCF_Reader(vcf_file)
            reader.parse_meta()
            reader.make_info_dict()

        variants = []
        for var in filter(var_filter, reader):
            var_pos = cls(  var.id, var.ref, var.alt,
                            var.pos.chrom, var.pos.start, "")
            variants.append(var_pos)

        return variants


class GeneInterval(GenomicInterval):

    def __init__(self, name, chrom, start, end, *args, **kwargs):
        super().__init__(chrom, start, end)
        self.name = name

    def __str__(self):
        return "GeneInterval({} {}:{}-{})".format(  self.name, self.chrom,
                                                    self.start, self.end)

    def as_csv_line(self, fields=CSV_FIELDS, sep="\t"):

        line = ("{}" + sep) * 3 + "{}"
        content = ["", "", "", ""]

        content[fields.index("ID")] = self.name
        content[fields.index("CHR")] = self.chrom
        content[fields.index("START")] = self.start
        content[fields.index("END")] = self.end

        return line.format(*content)

    def as_bed_line(self):
        return self.as_csv_line(fields=BED_FIELDS)

    @classmethod
    def intervals_from_bed(cls, filename):

        if not os.path.exists(filename):
            print("[!] Could not locate BED file {}".format(filename))
            return []

        intervals = []
        for giv in BED_Reader(filename):
            intervals.append(cls(   giv.name, giv.iv.chrom,
                                    giv.iv.start, giv.iv.end))

        return intervals

    @classmethod
    def intervals_from_csv( cls, filename, comment_char="#",
                            fields=CSV_FIELDS):

        if not os.path.exists(filename):
            print("[!] Could not locate CSV file {}".format(filename))
            return []

        id_idx = fields.index("ID")
        chr_idx = fields.index("CHR")
        start_idx = fields.index("START")
        end_idx = fields.index("END")
        intervals = []

        with open(filename, "r") as csv_file:

            def decomment(csvfile):
                for row in csvfile:
                    raw = row.split(comment_char)[0].strip()
                    if raw: yield raw

            csv_reader = csv.reader(decomment(csv_file),
                                        delimiter=",", quotechar='"')

            for linenum, line in enumerate(csv_reader, start=1):
                if line and not line[0] == comment_char:
                    try:
                        gene_iv = GeneInterval( line[id_idx],
                                                line[chr_idx],
                                                int(line[start_idx]),
                                                int(line[end_idx]))
                        intervals.append(gene_iv)

                    except IndexError as ie:
                        error = "[!] Parsing error in {} line {}:\n" +\
                                "    \"{}\" could not be parsed as GeneInterval"
                        print(error.format(filename, linenum, ", ".join(line)))
                        return []
                    except ValueError as ve:
                        error = "[!] Parsing error in {} line {}:\n" + \
                                "    \"{}\" could not be interpreted as {}"
                        print(error.format( filename, linenum, ", ".join(line),
                                            ", ".join(fields)))
                        return []
        return intervals


if __name__ == "__main__":
    print("apparently I have nothing to do ...")
