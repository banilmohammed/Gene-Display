#!/usr/bin/env python3

"""
Main program to run this tool. Contains main function.
"""

import sys
from streamlit import cli as stcli
from commandLineParse import CommandLineParse
import fileCleaner as fc


def main():
    """ Run different modules based on the appropriate command line flags that are selected by the user."""
    # create object to access actual arguments
    clArgs = CommandLineParse()
    # run file clean module if annotate is selected and see is not
    if clArgs.args.annotate is True and clArgs.args.see is False:
        fileClean = fc.SeriesData(
            clArgs.args.output,
            clArgs.args.input,
            clArgs.args.types,
        )
        fileClean.myGeneCall()
        fileClean.combineDataFrame()
        fileClean.dataframeOutputter()
    # run existing data if both annotate and see are false
    elif clArgs.args.annotate is False and clArgs.args.see is False:
        fc.ExistingData(clArgs.args.input)
    # run visualization module if see is selected and annotate is not
    elif clArgs.args.see is True and clArgs.args.annotate is False:
        sys.argv = ["streamlit", "run", "graphVisualization.py"]
        sys.exit(stcli.main())


if __name__ == "__main__":
    main()
