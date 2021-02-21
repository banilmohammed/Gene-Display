#!/usr/bin/env python3

"""
Handles the file cleaning of GEO series data. Specifically GSE23006,
GSE8056, GSE460.

Classes:
    SeriesData: parent class that will contain the parsed out data
file as well as methods to clean the data file
    GSE23006: child class of SeriesData, overrides the methods for
    file cleaning according to how the GSE23006 data file requires
    GSE8056: child class of SeriesData, overrides the methods for
    file cleaning according to how the GSE8056 data file requires
    GSE460: child class of SeriesData, overrides the methods for
    file cleaning according to how the GSE460 data file requires
"""
import re
import pandas as pd
import requests


class SeriesData:
    def __init__(self, fileName):
        regex = r"^!Sample(?=_title).*|^[^!I].*"
        reCompiled = re.compile(regex)
        with open(fileName, "r") as f:
            tableData = f.readlines()
            filterData = list(filter(reCompiled.match, tableData))
            self.cleanedData = list(map(lambda x: x.split("\t"), filterData))

    def toDataFrame(self):
        df = pd.DataFrame(self.cleanedData[3:], columns=self.cleanedData[1])
        return df


class GSE23006(SeriesData):
    def geneAnnotator(self):
        geneDataFrame = self.toDataFrame()
        affyProbeIDs = geneDataFrame["!Sample_title"].str.replace('"', "").to_list()
        headers = {"content-type": "application/x-www-form-urlencoded"}
        params = f"q={','.join(affyProbeIDs[:900])}&scopes=reporter&fields=name,symbol"
        res = requests.post("http://mygene.info/v3/query", data=params, headers=headers)
        print(res.text)


class GSE8056(SeriesData):
    pass


class GSE460(SeriesData):
    pass


if __name__ == "__main__":
    test = GSE23006("GSE23006_series_matrix.txt")
    test.geneAnnotator()
