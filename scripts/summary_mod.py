# Written by Colleen Xu
# using Python 3.7
# Original version written 20190603 by Megan Grout (groutm@ohsu.edu) ; Jacob Gutierrez (gutierja@ohsu.edu) 6/10/19 ; Colleen Xu (xco@ohsu.edu) 6/10/19 
#
# The purpose of this script is to create an class to aggregate and display summary data from the modules.

# Import libraries
import pandas as pd
import numpy as np

# Main class
class SummaryMod(object):
    # Initializing function
    def __init__(self, disease_name='NA', mondo_id='MONDO:XXXXXXX'):
        # Store the disease names and mondo id
        self.disease_name = disease_name
        self.mondo_id = mondo_id
        
#        # Store a set of the input gene symbols
#        self.input_gene_set = [x['hit_symbol'] for x in input_gene_set]

        # Store current modules being used
        self.current_mods = list()

        # Stores brief summary tables for individual modules 
        self.module_summaries = dict()

        # Dataframes for summaries across modules 
        self.brief_summary = pd.DataFrame()
        self.full_summary = pd.DataFrame(columns = ['hit_symbol','hit_id', 'input_symbol', 'input_id'])

    # Method formats the disease name for printing 
    def format_print(self, title=''):
        print('\n' + title + ' for ' +
                  self.disease_name + '(' + self.mondo_id + '):\n')

    def build_full_summary(self, mod_results):
        """
        Called within the add1A, add1B, etc. modules.
        Combines existing full_summary with the individual module's processed results each time it's called
        Method builds the full summary as a pandas dataframe
        Returns nothing

        Updates the self.full_summary dataframe by merging the new mod_results data into self.full_summary by input-output gene. 
        If the input-output gene relationship already exists, new columns are added to the end reflecting the new relationship.
        """
        # Combine existing full_summary with module data 
        self.full_summary = pd.merge(self.full_summary, mod_results, on=['hit_symbol', 'hit_id', 'input_symbol','input_id'], how='outer')        


    def build_brief_summary(self):
        """
        This method builds the brief summary as a pandas dataframe. 
        It returns nothing and takes no parameters.
        
        Everytime it's called, the brief_summary is built from scratch from the full summary pandas df. 

        The brief table displays each unique output gene in one row. 
        """
        self.brief_summary = pd.DataFrame.copy(self.full_summary)
        
        # turn input_symbols, scores, ranks into lists. 
        # Note that default groupby will cause issues with the index (hit_symbol becomes index) that needs to be reset below 
        self.brief_summary = self.brief_summary.groupby(['hit_symbol', 'hit_id']).agg(list)
        self.brief_summary.reset_index(inplace=True)  # move output gene to its own column

        
        # now I have lists with NAs inside. Need to get NAs removed. 
        original_count_cols = ['num_protein_interactions']
        removing_NA_cols = [i for i in self.brief_summary.columns if (i.endswith('_score') or i.endswith('_rank') or \
                                                                      i in original_count_cols)]
        for col in removing_NA_cols:
            self.brief_summary[col] = [list(pd.Series(x).dropna()) for x in self.brief_summary[col]]
            ## WIP: following line of code causes error with adding MOD1B SUMMARY. move to later in function?
            ## remove empty lists, replace with empty cells
