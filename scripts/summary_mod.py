# Written 20190603 by Megan Grout (groutm@ohsu.edu) ; Jacob Gutierrez (gutierja@ohsu.edu) 6/10/19 ; Colleen Xu (xco@ohsu.edu) 6/10/19 
# using Python 3
#
# The purpose of this script is to create an class to
# aggregate and display summary data from the automated
# modules.

# Import libraries
import pandas as pd


# Main class
class SummaryMod(object):

    # Initializing function
    def __init__(self, disease_name='NA', mondo_id='MONDO:XXXXXXX'):

        # Store the disease names and mondo id
        self.disease_name = disease_name
        self.mondo_id = mondo_id

        # Store current modules being used
        self.current_mods = list()

        # stores the dataframe from all the raw module output
        # The keys are 'mod1A', 'mod1B', etc. (the module names) 
        # This allows for retrival of raw data later on 
        self.raw_module_data = dict()

        # Stores brief summary tables for individual modules 
        self.module_summaries = dict()

        # Dataframes for summaries across modules 
        self.brief_summary = pd.DataFrame()
        self.full_summary = pd.DataFrame(columns = ['output_gene','input_gene'])

        # Stores the naming conventions for the summary columns
        self.module_names = dict()


    # Method formats the disease name for printing 
    def format_print(self, title=''):

        print("\n" + title + " for " +
                  self.disease_name + "(" + self.mondo_id + "):\n")

        # END


    # This method builds the full summary as a pandas dataframe. It returns nothing
    # and is given a pandas dataframe of an individual module's results.
    def build_full_summary(self, mod_results):
        """
        Method builds the full summary as a pandas dataframe.
        Combines existing full_summary with the individual module's results each time called
        
        Parameters: 
        mod_results >  Formatted module output with the following columns 

        output_gene | input_gene | Scores or Hits | Terms (optional)

        Output: None

        Updates the self.full_summary dataframe by merging the new mod_results data into self.full_summary by input-output gene. 
        If the input-output gene relationship already exists the new columns is added to the end reflecting the new relationship.
        """

        # Combine exisiting full_summary with mod pre-processed data
        # If full_summary is empty, it will only hold mod info and columns pertaining to particular mod
        self.full_summary = pd.merge(self.full_summary, mod_results, on=['input_gene','output_gene'], how='outer')        

#        ## CX: calculate sum of ranks for sorting
#        self.full_summary['sum_ranks'] = self.full_summary.filter(regex=("_rank$")).sum(axis=1)
#
#        # Now do the sorting
#        self.full_summary = self.full_summary.sort_values(['sum_ranks'], ascending = True)
#
#        # Now drop the column used to sort
#        self.full_summary = self.full_summary.drop(columns="sum_ranks")

        # End 


    def build_brief_summary(self):
        """
        This method builds the brief summary as a pandas dataframe. 
        It returns nothing and takes no parameters.
        
        Everytime it's called, the brief_summary is built from scratch from the full summary pandas df. 

        If optional terms are included, the self.module_names must be populated to format the columns 

        The brief table displays each unique output gene. The following columns show counts (number of lines of supporting evidence from each module). 

        Brief Table Format:
        output_gene | input_gene_cnts | lines_of_evidence | Mod1A_counts | etc...
        """
        self.brief_summary = pd.DataFrame.copy(self.full_summary)
        
        ## remove columns with "_rank" in them, rename columns
        droplist = [i for i in self.brief_summary.columns if i.endswith('_rank')]
        self.brief_summary.drop(droplist,axis=1,inplace=True)
        
        # Find counts of support for each unique output gene 
        self.brief_summary = self.brief_summary.groupby(['output_gene']).aggregate('count')
        
        ## This is used to rename the columns
        for term in self.module_names.keys():

            # Search for the title then replace with the dictionary created in the addmod___ method
            if term in list(self.brief_summary.columns.values):
                self.brief_summary = self.brief_summary.drop(columns=term)
                self.brief_summary = self.brief_summary.rename(
                    index=str, columns = self.module_names[term])

        # sort by the total number of input genes for each output gene
        # Make total lines_of_evidence and reorder the columns 
        self.brief_summary['lines_of_evidence'] =  self.brief_summary.drop('input_gene', axis=1).sum(axis=1)

        # Send the total lines_of_evidence to the second columns
        cols = self.brief_summary.columns.tolist() # Find column names 
        cols.insert(0, cols.pop(cols.index('input_gene'))) # input_gene is first
        cols.insert(1, cols.pop(cols.index('lines_of_evidence'))) # lines_of_evidence is second then everything else is after that 
        self.brief_summary = self.brief_summary.reindex(columns=cols)
        
        # Now sort
        self.brief_summary = self.brief_summary.sort_values(['lines_of_evidence'],ascending =False)
        self.brief_summary.reset_index(inplace=True)  # move output gene to its own column
        
        # Reordering full summary based on brief summary
        new_row_order = self.brief_summary['output_gene'].tolist() # get row names (output_genes)
        new_rows_idx = dict(zip(new_row_order,range(len(new_row_order)))) # make ordered dict of output_genes 
        self.full_summary['output_rank'] = self.full_summary['output_gene'].map(new_rows_idx) # map the full summary to this order
        self.full_summary = self.full_summary.sort_values('output_rank') # Sort based on new mapping
        self.full_summary = self.full_summary.drop('output_rank',axis=1) # Remove the sorting column
        # End


    # This function takes in the Module1A results and updates both summaries
    def add1A(self, mod1a_results):
        # Immediately store raw data
        self.raw_module_data['mod1A'] = mod1a_results

        ##### Format Data for Cross Module Summary #####
        ## Rename the columns
        self.module_names['Func_assoc_terms'] = {'Func_sim_score':'Func_sim_input_gene_ct'}

        # drop irrelevant columns
        mod1a_processed = mod1a_results.drop(columns=['hit_id','input_id','shared_terms','shared_term_names','module'])
        
        # drop duplicates in input
        mod1a_processed = mod1a_processed.drop_duplicates(subset=['input_symbol','hit_symbol'])
        
        # rename columns to match full_summary desired output column names
        mod1a_processed = mod1a_processed.rename(index = str, columns = {'hit_symbol':'output_gene','input_symbol':'input_gene','score':'functional_sim_score'})
        
        ## CX: code isn't working so I commented it out. 
        # Recast GO terms as a list, so we can do sorting later
