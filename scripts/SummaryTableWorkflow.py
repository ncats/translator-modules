#!/usr/bin/env python3

# Uncomment when we need to debug
# import logging
# logging.basicConfig(level=logging.INFO)

#import requests
#from os import makedirs
#from pathlib import Path
#from html3.html3 import XHTML

import argparse
import pandas as pd

#############################################################
# First, before loading all our analysis modules, we need
# to tweak OntoBio to disable its @cachier cache. Our
# patched Ontobio has an 'ignore_cache' flag which may be
# overridden here before the rest of the system is loaded.
# We do this because cachier seems to introduce an odd system
# instability resulting in deep recursion on one method,
# creating new threads and consuming stack memory to the point
# of system resource exhaustion!  We conjecture that cachier
# caching is unnecessary since we read the pertinent ontology
# catalogs in just once into memory, for readonly reuse.
##############################################################
# 9 July 2019 - this snippet of configuration buried into the core.generic_similarity.py module
#from ontobio.config import get_config
#get_config().ignore_cache = True

# Now we can import the remainder of the modules (some which call Ontobio)

from translator_modules.disease.gene.disease_associated_genes import DiseaseNameLookup  ## CX: to look up name
from translator_modules.disease.gene.disease_associated_genes import DiseaseAssociatedGeneSet
from translator_modules.gene.gene.functional_similarity import FunctionalSimilarity
from translator_modules.gene.gene.phenotype_similarity import PhenotypeSimilarity
from translator_modules.gene.gene.gene_interaction import GeneInteractions

from translator_modules.gene.gene.gene_to_gene_bicluster import GeneToGeneBiclusters
from translator_modules.core.ids.IDs import TranslateIDs

from scripts.summary_mod import SummaryMod

_SCRIPTNAME = 'SummaryTableWorkflow.py'
# Flag to control console output
_echo_to_console = False


# Data type of switch input is interpreted as a Boolean value
def set_console_echo(switch):
    global _echo_to_console
    _echo_to_console = switch


def disease_gene_lookup(mondo_id):

    gene_set = DiseaseAssociatedGeneSet(mondo_id)

    return gene_set


STD_RESULT_COLUMNS = ['hit_id', 'hit_symbol', 'input_id', 'input_symbol', 'score']


def similarity(model, input_gene_set, threshold, module, title):

#    input_gene_set = disease_associated_gene_set.get_data_frame()

    # Perform the comparison on specified gene set
    results = model.compute_similarity(input_gene_set, threshold)

    results['module'] = module

    return results


def gene_interactions(model, input_gene_set, threshold, module, title):

#    input_gene_set = disease_associated_gene_set.get_data_frame()

    # Perform the comparison on specified gene set
    
    ## convert float input to int 
    lower_bound = int(threshold)
    results = model.get_interactions(input_gene_set, lower_bound)

    results['module'] = module

    return results


def gene_gene_bicluster(input_gene_set, threshold, module):
    # Written by CX, from Marcin's WF9 gene-gene bicluster stuff
#    input_gene_set = disease_associated_gene_set.get_data_frame()

    ## get the raw results (only those above threshold)
    results = GeneToGeneBiclusters(input_gene_set, threshold).get_data_frame()

    ## set module column: used in summary module
    results['module'] = module
    
    ## reorder columns 
    cols = ['hit_id', 'hit_symbol', 'input_id', 'input_symbol', 'score', 'module']
    results = results.reindex(columns=cols)

    return results


