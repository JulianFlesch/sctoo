import os
import argparse


class Description:
    NAME = "sctoo"
    VERSION = "0.1"
    SHORT = "Sctoo tools for binning and linear modelling of genomic variants"


class InputFileAction(argparse.Action):
    """
    Handles input files.
    Binds an InputFile object to the arparse namespace.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            file = values[0]
            if not os.path.exists(file):
                msg = "File not found: {}".format(file)
                raise(parser.error(msg))
            if option_string in ("-v", "--variants") and \
                not file.endswith("vcf"):
                msg = "No .vcf file: {}".format(file)
                raise(parser.error(msg))
            if option_string in ("-i", "--intervals") and \
                not file.endswith("bed"):
                msg = "No .bed file: {}".format(file)
                raise(parser.error(msg))
        except RuntimeError:
            parser.error()

        # add the object to the namespace
        setattr(namespace, self.dest, file)


class OutputFileAction(argparse.Action):
    """
    Handles input files.
    Binds an InputFile object to the arparse namespace.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            file = values[0]
            if os.path.exists(file):
                msg = "Aborting: File {} exists. ".format(file)
                raise(parser.error(msg))
            if option_string in ("-o", "--out") and \
                not file.endswith("bed"):
                msg = "Bed file ending (.bed) required: {}".format(file)
                raise(parser.error(msg))
        except RuntimeError:
            parser.error()

        # add the object to the namespace
        setattr(namespace, self.dest, file)


def parse_args():

    parser = argparse.ArgumentParser(   description=Description.SHORT,
                                        prog=Description.NAME)

    # version info
    parser.add_argument(
        "-V", "--version", action="version",
        version="%(prog)s "+Description.VERSION)

    # make subcommands available
    subparsers = parser.add_subparsers(dest="subcommand")

    # binner
    binner = subparsers.add_parser("binner",
        help="Bin variants presented in VCF files by intervals from csv or " + \
        "bed files")

    binner.add_argument("-v", "--variants", type=str, action=InputFileAction,
        nargs=1, help="Path to a vcf file with variants", required=True)
    binner.add_argument("-i", "--intervals", type=str, action=InputFileAction,
        nargs=1, help="Path to a bed file intervals", required=True)
    binner.add_argument("-o", "--out", type=str, action=OutputFileAction,
        nargs=1, help="Path to a bed/csv file to write the binned variants to")
    binner.add_argument("--only-somatic", action="store_true",
        help="Include only somatic variants, as annotated by VarScan2")

    fitter = subparsers.add_parser("lin-fitter",
        help="Fit a linear model to binned somatic variants")


    job = parser.parse_args()
    return job
