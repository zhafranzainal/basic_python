import pdfplumber
import re
import camelot
from IPython.display import display

with pdfplumber.open("COURSE_CATALOG_IJA.pdf") as pdf:
    extracted_text = ''

    for page in pdf.pages:
        text = page.extract_text()
        extracted_text += text

extracted_text = extracted_text \
    .replace("\n", " ") \
    .replace("03-OCT-23 11:09 AM", "") \
    .replace("Pre-Requisite : NO ", "") \
    .replace("Remarks : NO ", "") \
    .replace("Level : DEGREE ", "") \
    .replace("COURSE TIMETABLE ", "") \
    .replace("Academic Session 2023/2024 ", "") \
    .replace("Sec Day Time Loc Mode Cap Exam Staff ", "")

extracted_text = re.sub(r'Couse Synopsis : .*?Campus', 'Campus', extracted_text, flags=re.DOTALL)

pattern = r"Semester (I|II) Course Code : ([A-Z]{3}\d{4})[\s\S]+?Course Name : (.+?)\d"
matches = re.findall(pattern, extracted_text)

tables = camelot.read_pdf('https://or.ump.edu.my/or/CourseCatalog/COURSE_CATALOG_IJA.pdf', pages='345-381',
                          line_scale=17)


def split_header(table_index, header_row):
    # Split header into its respective column
    header_elements = tables[table_index].df.iloc[header_row, 0].split()
    tables[table_index].df.iloc[header_row, :len(header_elements)] = header_elements


