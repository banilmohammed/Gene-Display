# GeneViz
GeneViz is a project for BME 160, Introduction to Research Programming. It solves the problem of being able to compare data from different datasets and visualizing data in an easy to see manner. It makes heavy use of two libraries: pandas and streamlit to make an easy to use command line application. 

### Installation
Before using GeneViz, please ensure that you have conda installed. GeneViz makes use of a particular conda environment to ensure that local package installations do not interfere with the versions that are used within this program. If you do not have conda installed please follow [this link](https://www.anaconda.com/products/individual). Once you have installed conda, follow the steps below.

1. Navigate to the directory where you cloned this repository and run this command to setup the conda environment

		conda env create -f bme160_final.yml

2. The conda environment should now be created. Activate the conda environment by using

		conda activate bme160_final

3. You should see the name **bme160_final** within parenthesis next to your prompt in your terminal. You can now start using the program.

### Usage
GeneViz has a variety of command line options that can be used to customize what you would like the program to do.
| Command       | Meaning       |
| ------------- |:-------------:|
| -a, --annotate      | when used, it indicates that the input file needs to be annotated |
| -i, --input      | name of file that is to be inputted     |
| -s, --see | when used, it indicates that you would like to run the streamlit app to visualize data      |
| -o, --output | when used, it indicates that you would like to output annotated input file as csv      |
| -t, --type | input type of sample in input file      |
| -v, --version | version information   |

An example usage may be as following:
	
	$python3 main.py -a -o -i GSE460_series_matrix.txt -t skin

### Additional Notes
A couple additional notes for this program. There is a particular folder structure in place. **Infiles** is where input files go, **outfiles** is where the outputed csv files will appear, and **data** is where the pickle objects reside. Final note, when importing new datasets, there is a particular structure that the headers need to be in. It is as follows:

	exampleSampleType, Xhrs_replicateY


