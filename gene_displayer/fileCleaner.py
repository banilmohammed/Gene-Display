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
import concurrent.futures


class SeriesData:
    def __init__(self, fileName):
        regex = r"^!Sample(?=_title).*|^[^!I].*"
        reCompiled = re.compile(regex)
        with open(fileName, "r") as f:
            tableData = f.readlines()
            filterData = list(filter(reCompiled.match, tableData))
        cleanedData = list(map(lambda x: x.split("\t"), filterData))
        self.df = pd.DataFrame(cleanedData[3:], columns=cleanedData[1])
        self.df.rename(columns={"!Sample_title": "affy_gene_probe_id"}, inplace=True)
        self.geneAnnotateDf = pd.DataFrame(
            columns=[
                "affy_gene_probe_id",
                "Gene Name",
                "Gene Description",
                "Homologene",
                "GCC acc",
                "RefSeq",
            ]
        )
        self.affyProbeIDs = self.df["affy_gene_probe_id"].str.replace('"', "").to_list()

    def myGeneCall(self, probe_id):
        query = f"q=reporter:{probe_id}"
        fields = "fields=symbol,name,refseq,homologene,accession"
        url = f"http://mygene.info/v3/query?{query}&{fields}&size=1"
        res = requests.get(url)
        if len(res.json()["hits"]) != 0:
            # for all the hardcoded stuff aka [0] ask about how to choose right one
            jsonResponse = res.json()["hits"][0]
            self.geneAnnotateDf = self.geneAnnotateDf.append(
                {
                    "affy_gene_probe_id": probe_id,
                    "Gene Name": jsonResponse["symbol"],
                    "Gene Description": jsonResponse["name"],
                    "Homologene": jsonResponse["homologene"]["genes"][0][0],
                    "GCC acc": jsonResponse["accession"]["genomic"][0],
                    "RefSeq": jsonResponse["refseq"]["genomic"],
                },
                ignore_index=True,
            )

    def parallelAPI(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.myGeneCall, self.affyProbeIDs[:50])

    def combineDataFrame(self, df1, df2):
        merged_df = pd.merge(df1, df2, on="affy_gene_probe_id", how="outer")
        return merged_df


class GSE23006(SeriesData):
    pass


class GSE8056(SeriesData):
    pass


class GSE460(SeriesData):
    pass


if __name__ == "__main__":
    test = SeriesData("GSE23006_series_matrix.txt")
    test.parallelAPI()
    print(test.geneAnnotateDf.head())
