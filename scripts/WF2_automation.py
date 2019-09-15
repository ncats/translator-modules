#!/usr/bin/env python3

# Uncomment when we need to debug
# import logging
# logging.basicConfig(level=logging.INFO)

import requests
from os import makedirs
from pathlib import Path
import argparse

import pandas as pd
from html3.html3 import XHTML


from translator_modules.disease.gene.disease_associated_genes import DiseaseAssociatedGeneSet
from translator_modules.gene.gene.functional_similarity import FunctionalSimilarity
from translator_modules.gene.gene.phenotype_similarity import PhenotypeSimilarity
from translator_modules.gene.gene.gene_interaction import GeneInteractions
from translator_modules.core.standard_output import StandardOutput

_SCRIPTNAME = 'WF2_automation.py'

# Flag to control console output
_echo_to_console = False


# Data type of switch input is interpreted as a Boolean value
def set_console_echo(switch):
    global _echo_to_console
    _echo_to_console = switch


def output_file(tag, title, ext):
    # takes the tidbit directory that is relative to the current directory
    # parameterized across two functions so that it's made explicit without
    # over-encoding the paths within their constructor arguments (makes it easier to edit.)

    folder_name = tag.replace(" ", "_")
    tidbit_path = Path("Tidbit").relative_to(".") / folder_name

    filename = title.replace(" ", "_")
    output_file_path = tidbit_path / (filename + "." + ext)
    makedirs(tidbit_path, exist_ok=True)

    # Path objects compatible with file operations
    output = open(output_file_path, "w+")
    output.info = {'tag': tag, 'title': title}
    return output


def dump_html(output, body, columns=None):
    title = output.info['title'] + " for " + output.info['tag']

    doc = XHTML()

    doc.head.title(title)
    doc.body.h1(title)
    doc.body.p.text(body.to_html(escape=False, columns=columns), escape=False)

    output.write(str(doc))


def disease_gene_lookup(disease_name, mondo_id):
    gene_set = DiseaseAssociatedGeneSet(mondo_id)

    # save the seed gene definition and gene list to a
    # file under the "Tidbit/<symbol>" subdirectory

    output = output_file(disease_name, "Definition", "json")
    gene_set.echo_input_object(output)
    output.close()

    # save the gene list to a file under the "Tidbit" subdirectory
    df = gene_set.get_data_frame()

    # Dump HTML representation
    output = output_file(disease_name, "Disease Associated Genes", "html")
    dump_html(output, df)
    output.close()

    # Dump JSON representation
    output = output_file(disease_name, "Disease Associated Genes", "json")
    df.to_json(output)
    output.close()

    # genes to investigate
    return gene_set


STD_RESULT_COLUMNS = ['hit_id', 'hit_symbol', 'input_id', 'input_symbol', 'score']


def similarity(model, disease_associated_gene_set, threshold, module, title):
    input_gene_set = disease_associated_gene_set.get_data_frame()

    # Perform the comparison on specified gene set
    results = model.compute_similarity(input_gene_set, threshold)

    results['module'] = module

    # save the gene list to a file under the "Tidbit" subdirectory

    # Dump HTML representation
    output = output_file(disease_associated_gene_set.get_input_disease_name(), title, "html")
    dump_html(output, results, columns=STD_RESULT_COLUMNS)
    output.close()

    # Dump JSON representation
    output = output_file(disease_associated_gene_set.get_input_disease_name(), title, "json")
    results.to_json(output)
    output.close()

    return results


def gene_interactions(model, disease_associated_gene_set, threshold, module, title):
    input_gene_set = disease_associated_gene_set.get_data_frame()

    # Perform the comparison on specified gene set
    results = model.get_interactions(input_gene_set, threshold)

    results['module'] = module

    # save the gene list to a file under the "Tidbit" subdirectory

    # Dump HTML representation
    output = output_file(disease_associated_gene_set.get_input_disease_name(), title, "html")
    dump_html(output, results)
    output.close()

    # Dump JSON representation
    output = output_file(disease_associated_gene_set.get_input_disease_name(), title, "json")

    # dumping the whole table in the JSON? or should I just dump the head?
    results.to_json(output)
    output.close()

    return results


def aggregate_results(results_a, results_b, input_object_id):
    all_results = pd.concat([results_a, results_b])
    so = StandardOutput(results=all_results.to_dict(orient='records'), input_object_id=input_object_id)
    return so.output_object


def publish_to_rtx(std_api_response_json, input_disease_symbol, input_disease_mondo, title):
    # get the URL for these results displayed in the RTX UI
    rtx_ui_request_url = "https://rtx.ncats.io/api/rtx/v1/response/process"
    to_post = {"options": ["Store", "ReturnResponseId"], "responses": [std_api_response_json]}
    rtx_ui_url = requests.post(rtx_ui_request_url, json=to_post)

    # Write out a master index web page
    output = output_file(input_disease_symbol, "index", "html")
    file_index(output, input_disease_symbol, input_disease_mondo, rtx_ui_url)
    output.close()

    return rtx_ui_url


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
Comma delimited 'name, MONDO identifier'
2-tuple string of a single disease to analyze"""
                               )

    # disease input as a list
    disease_query.add_argument('-l', '--diseaseTable',
                               help="""