#            self.brief_summary[col] = [np.nan if x==list() else x for x in self.brief_summary[col]]
            
            # create new columns counting the number of scores for Mod1A, Mod1B
            if col.endswith('_score'):
                ## creating new col name by removing _score from the end
                new_col_name = col[:-6] + '_count'
                self.brief_summary[new_col_name] = [len(x) for x in self.brief_summary[col]]
                # replace any 0 (no scores/ranks/counts in list) with empty cell
                self.brief_summary[new_col_name] = [np.nan if x==0 else x for x in self.brief_summary[new_col_name]]
            
            # calculate actual count of protein interactions from length of list, rank
            elif col=='num_protein_interactions':
                self.brief_summary['protein_interaction_count'] = [len(x) for x in self.brief_summary[col]]
                # replace any 0 (no counts in list) with empty cell
                self.brief_summary['protein_interaction_count'] = [np.nan if x==0 else x for x in self.brief_summary['protein_interaction_count']]
                # Smaller ranks = higher scores. This is easier: if larger scores = better, rank depends on how many entries are in table
                self.brief_summary['interaction_count_rank'] = self.brief_summary['protein_interaction_count'].rank(ascending=False, method='min')
                # drop original column, use protein_interaction_count from now on 
                self.brief_summary.drop('num_protein_interactions',axis=1,inplace=True)  
        
        ## Calculating total hits, number of modules
        self.brief_summary['total_hits'] = self.brief_summary.filter(regex=('_count$')).sum(axis=1)
        self.brief_summary['num_modules'] = self.brief_summary.filter(regex=('_count$')).count(axis=1)
    
        ## adding a column to mark whether output gene is input gene (disease associated) or not
        # first, find the set of input genes in the table
        input_genes = set()
        for x in self.brief_summary['input_symbol']:
            if x!=list():
                input_genes.update(x)
        # make column comparing output_gene symbol to input_genes set
        self.brief_summary['is_input_gene'] = ['Y' if x in input_genes else 'N' for x in self.brief_summary['hit_symbol']]

        # sort table by number of modules, then total hits, then hit_symbol 
        self.brief_summary = self.brief_summary.sort_values(by=['num_modules','total_hits', 'hit_symbol'], ascending=[False, False, True])
 
        ## CX: next is reordering columns     
        cols_to_order = ['hit_symbol', 'hit_id', 'input_symbol', 'input_id', 'is_input_gene', 'num_modules', 'total_hits', \
                         'functional_sim_count', 'phenotype_sim_count', 'protein_interaction_count']
        ## puts columns I want to order in front/in order if they are in dataframe. Then puts everything else. 
        cols = [x for x in cols_to_order if x in self.brief_summary] + [x for x in self.brief_summary if x not in cols_to_order]
        self.brief_summary = self.brief_summary.reindex(columns=cols)

        
        # Reordering full summary based on brief summary
        new_row_order = self.brief_summary['hit_symbol'].tolist() # get row names (output_genes)
        new_rows_idx = dict(zip(new_row_order,range(len(new_row_order)))) # make ordered dict of output_genes 
        self.full_summary['output_rank'] = self.full_summary['hit_symbol'].translate(new_rows_idx) # map the full summary to this order
        self.full_summary = self.full_summary.sort_values('output_rank') # Sort based on new mapping
        self.full_summary = self.full_summary.drop('output_rank',axis=1) # Remove the sorting column


    def add_scorebased_module(self, results):
        """
        This includes Module 1A, 1B, WF9 modules?
        Input: results dataframe with the following columns: 'hit_id', 'hit_symbol', 'input_id', 'input_symbol', 'score',
       'shared_term_names', 'shared_terms', 'module'
        Drops columns, removes duplicate gene symbol rows, renames columns, creates rank columns
        Builds full summary, brief summary, and individual module output table
        """
        # record what module the results are from
        module = list(results['module'])[0]    
        
        # WIP: drop duplicate gene symbols. BUT maybe we want to keep these?
        processed_results = results.drop_duplicates(subset=['input_symbol','hit_symbol'])        

        if results.empty==True:  ## don't need to go forward 
            print(module + " returned no results and was not loaded into summary.")
            return  ## exit function
        
        else:  ## run normally
            # drop irrelevant columns
    #        processed_results = results.drop(columns=['shared_terms','shared_term_names', 'module'])
            processed_results = processed_results.drop(columns=['shared_term_names', 'module'])
        
            
            # ADD ELIF statements for additional columns
            # rename columns according to module the results are from, create ranks
            # Smaller ranks = higher scores. This is easier: if larger scores = better, rank depends on how many entries are in table
            if module=='Mod1A':
                processed_results = processed_results.drop(columns=['shared_terms'])
                processed_results = processed_results.rename(index = str, columns = {'score':'functional_sim_score'})
                processed_results['functional_sim_rank'] = processed_results['functional_sim_score'].rank(ascending=False, method='min')        
    
            elif module=='Mod1B':
                ## ISSUE WITH EFO 'PHENOTYPE' TERMS
                ## wait this code doesn't seem to be working for lafora disease because all results are filtered out by loc statement
                ## ..but it's working for fanconi anemia...
                processed_results = processed_results.loc[[False if "EFO" in str(x) else True for x in processed_results.shared_terms],:]

                ## Like in Lafora Disease case, if processed_results is empty there's no need to go forward
                if processed_results.empty==True:
                    print(module + " returned no results and was not loaded into summary.")
                    return  ## exit function
                
                ## The following code continues for Mod1B output if processed_results wasn't empty
                processed_results = processed_results.drop(columns=['shared_terms'])
                processed_results = processed_results.rename(index = str, columns = {'score':'phenotype_sim_score'})            
                processed_results['phenotype_sim_rank'] = processed_results['phenotype_sim_score'].rank(ascending=False, method='min')          
            
            else:  ## what to do if module not recognized. placeholder code?
                print("Module not recognized and not loaded into summary.")
                return  ## exit function
            
            ## run for any module (when processed results aren't empty)
            # Update full table
            self.build_full_summary(processed_results)
    
            # Update brief table
            self.build_brief_summary()
            
            # Make individual module summary (counts number of input genes corresponding to a unique output gene for this module)
            individual_sum = pd.DataFrame.copy(processed_results)
            individual_sum = individual_sum.groupby(['hit_symbol']).agg(list)  # grouping by unique output gene
            individual_sum['sim_count'] = [len(x) for x in individual_sum.filter(regex='_score$', axis=1).squeeze()]
            ## WARNING: if other columns of lists were included, they would no longer correspond to input_symbols after this sorting
            ## columns: input_id, functional_sim_score, functional_sim_rank
            individual_sum['input_symbol'] = [sorted(x) for x in individual_sum['input_symbol']] 
            # Smaller ranks = higher scores. 
            individual_sum = individual_sum.sort_values(by=['sim_count','hit_symbol'], ascending=[False, True]).reset_index()
            individual_sum = individual_sum.filter(items=['hit_symbol', 'input_symbol', 'sim_count'])
            self.module_summaries[module] = individual_sum        
        

    # This function takes in the Module1E results and updates both tables
    # NOTE: could be expanded to work with more presence/absence modules (where counting presence makes sense)
    def add1E(self, results):
        # WIP: drop duplicate gene symbols. BUT maybe we want to keep these?
        processed_results = results.drop_duplicates(subset=['input_symbol','hit_symbol'])

        if results.empty==True:          ## don't need to go forward 
            print("Mod1E returned no results and was not loaded into summary.")
            return  ## exit function
        
        else:        ## going forward normally
            processed_results = processed_results.drop(columns=['module'])
            processed_results = processed_results.rename(index = str, columns = {'score':'num_protein_interactions'})
            
            # Update full table
            self.build_full_summary(processed_results)
    
            # Update brief table
            self.build_brief_summary()
            
            ## NEED TO UPDATE THIS PART'S COLUMN NAMES IN ORDER TO EXPAND THIS FUNCTION TO OTHER MODULES
            # Make individual module summary (counts number of input genes corresponding to a unique output gene for this module)
            individual_sum = pd.DataFrame.copy(processed_results)
            individual_sum = individual_sum.groupby(['hit_symbol']).agg(list)
            # adjust the columns' values: number of hits found, sort input genes
            individual_sum['protein_interaction_count'] = [len(x) for x in individual_sum['num_protein_interactions']]
            ## WARNING: input_id list won't correspond to input_symbols after this sorting
            individual_sum['input_symbol'] = [sorted(x) for x in individual_sum['input_symbol']]
            # Smaller ranks = higher scores. 
            individual_sum = individual_sum.sort_values(by=['protein_interaction_count','hit_symbol'], ascending=[False, True]).reset_index()
            individual_sum = individual_sum.filter(items=['hit_symbol', 'input_symbol', 'protein_interaction_count'])
            self.module_summaries['Mod1E'] = individual_sum
        