#        mod1a_processed['Func_assoc_terms'] = mod1a_processed['Func_assoc_terms'].astype(str)

        ## CX: create ranks
        mod1a_processed['functional_sim_rank'] = mod1a_processed['functional_sim_score'].rank(ascending=False, method='min')        
        
        # Update full table
        self.build_full_summary(mod1a_processed)

        # Update brief table
        self.build_brief_summary()

        ##### Format Data for individual module Summary #####
        ## Written by Colleen Xu 

        Mod1A_part1 = mod1a_results.groupby(['hit_symbol','hit_id'])['input_symbol'].apply(list).reset_index()
        Mod1A_part2 = mod1a_results.groupby(['hit_symbol','hit_id'])['input_id'].apply(list).reset_index()
        Mod1A_part3 = mod1a_results.groupby(['hit_symbol','hit_id']).aggregate({'score': 'count'}).rename(index=str, columns={'score':'functional_sim_count'})
    
        ## Merge the parts together!
        Mod1A_final = Mod1A_part1.merge(Mod1A_part2, on=['hit_symbol', 'hit_id'])
        ## Another merge, and sort in descending order of number of interactions, ascending alphabetical order
        Mod1A_final = Mod1A_final.merge(Mod1A_part3, on=['hit_symbol', 'hit_id'])
        Mod1A_final = Mod1A_final.sort_values(by=['functional_sim_count','hit_symbol'], ascending=[False, True])
    
        Mod1A_final['input_symbol'] = [sorted(x) for x in Mod1A_final['input_symbol']]
        Mod1A_final = Mod1A_final.reset_index()
        
        self.module_summaries['mod1A'] = Mod1A_final.filter(items=['hit_symbol', 'input_symbol', 'functional_sim_count']).rename(index=str, columns={'hit_symbol': 'output_gene', 'input_symbol':'input_gene'})
        
        # END
        

    # This function takes in the Module1B results and updates both tables
    def add1B(self, mod1b_results):    
        ## Imediately store raw data
        self.raw_module_data['mod1B'] = mod1b_results

        ##### Format Data for Cross Module Summary #####
        ## Rename the columns
        self.module_names['Pheno_assoc_terms'] = {'Pheno_sim_score':'Pheno_sim_input_gene_ct'}

        # drop irrelevant columns
        mod1b_processed = mod1b_results.drop(columns=['hit_id','input_id','shared_terms','shared_term_names','module'])
        
        # drop duplicates in input
        mod1b_processed = mod1b_processed.drop_duplicates(subset=['input_symbol','hit_symbol'])
        
        # rename columns to match desired full_summary output column names
        mod1b_processed = mod1b_processed.rename(index = str, columns = {'hit_symbol':'output_gene','input_symbol':'input_gene','score':'phenotype_sim_score'})
        
        ## CX: code isn't working so I commented it out.         
