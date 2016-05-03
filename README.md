# ln2sql

ln2sql is a tool to query a database in natural language, as described in the following French paper (which can be found in the <i>docs/</i> directory):

<i><a rel="license" href="https://www.researchgate.net/publication/278965118_fr2sql_Interrogation_de_bases_de_donnees_en_francais">Benoît Couderc and Jérémy Ferrero. fr2sql : Database Query in French. (fr2sql : Interrogation de bases de données en français [in French]). In Proceedings of the 17th RECITAL (affiliated with the 22th TALN Conference). June 2015. Caen, France. ATALA. pp.1-12 </a></i>

In view to learn Python, I recently decided to implement our originally PHP project in Python. In addition, that will allow me to share the tool with the English-speaking community by making it public available.

### Features in development

- [X] Import a database schema from SQL dump
- [X] Import a thesaurus from LibreOffice thesaurus template
- [X] Import stopword lists
- [X] Match database keywords with input sentence
- [X] Parse input sentence in query sections
- [X] Print query structure in JSON
- [ ] Product query
- [X] Exception and error handling
- [ ] User Interface
- [ ] Multi-threading

### SQL statement supported

- [ ] one-column select
- [ ] multi-column select
- [ ] table select
- [ ] count select
- [ ] inner join
- [ ] where
- [ ] comparison
- [ ] junction
- [ ] disjunction
- [ ] cross-condition
- [ ] sum
- [ ] avg
- [ ] min
- [ ] max
- [ ] between
- [ ] order by
- [ ] group by
- [ ] multi query
- [ ] date support
- [ ] negation support

### Usage

```
usage: ./ln2sql.py -d <path> -l <language> -i <input-sentence> [-t] [-j <path>]
-h						print this help message
-d <path>				path to sql dump file
-l <language>			language of the input sentence
-i <input-sentence>		input sentence to parse
-j <path>				path to JSON output file
-t						use thesaurus
```
Example:
```
./ln2sql.py -i "Quel est l'âge de l'élève et du professeur dont le prénom est Jean ?" -l french -d ./bdd/tal.sql -j output.json
```

### The Query Structure in JSON

#### Class usage

```python
from Query import *

# Create the Select, From and Join object directly in the Query constructor
query = Query(Select(True, ['name', 'nickname', 'age']), From('student'), Join(['professor', 'class']))
# Create three condition objects
condition1 = Condition('name', '==', 'Nemmar')
condition2 = Condition('nickname', '==', 'Jean')
condition3 = Condition('age', '>=', '16')
# Create a Where object with an initial condition
where = Where(condition1)
# Add two conditions to the Where object
where.add_condition('and', condition2)
where.add_condition('or', condition3)
# Add Where, GroupBy and OrderBy objects to the Query object
query.set_where(where)
query.set_group_by(GroupBy(['name', 'nickname']))
query.set_order_by(OrderBy('name', 'desc'))
# Print the Query object
query.print_me()
```

#### JSON format

```JSON
{
	"select": {
		"count": "True",
		"columns": ["name", "nickname", "age"]
	},
	"from": {
		"table": "student"
	},
	"join": {
		"tables": ["professor", "class"]
	},
	"where": {
		"conditions": [
			{ "column": "name",
			  "operator": "==",
			  "value": "Nemmar"
			},
			{ "operator": "and" },
			{ "column": "nickname",
			  "operator": "==",
			  "value": "Jean"
			},
			{ "operator": "or" },
			{ "column": "age",
			  "operator": ">=",
			  "value": "16"
			}
		]
	},
	"group_by": {
		"columns": ["name", "nickname"]
	},
	"order_by": {
		"order": "desc",
		"column": "name"
	}
}
```
<br/>

### <img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /> License

This tool is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