def fix_mode(table_index, starting_row, mode_row):
    # Split column "mode" into its respective row
    modes = tables[table_index].df.iloc[mode_row, 4].split()
    for i in range(starting_row, starting_row + len(modes) // 2):
        mode_offset = 2 * (i - starting_row)
        tables[table_index].df.iloc[i, 4] = modes[mode_offset] + modes[mode_offset + 1]


def clean_table(table_index, header_row, mode_row):
    split_header(table_index, header_row)
    starting_row = header_row + 1

    fix_mode(table_index, starting_row, mode_row)


def clean_table_two_rows_no_exam(table_index, header_row):
    split_header(table_index, header_row)
    starting_row = header_row + 1

    row1 = tables[table_index].df.iloc[starting_row, 0].split()
    tables[table_index].df.iloc[starting_row, 0] = row1[4]
    tables[table_index].df.iloc[starting_row, 1] = row1[5]
    tables[table_index].df.iloc[starting_row, 2] = row1[6] + ' ' + row1[13]
    tables[table_index].df.iloc[starting_row, 3] = row1[7] + ' ' + row1[14]
    tables[table_index].df.iloc[starting_row, 4] = row1[0] + row1[1]
    tables[table_index].df.iloc[starting_row, 5] = row1[8] + ' ' + row1[15]
    tables[table_index].df.iloc[starting_row, 6] = row1[9]
    tables[table_index].df.iloc[starting_row, 7] = ' '.join(row1[10:13])

    row2 = tables[table_index].df.iloc[starting_row + 1, 0].split()
    tables[table_index].df.iloc[starting_row + 1, 0] = row2[0]
    tables[table_index].df.iloc[starting_row + 1, 1] = row2[1]
    tables[table_index].df.iloc[starting_row + 1, 2] = row2[2] + ' ' + row2[9]
    tables[table_index].df.iloc[starting_row + 1, 3] = row2[3] + ' ' + row2[10]
    tables[table_index].df.iloc[starting_row + 1, 4] = row1[2] + row1[3]
    tables[table_index].df.iloc[starting_row + 1, 5] = row2[4] + ' ' + row2[11]
    tables[table_index].df.iloc[starting_row + 1, 6] = row2[5]
    tables[table_index].df.iloc[starting_row + 1, 7] = ' '.join(row2[6:9])


def clean_table_two_rows_has_exam1(table_index, header_row):
    split_header(table_index, header_row)
    starting_row = header_row + 1

    row1 = tables[table_index].df.iloc[starting_row, 0].split()
    tables[table_index].df.iloc[starting_row, 0] = row1[4]
    tables[table_index].df.iloc[starting_row, 1] = row1[5]
    tables[table_index].df.iloc[starting_row, 2] = row1[6] + ' ' + row1[16]
    tables[table_index].df.iloc[starting_row, 3] = row1[7] + ' ' + row1[17]
    tables[table_index].df.iloc[starting_row, 4] = row1[0] + row1[1]
    tables[table_index].df.iloc[starting_row, 5] = row1[8] + ' ' + row1[18]
    tables[table_index].df.iloc[starting_row, 6] = ' '.join(row1[9:13])
    tables[table_index].df.iloc[starting_row, 7] = ' '.join(row1[13:16])

    row2 = tables[table_index].df.iloc[starting_row + 1, 0].split()
    tables[table_index].df.iloc[starting_row + 1, 0] = row2[0]
    tables[table_index].df.iloc[starting_row + 1, 1] = row2[1]
    tables[table_index].df.iloc[starting_row + 1, 2] = row2[2] + ' ' + row2[12]
    tables[table_index].df.iloc[starting_row + 1, 3] = row2[3] + ' ' + row2[13]
    tables[table_index].df.iloc[starting_row + 1, 4] = row1[2] + row1[3]
    tables[table_index].df.iloc[starting_row + 1, 5] = row2[4] + ' ' + row2[14]
    tables[table_index].df.iloc[starting_row + 1, 6] = ' '.join(row2[5:9])
    tables[table_index].df.iloc[starting_row + 1, 7] = ' '.join(row2[9:12])


def clean_table_two_rows_has_exam3(table_index, header_row):
    starting_row = header_row + 1

    row1 = tables[table_index].df.iloc[starting_row, 0].split()
    tables[table_index].df.iloc[starting_row, 0] = row1[4]
    tables[table_index].df.iloc[starting_row, 1] = row1[6]
    tables[table_index].df.iloc[starting_row, 2] = row1[10] + ' ' + row1[16]
    tables[table_index].df.iloc[starting_row, 3] = row1[11] + ' ' + row1[17]
    tables[table_index].df.iloc[starting_row, 4] = row1[0] + row1[1]
    tables[table_index].df.iloc[starting_row, 5] = row1[12] + ' ' + row1[18]
    tables[table_index].df.iloc[starting_row, 6] = row1[5] + ' ' + row1[7] + ' ' + row1[8] + ' ' + row1[9]
    tables[table_index].df.iloc[starting_row, 7] = ' '.join(row1[13:16])

    row2 = tables[table_index].df.iloc[starting_row + 1, 0].split()
    tables[table_index].df.iloc[starting_row + 1, 0] = row2[0]
    tables[table_index].df.iloc[starting_row + 1, 1] = row2[2]
    tables[table_index].df.iloc[starting_row + 1, 2] = row2[6] + ' ' + row2[12]
    tables[table_index].df.iloc[starting_row + 1, 3] = row2[7] + ' ' + row2[13]
    tables[table_index].df.iloc[starting_row + 1, 4] = row1[2] + row1[3]
    tables[table_index].df.iloc[starting_row + 1, 5] = row2[8] + ' ' + row2[14]
    tables[table_index].df.iloc[starting_row + 1, 6] = row2[1] + ' ' + row2[3] + ' ' + row2[4] + ' ' + row2[5]
    tables[table_index].df.iloc[starting_row + 1, 7] = ' '.join(row2[9:12])


# TABLE 1 SEM I
clean_table(0, 1, 3)

# TABLE 2 SEM I
fix_mode(1, 2, 3)

# TABLE 3 SEM I
clean_table(2, 1, 10)

# TABLE 3 SEM II
clean_table(2, 20, 29)

# TABLE 4 SEM I
fix_mode(3, 2, 3)

# TABLE 5 SEM II
clean_table(4, 1, 3)

# TABLE 6 SEM I
clean_table_two_rows_no_exam(5, 1)

# TABLE 6 SEM II
clean_table(5, 5, 11)

# TABLE 7 SEM I
clean_table(6, 1, 7)

# TABLE 7 SEM II
clean_table_two_rows_has_exam1(6, 15)

# TABLE 8 SEM I
fix_mode(7, 2, 3)

# TABLE 9 SEM I
clean_table(8, 1, 6)

# TABLE 10 SEM I
fix_mode(9, 2, 4)

# TABLE 11 SEM I
clean_table(10, 1, 6)

# TABLE 12 SEM I
clean_table(11, 1, 4)

# TABLE 12 SEM II
clean_table(11, 8, 10)

# TABLE 13 SEM I
clean_table(12, 1, 4)

# TABLE 13 SEM II
clean_table(12, 9, 15)

# TABLE 14 SEM I
clean_table(13, 1, 4)

# TABLE 14 SEM II
clean_table(13, 8, 13)

# TABLE 15 SEM I
clean_table(14, 1, 3)

# TABLE 15 SEM II
clean_table(14, 7, 9)

# TABLE 16 SEM I
clean_table_two_rows_has_exam1(15, 1)

# TABLE 16 SEM II
clean_table(15, 5, 8)

# TABLE 17 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[16].df.iloc[1, :6] = tables[16].df.iloc[1, 0].split()

# Split column "mode" into its respective row
modes = tables[16].df.iloc[4, 4].split()
tables[16].df.iloc[2, 4] = modes[0]
tables[16].df.iloc[3, 4] = modes[1]
tables[16].df.iloc[4, 4] = modes[2] + modes[3]
tables[16].df.iloc[5, 4] = modes[4]
tables[16].df.iloc[6, 4] = modes[5]
tables[16].df.iloc[7, 4] = modes[6] + modes[7]

# TABLE 17 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[16].df.iloc[9, :6] = tables[16].df.iloc[9, 0].split()
tables[16].df = tables[16].df.drop(11).reset_index(drop=True)

column1 = tables[16].df.iloc[10, 0].split()
tables[16].df.iloc[10, 0:2] = column1[0:2]

tables[16].df.iloc[10, 6] = tables[16].df.iloc[10, 6][2:]
tables[16].df.iloc[11, 6] = "Y " + tables[16].df.iloc[11, 6]

column4 = tables[16].df.iloc[11, 4].split()
tables[16].df.iloc[10:13, 4] = [column4[0], column4[1] + column4[2] + column4[3], column4[4] + column4[5] + column4[6]]

# TABLE 18 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[17].df.iloc[1, :6] = tables[17].df.iloc[1, 0].split()

# Split column "mode" into its respective row
modes = tables[17].df.iloc[5, 4].split()
tables[17].df.iloc[2, 4] = modes[0] + modes[1]
tables[17].df.iloc[3, 4] = modes[2] + modes[3]
tables[17].df.iloc[4, 4] = modes[4]
tables[17].df.iloc[5, 4] = modes[5]
tables[17].df.iloc[6, 4] = modes[6] + modes[7]
tables[17].df.iloc[7, 4] = modes[8]
tables[17].df.iloc[8, 4] = modes[9]
tables[17].df.iloc[9, 4] = modes[10] + modes[11]

# TABLE 18 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[17].df.iloc[11, :6] = tables[17].df.iloc[11, 0].split()
tables[17].df = tables[17].df.drop(13).reset_index(drop=True)

row1 = tables[17].df.iloc[12, 0].split()
row2 = tables[17].df.iloc[13, 0].split()

tables[17].df.iloc[12, 0] = row1[0]
tables[17].df.iloc[12, 1] = row1[1]
tables[17].df.iloc[12, 2] = row1[2]
tables[17].df.iloc[12, 3] = row1[3]
tables[17].df.iloc[12, 4] = row2[0]
tables[17].df.iloc[12, 5] = row1[4]
tables[17].df.iloc[12, 6] = tables[17].df.iloc[12, 6][2:]

tables[17].df.iloc[13, 0] = row2[4]
tables[17].df.iloc[13, 1] = row2[5]
tables[17].df.iloc[13, 2] = row2[6] + ' ' + row2[9] + ' ' + row2[12]
tables[17].df.iloc[13, 3] = row2[7] + ' ' + row2[10] + ' ' + row2[13]
tables[17].df.iloc[13, 4] = row2[1] + ' ' + row2[2] + ' ' + row2[3]
tables[17].df.iloc[13, 5] = row2[8] + ' ' + row2[11] + ' ' + row2[14]
tables[17].df.iloc[13, 6] = "Y " + tables[17].df.iloc[13, 6]

# TABLE 19 SEM I
clean_table(18, 1, 6)

# TABLE 19 SEM II
clean_table(18, 12, 17)

# TABLE 20 SEM I
clean_table(19, 1, 4)

# TABLE 20 SEM II
clean_table(19, 9, 11)

# TABLE 21 SEM I
clean_table(20, 1, 5)

# TABLE 21 SEM II
clean_table_two_rows_no_exam(20, 11)

# TABLE 22 SEM I
clean_table(21, 1, 4)

# TABLE 22 SEM II
clean_table(21, 9, 16)

# TABLE 23 SEM I
clean_table_two_rows_no_exam(22, 1)

# TABLE 23 SEM II
clean_table(22, 5, 10)

# TABLE 24 SEM I
clean_table(23, 1, 6)

# TABLE 24 SEM II
clean_table(23, 12, 17)

# TABLE 25 SEM I
clean_table(24, 1, 4)

# TABLE 25 SEM II
clean_table(24, 8, 11)

# TABLE 26 SEM I
clean_table(25, 1, 6)

# TABLE 26 SEM II
clean_table(25, 12, 16)

# TABLE 27 SEM I
clean_table(26, 1, 4)

# TABLE 27 SEM II
clean_table(26, 8, 10)

# TABLE 28 SEM I
clean_table(27, 1, 3)

# TABLE 28 SEM II
clean_table(27, 6, 9)

# TABLE 29 SEM I
clean_table(28, 1, 3)

# TABLE 29 SEM II
clean_table(28, 6, 9)

# TABLE 30 SEM I
clean_table(29, 1, 3)

# TABLE 30 SEM II
clean_table(29, 6, 9)

# TABLE 31 SEM I
clean_table(30, 1, 4)

# TABLE 31 SEM II
fix_mode(30, 10, 11)

# TABLE 32 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[31].df.iloc[1, :6] = tables[31].df.iloc[1, 0].split()
tables[31].df = tables[31].df.drop(11).reset_index(drop=True)

# Split column "mode" into its respective row
modes = tables[31].df.iloc[4, 4].split()
tables[31].df.iloc[2, 4] = modes[0]
tables[31].df.iloc[3, 4] = modes[1]
tables[31].df.iloc[4, 4] = modes[2] + modes[3]
tables[31].df.iloc[5, 4] = modes[4]
tables[31].df.iloc[6, 4] = modes[5]
tables[31].df.iloc[7, 4] = modes[6] + modes[7]

rows = [(2, 6), (4, 6), (5, 6), (7, 6), (12, 6)]
for row, column in rows:
    split_row = tables[31].df.iloc[row, column].split()
    tables[31].df.iloc[row, column] = f"{split_row[3]} {' '.join(split_row[:3])}"

# TABLE 32 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[31].df.iloc[9, :6] = tables[31].df.iloc[9, 0].split()

column1 = tables[31].df.iloc[10, 0].split()
tables[31].df.iloc[10, 0:2] = column1[0:2][::-1]

tables[31].df.iloc[10, 6] = tables[31].df.iloc[10, 6][2:]
tables[31].df.iloc[11, 6] = "Y " + tables[31].df.iloc[11, 6]

modes = tables[31].df.iloc[11, 4].split()
tables[31].df.iloc[10:13, 4] = [modes[0], modes[1] + modes[2] + modes[3], modes[4] + modes[5] + modes[6]]

# TABLE 33 SEM I
# Split column "mode" into its respective row
modes = tables[32].df.iloc[6, 4].split()
for i in range(2, 11):
    tables[32].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]
    split_row = tables[32].df.iloc[i, 6].split()
    tables[32].df.iloc[i, 6] = f"{split_row[3]} {' '.join(split_row[:3])}"