name of a tab delimited text file table of disease names - in the first column - 
and associated MONDO identifiers - in the second column"""
                               )

    parser.add_argument('-f', '--functionalThreshold',
                        type=float, default=0.75, help='value of Functional Similarity threshold')

    parser.add_argument('-p', '--phenotypeThreshold',
                        type=float, default=0.35, help='value of Phenotype Similarity threshold')

    parser.add_argument('-g', '--geneInteractionThreshold',
                        type=float, default=12, help='value of Gene Interaction threshold')

    args = parser.parse_args()

    print("\nRunning the " + _SCRIPTNAME + " script...")

    if args.verbose:
        print("Echoing results verbosely to the console!\n")
        set_console_echo(True)

    # read in the diseases to analyze
    disease_list = []

    if args.disease:
        disease_name, mondo_id = args.disease.split(',')
        disease_name = disease_name.strip()
        print("\nSingle disease specified:\t" + disease_name + "(" + mondo_id + "):\n")
        disease_list.append((disease_name, mondo_id))

    elif args.diseaseTable:

        disease_table_filename = args.diseaseTable
        print("Table of diseases specified in file:\t\t" + disease_table_filename)

        with open(disease_table_filename, "r") as diseases:
            for entry in diseases.readlines():

                field = entry.split("\t")

                # Skip the header
                if str(field[0]).lower() == "disease":
                    continue

                # The first field is assumed to be the gene name or symbol, the second field, the MONDO identifier
                disease_name = field[0]
                disease_name = disease_name.strip()

                mondo_id = field[1]

                disease_list.append((disease_name, mondo_id))

    functional_threshold = args.functionalThreshold
    print("Functional Similarity Threshold:\t" + str(functional_threshold))

    phenotype_threshold = args.phenotypeThreshold
    print("Phenotype Similarity Threshold: \t" + str(phenotype_threshold))

    gene_interaction_threshold = args.geneInteractionThreshold
    print("Gene Interaction Threshold: \t\t" + str(gene_interaction_threshold))

    print("\nLoading source ontology and annotation...")

    # Ontology Catalogs only need to be initialized once!

    # Functional similarity using Jaccard index threshold
    # Called once, creating this object triggers
    # its initialization with GO ontology and annotation
    func_sim_human = FunctionalSimilarity('human')

    # Phenotype similarity using OwlSim calculation threshold
    # Called once, creating this object triggers
    # its initialization with GO ontology and annotation
    pheno_sim_human = PhenotypeSimilarity('human')

    # Gene interactions curated in the Biolink (Monarch) resource
    interactions_human = GeneInteractions()

    # Initalizing list of summaries, for use with a file of diseases
    disease_summaries = []

    # diseases.tsv is assumed to be a tab delimited
    # file of diseases named (column 0) with their MONDO identifiers (column 1)
    # The optional header should read 'Disease' in the first column
    for disease_name, mondo_id in disease_list:

        print("\nProcessing " + disease_name + "(" + mondo_id + "):\n")

        disease_associated_gene_set = \
            disease_gene_lookup(
                disease_name,
                mondo_id
            )

        if _echo_to_console:
            print(
                "\nDisease Associated Input Gene Set for " +
                disease_name + "(" + mondo_id + "):\n")
            print(disease_associated_gene_set.get_data_frame().to_string())

        mod1a_results = \
            similarity(
                func_sim_human,
                disease_associated_gene_set,
                functional_threshold,
                'Mod1A',
                'Functionally Similar Genes'
            )

        ## This builds a brief summary for just this module and creates the across summary tables
        if not mod1a_results.empty:  # will only work if Mod1A returned results
            summary_mod.add_scorebased_module(mod1a_results)
            if _echo_to_console:
                summary_mod.show_single_mod_summary('Mod1A')

        mod1b_results = \
            similarity(
                pheno_sim_human,
                disease_associated_gene_set,
                phenotype_threshold,
                'Mod1B',
                'Phenotypic Similar Genes'
            )

        ## Add output to brief summary
        if not mod1b_results.empty:
            summary_mod.add_scorebased_module(mod1b_results)
            if _echo_to_console:
                summary_mod.show_single_mod_summary('Mod1B')

        # Find Interacting Genes from Monarch data
        mod1e_results = \
            gene_interactions(
                interactions_human,
                disease_associated_gene_set,
                gene_interaction_threshold,
                'Mod1E',
                "Gene Interactions"
            )

        ## JG: Add output into summary
        if not mod1e_results.empty:
            summary_mod.add1E(mod1e_results)
            if _echo_to_console:
                summary_mod.show_single_mod_summary('Mod1E')


            std_api_response_json = \
                aggregate_results(
                    mod1a_results,
                    mod1b_results,
                    disease_associated_gene_set.get_input_disease_id()
                )

            # Echo to console
            if _echo_to_console:
                print("\nAggregate Mod1A and Mod1B Results as JSON for '" +
                      disease_name + "(" + mondo_id + "):\n")
                print(std_api_response_json)

    print("\nWF2 Processing complete!")

    # Success!
    exit(0)


if __name__ == '__main__':
    main()