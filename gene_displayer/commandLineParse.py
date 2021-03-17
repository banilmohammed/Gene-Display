#!/usr/bin/env python3

import argparse


class CommandLineParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="A simple program to annotate microarray data with gene names, symbols, refseq ids, and homologene ids as well as visualize gene concentrations.",
            add_help=True,
            prefix_chars="-",
        )
        self.parser.add_argument(
            "-s",
            "--see",
            action="store_true",
            help="Toggle gene comparison visualizer",
        )
        self.parser.add_argument(
            "-a",
            "--annotate",
            action="store_true",
            help="Annotate given file with gene symbol, gene description, homologene id, and refseq id",
        )
        self.parser.add_argument(
            "-o",
            "--output",
            action="store_true",
            help="Output annotated file as csv",
        )
        self.parser.add_argument(
            "-i",
            "--input",
            action="store",
            help="Input file to be annotated or stored",
        )
        self.parser.add_argument(
            "-t",
            "--types",
            action="append",
            help="Input all the different types of samples included in data",
        )
        self.parser.add_argument(
            "-v", "--version", action="version", version="gene displayer 0.1.0"
        )
        self.args = self.parser.parse_args()
