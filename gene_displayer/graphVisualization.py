import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class streamlit:
    dataframes = [ 'cleaned_skin_data', 'cleaned_tongue_data' ]
    inputGenes = []
    datasets = []
    smallDataframes = dict()
    userDataframes = dict()
    graphButton = ''
    selectReplicates = ''
    selectNavigation = ''
    xAxis = []
    specifiedDataframes = dict()
    plottingGenes = dict()

    def createSidebar():
        st.title('GeneVis: A Tool to Compare Datasets')
        st.sidebar.title('Visualization Selector')
        st.sidebar.markdown('Select Two Datasets to Compare')
        streamlit.datasets = st.sidebar.multiselect('Select Datasets', streamlit.dataframes)
        st.sidebar.markdown('Input Gene Names (separate by commas if more than one gene)')
        userInput = st.sidebar.text_input("Gene names: ")
        newString = userInput.replace(" ", "")
        streamlit.inputGenes = newString.split(',')
        st.sidebar.markdown('Choose Replicates to be Graphed')
        streamlit.selectReplicates = st.sidebar.radio('Replicates', ('replicate1', 'replicate2', 'replicate3', 'average'))
        st.sidebar.markdown('Graphing')
        streamlit.graphButton = st.sidebar.checkbox("Click to Graph")

    def navBar():
        if streamlit.graphButton:
            st.sidebar.title('Navigation')
            streamlit.selectNavigation = st.sidebar.radio('Go to', ('Comparison', 'Individual', 'Dataframe'))

    def collectDataframes():
        if streamlit.graphButton:
            for dataset in streamlit.datasets:
                newRead = pd.read_csv(dataset + '.csv', index_col = "Gene name")
                rows = newRead.loc[streamlit.inputGenes]
                rows = rows.reset_index()
                streamlit.smallDataframes[dataset] = rows

    def specifyDataframes():
            for i in streamlit.smallDataframes:
                df = streamlit.smallDataframes[i]
                if streamlit.selectReplicates == 'replicate1' or streamlit.selectReplicates == 'replicate2' or  streamlit.selectReplicates == 'replicate3':
                    colDrop = []
                    for column in df.columns:
                        if streamlit.selectReplicates not in column and column != 'Gene description' and column != 'Gene name':
                            colDrop.append(column)
                    cleanedDF = df.drop(columns = colDrop)
                    cleanedDF = cleanedDF.set_index('Gene name')
                    streamlit.userDataframes[i] = cleanedDF
                else:
                    columns = []
                    geneDescription = df['Gene description'].tolist()
                    geneName = df['Gene name'].tolist()
                    df = df.drop(columns = ['Gene description', 'Gene name'])
                    for column in df.columns:
                        newString = column[:column.index('_')]
                        finalString = newString + '_average'
                        columns.append(finalString)
                    df.columns = columns
                    df = df.T
                    df = df.reset_index()
                    df = df.groupby('index', sort=False).mean().transpose()
                    df.insert(0, 'Gene name', geneName)
                    df.insert(1, 'Gene description', geneDescription)
                    cleanedDF = df.set_index('Gene name')
                    streamlit.userDataframes[i] = cleanedDF

    def createDataframes():
        if streamlit.graphButton and streamlit.selectNavigation == 'Dataframe':
            st.header('Dataframes')
            for df in streamlit.userDataframes:
                st.markdown(df)
                st.write(streamlit.userDataframes[df])

    def createIndividuals():
        if streamlit.graphButton and streamlit.selectNavigation == 'Individual':
            st.header('Individual Graphs for Each Dataset')
            for i in streamlit.userDataframes:
                df = streamlit.userDataframes[i]
                newDF = df.drop(columns = 'Gene description')
                transposedDF = newDF.T
                st.subheader(i)
                fig, ax = plt.subplots()
                for column in set(transposedDF.columns.tolist()):
                    transposedDF.plot(kind = 'line', y = column, ax=ax, rot=45, alpha = 0.5)
                plt.title(i)
                plt.xlabel('Time')
                plt.ylabel('Decay')
                plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
                st.write(fig)

    def createComparison():
        if streamlit.graphButton and streamlit.selectNavigation == 'Comparison':
            st.header('Comparing Datasets')
            dataframes = []
            for i in streamlit.userDataframes:
                columns = []
                df = streamlit.userDataframes[i]
                newDF = df.drop(columns = 'Gene description')
                transposedDF = newDF.T
                for column in transposedDF.columns:
                    newString = column + '_' + i
                    columns.append(newString)
                transposedDF.columns = columns
                dataframes.append(transposedDF.T)
            combinedDF = pd.concat(dataframes)
            fig, ax = plt.subplots()
            for column in set(combinedDF.T.columns.tolist()):
                combinedDF.T.plot(kind = 'line', y = column, ax=ax, rot=45, alpha = 0.5)
            plt.title('Comparing Datasets')
            plt.xlabel('Time')
            plt.ylabel('Decay')
            plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
            st.write(fig)

streamlit.createSidebar()
streamlit.navBar()
streamlit.collectDataframes()
streamlit.specifyDataframes()
streamlit.createDataframes()
streamlit.createIndividuals()
streamlit.createComparison()
