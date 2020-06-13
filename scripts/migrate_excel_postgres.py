from datetime import datetime

import psycopg2
import xlrd

file_name = "mentors_data.xlsx"

wb = xlrd.open_workbook(file_name)
sheet = wb.sheet_by_index(0)

data = []

for i in range(1, sheet.nrows):
	row = list()
	row.append(sheet.cell_value(i, 1).split()[0])  # first_name (0)
	row.append(sheet.cell_value(i, 1).split()[1])  # last_name (1)
	row.append(sheet.cell_value(i, 2))  # e-mail (2)
	row.append(sheet.cell_value(i, 3))  # phone (3)
	seconds = (sheet.cell_value(i, 0) - 25569) * 86400.0
	row.append(datetime.utcfromtimestamp(seconds))  # created_on (4)
	row.append(sheet.cell_value(i, 7))  # workplace (5)
	row.append(sheet.cell_value(i, 8))  # job_title (6)
	row.append(sheet.cell_value(i, 9))  # bio (7)
	row.append("")  # academic_bio (8)
	row.append(sheet.cell_value(i, 10))  # job_search (9)
	row.append(sheet.cell_value(i, 11))  # availability (10)
	row.append(sheet.cell_value(i, 12))  # match_preferences (11)
	row.append("False")  # multiple_mentees (12)
	row.append("False")  # can_simulate (13)
	row.append("{}")  # technologies (14)
	row.append(sheet.cell_value(i, 6))  # years_experience (15)
	row.append(sheet.cell_value(i, 13))  # comments (16)
	data.append(tuple(row))

insert_sql = """INSERT INTO public.mentor(
	first_name, last_name, email, phone, created_on, workplace, job_title, bio, academic_bio, job_search,
	availability, match_preferences, multiple_mentees, can_simulate, technologies, years_experience, comments)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

with psycopg2.connect(host="localhost", database="postgres", user="postgres", password="somePassword") as conn:
	cur = conn.cursor()

	for row in data:
		print(insert_sql % row)
		cur.execute(insert_sql, row)
		conn.commit()