# TABLE 33 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[32].df.iloc[12, :6] = tables[32].df.iloc[12, 0].split()

# Split column "mode" into its respective row
modes = tables[32].df.iloc[15, 4].split()
for i in range(13, 18):
    tables[32].df.iloc[i, 4] = modes[2 * (i - 13)] + modes[2 * (i - 13) + 1]
    split_row = tables[32].df.iloc[i, 6].split()
    tables[32].df.iloc[i, 6] = f"{split_row[3]} {' '.join(split_row[:3])}"

# TABLE 34 SEM I
clean_table(33, 1, 4)

# TABLE 34 SEM II
clean_table(33, 9, 11)

# TABLE 35 SEM I
clean_table(34, 1, 4)

# TABLE 35 SEM II
clean_table(34, 9, 11)

# TABLE 36 SEM I
tables[35].df = tables[35].df.reindex(columns=[*tables[35].df.columns, *range(8)])
tables[35].df = tables[35].df.iloc[:, 1:].reset_index(drop=True)
tables[35].df = tables[35].df.fillna('')

clean_table_two_rows_has_exam1(35, 1)

# TABLE 37 SEM I
clean_table(36, 1, 7)

# TABLE 37 SEM II
clean_table(36, 15, 18)

# TABLE 38 SEM I
clean_table(37, 1, 7)

