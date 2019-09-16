# CX Summary-Module Translator version

## Directions:

My workflow script (scripts/SummaryTableWorkflow.py) currently **MUST** be run from the root directory 
(translator-modules). 

9/15/19 7pm: It should work with the environment/dependencies described in the master/develop branch ReadMe.
I still need to check this.


SummaryTableWorkflow.py script **MUST** be run with one of the following parameters:

* -d MONDO:####### <- replace hashes with the MONDO ID of the single disease of interest
* -l path to text file of diseases of interest 
	- Within the text file...each line has one MONDO disease ID in the following format (MONDO:######). 
	- See tests/CXtest_diseaselist.txt for an example
	- WARNING: This will take 10+ minutes to run. I also have a bug where you cannot see the individual 
		module results as the code is running, while you can when running a single disease or gene 
		list. 
* -j path to text file of genes of interest
	- Within the text file...first line has the name of your query (can be anything you want)...
		subsequent lines have one approved gene symbol per line.
	- See tests/CXtest_inputgenes.txt and tests/CXtest_errorgenes.txt for examples


User can set custom thresholds (filtering the results) using the following parameters. Defaults will be used 
if parameter is not specified. 

* -f (default 0.75). Threshold for functional (jaccard) similarity between input gene and desired output gene. 
	- Accepts number between 0 (returns all results) and 1 (returns genes with exactly the same 
		functional annotation as the input gene), inclusive.
	- Functional similarity calculation uses set of inferred and direct annotations for two genes. 
* -p (default 0.35) Threshold for phenotypic similarity between input gene and desired output gene. 
	- Accepts number between 0 (returns all results) and 1 (returns genes with exactly the same phenotypic 
		annotation as the input gene), inclusive. 
	- Functional similarity calculation uses set of inferred and direct annotations for two genes. 
		Has a known bug! See above point.
* -g (default 9) Threshold for number of gene-gene interactions between input genes and desired output gene. 
	- Accepts integers 0 (return all results) and larger (note that the maximum number of gene-gene 
		interactions with the inputs = number of input genes).
* -b (default 0.1) Threshold for gene-gene-bicluster scores.
	- Accepts number between 0 (returns all results) and 1 (not a reasonable parameter value: accepted 
		output gene would need to be in every bicluster to be returned to the user).  
	- Bicluster set is created using input genes. 
	- score is number of biclusters an output gene is in / total number of unique biclusters.

 
## Example prompts

###Single diseases:
**Fanconi anemia** (runs for ~10 minutes): python scripts/SummaryTableWorkflow.py -v -d MONDO:0019391 -f 0.5 -p 0.34 -g 9 -b 0.05

**Lafora disease** (runs for ~6.5 minutes): python scripts/SummaryTableWorkflow.py -v -d MONDO:0009697 -f 0.3 -p 0.2 -g 0 -b 0.1

###Gene list queries: 
**Fanconi anemia disease genes**: python scripts/SummaryTableWorkflow.py -v -j ./tests/CXtest_inputgenes.txt -f 0.5 -p 0.34 -g 9 -b 0.05

**Lafora disease genes + erroneous entries**: 
python scripts/SummaryTableWorkflow.py -v -j ./tests/CXtest_errorgenes.txt -f 0.3 -p 0.2 -g 0 -b 0.1 

###Disease list (runs for 10.5 minutes):
python scripts/SummaryTableWorkflow.py -l ./tests/CXtest_diseaselist.txt 