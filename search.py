import json
import pymysql
import time
import random
import glob
import os
from os.path import abspath

def get_cols(dbname, table, cursor):
	sql = 'show columns from `%s`.`%s`;' % (dbname, table)
	cursor.execute(sql)
	return [i[0] for i in cursor.fetchall()]

def search_table(dbname, table, query_cols, kw, cursor, conn):
	kw = conn.escape_string(kw)
	cols = get_cols(dbname, table, cursor)
	query_cols = [i for i in query_cols if i in cols]
	sql = 'select `%s` from `%s`.`%s` where `' % ('`,`'.join(cols), dbname, table)
	sql += ("` like '%s%%' or `" % kw).join(query_cols) + ("` like '%s%%';" % kw)
	cursor.execute(sql)
	cols.append('from_table')
	results = list(cursor.fetchall())
	for i in range(len(results)):
		results[i] = list(results[i])
		results[i].append(table)
	return [cols, results]

def merge_results(a, b, cols_sort):
	def _add_dict(x):
		tmp_dict = {}
		for i in range(len(x[0])):
			tmp_dict[x[0][i]] = i
		x.append(tmp_dict)
	_add_dict(a)
	_add_dict(b)
	cols = set(a[0] + b[0])
	cols.remove('from_table')
	cols = list(cols)
	tmp_cols = [i for i in cols_sort if i in cols]
	for i in cols:
		if i not in tmp_cols:
			tmp_cols.append(i)
	cols = tmp_cols
	cols.append('from_table')
	def _sort(cols, data):
		sorted_lines = []
		for line in data[1]:
			tmp_line = []
			for col in cols:
				if col in data[2]:
					tmp_line.append(line[data[2][col]])
				else:
					tmp_line.append('')
			sorted_lines.append(tmp_line)
		return sorted_lines
	return [cols, _sort(cols, a) + _sort(cols, b)]

if __name__ == '__main__':
	for infile in glob.glob('./res/*.html'): os.remove(infile)
	with open('config.json', encoding='utf-8') as f:
		conf = json.load(f)

	conn = pymysql.connect(host=conf['host'], port=int(conf['port']), user=conf['user'], password=conf['pass'])
	cursor = conn.cursor()
	db_tables = {}

	for dbname in conf['dbnames']:
		cursor.execute('select table_name from information_schema.tables where table_schema = "%s";' % dbname)
		db_tables[dbname] = [i[0] for i in cursor.fetchall()]

	while (1):
		try:
			search = input('>>> ')
			result = []
			for dbname in db_tables:
				for table in db_tables[dbname]:
					curr_result = search_table(dbname, table, conf['query_cols'], search, cursor, conn)
					if result:
						result = merge_results(result, curr_result, conf['cols_sort'])
					else:
						result = curr_result
			if not result[1]: continue
			json_data = 'var data = ' + json.dumps(result)
			with open('./res/template.tpl', encoding="utf-8") as f:
				html = f.read()
			html = html.replace('xxxxxcaptionxxxxx', '搜索：' + search)
			html = html.replace('/////json/////', json_data)
			tmpname = './res/%s%s.html' % (int(time.time()), random.randint(1000,9999))
			tmpname = abspath(tmpname)
			with open(tmpname, 'w', encoding="utf-8") as f:
				f.write(html)
			os.startfile(tmpname)
		except KeyboardInterrupt:
			exit()