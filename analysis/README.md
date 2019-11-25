# Analysis
Search and analysis the name in the java file.
## Setup 
* python 3.6.5
* jsonpickle 1.2
* nltk 3.4.5
* six 1.13.0
## Usage
Get into the analysis folder and run following command in terminal.
```
python3 search.py -d [INPUT_DICTORY_PATH] -o [OUTPUT_PATH]
```
## Rules of Analysis Naming Convention
We use WordNet lexical database to analysis if a word is possible a noun or adjective or verb, etc. We set up different rules for different types of name:
* Class Name
  * It should start with the uppercase letter.
  * It should be a noun.
  * It should follow camel-case syntax.
* Enum Name
  * It should start with the uppercase letter.
  * It should be a noun.
  * It should follow camel-case syntax.
* Interface Name
  * It should start with the uppercase letter.
  * It should be an adjective.
  * It should follow camel-case syntax
* Method Name
  * It should start with lowercase letter.
  * It should be a verb or adverb.
  * It should follow camel-case syntax.
* Variable Name
  * It should start with a lowercase letter.
  * It should not start with the special characters.
  * Avoid using one-character variables such as x, y, z.
  * It should follow camel-case syntax.
* Constant Name
  * It should be in uppercase letters.
  * If the name contains multiple words, it should be separated by an underscore(_).
  * It may contain digits but not as the first letter.

## Our Backend Ouput Template
```
{
  name:...,
  fileName:...,
  filePath:...,
  line:...,
  position:...,
  parent:...,
  isOutlier:...,
  type:...,
  subNames:[...]
  variableType:..., (appear when type is variable)
  errorMessage:...(appear when isOutlier is true)
}
```
## Limitation of WordNet Analysis
* We can't analysis determiners, prepositions, pronouns, conjunctions, and particles because WordNet only contains "open-class words": nouns, verbs, adjectives, and adverbs.
* We can't analysis a word not in the word bank of WordNet.
* We can't analysis an abbreviation 