# TABLE 38 SEM II
clean_table(37, 15, 19)

# TABLE 39 SEM I
tables[38].df = tables[38].df.reindex(columns=[*tables[38].df.columns, *range(8)])
tables[38].df = tables[38].df.iloc[:, 1:].reset_index(drop=True)
tables[38].df = tables[38].df.fillna('')

clean_table_two_rows_no_exam(38, 1)

# TABLE 40 SEM I
clean_table(39, 1, 3)

# TABLE 40 SEM II
clean_table(39, 7, 9)

# TABLE 41 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[40].df.iloc[1, :6] = tables[40].df.iloc[1, 0].split()

# TABLE 41 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[40].df.iloc[4, :6] = tables[40].df.iloc[4, 0].split()

# TABLE 42 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[41].df.iloc[1, :6] = tables[41].df.iloc[1, 0].split()

# TABLE 42 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[41].df.iloc[4, :6] = tables[41].df.iloc[4, 0].split()

# TABLE 43 SEM II
tables[42].df = tables[42].df.reindex(columns=[*tables[42].df.columns, *range(8)])
tables[42].df = tables[42].df.iloc[:, 1:].reset_index(drop=True)
tables[42].df = tables[42].df.fillna('')

clean_table_two_rows_no_exam(42, 1)

# TABLE 44 SEM I
tables[43].df = tables[43].df.reindex(columns=[*tables[43].df.columns, *range(8)])
tables[43].df = tables[43].df.iloc[:, 1:].reset_index(drop=True)
tables[43].df = tables[43].df.fillna('')

