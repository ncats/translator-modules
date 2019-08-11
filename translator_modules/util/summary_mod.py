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

        # Store current modules being used
        self.current_mods = list()

        # Stores brief summary tables for individual modules 
        self.module_summaries = dict()

        # Dataframes for summaries across modules 
        self.brief_summary = pd.DataFrame()
        self.full_summary = pd.DataFrame(columns = ['hit_symbol','input_symbol', 'input_id', 'hit_id'])

    # Method formats the disease name for printing 
    def format_print(self, title=''):
        print("\n" + title + " for " +
                  self.disease_name + "(" + self.mondo_id + "):\n")

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
        ## CX if i included 'module' column, after I merge, I have two versions of module column: module x and module y. need to merge them. 
#        print("full sum columns\n")
#        print(self.full_summary.columns)
#        self.full_summary.reset_index(drop=True, inplace=True) 
        
#        if 'module_x' in self.full_summary.columns:
#            self.full_summary['module'] = self.full_summary[['module_x','module_y']].apply(list, axis=1)
#            self.full_summary.drop(['module_x','module_y'],axis=1,inplace=True)


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
        
        ## TO DO: rename columns: prefix num for "score" columns!
        ## then don't need the awkward including of protein interactions for some later code
        ## need to dropna for the rank columns too maybe
        ## error where some rows are missing rank sums. 
        
#        print("\nBefore reseting index after group by\n")
#        print(self.brief_summary.columns)
#        self.brief_summary.reset_index(inplace=True) 
#        print("\nAfter resetting index\n")
#        print(self.brief_summary.columns)
        
        # convert score/interaction/module lists to counts
        other_counted_cols = ['num_protein_interaction']
        counted_columns = [i for i in self.brief_summary.columns if (i.endswith('_score') or i in other_counted_cols)]
        for col in counted_columns:
            self.brief_summary[col] = [len(pd.Series(x).dropna()) for x in self.brief_summary[col]]
            self.brief_summary[col] = [np.nan if x==0 else x for x in self.brief_summary[col]]
        
        # IF num_protein_interactions included, calculate ranks 
        if 'num_protein_interaction' in self.brief_summary.columns: 
            self.brief_summary['protein_interaction_rank'] = self.brief_summary['num_protein_interaction'].rank(ascending=False, method='min')        
            # perhaps a way to turn one number into a list of one number
#            self.brief_summary['protein_interaction_rank'] = [[i] for i in self.brief_summary['protein_interaction_rank']]              
        
        ## DEBUGGING: I am looking at brief summary in this view to check counts in _score columns and lists in the rank columns 
        self.brief_summary = self.brief_summary.sort_values(by=['hit_symbol'], ascending=[True]).reset_index()
        
#        # Use ranks and module count to calculate a sorting_score 
#        # excluded ranks include any made above (in this function)
#        excluded_ranks = ['protein_interaction_rank']  
#        rank_columns = [i for i in self.brief_summary.columns if (i.endswith('_rank') and i not in excluded_ranks)]
#        
#        for col in rank_columns:
#            self.brief_summary[col] = [sum(x) for x in self.brief_summary[col]]
#        
#        ## CX: NOTICE this is the number of mods called so far! Not the num of mods that give that particular output gene
#        num_mods = len(self.module_summaries.keys())
#        self.brief_summary['sorting_score'] = self.brief_summary.filter(regex=("_rank$")).sum(axis=1) / num_mods        
#        
#        # sort table by sorting_score 
#        self.brief_summary = self.brief_summary.sort_values(by=['sorting_score','hit_symbol'], ascending=[False, True]).reset_index()
        
