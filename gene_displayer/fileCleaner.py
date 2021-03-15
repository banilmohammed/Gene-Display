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
import mygene
import pickle


class SeriesData:
    def __init__(self, fileName):
        self.filename = fileName.split("/")[2]
        # regex for matching sample title and rows in data table
        regex = r"^!Sample(?=_title).*|^[^!I].*"
        reCompiled = re.compile(regex)  # compile regex for speed
        # open the file and filter out lines that match regex
        with open(fileName, "r") as f:
            tableData = f.readlines()
            filterData = list(filter(reCompiled.match, tableData))
        # split the data on the tab character to get each row as element in list
        cleanedData = list(map(lambda x: x.split("\t"), filterData))
        self.df = pd.DataFrame(cleanedData[3:], columns=cleanedData[1])
        # rename column with affy probe ID
        self.df.rename(columns={"!Sample_title": "affy_gene_probe_id"}, inplace=True)
        self.df["affy_gene_probe_id"] = self.df["affy_gene_probe_id"].str.replace(
            '"', ""
        )
        # take out quotes from affy probe ids and convert it to list
        self.affyProbeIDs = self.df["affy_gene_probe_id"].str.replace('"', "").to_list()
        self.geneAnnotateDf = None
        self.combinedDf = None

    def myGeneCall(self):
        mg = mygene.MyGeneInfo()
        # query with affy probe ids
        # maybe add GenBank acc as well
        self.geneAnnotateDf = mg.querymany(
            self.affyProbeIDs,
            scopes="reporter",
            fields="symbol, name, refseq, homologene, acession",
            as_dataframe=True,
            df_index=False,
            verbose=True,
        )
        # drop these columns
        self.geneAnnotateDf.drop(
            [
                "_id",
                "_score",
                "homologene.genes",
                "refseq.protein",
                "refseq.rna",
                "refseq.translation",
                "refseq.translation.protein",
                "refseq.translation.rna",
                "notfound",
            ],
            axis=1,
            inplace=True,
        )
        self.geneAnnotateDf.dropna(axis=0, inplace=True)
        # reorder columns
        self.geneAnnotateDf = self.geneAnnotateDf.reindex(
            columns=[
                "query",
                "homologene.id",
                "symbol",
                "name",
                "refseq.genomic",
            ],
        )
        # rename to more human readable form
        self.geneAnnotateDf.rename(
            columns={
                "query": "affy_gene_probe_id",
                "homologene.id": "HG ID",
                "symbol": "Gene Name",
                "name": "Gene Description",
                "refseq.genomic": "RefSeq",
            },
            inplace=True,
        )

    def dataframeSorter(self, sampleTypes):
        # MAKE SURE FOLDER NAME IS EXACT -- find way around this
        if len(sampleTypes) > 1:
            for sample in sampleTypes:
                sampleColumns = self.combinedDf.columns[
                    ~self.combinedDf.columns.str.contains(sample)
                ].to_list()
                # self.combinedDf[sampleColumns].to_csv(
                #    f"{self.filename[:-4]}_{sample}.csv", index=False
                # )
                newFilename = f"{self.filename[:-4]}_{sample}"
                # self.combinedDf[sampleColumns].to_sql(newFilename, conn)

        else:
            # self.combinedDf.to_csv(f"{self.filename[:-4]}.csv", index=False)
            self.combinedDf.to_pickle(f"../data/{self.filename[:-4]}.pkl")

    def combineDataFrame(self):
        # merge on probe ids and unionize keys of both dataframes
        self.combinedDf = pd.merge(
            self.geneAnnotateDf, self.df, on="affy_gene_probe_id", how="outer"
        )

        self.combinedDf.dropna(axis=0, inplace=True)
        self.combinedDf.drop(["affy_gene_probe_id"], axis=1, inplace=True)
        self.combinedDf.drop_duplicates(subset="Gene Name", inplace=True)


if __name__ == "__main__":
    test = SeriesData("../infiles/GSE460_series_matrix.txt")
    test.myGeneCall()
    test.combineDataFrame()
    # test.combinedDf.to_csv("output.csv", index=False)
    test.dataframeSorter(["skin"])