clean_table_two_rows_no_exam(43, 1)

# TABLE 45 SEM I
clean_table(44, 1, 3)

# TABLE 45 SEM II
clean_table(44, 6, 8)

# TABLE 46 SEM I
clean_table(45, 1, 3)

# TABLE 46 SEM II
fix_mode(45, 8, 9)

# TABLE 47 SEM I
clean_table(46, 1, 3)

# TABLE 47 SEM II
clean_table(46, 6, 8)

# TABLE 48 SEM I
clean_table(47, 1, 3)

# TABLE 48 SEM II
fix_mode(47, 8, 9)

# TABLE 49 SEM I
clean_table(48, 1, 3)

# TABLE 49 SEM II
clean_table(48, 7, 9)

# TABLE 50 SEM I
clean_table(49, 1, 3)

# TABLE 50 SEM II
fix_mode(49, 8, 9)

# TABLE 51 SEM I
tables[50].df = tables[50].df.reindex(columns=[*tables[50].df.columns, *range(8)])
tables[50].df = tables[50].df.iloc[:, 1:].reset_index(drop=True)
tables[50].df = tables[50].df.fillna('')

clean_table_two_rows_has_exam1(50, 1)

# TABLE 51 SEM II
clean_table_two_rows_has_exam1(50, 5)

# TABLE 52 SEM I
clean_table(51, 1, 3)

# TABLE 52 SEM II
clean_table_two_rows_no_exam(51, 6)

# TABLE 53 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[52].df.iloc[1, :6] = tables[52].df.iloc[1, 0].split()

# TABLE 53 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[52].df.iloc[4, :6] = tables[52].df.iloc[4, 0].split()

# TABLE 54 SEM I
tables[53].df = tables[53].df.reindex(columns=[*tables[53].df.columns, *range(8)])
tables[53].df = tables[53].df.iloc[:, 1:].reset_index(drop=True)
tables[53].df = tables[53].df.fillna('')

# Split "Sec Day Time Loc Mode Cap Exam Staff" into its respective column
tables[53].df.iloc[1, :8] = tables[53].df.iloc[1, 0].split()

row1 = tables[53].df.iloc[2, 0].split()
tables[53].df.iloc[2, 0] = row1[8]
tables[53].df.iloc[2, 1] = row1[9]
tables[53].df.iloc[2, 2] = row1[10] + ' ' + row1[16]
tables[53].df.iloc[2, 3] = row1[11] + ' ' + row1[17]
tables[53].df.iloc[2, 4] = row1[0] + row1[1]
tables[53].df.iloc[2, 5] = row1[12] + ' ' + row1[18]
tables[53].df.iloc[2, 6] = row1[4] + ' ' + row1[5] + ' ' + row1[6] + ' ' + row1[7]
tables[53].df.iloc[2, 7] = row1[13] + ' ' + row1[14] + ' ' + row1[15]

row2 = tables[53].df.iloc[3, 0].split()
tables[53].df.iloc[3, 0] = row2[4]
tables[53].df.iloc[3, 1] = row2[5]
tables[53].df.iloc[3, 2] = row2[6] + ' ' + row2[12]
tables[53].df.iloc[3, 3] = row2[7] + ' ' + row2[13]
tables[53].df.iloc[3, 4] = row1[2] + row1[3]
tables[53].df.iloc[3, 5] = row2[8] + ' ' + row2[14]
tables[53].df.iloc[3, 6] = row2[0] + ' ' + row2[1] + ' ' + row2[2] + ' ' + row2[3]
tables[53].df.iloc[3, 7] = row2[9] + ' ' + row2[10] + ' ' + row2[11]