#        ## remove columns with "_rank" in them
#        droplist = [i for i in self.brief_summary.columns if i.endswith('_rank')]
#        self.brief_summary.drop(droplist,axis=1,inplace=True)
#        
#        # Make total_hits and reorder the columns 
#        other_counted_cols = ['num_protein_interaction']
#        counted_columns = [i for i in self.brief_summary.columns if (i.endswith('_score') or i in other_counted_cols)]
#        for col in counted_columns:
#            self.brief_summary[col] = [len(x) for x in self.brief_summary[col]]
#        self.brief_summary['total_hits'] =  self.brief_summary.drop(['input_symbol', 'input_id'], axis=1).sum(axis=1)
#
#        # Send the total lines_of_evidence to the second columns
#        cols = self.brief_summary.columns.tolist() # Find column names 
#        cols.insert(0, cols.pop(cols.index('input_symbol'))) # input_gene is first
#        cols.insert(1, cols.pop(cols.index('total_hits'))) # total_hits is second then everything else is after that 
#        self.brief_summary = self.brief_summary.reindex(columns=cols)
#        
#        # Now sort
#        self.brief_summary = self.brief_summary.sort_values(['total_hits'],ascending =False)
#        self.brief_summary.reset_index(inplace=True)  # move output gene to its own column
        
        # Reordering full summary based on brief summary
        new_row_order = self.brief_summary['hit_symbol'].tolist() # get row names (output_genes)
        new_rows_idx = dict(zip(new_row_order,range(len(new_row_order)))) # make ordered dict of output_genes 
        self.full_summary['output_rank'] = self.full_summary['hit_symbol'].map(new_rows_idx) # map the full summary to this order
        self.full_summary = self.full_summary.sort_values('output_rank') # Sort based on new mapping
        self.full_summary = self.full_summary.drop('output_rank',axis=1) # Remove the sorting column


    # This function takes in the Module1A results and updates both summaries
    def add1A(self, mod1a_results):
        ##### Format Data for Cross Module Summary #####
        # drop irrelevant columns
        mod1a_processed = mod1a_results.drop(columns=['shared_terms','shared_term_names', 'module'])
        
        # drop duplicates in input
        mod1a_processed = mod1a_processed.drop_duplicates(subset=['input_symbol','hit_symbol'])
        
        # rename columns to match full_summary desired output column names
        mod1a_processed = mod1a_processed.rename(index = str, columns = {'score':'functional_sim_score'})

        ## CX: create ranks
        mod1a_processed['functional_sim_rank'] = mod1a_processed['functional_sim_score'].rank(ascending=False, method='min')        

        ##### Format Data for individual module Summary #####
        # rename score and keep only what will be used in mini-summary
        Mod1A = mod1a_results.rename(index=str, columns={'score':'functional_sim_count'}).filter(items=['hit_symbol', 'input_symbol', 'functional_sim_count']) 
        # turn input_symbol and functional sim count into lists 
        Mod1A = Mod1A.groupby(['hit_symbol']).agg(list)
        # adjust the columns' values: number of hits found, sort input genes
        Mod1A['functional_sim_count'] = [len(x) for x in Mod1A['functional_sim_count']]
        Mod1A['input_symbol'] = [sorted(x) for x in Mod1A['input_symbol']] ## Can't just do this if input_ids were included (need to stay corresponding to symbols)
        # sort table by number of hits, output gene name. then save it as a individual module summary
        Mod1A = Mod1A.sort_values(by=['functional_sim_count','hit_symbol'], ascending=[False, True]).reset_index()
        self.module_summaries['mod1A'] = Mod1A
        
        # Update full table
        self.build_full_summary(mod1a_processed)

        # Update brief table
        self.build_brief_summary()

    # This function takes in the Module1B results and updates both tables
    def add1B(self, mod1b_results):    
        ##### Format Data for Cross Module Summary #####
        # drop irrelevant columns
        mod1b_processed = mod1b_results.drop(columns=['shared_terms','shared_term_names', 'module'])
        
        # drop duplicates in input
        mod1b_processed = mod1b_processed.drop_duplicates(subset=['input_symbol','hit_symbol'])
        
        # rename columns to match desired full_summary output column names
        mod1b_processed = mod1b_processed.rename(index = str, columns = {'score':'phenotype_sim_score'})
        
        ## CX: create ranks
        mod1b_processed['phenotype_sim_rank'] = mod1b_processed['phenotype_sim_score'].rank(ascending=False, method='min')

        ##### Format Data for individual module Summary #####
        # rename score and keep only what will be used in mini-summary
        Mod1B = mod1b_results.rename(index=str, columns={'score':'phenotype_sim_count'}).filter(items=['hit_symbol', 'input_symbol', 'phenotype_sim_count']) 
        # turn input_symbol and phenotype sim count into lists 
        Mod1B = Mod1B.groupby(['hit_symbol']).agg(list)
        # adjust the columns' values: number of hits found, sort input genes
        Mod1B['phenotype_sim_count'] = [len(x) for x in Mod1B['phenotype_sim_count']]
        Mod1B['input_symbol'] = [sorted(x) for x in Mod1B['input_symbol']] ## Can't just do this if input_ids were included (need to stay corresponding to symbols)
        # sort table by number of hits, output gene name. then save it as a individual module summary
        Mod1B = Mod1B.sort_values(by=['phenotype_sim_count','hit_symbol'], ascending=[False, True]).reset_index()
        self.module_summaries['mod1B'] = Mod1B

        # Update full table
        self.build_full_summary(mod1b_processed)
    
        # Update brief table
        self.build_brief_summary()

    # This function takes in the Module1E results and updates both tables
    def add1E(self, mod1e_results):
        mod1e_processed = mod1e_results.drop(columns=['module'])
        
        ##### Format Data for Cross Module Summary #####        
        # drop duplicates in input
        mod1e_processed = mod1e_processed.drop_duplicates(subset=['input_symbol','hit_symbol'])

        # rename columns to match desired full_summary output column names
        mod1e_processed = mod1e_processed.rename(index = str, columns = {'score':'num_protein_interaction'})

        ##### Format Data for individual module Summary #####
        # rename score and keep only what will be used in mini-summary
        Mod1E = mod1e_results.rename(index=str, columns={'score':'num_protein_interaction'}).filter(items=['hit_symbol', 'input_symbol', 'num_protein_interaction']) 
        # turn input_symbol and phenotype sim count into lists 
        Mod1E = Mod1E.groupby(['hit_symbol']).agg(list)
        # adjust the columns' values: number of hits found, sort input genes
        Mod1E['num_protein_interaction'] = [len(x) for x in Mod1E['num_protein_interaction']]
        Mod1E['input_symbol'] = [sorted(x) for x in Mod1E['input_symbol']] ## Can't just do this if input_ids were included (need to stay corresponding to symbols)
        # sort table by number of hits, output gene name. then save it as a individual module summary
        Mod1E = Mod1E.sort_values(by=['num_protein_interaction','hit_symbol'], ascending=[False, True]).reset_index()
        self.module_summaries['mod1E'] = Mod1E
        
        # Update full table
        self.build_full_summary(mod1e_processed)

        # Update brief table
        self.build_brief_summary()

    # Method takes in a query or list of queries (module names) and returns their brief summary
    def show_single_mod_summary(self,query):

        # check if single query and make into list most extensible 
        if isinstance(query, str):
            query = [query] # make it into list of one 

        # For each query in the list display the brief data
        for mod in query:
            if mod in self.module_summaries.keys():
                self.format_print(mod + ' results')
                print(self.module_summaries[mod].to_string())
            else:
                print('module query not found')
        return 

    # Method returns list of brief summary tables for individual modules 
    def get_single_mod_summaries(self):
        return self.module_summaries

    # This function shows the current modules loaded into the object by referencing the current raw data stored
    def show_mods(self):
        self.current_mods = list(self.module_summaries.keys())
        print('Modules Currently Loaded: ' + \
            ', '.join(self.current_mods))
        
    # Method returns list of current modules used as dictionary keys
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
    def write_brief_csv(self, filename ="brief_summary.csv"):
        self.brief_summary.to_csv(filename, index=False)  

    # This function writes the full table to csv
    # An optional parameter specifies the filename
    def write_full_csv(self, filename="full_summary.csv"):
        self.full_summary.reset_index(drop=True, inplace=True)
        self.full_summary.to_csv(filename, index=False)

    # This function writes both the brief and full tables to csv and json 
    def write_all_csv(self, brief_name, full_name):
        self.write_brief_csv(brief_name)
        self.write_full_csv(full_name)

    # This function writes the brief table to json
    # An optional parameter specifies the filename
    def write_brief_json(self, filename="brief_summary.json"):
        self.brief_summary.to_json(filename)

    # This function writes the full table to json
    # An optional parameter specifies the filename
    def write_full_json(self, filename="full_summary.json"):
        self.full_summary.reset_index(drop=True, inplace=True)
        self.full_summary.to_json(filename)

    # This function writes both the brief and full tables to json
    def write_all_json(self, brief_name, full_name):
        self.write_brief_json(brief_name)
        self.write_full_json(full_name)