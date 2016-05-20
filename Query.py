# -*- coding: utf-8 -*

import sys
import unicodedata

reload(sys)
sys.setdefaultencoding("utf-8")

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class Select():
	columns = []

	def __init__(self):
		self.columns = []

	def add_column(self, column, column_type):
		self.columns.append([column, column_type])

	def get_columns(self):
		return self.columns

	def get_just_column_name(self, column):
		if column != str(None):
			return column.rsplit('.', 1)[1]
		else:
			return column

	def print_column(self, selection):
		column = selection[0]
		column_type = selection[1]

		if column is None:
			if column_type == 'COUNT':
				return color.BOLD + 'COUNT(' + color.END + '*' + color.BOLD + ')' + color.END
			else:
				return '*'
		else:
			if column_type == 'COUNT':
				return color.BOLD + 'COUNT(' + color.END + str(column) + color.BOLD + ')' + color.END
			elif column_type == 'AVG':
				return color.BOLD + 'AVG(' + color.END + str(column) + color.BOLD + ')' + color.END
			elif column_type == 'SUM':
				return color.BOLD + 'SUM(' + color.END + str(column) + color.BOLD + ')' + color.END
			elif column_type == 'MAX':
				return color.BOLD + 'MAX(' + color.END + str(column) + color.BOLD + ')' + color.END
			elif column_type == 'MIN':
				return color.BOLD + 'MIN(' + color.END + str(column) + color.BOLD + ')' + color.END
			else:
				return str(column)

	def __str__(self):
		select_string = ''
		for i in range(0, len(self.columns)):
			if i == (len(self.columns)-1):
				select_string = select_string + str(self.print_column(self.columns[i]))
			else:
				select_string = select_string + str(self.print_column(self.columns[i])) + ', '

		return color.BOLD + 'SELECT ' + color.END + select_string + '\n'

	def print_json(self, output):
		if len(self.columns) >= 1:
			if len(self.columns) == 1:
				output.write('\t"select": {\n')
				output.write('\t\t"column": "' + self.get_just_column_name(str(self.columns[0][0])) + '",\n')
				output.write('\t\t"type": "' + str(self.columns[0][1]) + '"\n')
				output.write('\t},\n')
			else:
				output.write('\t"select": {\n')
				output.write('\t\t"columns": [\n')
				for i in range(0, len(self.columns)):
					if i == (len(self.columns)-1):
						output.write('\t\t\t{ "column": "' + self.get_just_column_name(str(self.columns[i][0])) + '",\n')
						output.write('\t\t\t  "type": "' + str(self.columns[i][1]) + '"\n')
						output.write('\t\t\t}\n')
					else:
						output.write('\t\t\t{ "column": "' + self.get_just_column_name(str(self.columns[i][0])) + '",\n')
						output.write('\t\t\t  "type": "' + str(self.columns[i][1]) + '"\n')
						output.write('\t\t\t},\n')
				output.write('\t\t]\n')
				output.write('\t},\n')
		else:
			output.write('\t"select": {\n')
			output.write('\t},\n')

class From():
	table = ''

	def __init__(self, table=None):
		if table is not None:
			self.table = table
		else:
			self.table = ''

	def set_table(self, table):
		self.table = table

	def get_table(self):
		return self.table

	def __str__(self):
		return color.BOLD + 'FROM ' + color.END + str(self.table) + '\n'

	def print_json(self, output):
		if self.table != '':
			output.write('\t"from": {\n')
			output.write('\t\t"table": "' + str(self.table) + '"\n')
			output.write('\t},\n')
		else:
			output.write('\t"from": {\n')
			output.write('\t},\n')

class Join():
	tables = []
	links = []

	def __init__(self):
		self.tables = []
		self.links = []

	def add_table(self, table):
		if table not in self.tables:
			self.tables.append(table)

	def set_links(self, links):
		self.links = links

	def get_tables(self):
		return self.tables

	def get_links(self):
		return self.links

	def __str__(self):
		if len(self.links) >= 1:
			string = ''
			for i in range(0, len(self.links)):
				string += color.BOLD + 'INNER JOIN ' + color.END + str(self.links[i][2]) + '\n' + color.BOLD + 'ON ' + color.END + str(self.links[i][0]) + '.' + str(self.links[i][1]) + ' = ' + str(self.links[i][2]) + '.' + str(self.links[i][1]) + '\n'
			return string
		elif len(self.tables) >= 1:
			if len(self.tables) == 1:
				return color.BOLD + 'NATURAL JOIN ' + color.END + self.tables[0] + '\n'
			else:
				string = color.BOLD + 'NATURAL JOIN ' + color.END
				for i in range(0, len(self.tables)):
					if i == (len(self.tables)-1):
						string += str(self.tables[i])
					else:
						string += str(self.tables[i]) + ', '
				return string + '\n'
		else:
			return ''

	def print_json(self, output):
		if len(self.tables) >= 1:
			if len(self.tables) == 1:
				output.write('\t"join": {\n')
				output.write('\t\t"table": "' + str(self.tables[0]) + '"\n')
				output.write('\t},\n')
			else:
				output.write('\t"join": {\n')
				output.write('\t\t"tables": [')
				for i in range(0, len(self.tables)):
					if i == (len(self.tables)-1):
						output.write('"' + str(self.tables[i]) + '"')
					else:
						output.write('"' + str(self.tables[i]) + '", ')
				output.write(']\n')
				output.write('\t},\n')
		else:
			output.write('\t"join": {\n')
			output.write('\t},\n')