# TABLE 55 SEM I
tables[54].df = tables[54].df.reindex(columns=[*tables[54].df.columns, *range(8)])
tables[54].df = tables[54].df.iloc[:, 1:].reset_index(drop=True)
tables[54].df = tables[54].df.fillna('')

# Split "Sec Day Time Loc Mode Cap Exam Staff" into its respective column
split_headers = tables[54].df.iloc[1, 0].split()
correct_order = [split_headers[1], split_headers[2], split_headers[3], split_headers[4],
                 split_headers[5], split_headers[6], split_headers[0], split_headers[7]]
tables[54].df.iloc[1, :8] = correct_order

row1 = tables[54].df.iloc[2, 0].split()
tables[54].df.iloc[2, 0] = row1[8]
tables[54].df.iloc[2, 1] = row1[9]
tables[54].df.iloc[2, 2] = row1[10] + ' ' + row1[16]
tables[54].df.iloc[2, 3] = row1[11] + ' ' + row1[17]
tables[54].df.iloc[2, 4] = row1[0] + row1[1]
tables[54].df.iloc[2, 5] = row1[12] + ' ' + row1[18]
tables[54].df.iloc[2, 6] = row1[4] + ' ' + row1[5] + ' ' + row1[6] + ' ' + row1[7]
tables[54].df.iloc[2, 7] = row1[13] + ' ' + row1[14] + ' ' + row1[15]

row2 = tables[54].df.iloc[3, 0].split()
tables[54].df.iloc[3, 0] = row2[4]
tables[54].df.iloc[3, 1] = row2[5]
tables[54].df.iloc[3, 2] = row2[6] + ' ' + row2[12]
tables[54].df.iloc[3, 3] = row2[7] + ' ' + row2[13]
tables[54].df.iloc[3, 4] = row1[2] + row1[3]
tables[54].df.iloc[3, 5] = row2[8] + ' ' + row2[14]
tables[54].df.iloc[3, 6] = row2[0] + ' ' + row2[1] + ' ' + row2[2] + ' ' + row2[3]
tables[54].df.iloc[3, 7] = row2[9] + ' ' + row2[10] + ' ' + row2[11]

# TABLE 55 SEM II
# Split "Sec Day Time Loc Mode Cap Exam Staff" into its respective column
split_headers = tables[54].df.iloc[5, 0].split()
correct_order = [split_headers[1], split_headers[2], split_headers[3], split_headers[4],
                 split_headers[5], split_headers[6], split_headers[0], split_headers[7]]
tables[54].df.iloc[5, :8] = correct_order

row1 = tables[54].df.iloc[6, 0].split()
tables[54].df.iloc[6, 0] = row1[8]
tables[54].df.iloc[6, 1] = row1[9]
tables[54].df.iloc[6, 2] = row1[10] + ' ' + row1[16]
tables[54].df.iloc[6, 3] = row1[11] + ' ' + row1[17]
tables[54].df.iloc[6, 4] = row1[0] + row1[1]
tables[54].df.iloc[6, 5] = row1[12] + ' ' + row1[18]
tables[54].df.iloc[6, 6] = row1[4] + ' ' + row1[5] + ' ' + row1[6] + ' ' + row1[7]
tables[54].df.iloc[6, 7] = row1[13] + ' ' + row1[14] + ' ' + row1[15]

row2 = tables[54].df.iloc[7, 0].split()
tables[54].df.iloc[7, 0] = row2[4]
tables[54].df.iloc[7, 1] = row2[5]
tables[54].df.iloc[7, 2] = row2[6] + ' ' + row2[12]
tables[54].df.iloc[7, 3] = row2[7] + ' ' + row2[13]
tables[54].df.iloc[7, 4] = row1[2] + row1[3]
tables[54].df.iloc[7, 5] = row2[8] + ' ' + row2[14]
tables[54].df.iloc[7, 6] = row2[0] + ' ' + row2[1] + ' ' + row2[2] + ' ' + row2[3]
tables[54].df.iloc[7, 7] = row2[9] + ' ' + row2[10] + ' ' + row2[11]

# TABLE 56 SEM I
clean_table(55, 1, 4)

# TABLE 56 SEM II
clean_table(55, 9, 17)

