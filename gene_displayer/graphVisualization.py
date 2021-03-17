<<<<<<< HEAD
import streamlit as st # using this package for the front end interface
import pandas as pd #using dataframes to read files and be able to plot them onto the front end
import matplotlib.pyplot as plt #helps to plot the dataframes
import re #regex
=======
import streamlit as st  # using this package for the front end interface
import pandas as pd  # using dataframes to read files and be able to plot them onto the front end
import matplotlib.pyplot as plt  # helps to plot the dataframes
import os

>>>>>>> 7ab24749772af2f36faf6462addc6ec20e57e129

class streamlit:
    """
    A class that represents streamlit

    Class Parameters
    ----------------
    dataframes : list
        List of dataframes in database.
    inputGenes : list
        List of gene names that the user has inputted.
    datasets : list
        List of datasets that the user has chosen.
    geneDataframes : dict
        Dictionary with keys as the dataset names, and values as the dataset specified by the user's inputs of the genes.
    userDataframes : dict
        Dictionary with keys as the dataset names, and values as the dataset specified by the user's inputs of the replicates.
    graphButton : boolean
        Boolean value of the sidebar checkbox.
    selectReplicates : str
        A string of the specified replicate that the user chose.
    selectNavigation : str
        A str of the location that the user chose.

    Methods
    -------
    createSidebar()
        Create the sidebar of the website and title of the website.
    navBar()
        Create the navigation bar when the user clicks the graph button.
    collectDataframes()
        Create a dictionary of the datasets that the user selected for plotting.
    specifyDataframes()
        Create dictionary of the datasets specified by the user's selected options for plotting.
    createDataframes()
        Print out the dataframes specified to the users inputs.
    createIndividuals()
        Plot a line graph for each dataset.
    createComparison()
        Plot a line graph of both datasets.
    """

    # Class Parameters
    dataframes = list(
        map(lambda x: x[:-4], os.listdir("../data"))
    )  # List of dataframes in database.
    inputGenes = []  # List of gene names that the user has inputted.
    datasets = []  # List of datasets that the user has chosen.
    geneDataframes = (
        dict()
    )  # Dictionary with keys as the dataset names, and values as the dataset specified by the user's inputs of the genes.
    userDataframes = (
        dict()
    )  # Dictionary with keys as the dataset names, and values as the dataset specified by the user's inputs of the replicates.
    graphButton = False  # Boolean value of the sidebar checkbox.
    selectReplicates = ""  # A string of the specified replicate that the user chose.
    selectNavigation = ""  # A str of the location that the user chose.

    def createSidebar():
        """
        Create the sidebar of the website.
        """
        st.title("GeneVis: A Tool to Compare Datasets")  # set title of website page
        st.sidebar.title("Visualization Selector")  # set sidebar title
        st.sidebar.markdown(
            "Select Two Datasets to Compare"
        )  # set markdown title telling user to choose datasets
        streamlit.datasets = st.sidebar.multiselect(
            "Select Datasets", streamlit.dataframes
        )  # create multiselect option of the datasets
        st.sidebar.markdown(
            "Input Gene Names (separate by commas if more than one gene)"
        )  # set markdown title telling user to input genes
        userInput = st.sidebar.text_input(
            "Gene names: "
        )  # create a text box for user to input genes
        newString = userInput.replace(
            " ", ""
        )  # delete the whitespace within the user's input
        streamlit.inputGenes = newString.split(",")  # split the string by commas
        st.sidebar.markdown(
            "Choose Replicates to be Graphed"
        )  # set markdown title telling user to choose the replicates
        streamlit.selectReplicates = st.sidebar.radio(
            "Replicates", ("replicate1", "replicate2", "replicate3", "average")
        )  # create a selection of the replicate options to choose from
        st.sidebar.markdown("Graphing")  # set markdown title of the graphing button
        streamlit.graphButton = st.sidebar.checkbox(
            "Click to Graph"
        )  # create a checkbox the user can click on to graph

    def navBar():
        """
        Create the navigation bar when the user clicks the graph button.
        """
        if streamlit.graphButton:  # check if graphbutton is selected
            st.sidebar.title("Navigation")  # set a navbar title
            streamlit.selectNavigation = st.sidebar.radio(
                "Go to", ("Comparison", "Individual", "Dataframe")
            )  # create a selection of the different pages

    def collectDataframes():
        """
        Create a dictionary of the datasets that the user selected for plotting.
<<<<<<< HEAD
        '''
        if streamlit.graphButton: #check if the graph button is selected
            for dataset in streamlit.datasets: #iterate over the datasets that the user selected
                newRead = pd.read_csv(dataset + '.csv', index_col = 'Gene Name') # Read the file
                rows = newRead.loc[streamlit.inputGenes] #create a new dataframe of only the genes that the user specified
                rows = rows.reset_index() #reset the indexing
                streamlit.geneDataframes[dataset] = rows #set the key of the geneDataframes dictionary to the dataset name and the value to the dataframe
=======
        """
        if streamlit.graphButton:  # check if the graph button is selected
            for (
                dataset
            ) in streamlit.datasets:  # iterate over the datasets that the user selected
                newRead = pd.read_pickle(f"../data/{dataset}.pkl")  # Read the file
                newRead.set_index("Gene Name", inplace=True)
                rows = newRead.loc[
                    streamlit.inputGenes
                ]  # create a new dataframe of only the genes that the user specified
                rows = rows.reset_index()  # reset the indexing
                streamlit.geneDataframes[
                    dataset
                ] = rows  # set the key of the geneDataframes dictionary to the dataset name and the value to the dataframe
