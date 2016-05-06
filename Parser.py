# -*- coding: utf-8 -*

import re
import sys
import unicodedata
from threading import Thread
from Exception import ParsingException
from Query import *

reload(sys)
sys.setdefaultencoding("utf-8")

class SelectParser(Thread):
    def __init__(self, columns_of_select, phrase, count_keywords, sum_keywords, average_keywords, max_keywords, min_keywords):
        Thread.__init__(self)
        self.select_object = None
        self.columns_of_select = columns_of_select
        self.phrase = phrase
        self.count_keywords = count_keywords
        self.sum_keywords = sum_keywords
        self.average_keywords = average_keywords
        self.max_keywords = max_keywords
        self.min_keywords = min_keywords

    def run(self):
        self.select_object = Select()
        is_count = False
        number_of_select_column = len(self.columns_of_select)

        if number_of_select_column == 0:
            for count_keyword in self.count_keywords:
                if count_keyword in self.phrase:
                    is_count = True

            if is_count:
                self.select_object.add_column(None, 'COUNT')
            else:
                self.select_object.add_column(None, None)
        else:
            select_phrases = []
            previous_index = 0
            for i in range(0,len(self.phrase)):
                if self.phrase[i] in self.columns_of_select:
                    select_phrases.append(self.phrase[previous_index:i+1])
                    previous_index = i+1

            for i in range(0, len(select_phrases)):
            	select_type = None
            	phrase = ' '.join(select_phrases[i])

                for keyword in self.average_keywords:
                    if keyword in phrase:
                    	select_type = 'AVG'
                for keyword in self.count_keywords:
                    if keyword in phrase:
                    	select_type = 'COUNT'
                for keyword in self.max_keywords:
                    if keyword in phrase:
                    	select_type = 'MAX'
                for keyword in self.min_keywords:
                    if keyword in phrase:
                    	select_type = 'MIN'
                for keyword in self.sum_keywords:
                    if keyword in phrase:
                        select_type = 'SUM'
                self.select_object.add_column(self.columns_of_select[i], select_type)


    def join(self):
        Thread.join(self)
        return self.select_object

class FromParser(Thread):
    def __init__(self, tables_of_from, phrase, columns_of_select, columns_of_where, database_dico, junction_keywords, disjunction_keywords):
        Thread.__init__(self)
        self.queries = None
        self.tables_of_from = tables_of_from
        self.phrase = phrase
        self.columns_of_select = columns_of_select
        self.columns_of_where = columns_of_where
        self.junction_keywords = junction_keywords
        self.disjunction_keywords = disjunction_keywords
        self.database_dico = database_dico

    def get_tables_of_column(self, column):
        tmp_table = []
        for table in self.database_dico:
            if column in self.database_dico[table]:
                 tmp_table.append(table)
        return tmp_table

    def run(self):
        if len(self.tables_of_from) == 0:
            raise ParsingException("No table name found in sentence!")

        real_tables_of_from =[]
        self.queries = []
        number_of_junction_words = 0
        number_of_disjunction_words = 0

        for word in self.phrase:
            if word in self.junction_keywords:
                number_of_junction_words += 1
            if word in self.disjunction_keywords:
                number_of_disjunction_words += 1

        if (number_of_junction_words + number_of_disjunction_words) == (len(self.tables_of_from) - 1):
            real_tables_of_from = self.tables_of_from
        elif (number_of_junction_words + number_of_disjunction_words) < (len(self.tables_of_from) - 1):
            real_tables_of_from = self.tables_of_from[:(number_of_junction_words + number_of_disjunction_words + 1)]
            # here, there are may be also table in where section, the parsing task is more complicated
        elif (number_of_junction_words + number_of_disjunction_words) > (len(self.tables_of_from) - 1):
            raise ParsingException("More junction and disjunction keywords than table name in FROM!")

        for table in real_tables_of_from:
            query = Query()
            query.set_from(From(table))
            join_object = None
            join_object = Join()
            for column in self.columns_of_select:
                if column not in self.database_dico[table]:
                    foreign_tables = self.get_tables_of_column(column)
                    for foreign_table in foreign_tables:
                        join_object.add_table(foreign_table)
            for column in self.columns_of_where:
                if column not in self.database_dico[table]:
                    foreign_tables = self.get_tables_of_column(column)
                    for foreign_table in foreign_tables:
                        join_object.add_table(foreign_table)
            query.set_join(join_object)
            self.queries.append(query)

    def join(self):
        Thread.join(self)
        return self.queries

class WhereParser(Thread):
    def __init__(self, number_of_where_column, phrase):
        Thread.__init__(self)
        self.where_object = None

    def run(self):
        self.where_object = Where()

    def join(self):
        Thread.join(self)
        return self.where_object