# TABLE 57 SEM I
tables[56].df = tables[56].df.drop(3).reset_index(drop=True)
tables[56].df = tables[56].df.drop(4).reset_index(drop=True)
tables[56].df = tables[56].df.drop(5).reset_index(drop=True)
tables[56].df = tables[56].df.drop(7).reset_index(drop=True)
tables[56].df = tables[56].df.drop(10).reset_index(drop=True)
tables[56].df = tables[56].df.drop(11).reset_index(drop=True)
tables[56].df = tables[56].df.drop(12).reset_index(drop=True)
tables[56].df = tables[56].df.drop(13).reset_index(drop=True)
tables[56].df = tables[56].df.drop(14).reset_index(drop=True)

tables[56].df.insert(loc=1, column='1', value="")
tables[56].df.columns = range(len(tables[56].df.columns))

for i in range(2, 7):
    split_column = tables[56].df.iloc[i, 0].split()
    tables[56].df.iloc[i, 0] = split_column[0]
    tables[56].df.iloc[i, 1] = split_column[1]

clean_table(56, 1, 4)

# TABLE 57 SEM II
split_column = tables[54].df.iloc[5, 0].split()

for i in range(9, 14):
    split_column = tables[56].df.iloc[i, 0].split()
    tables[56].df.iloc[i, 0] = split_column[0]
    tables[56].df.iloc[i, 1] = split_column[1]

clean_table(56, 8, 11)

# TABLE 58 SEM I
fix_mode(57, 2, 4)

# TABLE 58 SEM II
# Split "Sec Day Time Loc Mode Cap Exam Staff" into its respective column
tables[57].df.iloc[9, :8] = tables[57].df.iloc[9, 0].split()

row1 = tables[57].df.iloc[10, 0].split()
tables[57].df.iloc[10, 0] = row1[4]
tables[57].df.iloc[10, 1] = row1[6]
tables[57].df.iloc[10, 2] = row1[7] + ' ' + row1[13]
tables[57].df.iloc[10, 3] = row1[8] + ' ' + row1[14]
tables[57].df.iloc[10, 4] = row1[0] + row1[1]
tables[57].df.iloc[10, 5] = row1[9] + ' ' + row1[15]
tables[57].df.iloc[10, 6] = row1[5]
tables[57].df.iloc[10, 7] = ' '.join(row1[10:13])

row2 = tables[57].df.iloc[11, 0].split()
tables[57].df.iloc[11, 0] = row2[0]
tables[57].df.iloc[11, 1] = row2[2]
tables[57].df.iloc[11, 2] = row2[3] + ' ' + row2[9]
tables[57].df.iloc[11, 3] = row2[4] + ' ' + row2[10]
tables[57].df.iloc[11, 4] = row1[2] + row1[3]
tables[57].df.iloc[11, 5] = row2[5] + ' ' + row2[11]
tables[57].df.iloc[11, 6] = row2[1]
tables[57].df.iloc[11, 7] = ' '.join(row2[6:9])

# TABLE 59 SEM I
clean_table(58, 1, 4)

# TABLE 59 SEM II
clean_table(58, 8, 10)

# TABLE 60 SEM I
clean_table(59, 1, 3)

# TABLE 60 SEM II
# Split "Sec Day Time Loc Mode Cap Exam Staff" into its respective column
split_headers = tables[59].df.iloc[6, 0].split()
correct_order = [split_headers[0], split_headers[1], split_headers[2], split_headers[3],
                 split_headers[4], split_headers[5], split_headers[7], split_headers[6]]
tables[59].df.iloc[6, :8] = correct_order

row1 = tables[59].df.iloc[7, 0].split()
tables[59].df.iloc[7, 0] = row1[5]
tables[59].df.iloc[7, 1] = row1[6]
tables[59].df.iloc[7, 2] = row1[7] + ' ' + row1[13]
tables[59].df.iloc[7, 3] = row1[8] + ' ' + row1[14]
tables[59].df.iloc[7, 4] = row1[0] + row1[1]
tables[59].df.iloc[7, 5] = row1[9] + ' ' + row1[15]
tables[59].df.iloc[7, 6] = row1[4]
tables[59].df.iloc[7, 7] = ' '.join(row1[10:13])

row2 = tables[59].df.iloc[8, 0].split()
tables[59].df.iloc[8, 0] = row2[1]
tables[59].df.iloc[8, 1] = row2[2]
tables[59].df.iloc[8, 2] = row2[3] + ' ' + row2[9]
tables[59].df.iloc[8, 3] = row2[4] + ' ' + row2[10]
tables[59].df.iloc[8, 4] = row1[2] + row1[3]
tables[59].df.iloc[8, 5] = row2[5] + ' ' + row2[11]
tables[59].df.iloc[8, 6] = row2[0]
tables[59].df.iloc[8, 7] = ' '.join(row2[6:9])

