# TranslatorCWL Porcelain
## Commands without cruft

This [porcelain](https://stackoverflow.com/a/6976506) for TranslatorCWL assists SMEs in chaining together TranslatorCWL workflows, and writing CWL specs within Translator.

Why? CWL specifications still make you care about how the data is formatted, rather than what it is. File types, commands, and connections from one workflow to another still need to be declared explicitly. If you are composing these specifications, there is a lot of repetition.
And as the Biolink Model becomes larger, or as it undergoes more changes, it's hard to remember exactly the exact way slots and categories are named.

The less we talk about computers and the more we talk about actions and concepts, the better. And you should be able to write down concepts in the way *you* are familiar with, rather than our way. (But our way should be as clean and consistent as possible.) Here, we do both.

### Features
* Typeahead/Autosuggest concept names contained in the Biolink Model
* Connect scripts together just by writing down their names (and an arrow?)
* Instant feedback for if your script will work or not
* Friendly syntax for splitting commands in parallel

### Examples
#### WIP

Workflow 2 - Parallel outputs

`$ GeneByDisease -> FunctionalSimilarity | PhenotypeSimilarity | InteractionsByGene`

Parallel Inputs

`$ GeneByDisease | GeneBySymbol -> PhenotypeByGene`

Get by Slot?

`$ GeneByDisease ->causes PhenotypeByGene`
 
### TODO
* Should this be supported in native CLI, or be its own text editor?
  * Native CLI would mean using Unix Pipes, but having autocomplete implies using Unix autocomplete or its own shell? 
* Could this be implemented just with Python functions and Python FIRE? The number of operations is small.
* Transpile to CWL spec?
* Requires CWL spec?
* Is this a writer for CWL specs?
* Is the Biolink Model autocomplete 
* Syntax possibilities
  * `Gene / Disease` for Gene By Disease?
  * `->causes` for slot?