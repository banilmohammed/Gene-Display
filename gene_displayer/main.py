#!/usr/bin/env python3

import sys
from streamlit import cli as stcli
from commandLineParse import CommandLineParse
import fileCleaner as fc


def main():
    clArgs = CommandLineParse()
    if clArgs.args.annotate is True and clArgs.args.see is False:
        fileClean = fc.SeriesData(
            clArgs.args.output,
            clArgs.args.input,
            clArgs.args.types,
        )
        fileClean.myGeneCall()
        fileClean.combineDataFrame()
        fileClean.dataframeOutputter()
    elif clArgs.args.annotate is False and clArgs.args.see is False:
        fc.ExistingData(clArgs.args.input)
    elif clArgs.args.see is True and clArgs.args.annotate is False:
        sys.argv = ["streamlit", "run", "graphVisualization.py"]
        sys.exit(stcli.main())


if __name__ == "__main__":
    main()