#        mod1b_processed['Pheno_assoc_terms'] = mod1b_processed['Pheno_assoc_terms'].astype(str)

        ## CX: create ranks
        mod1b_processed['phenotype_sim_rank'] = mod1b_processed['phenotype_sim_score'].rank(ascending=False, method='min')
        
        # Update full table
        self.build_full_summary(mod1b_processed)
    
        # Update brief table
        self.build_brief_summary()

         ##### Format Data for individual module Summary #####
        ## Written by Colleen Xu 

        ## merging columns, creating lists of the inputs and sums of the scores
        ## CX note: obviously it would be nice to do this all at once. the apply(list) only worked on one column at a time. aggregate only accepts a limited number of functions
        Mod1B_part1 = mod1b_results.groupby(['hit_symbol','hit_id'])['input_symbol'].apply(list).reset_index()
        Mod1B_part2 = mod1b_results.groupby(['hit_symbol','hit_id'])['input_id'].apply(list).reset_index()
        Mod1B_part3 = mod1b_results.groupby(['hit_symbol','hit_id']).aggregate({'score': 'count'}).rename(index=str, columns={'score':'phenotype_sim_count'})

        ## Merge the parts together!
        Mod1B_final = Mod1B_part1.merge(Mod1B_part2, on=['hit_symbol', 'hit_id'])
        ## Another merge, and sort in descending order of number of interactions, ascending alphabetical order
        Mod1B_final = Mod1B_final.merge(Mod1B_part3, on=['hit_symbol', 'hit_id'])
        Mod1B_final = Mod1B_final.sort_values(by=['phenotype_sim_count','hit_symbol'], ascending=[False, True])
        Mod1B_final['input_symbol'] = [sorted(x) for x in Mod1B_final['input_symbol']]        
        Mod1B_final = Mod1B_final.reset_index()
        
        self.module_summaries['mod1B'] = Mod1B_final.filter(items=['hit_symbol', 'input_symbol', 'phenotype_sim_count']).rename(index=str, columns={'hit_symbol': 'output_gene', 'input_symbol':'input_gene'})

        # END


    # This function takes in the Module1E results and updates both tables
    def add1E(self, mod1e_results):
        # Store raw data
        self.raw_module_data['mod1E'] = mod1e_results

        ##### Format Data for Cross Module Summary #####
        # drop irrelevant columns
        mod1e_processed = mod1e_results.drop(columns=['hit_id','input_id', 'module'])
        
        # drop duplicates in input
        mod1e_processed = mod1e_processed.drop_duplicates(subset=['input_symbol','hit_symbol'])

        # rename columns to match desired full_summary output column names
        mod1e_processed = mod1e_processed.rename(index = str, columns = {'hit_symbol':'output_gene','input_symbol':'input_gene','score':'interactions'})

        ## CX: create ranks
        mod1e_processed['interaction_rank'] = mod1e_processed['interactions'].rank(ascending=False, method='min')
        
        # Update full table
        self.build_full_summary(mod1e_processed)

        # Update brief table
        self.build_brief_summary()

        ##### Format Data for individual module Summary #####
        ## Written by Colleen Xu 
        ## merging columns, creating lists of the inputs and sums of the scores
        ## CX note: obviously it would be nice to do this all at once. the apply(list) only worked on one column at a time. aggregate only accepts a limited number of functions
        Mod1E_part1 = mod1e_results.groupby(['hit_symbol','hit_id'])['input_symbol'].apply(list).reset_index()
        Mod1E_part2 = mod1e_results.groupby(['hit_symbol','hit_id'])['input_id'].apply(list).reset_index()    
        Mod1E_part3 = mod1e_results.groupby(['hit_symbol','hit_id']).aggregate({'score': 'sum'}).rename(index=str, columns={'score':'interactions'})
        ## Merge the parts together!
        Mod1E_final = Mod1E_part1.merge(Mod1E_part2, on=['hit_symbol', 'hit_id'])
        ## Another merge, and sort in descending order of number of interactions, ascending alphabetical order
        Mod1E_final = Mod1E_final.merge(Mod1E_part3, on=['hit_symbol', 'hit_id'])
        Mod1E_final = Mod1E_final.sort_values(by=['interactions','hit_symbol'], ascending=[False, True])
        Mod1E_final['input_symbol'] = [sorted(x) for x in Mod1E_final['input_symbol']]        
        Mod1E_final = Mod1E_final.reset_index()
        
        self.module_summaries['mod1E'] = Mod1E_final.filter(items=['hit_symbol', 'input_symbol', 'interactions']).rename(index=str, columns={'hit_symbol': 'output_gene', 'input_symbol':'input_gene'})
        
        # END

    # Method takes in a query or list of queries (module names) and returns their brief summary
    def show_single_mod_summary(self, query):

        # check if single query and make into list most extensible 
        if isinstance(query, str):
            query = [query] # make it into list of one 

        # For each query in the list display the brief data
        for mod in query:
            if mod in self.raw_module_data.keys():
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
        self.current_mods = list(self.raw_module_data.keys())
        print('Modules Currently Loaded: ' + \
            ', '.join(self.current_mods))
        
    # Method returns list of current modules used as dictionary keys
    def get_mods(self):
        self.current_mods = list(self.raw_module_data.keys())
        return self.current_mods

    # This function returns a dictionary of the raw data if people want to play with it 
    # Allows for the analysis of the raw data in other ways. 
    # envisioned summary_module as basically a container for all module output
    def return_raw_output(self):
        return self.raw_module_data

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
        self.brief_summary.to_csv(filename, index=False)  # there is an issue with this! it's not including output genes

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