class GroupByParser(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.group_by_object = None

    def run(self):
        self.group_by_object = GroupBy()

    def join(self):
        Thread.join(self)
        return self.group_by_object

class OrderByParser(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.order_by_object = None

    def run(self):
        self.order_by_object = OrderBy()

    def join(self):
        Thread.join(self)
        return self.order_by_object

class Parser:
    database_object = None
    database_dico = None
    language = None
    thesaurus_object = None

    count_keywords = []
    sum_keywords = []
    average_keywords = []
    max_keywords = []
    min_keywords = []
    junction_keywords = []
    disjunction_keywords = []

    french_count_keywords = ['combien', 'nombre']
    french_sum_keywords = ['somme', 'total']
    french_average_keywords = ['moyenne']
    french_max_keywords = ['maximum', 'maximale', 'plus grand']
    french_min_keywords = ['minimum', 'minimale', 'plus petit']
    french_junction_keywords = ['et']
    french_disjunction_keywords = ['ou']

    english_count_keywords = ['how many', 'number']
    english_sum_keywords = ['sum', 'total']
    english_average_keywords = ['average']
    english_max_keywords = ['maximum']
    english_min_keywords = ['minimum']
    english_junction_keywords = ['and']
    english_disjunction_keywords = ['or']

    def __init__(self, language=None, database=None):
        if language is not None:
            self.language = language
        else:
            self.language = 'french'

        self.load_language_resources()

        if database is not None:
            self.database_object = database
            self.database_dico = self.database_object.get_tables_into_dictionnary()

    def load_language_resources(self):
        if self.language == 'french':
            self.count_keywords = self.french_count_keywords
            self.sum_keywords = self.french_sum_keywords
            self.average_keywords = self.french_average_keywords
            self.max_keywords = self.french_max_keywords
            self.min_keywords = self.french_min_keywords
            self.junction_keywords = self.french_junction_keywords
            self.disjunction_keywords = self.french_disjunction_keywords
        elif self.language == 'english':
            self.count_keywords = self.english_count_keywords
            self.sum_keywords = self.english_sum_keywords
            self.average_keywords = self.english_average_keywords
            self.max_keywords = self.english_max_keywords
            self.min_keywords = self.english_min_keywords
            self.junction_keywords = self.english_junction_keywords
            self.disjunction_keywords = self.english_disjunction_keywords
        else:
            raise ParsingException("No resource found!")

    def set_database(self, database):
        self.database_object = database
        self.database_dico = self.database_object.get_tables_into_dictionnary()

    def set_language(self, language):
        self.language = language
        self.load_language_resources()

    def set_thesaurus(self, thesaurus):
        self.thesaurus_object = thesaurus

    def remove_accents(self, string):
        nkfd_form = unicodedata.normalize('NFKD', unicode(string))
        return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

    def parse_sentence(self, sentence):
        number_of_table = 0
        number_of_select_column = 0
        number_of_where_column = 0
        last_table_position = 0
        columns_of_select = []
        columns_of_where = []
        tables_of_from = []
        select_phrase = ''
        from_phrase = ''
        where_phrase = ''
        
        words = re.findall(r"[\w]+", self.remove_accents(sentence))

        for i in range(0, len(words)):
            if words[i] in self.database_dico:
                if number_of_table == 0:
                    select_phrase = words[:i]
                tables_of_from.append(words[i])
                number_of_table+=1
                last_table_position = i
            for table in self.database_dico:
                if words[i] in self.database_dico[table]:
                    if number_of_table == 0:
                        columns_of_select.append(words[i])
                        number_of_select_column+=1
                    else:
                        if number_of_where_column == 0:
                            from_phrase = words[len(select_phrase):last_table_position+1]
                        columns_of_where.append(words[i])
                        number_of_where_column+=1
                    break
                else:
                    if (number_of_table != 0) and (number_of_where_column == 0) and (i == (len(words)-1)):
                        from_phrase = words[len(select_phrase):]

        where_phrase = words[len(select_phrase) + len(from_phrase):]
        
        if (number_of_select_column + number_of_table + number_of_where_column) == 0:
            raise ParsingException("No keyword found in sentence!")

        print 'SELECT : ' + ' '.join(select_phrase)
        print 'FROM : ' + ' '.join(from_phrase)
        print 'WHERE : ' + ' '.join(where_phrase)
        sys.exit()

        select_parser = SelectParser(columns_of_select, select_phrase, self.count_keywords, self.sum_keywords, self.average_keywords, self.max_keywords, self.min_keywords)
        from_parser = FromParser(tables_of_from, from_phrase, columns_of_select, columns_of_where, self.database_dico, self.junction_keywords, self.disjunction_keywords)
        where_parser = WhereParser(number_of_where_column, where_phrase)
        group_by_parser = GroupByParser()
        order_by_parser = OrderByParser()

        select_parser.start()
        from_parser.start()
        where_parser.start()
        group_by_parser.start()
        order_by_parser.start()

        select_object = select_parser.join()
        queries = from_parser.join()
        where_object = where_parser.join()
        group_by_object = group_by_parser.join()
        order_by_object = order_by_parser.join()

        for query in queries:
            query.set_select(select_object)
            query.set_where(where_object)
            query.set_group_by(group_by_object)
            query.set_order_by(order_by_object)

        return queries