# TABLE 61 SEM I
clean_table(60, 1, 3)

# TABLE 62 SEM II
tables[61].df = tables[61].df.reindex(columns=[*tables[61].df.columns, *range(8)])
tables[61].df = tables[61].df.iloc[:, 1:].reset_index(drop=True)
tables[61].df = tables[61].df.fillna('')

tables[61].df.iloc[1, :8] = tables[61].df.iloc[1, 0].split()

clean_table_two_rows_has_exam3(61, 1)

# TABLE 63 SEM I
tables[62].df = tables[62].df.reindex(columns=[*tables[62].df.columns, *range(8)])
tables[62].df = tables[62].df.iloc[:, 1:].reset_index(drop=True)
tables[62].df = tables[62].df.fillna('')

tables[62].df.iloc[1, :8] = tables[62].df.iloc[1, 0].split()

row1 = tables[62].df.iloc[2, 0].split()
tables[62].df.iloc[2, 0] = row1[8]
tables[62].df.iloc[2, 1] = row1[10]
tables[62].df.iloc[2, 2] = row1[14] + ' ' + row1[19]
tables[62].df.iloc[2, 3] = row1[15] + ' ' + row1[20]
tables[62].df.iloc[2, 4] = row1[0] + row1[1]
tables[62].df.iloc[2, 5] = row1[4] + ' ' + row1[5]
tables[62].df.iloc[2, 6] = row1[9] + ' ' + row1[11] + ' ' + row1[12] + ' ' + row1[13]
tables[62].df.iloc[2, 7] = ' '.join(row1[16:19])

row2 = tables[62].df.iloc[3, 0].split()
tables[62].df.iloc[3, 0] = row2[0]
tables[62].df.iloc[3, 1] = row2[2]
tables[62].df.iloc[3, 2] = row2[6] + ' ' + row2[11]
tables[62].df.iloc[3, 3] = row2[7] + ' ' + row2[12]
tables[62].df.iloc[3, 4] = row1[2] + row1[3]
tables[62].df.iloc[3, 5] = row1[6] + ' ' + row1[7]
tables[62].df.iloc[3, 6] = row2[1] + ' ' + row2[3] + ' ' + row2[4] + ' ' + row2[5]
tables[62].df.iloc[3, 7] = ' '.join(row2[8:11])

# TABLE 63 SEM II
# Split "Sec Day Time Loc Mode Cap Exam Staff" into its respective column
split_headers = tables[62].df.iloc[5, 0].split()
correct_order = [split_headers[0], split_headers[1], split_headers[2], split_headers[3],
                 split_headers[4], split_headers[5], split_headers[7], split_headers[6]]
tables[62].df.iloc[5, :8] = correct_order

clean_table_two_rows_has_exam3(62, 5)

# TABLE 64 SEM I
tables[63].df = tables[63].df.reindex(columns=[*tables[63].df.columns, *range(8)])
tables[63].df = tables[63].df.iloc[:, 1:].reset_index(drop=True)
tables[63].df = tables[63].df.fillna('')

split_headers = tables[63].df.iloc[1, 0].split()
correct_order = [split_headers[1], split_headers[2], split_headers[3], split_headers[4],
                 split_headers[5], split_headers[6], split_headers[0], split_headers[7]]
tables[63].df.iloc[1, :8] = correct_order

clean_table_two_rows_has_exam3(63, 1)

# TABLE 65 SEM I
fix_mode(64, 2, 3)

# TABLE 66 SEM II
tables[65].df = tables[65].df.reindex(columns=[*tables[65].df.columns, *range(8)])
tables[65].df = tables[65].df.iloc[:, 1:].reset_index(drop=True)
tables[65].df = tables[65].df.fillna('')

split_headers = tables[65].df.iloc[1, 0].split()
correct_order = [split_headers[1], split_headers[2], split_headers[3], split_headers[4],
                 split_headers[5], split_headers[6], split_headers[0], split_headers[7]]
tables[65].df.iloc[1, :8] = correct_order

clean_table_two_rows_has_exam3(65, 1)

# TABLE 67 SEM I
clean_table(66, 1, 4)

# TABLE 68 SEM II
fix_mode(67, 2, 4)

# Display each table under its corresponding course code
for i, match in enumerate(matches):
    print(f"{i + 1}. Course Code: {match[1]}")
    print(f"Course Name: {match[2]}")
    print(f"Semester Offered: {match[0]}")
    print()

    if i < len(tables):
        table = tables[i]
        table.df = table.df.map(lambda x: x.replace('\n', ' '))
        display(table.df)
