#!/usr/bin/env python3

"""
Module that makes use of argparse to create command line parsing class to deal with
command line arguments.

Classes:
    CommandLineParse: class to parse out command line arguments provided by user
"""

import argparse


class CommandLineParse:
    """
    Class to act as a wrapper for argparse and to initialize all the command line
    arguments for this program.

    Initialized: argument to toggle streamlit app to start, argument to indicate
    input file needs to annotated, argument to indicate input file should be output
    to csv, argument to indicate what input file is, argument to display version
    information, argument to hold sample types within dataset variable to hold
    value of all arguments
    """

    def __init__(self):
        # initialize argparse object
        self.parser = argparse.ArgumentParser(
            description="A simple program to annotate microarray data with gene names, symbols, refseq ids, and homologene ids as well as visualize gene concentrations.",
            add_help=True,
            prefix_chars="-",
        )
        # toggle streamlit app
        self.parser.add_argument(
            "-s",
            "--see",
            action="store_true",
            help="Toggle gene comparison visualizer",
        )
        # file needs to be annotated
        self.parser.add_argument(
            "-a",
            "--annotate",
            action="store_true",
            help="Annotate given file with gene symbol, gene description, homologene id, and refseq id",
        )
        # file needs to be output as csv
        self.parser.add_argument(
            "-o",
            "--output",
            action="store_true",
            help="Output annotated file as csv",
        )
        # name of input file
        self.parser.add_argument(
            "-i",
            "--input",
            action="store",
            help="Input file to be annotated or stored",
        )
        # types within sample
        self.parser.add_argument(
            "-t",
            "--types",
            action="append",
            help="Input all the different types of samples included in data",
        )
        # version information
        self.parser.add_argument(
            "-v", "--version", action="version", version="gene displayer 0.1.0"
        )
        self.args = self.parser.parse_args()