def main():
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        prog=_SCRIPTNAME, formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='NCATS Translator Workflow 2 Command Line Script'
    )

    parser.add_argument('-v', '--verbose', help='echo script output verbosely to console', action='store_true')

    disease_query = parser.add_mutually_exclusive_group(required=True)

    # single disease input specification as a 2-tuple
    disease_query.add_argument('-d', '--disease',
                               help="""
                               MONDO:####### identifier of a single disease"""
                               )

    # disease input as a list
    disease_query.add_argument('-l', '--diseaseTable',
                               help="""
                               name of text file - each line of file has the MONDO identifier of a single disease."""
                               )

    disease_query.add_argument('-j', '--geneTable',
                               help="""
			       name of text file - first line of file is name of query, each subsequent line 
			       has the approved gene symbol for one gene."""
                               )

    parser.add_argument('-f', '--functionalThreshold',
                        type=float, default=0.75, help='value of Functional Similarity threshold')

    parser.add_argument('-p', '--phenotypeThreshold',
                        type=float, default=0.35, help='value of Phenotype Similarity threshold')

    parser.add_argument('-g', '--geneInteractionThreshold',
                        type=float, default=12, help='value of Gene Interaction threshold')

    parser.add_argument('-b', '--geneBiclusterThreshold',
                        type=float, default=0.1, help='value of gene-gene bicluster threshold')

    args = parser.parse_args()

    print("\nRunning the " + _SCRIPTNAME + " script...")

    if args.verbose:
        print("Echoing results verbosely to the console!\n")
        set_console_echo(True)

    print("\nLoading source ontology and annotation...")

    
    disease_list = []
    # read in the diseases to analyze. disease_list will stay empty 
    # if file (list of input genes) is given instead
    if args.disease:
        mondo_id = args.disease
        disease_name = DiseaseNameLookup(mondo_id).disease_name
        print("\nSingle disease specified:\t" + disease_name + "(" + mondo_id + "):\n")
        disease_list.append((disease_name, mondo_id))
    
    elif args.diseaseTable:
        disease_table_filename = args.diseaseTable
        print("Table of diseases specified in file:\t\t" + disease_table_filename + "\n")
        with open(disease_table_filename, "r") as diseases:
            for entry in diseases.readlines():
                mondo_id = entry.strip()
                disease_name = DiseaseNameLookup(mondo_id).disease_name
                disease_list.append((disease_name, mondo_id))
    
    elif args.geneTable:
        gene_table_filename = args.geneTable
        print("Table of input genes specified in file:\t" + gene_table_filename + "\n")
        with open(gene_table_filename, "r") as gene_table:
            gene_table_lines = gene_table.readlines()
            query_name = gene_table_lines[0].strip()
            input_gene_symbols = [line.strip() for line in gene_table_lines[1:]]

    
    ## CX - it would be nice if we only initiated the models we were going to use. 
    ## otherwise we have to comment out modules here! 
    
    # Ontology Catalogs only need to be initialized once!
    functional_threshold = args.functionalThreshold
    print("Functional Similarity Threshold:\t" + str(functional_threshold))
    ## Functional similarity using Jaccard index threshold
    ## Called once, creating this object triggers
    ## its initialization with GO ontology and annotation
    print("Loading functional ontology (~4 minutes)...\n")
    func_sim_human = FunctionalSimilarity('human')

    phenotype_threshold = args.phenotypeThreshold
    print("Phenotype Similarity Threshold: \t" + str(phenotype_threshold))
    ## Phenotype similarity using OwlSim calculation threshold
    ## Called once, creating this object triggers
    ## its initialization with GO ontology and annotation
    print("Loading phenotype ontology...\n")
    pheno_sim_human = PhenotypeSimilarity('human')
    
    gene_interaction_threshold = args.geneInteractionThreshold
    print("Gene Interaction Threshold: \t\t" + str(gene_interaction_threshold))
    # Gene interactions curated in the Biolink (Monarch) resource
    print("Loading gene interaction info...\n")
    interactions_human = GeneInteractions()
    
    gene_gene_bicluster_threshold = args.geneBiclusterThreshold
    print("Gene-Gene Bicluster Score Threshold: \t" + str(gene_gene_bicluster_threshold))

    ## split the workflow based on whether this is disease based or query/input-gene-list based:
    if args.geneTable:  # working with a query_name, input_gene_symbols (list of approved gene symbols)
        print("\nProcessing " + query_name + ":\n")
    
        ## need to translate hgnc symbols -> hgnc ids in input_gene_list
        # first get a UNIQUE list of the input genes 
        input_gene_symbols = list(set(input_gene_symbols))
    
        # second, convert hgnc symbols to hgnc ids
        translation = "./translator_modules/core/ids/HUGO_geneids_download_v2.txt"
    
        ## I'm writing out the list comprehension so I can add print statement 
        input_hgnc_ids = []
        final_input_gene_symbols = []
        for (input_id, output_id) in TranslateIDs(input_gene_symbols, translation, \
            in_id="Approved symbol", out_id="HGNC ID").results:
            ## CX: List entry is (input_id, None) if the key/input_id isn't found in the translation dict
            ## CX: (input_id, '') if output/converted_id isn't found in translation dict 
            if (output_id!='' and output_id!=None):
                input_hgnc_ids.append(output_id)
                final_input_gene_symbols.append(input_id)
            else:
                print("Error: Matching HGNC ID for "+input_id+" not found. Excluded from Workflow.") 
                        
        query_input_genes = pd.DataFrame.from_dict({'hit_id':input_hgnc_ids, \
                                        'hit_symbol':final_input_gene_symbols}, \
                                         orient = 'columns')
  
        if _echo_to_console:
            print("\nInput Gene Set for " + query_name + ":\n")
            print(query_input_genes.to_string())
    
        # intialize summary module object
        summary_mod = SummaryMod(query_name)

        ## run modules based on whether argument was given in command prompt
        print("\nRunning functional similarity module...")
        mod1a_results = \
            similarity(
                func_sim_human,
                query_input_genes,
                functional_threshold,
                'Mod1A',
                'Functionally Similar Genes'
            )
        
        ## This builds a brief summary for just this module and creates the across summary tables
        if not mod1a_results.empty:  # will only work if Mod1A returned results
            summary_mod.add_scorebased_module(mod1a_results) 
            if _echo_to_console:
                summary_mod.show_single_mod_summary('Mod1A')
        else:
            print("Mod1A (Functional similarity) returned no results. Not included in summary.")
                
        print("\nRunning phenotypic similarity module...")            
        print("Note: current ontobio bug means that genes with EFO annotation won't be included in this module.")              
        mod1b_results = \
            similarity(
                pheno_sim_human,
                query_input_genes,
                phenotype_threshold,
                'Mod1B',
                'Phenotypic Similar Genes'
            )
        
        ## Add output to brief summary
        if not mod1b_results.empty:
            summary_mod.add_scorebased_module(mod1b_results)
            if _echo_to_console:
                summary_mod.show_single_mod_summary('Mod1B')
        else:
            print("Mod1B (phenotypic similarity) returned no results. Not included in summary module.")
                
        print("\nRunning gene interaction module...")            
        # Find Interacting Genes from Monarch data
        mod1e_results = \
            gene_interactions(
                interactions_human,
                query_input_genes,
                gene_interaction_threshold,
                'Mod1E',
                "Gene Interactions"
            )
            
        ## JG: Add output into summary 
        if not mod1e_results.empty:
            summary_mod.add1E(mod1e_results)
            if _echo_to_console:
                summary_mod.show_single_mod_summary('Mod1E')   
        else:
            print("Mod1E (gene-gene interactions) returned no results. Not included in summary module.")
          
        print("\nRunning gene-gene bicluster module...")                        
        # Find gene-gene bicluster information (from WF9)      
        gene_bicluster_results = gene_gene_bicluster( 
                                    query_input_genes, 
                                    gene_gene_bicluster_threshold,
                                    'gene_gene_bicluster'
                                    )
        
        if not gene_bicluster_results.empty:
            summary_mod.add_scorebased_module(gene_bicluster_results)
            if _echo_to_console:
                summary_mod.show_single_mod_summary('gene_gene_bicluster')  
        else:
            print("gene_gene_bicluster returned no results. Not included in summary module.")
        
        ## END OF WORKFLOW  
        if _echo_to_console:
            summary_mod.show_mods()  # CX: show the user what modules they ran in their analysis
    
        ## Write all out
        summary_csv_filenames = [query_name.replace(" ", "_") + '_brief_summary.csv', \
                                 query_name.replace(" ", "_") + '_full_summary.csv']
        summary_json_filenames = [query_name.replace(" ", "_") + '_brief_summary.json', \
                                  query_name.replace(" ", "_") + '_full_summary.json']
        
        summary_mod.write_all_csv(summary_csv_filenames[0], summary_csv_filenames[1])
        summary_mod.write_all_json(summary_json_filenames[0], summary_json_filenames[1])        
        
    ## not empty for disease table or single disease 
    elif disease_list!=[]:  
        # Initalizing list of summaries, mainly to accommodate file of diseases 
        disease_summaries = []
    
        for disease_name, mondo_id in disease_list:
            
            print("\nProcessing " + disease_name + "(" + mondo_id + "):\n")
    
            disease_associated_gene_set = \
                disease_gene_lookup(
                    mondo_id
                )
            """
            CX: disease_associated_gene_set inherits from Payload (abstract base class 'ABC')
            It has the class variables mod (I don't know what this is), results and the function get_data_frame
            The function get_data_frame returns the results object from DiseaseAssociatedGeneSet (input gene df). 
            """
    
            if _echo_to_console:
                print(
                    "\nDisease Associated Input Gene Set for " +
                    disease_name + "(" + mondo_id + "):\n")
                print(disease_associated_gene_set.get_data_frame().to_string())
    
            # intialize summary module object
            summary_mod = SummaryMod(disease_name)

            print("\nRunning functional similarity module...")
            mod1a_results = \
                similarity(
                    func_sim_human,
                    disease_associated_gene_set.get_data_frame(),
                    functional_threshold,
                    'Mod1A',
                    'Functionally Similar Genes'
                )
        
            ## This builds a brief summary for just this module and creates the across summary tables
            if not mod1a_results.empty:  # will only work if Mod1A returned results
                summary_mod.add_scorebased_module(mod1a_results) 
                if _echo_to_console:
                    summary_mod.show_single_mod_summary('Mod1A')
            else:
                print("Mod1A (Functional similarity) returned no results. Not included in summary module.")
                  
            print("\nRunning phenotypic similarity module...")   
            print("Note: current ontobio bug means that genes with EFO annotation won't be included in this module.")              
            mod1b_results = \
                similarity(
                    pheno_sim_human,
                    disease_associated_gene_set.get_data_frame(),
                    phenotype_threshold,
                    'Mod1B',
                    'Phenotypic Similar Genes'
                )
            
            ## Add output to brief summary
            if not mod1b_results.empty:
                summary_mod.add_scorebased_module(mod1b_results)
                if _echo_to_console:
                    summary_mod.show_single_mod_summary('Mod1B')
            else:
                print("Mod1B (Phenotypic similarity) returned no results. Not included in summary module.")
                   
            print("\nRunning gene interaction module...")               
            # Find Interacting Genes from Monarch data
            mod1e_results = \
                gene_interactions(
                    interactions_human,
                    disease_associated_gene_set.get_data_frame(),
                    gene_interaction_threshold,
                    'Mod1E',
                    "Gene Interactions"
                )
                
            ## JG: Add output into summary 
            if not mod1e_results.empty:
                summary_mod.add1E(mod1e_results)
                if _echo_to_console:
                    summary_mod.show_single_mod_summary('Mod1E')         
            else:
                print("Mod1E (gene-gene interactions) returned no results. Not included in summary module.")

            print("\nRunning gene-gene bicluster module...")                               
            # Find gene-gene bicluster information (from WF9)                      
            gene_bicluster_results = gene_gene_bicluster( 
                                        disease_associated_gene_set.get_data_frame(), 
                                        gene_gene_bicluster_threshold,
                                        'gene_gene_bicluster'
                                        )
            
            if not gene_bicluster_results.empty:
                summary_mod.add_scorebased_module(gene_bicluster_results)
                if _echo_to_console:
                    summary_mod.show_single_mod_summary('gene_gene_bicluster')  
            else:
                print("gene_gene_bicluster returned no results. Not included in summary.")
                        
            ## Put summary in list (only used when multiple diseases in one file are queried at once)
            disease_summaries.append(summary_mod)
    
            ## END OF WORKFLOW
            if _echo_to_console:
                summary_mod.show_mods()  # CX: show the user what modules they ran in their analysis
    
            ## Write all out            
            summary_csv_filenames = [disease_name.replace(" ", "_") + '_brief_summary.csv', \
                                     disease_name.replace(" ", "_") + '_full_summary.csv']
            summary_json_filenames = [disease_name.replace(" ", "_") + '_brief_summary.json', \
                                      disease_name.replace(" ", "_") + '_full_summary.json']
            
            summary_mod.write_all_csv(summary_csv_filenames[0], summary_csv_filenames[1])
            summary_mod.write_all_json(summary_json_filenames[0], summary_json_filenames[1])
        

    print("\nWF2 Processing complete!")

    # Success!
    exit(0)


if __name__ == '__main__':
    main()