class Condition():
	column = ''
	operator = ''
	value = ''

	def __init__(self, column, operator, value):
		self.column = column
		self.operator = operator
		self.value = value

	def get_column(self):
		return self.column

	def get_just_column_name(self, column):
		return column.rsplit('.', 1)[1]

	def get_operator(self):
		return self.operator

	def get_value(self):
		return self.value

	def get_in_list(self):
		return [self.column, self.operator, self.value]

	def __str__(self):
		return '' + '\n'

	def print_json(self, output):
		output.write('\t\t\t{ "column": "' + self.get_just_column_name(str(self.column)) + '",\n\t\t\t  "operator": "' + str(self.operator) + '",\n\t\t\t  "value": "' + str(self.value) + '"\n\t\t\t}')

class Where():
	conditions = []

	def __init__(self, clause=None):
		if clause is not None:
			self.conditions.append([None, clause])

	def add_condition(self, junction, clause):
		self.conditions.append([junction, clause])

	def get_conditions(self):
		return self.conditions

	def __str__(self):
		if len(self.conditions) >= 1:
			return '' + '\n'
		else:
			return ''

	def print_json(self, output):
		if len(self.conditions) >= 1:
			if len(self.conditions) == 1:
				output.write('\t"where": {\n')
				output.write('\t\t"condition": [\n')
				self.conditions[0][1].print_me(output)
				output.write('\n')
				output.write('\t\t]\n')
				output.write('\t},\n')
			else:
				output.write('\t"where": {\n')
				output.write('\t\t"conditions": [\n')
				for i in range(0, len(self.conditions)):
					if self.conditions[i][0] is not None:
						output.write('\t\t\t{ "operator": "' + str(self.conditions[i][0]) + '" },\n')
					self.conditions[i][1].print_me(output)
					if i != (len(self.conditions)-1):
						output.write(',')
					output.write('\n')
				output.write('\t\t]\n')
				output.write('\t},\n')
		else:
			output.write('\t"where": {\n')
			output.write('\t},\n')
    
class GroupBy():
	columns = []

	def __init__(self, columns=None):
		if columns is not None:
			self.columns = columns
		else:
			self.columns = []

	def add_column(self, column):
		self.columns.append(column)

	def get_columns(self):
		return self.columns

	def __str__(self):
		if len(self.columns) >= 1:
			return '' + '\n'
		else:
			return ''

	def print_json(self, output):
		if len(self.columns) >= 1:
			if len(self.columns) == 1:
				output.write('\t"group_by": {\n')
				output.write('\t\t"column": "' + self.get_just_column_name(str(self.columns[0])) + '"\n')
				output.write('\t},\n')
			else:
				output.write('\t"group_by": {\n')
				output.write('\t\t"columns": [')
				for i in range(0, len(self.columns)):
					if i == (len(self.columns)-1):
						output.write('"' + self.get_just_column_name(str(self.columns[i])) + '"')
					else:
						output.write('"' + self.get_just_column_name(str(self.columns[i])) + '", ')
				output.write(']\n')
				output.write('\t},\n')
		else:
			output.write('\t"group_by": {\n')
			output.write('\t},\n')

class OrderBy():
	column = ''
	order = None

	def __init__(self, column=None, order=None):
		if column is not None:
			self.column = column
		else:
			self.column = ''
		if order is not None:
			self.order = order
		else:
			self.order = None

	def add_order(self, column, order):
		self.column = column
		self.order = order

	def get_order(self):
		return [self.column, self.order]

	def __str__(self):
		if self.column != '':
			return '' + '\n'
		else:
			return ''

	def print_json(self, output):
		if self.column != '':
			output.write('\t"order_by": {\n')
			output.write('\t\t"order": "' + str(self.order) + '",\n')
			output.write('\t\t"column": "' + self.get_just_column_name(str(self.column)) + '"\n')
			output.write('\t}\n')
		else:
			output.write('\t"order_by": {\n')
			output.write('\t}\n')

class Query():
	select = None
	_from = None
	join = None
	where = None
	group_by = None
	order_by = None

	def __init__(self, select=None, _from=None, join=None, where=None, group_by=None, order_by=None):
		if select is not None:
			self.select = select
		if _from is not None:
			self._from = _from
		if join is not None:
			self.join = join
		if where is not None:
			self.where = where
		if group_by is not None:
			self.group_by = group_by
		if order_by is not None:
			self.order_by = order_by

	def set_select(self, select):
		self.select = select

	def get_select(self):
		return self.select

	def set_from(self, _from):
		self._from = _from

	def get_from(self):
		return self._from

	def set_join(self, join):
		self.join = join

	def get_join(self):
		return self.join

	def set_where(self, where):
		self.where = where

	def get_where(self):
		return self.where

	def set_group_by(self, group_by):
		self.group_by = group_by

	def get_group_by(self):
		return self.group_by

	def set_order_by(self, order_by):
		self.order_by = order_by

	def get_order_by(self):
		return self.order_by

	def __str__(self):
		return str(self.select) + str(self._from) + str(self.join) + str(self.where) + str(self.group_by) + str(self.order_by)

	def print_json(self, filename="output.json"):
		output = open(filename, 'a')
		output.write('{\n')
		self.select.print_json(output)
		self._from.print_json(output)
		self.join.print_json(output)
		self.where.print_json(output)
		self.group_by.print_json(output)
		self.order_by.print_json(output)
		output.write('}\n')
		output.close()