## Possible NEXT STEP: condensing these functions? like get_brief/full, show_brief/full, write_brief/full

    # Method takes in a query or list of queries (module names) and returns their brief summary
  
    def show_single_mod_summary(self,query):
        # check if single query and make into list if it is
        if isinstance(query, str):
            query = [query] # make it into list of one 

        # For each query in the list display the individual summary
        for mod in query:
            if mod in self.module_summaries.keys():
                self.format_print(mod + ' results')
                print(self.module_summaries[mod].to_string())
            else:
                print('module query not found')
        return 

    # Method returns list of modules (based on individual summary tables)
    def get_single_mod_summaries(self):
        return self.module_summaries

    # This function prints to screen the current modules loaded into the object 
    # referencing the current individual module summaries stored
    def show_mods(self):
        self.current_mods = list(self.module_summaries.keys())
        print('Modules Currently Loaded: ' + \
            ', '.join(self.current_mods))
        
    # Method returns list of current modules 
    def get_mods(self):
        self.current_mods = list(self.module_summaries.keys())
        return self.current_mods

    # This function prints the brief summary to console
    def show_brief(self):
        self.format_print('Brief Summary Table')
        print(self.brief_summary.to_string())
        
     # This function returns the brief table
    def get_brief(self):
        return self.brief_summary

    # This function prints the full summary to console
    def show_full(self):
        self.full_summary.reset_index(drop=True, inplace=True)
        self.format_print('Full Summary Table')
        print(self.full_summary.to_string())

    # This function returns the full table 
    def get_full(self):
        self.full_summary.reset_index(drop=True, inplace=True)
        return self.full_summary

    # This function returns both the brief and full summary tables 
    def get_all(self):
        return self.get_brief(), self.get_full()

    # Function prints both brief and full summary tables
    def show_all(self):
        self.format_print('Both Brief and Full Summary Tables')
        self.show_brief()
        self.show_full()
        

    # This function writes the brief summary table to csv
    # An optional parameter specifies the filename
    def write_brief_csv(self, filename ='brief_summary.csv'):
        self.brief_summary.to_csv(filename, index=False)  

    # This function writes the full table to csv
    # An optional parameter specifies the filename
    def write_full_csv(self, filename='full_summary.csv'):
        self.full_summary.reset_index(drop=True, inplace=True)
        self.full_summary.to_csv(filename, index=False)

    # This function writes both the brief and full tables to csv and json 
    def write_all_csv(self, brief_name, full_name):
        self.write_brief_csv(brief_name)
        self.write_full_csv(full_name)

    # This function writes the brief table to json
    # An optional parameter specifies the filename
    def write_brief_json(self, filename='brief_summary.json'):
        self.brief_summary.to_json(filename)

    # This function writes the full table to json
    # An optional parameter specifies the filename
    def write_full_json(self, filename='full_summary.json'):
        self.full_summary.reset_index(drop=True, inplace=True)
        self.full_summary.to_json(filename)

    # This function writes both the brief and full tables to json
    def write_all_json(self, brief_name, full_name):
        self.write_brief_json(brief_name)
        self.write_full_json(full_name)