>>>>>>> 7ab24749772af2f36faf6462addc6ec20e57e129

    def specifyDataframes():
        """
        Create dictionary of the datasets specified by the user's selected options for plotting.
        """
        for (
            i
        ) in (
            streamlit.geneDataframes
        ):  # iterate over the specified dataframes with the genes that the user selected
            df = streamlit.geneDataframes[i]  # get the dataframe
            if (
                streamlit.selectReplicates != "average"
            ):  # check if the selected replicate is not average
                colDrop = []  # create list of the columns to be dropped
                for (
                    column
                ) in df.columns:  # iterate over all the columns of the dataframe
                    # if the replicate name (replicate1, replicate2, or replicate 3) is not in the columns after columns, Gene Description, Gene Name, HG ID, and RefSeq
                    if (
                        streamlit.selectReplicates not in column
                        and column != "Gene Description"
                        and column != "Gene Name"
                        and column != "HG ID"
                        and column != "RefSeq"
                    ):
                        colDrop.append(
                            column
                        )  # append the column to the list of colDrop
                cleanedDF = df.drop(
                    columns=colDrop
                )  # drop all the columns in the list colDrop
                cleanedDF = cleanedDF.set_index(
                    "Gene Name"
                )  # set the index to Gene name
                # add the filtered out dataframe to the dictionary userdataframes with the key being the dataset name and the value being the filtered out dataframe
                streamlit.userDataframes[i] = cleanedDF
            else:
                columns = []  # create a column list of the new columns
                geneID = df[
                    "HG ID"
                ].tolist()  # set variable gene ID to the values within the column HD ID
                refSeq = df[
                    "RefSeq"
                ].tolist()  # set variable refSeq to the values within the column RefSeq
                geneDescription = df[
                    "Gene Description"
                ].tolist()  # set variable geneDescription to the values within the column Gene Description
                geneName = df[
                    "Gene Name"
                ].tolist()  # set variable geneName to the values within the column Gene Name
                df = df.drop(
                    columns=["Gene Description", "Gene Name", "RefSeq", "HG ID"]
                )  # drop columns Gene Description, Gene Name, RefSeq, and HG ID
                for column in df.columns:  # iterate over all the columns
                    newString = column[
                        0 : column.index("_") + 1
                    ]  # create a string with just the time
                    finalString = (
                        newString + "average"
                    )  # then concatenate '_average' to the string that has the time
                    columns.append(finalString)  # then append into the list columns
                df.columns = columns  # set these as the new column names
                df = df.T  # transpose the dataframe
                df = df.reset_index()  # reset the index
                df = (
                    df.groupby("index", sort=False).mean().transpose()
                )  # group the dataframe by the column 'index' and find the mean and then transpose
                # insert back all the columns that were dropped
                df.insert(0, "Gene Name", geneName)
                df.insert(1, "HG ID", geneID)
                df.insert(2, "Gene Description", geneDescription)
                df.insert(3, "RefSeq", refSeq)
                cleanedDF = df.set_index(
                    "Gene Name"
                )  # set the index of the dataframe to the column Gene Name
                # add the dataframe of averages to the dictionary userdataframes with the key being the dataset name and the value being the filtered out dataframe
                streamlit.userDataframes[i] = cleanedDF

    def createDataframes():
        """
        Print out the dataframes specified to the users inputs.
        """
        if (
            streamlit.selectNavigation == "Dataframe"
        ):  # check if the user chose dataframe in the navbar
            st.header("Dataframes")  # set the header name to 'Dataframes'
            for (
                df
            ) in streamlit.userDataframes:  # iterate over the filtered out dataframes
                st.markdown(df)  # set the markdown title as dataset name
                st.write(streamlit.userDataframes[df])  # write out the dataframe

    def createIndividuals():
        """
        Plot a line graph for each dataset.
<<<<<<< HEAD
        '''
        #check if the graph button is clicked and if the user chose 'Individual' in the navbar
        if streamlit.graphButton and streamlit.selectNavigation == 'Individual':
            st.header('Individual Graphs for Each Dataset') #set header name
            for i in streamlit.userDataframes: #iterate over the filtered dataframes dictionary
                df = streamlit.userDataframes[i] #get the dataframe
                xAxis = []
                newDF = df.drop(columns = ['HG ID', 'Gene Description', 'RefSeq']) # drop columns 'HG ID', 'Gene Description', 'RefSeq'
                for column in newDF.columns.tolist():
                    if column != 'Gene Name':
                        newCol = column.replace('"', "")
                        matchEx = re.match(r"(\d+?)hrs?", newCol)
                        xAxis.append(int(matchEx.groups()[0]))
                newDF.columns = xAxis
                transposedDF = newDF.T #transpose the dataframe
                st.subheader(i) #create a subheader, which is the dataset name
                fig, ax = plt.subplots() #create subplots
                for column in set(transposedDF.columns.tolist()): #iterate over the columns in the transposed dataframe
                    transposedDF.plot(kind = 'line', y = column, ax=ax, alpha = 0.5) #plot that column
                # set the title name, x-axis name, y-axis name, and put the legend outside
                plt.title(i)
                plt.xlabel('Time (hours)')
                plt.ylabel('Decay')
                plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
                #write the plot out onto the webpage
                st.write(fig)

    def createComparison():
        #check if the graph button is clicked and if the user chose 'Comparison' in the navbar
        if streamlit.graphButton and streamlit.selectNavigation == 'Comparison':
            st.header('Comparing Datasets') #set header name
            dataframes = [] #create a list of dataframes
            xAxis = []
            for i in streamlit.userDataframes: #iterate over the filtered dataframes dictionary
                columns = [] #create a column list
                df = streamlit.userDataframes[i] #get the dataframe
                newDF = df.drop(columns = ['HG ID', 'Gene Description', 'RefSeq']) #drop the columns 'HG ID', 'Gene Description', 'RefSeq'
                for column in newDF.columns.tolist():
                    if column != 'Gene Name':
                        newCol = column.replace('"', "")
                        matchEx = re.match(r"(\d+?)hrs?", newCol)
                        xAxis.append(int(matchEx.groups()[0]))
                newDF.columns = xAxis
                transposedDF = newDF.T #transpose the dataframe
                for column in transposedDF.columns: #iterate over the columns
                    newString = column + '_' + i #rename the columns to contain the dataset name
                    columns.append(newString) #append the new column name into the columns list
                transposedDF.columns = columns #set the transposed dataframe columns to the columns list created
                dataframes.append(transposedDF.T) #transpose dataframe again and append into the dataframes list
            if len(dataframes) > 1: #if the length of datframes is list is more than one
                combinedDF = pd.concat(dataframes) #concatenate all the dataframes together
                fig, ax = plt.subplots() #plot subplots
                for column in set(combinedDF.T.columns.tolist()): #iterate over the transposed dataframe columns
                    combinedDF.T.plot(kind = 'line', y = column, ax=ax, rot=45, alpha = 0.5) #plot each column into the graph of the transposed DataFrame
=======
        """
        # check if the graph button is clicked and if the user chose 'Individual' in the navbar
        if streamlit.graphButton and streamlit.selectNavigation == "Individual":
            st.header("Individual Graphs for Each Dataset")  # set header name
            for (
                i
            ) in (
                streamlit.userDataframes
            ):  # iterate over the filtered dataframes dictionary
                df = streamlit.userDataframes[i]  # get the dataframe
                newDF = df.drop(
                    columns=["HG ID", "Gene Description", "RefSeq"]
                )  # drop columns 'HG ID', 'Gene Description', 'RefSeq'
                transposedDF = newDF.T  # transpose the dataframe
                st.subheader(i)  # create a subheader, which is the dataset name
                fig, ax = plt.subplots()  # create subplots
                for column in set(
                    transposedDF.columns.tolist()
                ):  # iterate over the columns in the transposed dataframe
                    transposedDF.plot(
                        kind="line", y=column, ax=ax, rot=45, alpha=0.5
                    )  # plot that column
                # set the title name, x-axis name, y-axis name, and put the legend outside
                plt.title(i)
                plt.xlabel("Time")
                plt.ylabel("Decay")
                plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")
                # write the plot out onto the webpage
                st.write(fig)

    def createComparison():
        # check if the graph button is clicked and if the user chose 'Comparison' in the navbar
        if streamlit.graphButton and streamlit.selectNavigation == "Comparison":
            st.header("Comparing Datasets")  # set header name
            dataframes = []  # create a list of dataframes
            for (
                i
            ) in (
                streamlit.userDataframes
            ):  # iterate over the filtered dataframes dictionary
                columns = []  # create a column list
                df = streamlit.userDataframes[i]  # get the dataframe
                newDF = df.drop(
                    columns=["HG ID", "Gene Description", "RefSeq"]
                )  # drop the columns 'HG ID', 'Gene Description', 'RefSeq'
                transposedDF = newDF.T  # transpose the dataframe
                for column in transposedDF.columns:  # iterate over the columns
                    newString = (
                        column + "_" + i
                    )  # rename the columns to contain the dataset name
                    columns.append(
                        newString
                    )  # append the new column name into the columns list
                transposedDF.columns = columns  # set the transposed dataframe columns to the columns list created
                dataframes.append(
                    transposedDF.T
                )  # transpose dataframe again and append into the dataframes list
            if (
                len(dataframes) > 1
            ):  # if the length of datframes is list is more than one
                combinedDF = pd.concat(
                    dataframes
                )  # concatenate all the dataframes together
                fig, ax = plt.subplots()  # plot subplots
                for column in set(
                    combinedDF.T.columns.tolist()
                ):  # iterate over the transposed dataframe columns
                    combinedDF.T.plot(
                        kind="line", y=column, ax=ax, rot=45, alpha=0.5
                    )  # plot each column into the graph of the transposed DataFrame
>>>>>>> 7ab24749772af2f36faf6462addc6ec20e57e129
                # set the title name, x-axis name, y-axis name, and put the legend outside
                plt.title("Comparing Datasets")
                plt.xlabel("Time")
                plt.ylabel("Decay")
                plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")
                # write the plot out onto the webpage
                st.write(fig)
            else:
                for data in dataframes:
                    fig, ax = plt.subplots()  # plot subplots
                    for column in set(
                        data.T.columns.tolist()
                    ):  # iterate over the transposed dataframe columns
                        data.T.plot(
                            kind="line", y=column, ax=ax, rot=45, alpha=0.5
                        )  # plot each column into the graph of the transposed DataFrame
                    # set the title name, x-axis name, y-axis name, and put the legend outside
                    plt.title("Comparing Datasets")
                    plt.xlabel("Time")
                    plt.ylabel("Decay")
                    plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")
                    # write the plot out onto the webpage
                    st.write(fig)


streamlit.createSidebar()
streamlit.navBar()
streamlit.collectDataframes()
streamlit.specifyDataframes()
streamlit.createDataframes()
streamlit.createIndividuals()
streamlit.createComparison()
