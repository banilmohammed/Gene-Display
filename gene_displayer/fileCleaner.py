#!/usr/bin/env python3

"""
Module that handles the file cleaning of GEO series data. Specifically GSE23006,
GSE8056, GSE460.

Classes:
    SeriesData: class that will contain the parsed out data file as well as methods to clean the data file
    ExistingData: class that is used to serialized already annotated data into pickle objects
"""
import re
import pandas as pd
import mygene


class SeriesData:
    """
    Class to contain all methods relating to parsing out raw data as well as calling
    mygene api to annotate with extra information.

    Initialized: boolean variable to hold whether data will be output as csv as well,
    name of file, types of samples contained in the file, pandas dataframe to hold
    filtered data, list of all affymetrix probe ids, pandas dataframe to hold new
    information from mygene api, and finally pandas dataframe for the combination of
    filtered data and new information from mygene api

    Methods: myGeneCall(): query mygene api with affymetrix probe ids and store
    resulting information in pandas dataframe, dataframeOutputter(): serialize
    pandas dataframe into pickle object and export annotated data if output is
    true, combineDataFrame(): outer merge both filtered data and new information
    obtained from mygene api into a single pandas dataframe while dropping duplicates
    """

    def __init__(self, output, fileName, sampleTypes):
        self.output = output  # determines whether file is output as csv
        self.filename = fileName
        self.sampleTypes = sampleTypes
        filenamePath = f"../infiles/{fileName}"  # relative path of file
        # regex for matching sample title and rows in data table
        regex = r"^!Sample(?=_title).*|^[^!I].*"
        reCompiled = re.compile(regex)  # compile regex for speed
        # open the file and filter out lines that match regex
        with open(filenamePath, "r") as f:
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
        # initialize empty object parameters here for clarity
        self.geneAnnotateDf = None
        self.combinedDf = None

    def myGeneCall(self):
        """ Query MyGene API with all the affymetrix probe IDs and for each, get: gene symbol, gene name, refseq id, and homologene id. """
        mg = mygene.MyGeneInfo()
        # query with affy probe ids
        self.geneAnnotateDf = mg.querymany(
            self.affyProbeIDs,
            scopes="reporter",
            fields="symbol, name, refseq, homologene, acession",
            as_dataframe=True,
            df_index=False,
            verbose=False,
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

    def dataframeOutputter(self):
        """ Serialize combinded dataframe as pickle object located in data/ directory and output as csv if output is selected. """
        # if there are more than one type of sample in a given dataset
        if len(self.sampleTypes) > 1:
            for sample in self.sampleTypes:
                # filter out columns that have the sample that we are looking for
                sampleColumns = self.combinedDf.columns[
                    ~self.combinedDf.columns.str.contains(sample)
                ].to_list()
                # output to csv file located in outfiles/
                if self.output is True:
                    self.combinedDf[sampleColumns].to_csv(
                        f"../outfiles/{self.filename[:-4]}_{sample}.csv", index=False
                    )
                # serialize dataframe to pickle object located in data/
                self.combinedDf[sampleColumns].to_pickle(
                    f"../data/{self.filename[:-4]}_{sample}.pkl"
                )

        # same as above if there is only one sample type in given dataset
        else:
            if self.output is True:
                self.combinedDf.to_csv(
                    f"../outfiles/{self.filename[:-4]}.csv", index=False
                )
            self.combinedDf.to_pickle(f"../data/{self.filename[:-4]}.pkl")

    def combineDataFrame(self):
        """ Combine filtered data and new annotations from my gene api into one file. Also drop duplicated gene names. """
        # merge on probe ids and unionize keys of both dataframes
        self.combinedDf = pd.merge(
            self.geneAnnotateDf, self.df, on="affy_gene_probe_id", how="outer"
        )

        # drop all nan
        self.combinedDf.dropna(axis=0, inplace=True)
        # drop the column containing affymetrix probe ids, not needed anymore
        self.combinedDf.drop(["affy_gene_probe_id"], axis=1, inplace=True)
        # drop duplicated gene names
        self.combinedDf.drop_duplicates(subset="Gene Name", inplace=True)


class ExistingData:
    """
    Class to serialize pre cleaned data into pickle objects located in data/

    Initialized: pandas dataframe that reads in csv of pre cleaned data
    """

    def __init__(self, filename):
        # read in csv
        self.existDf = pd.read_csv(f"../infiles/{filename}")
        # serialize as pickle object located in data/
        self.existDf.to_pickle(f"../data/{filename[:-4]}.pkl")
