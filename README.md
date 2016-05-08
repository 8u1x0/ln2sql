# ln2sql

<b>ln2sql is a tool to query a database in natural language</b>, as described in the following French paper (which can be found in the <i>docs/</i> directory):

<i><a rel="license" href="https://www.researchgate.net/publication/278965118_fr2sql_Interrogation_de_bases_de_donnees_en_francais">Benoît Couderc and Jérémy Ferrero. fr2sql : Database Query in French. (fr2sql : Interrogation de bases de données en français [in French]). In Proceedings of the 17th RECITAL (affiliated with the 22th TALN Conference). June 2015. Caen, France. ATALA. pp.1-12 </a></i>

In view to learn Python, I recently decided to implement our originally PHP project in <b>Python</b>. In addition, that will allow me to share the tool with the English-speaking community by making it public available here.

### Extra features

- [X] Load a database schema from SQL dump
- [X] Import a personal thesaurus (<a rel="thesaurus" href="http://extensions.openoffice.org/en/search?f%5B0%5D=field_project_tags%3A157">OpenOffice template</a>)
- [X] Import a personal stop word list
- [X] Print a query structure in JSON
- [X] Exception and error handling
- [X] Graphical User Interface
- [X] Multi-threading

### SQL statement supported

- [X] one-column select
- [X] multiple columns select
- [X] all columns select
- [X] count-select
- [X] sum-select
- [X] avg-select
- [X] min-select
- [X] max-select
- [ ] inner join
- [ ] one-condition where
- [ ] multiple conditions where
- [ ] junction
- [ ] disjunction
- [ ] cross-condition
- [ ] equal operator
- [ ] not equal operator
- [ ] greater-than operator
- [ ] less-than operator
- [ ] between operator
- [ ] sum in condition
- [ ] avg in condition
- [ ] min in condition
- [ ] max in condition
- [ ] order by
- [ ] group by
- [X] multiple queries
- [ ] date support
- [ ] negation support

### Supported languages

The tool can deal with any language, so long as it has its configuration file (<i>i.e.</i> a file with the keywords of the language).

Language configuration files can be found in <i>lang/</i> directory. The files are CSV files. Each line represent a type of keywords. Anything before the colon is ignored. Keywords must be separated by a comma. 

You can build your own language configuration file following the English and French template.

### Usage

You can directly use the python wrapper by the following way:
```
usage: ./ln2sql.py -d <path> -l <path> -i <input-sentence> [-t <path>] [-j <path>]
-h						print this help message
-d <path>				path to sql dump file
-l <path>				path to language configuration file
-i <input-sentence>		input sentence to parse
-j <path>				path to JSON output file
-t <path>				path to thesaurus file
```
example of usage:
```
./ln2sql.py -i "What is the number of students?" -l lang/english.csv -d database/tal.sql -j output.json
```
or by graphical interface by typing the following command:
```
./ln2sql_gui.py
```
a window like the one below will appear:
<p align="center"><img src="https://raw.githubusercontent.com/FerreroJeremy/ln2sql/master/docs/graphical_user_interface.png" width="600"></p>

### JSON output

With the following input:
```
What is the average age of students whose name is Doe or age over 25?
```
the output is:
```JSON
{
	"select": {
		"column": "age",
		"type": "AVG"
	},
	"from": {
		"table": "student"
	},
	"join": {
	
	},
	"where": {
		"conditions": [
			{ "column": "name",
			  "operator": "==",
			  "value": "Doe"
			},
			{ "operator": "or" },
			{ "column": "age",
			  "operator": ">=",
			  "value": "25"
			}
		]
	},
	"group_by": {
	
	},
	"order_by": {
	
	}
}
```
### Conception

<p align="center">
<img src="https://raw.githubusercontent.com/FerreroJeremy/ln2sql/master/docs/mvc_class_diagram.png">
</p>
The tool is implemented under the Model-View-Controller pattern. The classes imported from the Python Standard Library do not appear in the diagram except those required for inheritance (<i>e.g.</i> <i>Thread</i> or <i>Exception</i>).

<br/>

### <img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /> License

This tool is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
