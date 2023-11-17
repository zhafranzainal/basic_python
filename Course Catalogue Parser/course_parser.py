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

tables = camelot.read_pdf('https://or.ump.edu.my/or/CourseCatalog/COURSE_CATALOG_IJA.pdf', pages='345-384')

# TABLE 1 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[0].df.iloc[1, :6] = tables[0].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[0].df.iloc[3, 4].split()[:8]
for i in range(2, 6):
    tables[0].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 2 SEM I
# Split column "mode" into its respective row
modes = tables[1].df.iloc[3, 4].split()[:8]
for i in range(2, 6):
    tables[1].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 3 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[2].df.iloc[1, :6] = tables[2].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[2].df.iloc[10, 4].split()[:34]
for i in range(2, 19):
    tables[2].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 3 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[2].df.iloc[20, :6] = tables[2].df.iloc[20, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[2].df.iloc[29, 4].split()[:34]
for i in range(21, 38):
    tables[2].df.iloc[i, 4] = modes[2 * (i - 21)] + modes[2 * (i - 21) + 1]

# TABLE 4 SEM I
# Split column "mode" into its respective row
modes = tables[3].df.iloc[3, 4].split()[:8]
for i in range(2, 6):
    tables[3].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 5 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[4].df.iloc[1, :6] = tables[4].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[4].df.iloc[3, 4].split()[:8]
for i in range(2, 6):
    tables[4].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 6 SEM I
# Split "Sec Day Time Loc Mode Cap Exam Staff" into its respective column
tables[5].df.iloc[1, :8] = tables[5].df.iloc[1, 0].split()[:8]

row1 = tables[5].df.iloc[2, 0].split()
tables[5].df.iloc[2, 0] = row1[4]
tables[5].df.iloc[2, 1] = row1[5]
tables[5].df.iloc[2, 2] = row1[6] + ' ' + row1[13]
tables[5].df.iloc[2, 3] = row1[7] + ' ' + row1[14]
tables[5].df.iloc[2, 4] = row1[0] + row1[1]
tables[5].df.iloc[2, 5] = row1[8] + ' ' + row1[15]
tables[5].df.iloc[2, 6] = row1[9]
tables[5].df.iloc[2, 7] = row1[10] + ' ' + row1[11] + ' ' + row1[12]

row2 = tables[5].df.iloc[3, 0].split()
tables[5].df.iloc[3, 0] = row2[0]
tables[5].df.iloc[3, 1] = row2[1]
tables[5].df.iloc[3, 2] = row2[2] + ' ' + row2[9]
tables[5].df.iloc[3, 3] = row2[3] + ' ' + row2[10]
tables[5].df.iloc[3, 4] = row1[2] + row1[3]
tables[5].df.iloc[3, 5] = row2[4] + ' ' + row2[11]
tables[5].df.iloc[3, 6] = row2[5]
tables[5].df.iloc[3, 7] = row2[6] + ' ' + row2[7] + ' ' + row2[8]

# TABLE 6 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[5].df.iloc[5, :6] = tables[5].df.iloc[5, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[5].df.iloc[11, 4].split()[:24]
for i in range(6, 18):
    tables[5].df.iloc[i, 4] = modes[2 * (i - 6)] + modes[2 * (i - 6) + 1]

# TABLE 7 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[6].df.iloc[1, :6] = tables[6].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[6].df.iloc[7, 4].split()[:24]
for i in range(2, 14):
    tables[6].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 7 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[6].df.iloc[15, :8] = tables[6].df.iloc[15, 0].split()[:8]

row1 = tables[6].df.iloc[16, 0].split()
tables[6].df.iloc[16, 0] = row1[4]
tables[6].df.iloc[16, 1] = row1[5]
tables[6].df.iloc[16, 2] = row1[6] + ' ' + row1[16]
tables[6].df.iloc[16, 3] = row1[7] + ' ' + row1[17]
tables[6].df.iloc[16, 4] = row1[0] + row1[1]
tables[6].df.iloc[16, 5] = row1[8] + ' ' + row1[18]
tables[6].df.iloc[16, 6] = row1[9] + ' ' + row1[10] + ' ' + row1[11] + ' ' + row1[12]
tables[6].df.iloc[16, 7] = row1[13] + ' ' + row1[14] + ' ' + row1[15]

row2 = tables[6].df.iloc[17, 0].split()
tables[6].df.iloc[17, 0] = row2[0]
tables[6].df.iloc[17, 1] = row2[1]
tables[6].df.iloc[17, 2] = row2[2] + ' ' + row2[12]
tables[6].df.iloc[17, 3] = row2[3] + ' ' + row2[13]
tables[6].df.iloc[17, 4] = row1[2] + row1[3]
tables[6].df.iloc[17, 5] = row2[4] + ' ' + row2[14]
tables[6].df.iloc[17, 6] = row2[5] + ' ' + row2[6] + ' ' + row2[7] + ' ' + row2[8]
tables[6].df.iloc[17, 7] = row2[9] + ' ' + row2[10] + ' ' + row2[11]

# TABLE 8 SEM I
# Split column "mode" into its respective row
modes = tables[7].df.iloc[3, 4].split()[:6]
for i in range(2, 5):
    tables[7].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 9 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[8].df.iloc[1, :6] = tables[8].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[8].df.iloc[6, 4].split()[:20]
for i in range(2, 12):
    tables[8].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 10 SEM I
# Split column "mode" into its respective row
modes = tables[9].df.iloc[4, 4].split()[:12]
for i in range(2, 8):
    tables[9].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 11 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[10].df.iloc[1, :6] = tables[10].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[10].df.iloc[6, 4].split()[:20]
for i in range(2, 12):
    tables[10].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 12 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[11].df.iloc[1, :6] = tables[11].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[11].df.iloc[4, 4].split()[:10]
for i in range(2, 7):
    tables[11].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 12 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[11].df.iloc[8, :6] = tables[11].df.iloc[8, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[11].df.iloc[10, 4].split()[:10]
for i in range(9, 13):
    tables[11].df.iloc[i, 4] = modes[2 * (i - 9)] + modes[2 * (i - 9) + 1]

# TABLE 13 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[12].df.iloc[1, :6] = tables[12].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[12].df.iloc[4, 4].split()[:12]
for i in range(2, 8):
    tables[12].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 13 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[12].df.iloc[9, :6] = tables[12].df.iloc[9, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[12].df.iloc[15, 4].split()[:24]
for i in range(10, 22):
    tables[12].df.iloc[i, 4] = modes[2 * (i - 10)] + modes[2 * (i - 10) + 1]

# TABLE 14 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[13].df.iloc[1, :6] = tables[13].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[13].df.iloc[4, 4].split()[:10]
for i in range(2, 7):
    tables[13].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 14 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[13].df.iloc[8, :6] = tables[13].df.iloc[8, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[13].df.iloc[13, 4].split()[:18]
for i in range(9, 18):
    tables[13].df.iloc[i, 4] = modes[2 * (i - 9)] + modes[2 * (i - 9) + 1]

# TABLE 15 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[14].df.iloc[1, :6] = tables[14].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[14].df.iloc[3, 4].split()[:8]
for i in range(2, 6):
    tables[14].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 15 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[14].df.iloc[7, :6] = tables[14].df.iloc[7, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[14].df.iloc[9, 4].split()[:8]
for i in range(8, 12):
    tables[14].df.iloc[i, 4] = modes[2 * (i - 8)] + modes[2 * (i - 8) + 1]

# TABLE 16 SEM I
# Split "Sec Day Time Loc Mode Cap Exam Staff" into its respective column
tables[15].df.iloc[1, :8] = tables[15].df.iloc[1, 0].split()[:8]

row1 = tables[15].df.iloc[2, 0].split()
tables[15].df.iloc[2, 0] = row1[4]
tables[15].df.iloc[2, 1] = row1[5]
tables[15].df.iloc[2, 2] = row1[6] + ' ' + row1[16]
tables[15].df.iloc[2, 3] = row1[7] + ' ' + row1[17]
tables[15].df.iloc[2, 4] = row1[0] + row1[1]
tables[15].df.iloc[2, 5] = row1[8] + ' ' + row1[18]
tables[15].df.iloc[2, 6] = row1[9] + ' ' + row1[10] + ' ' + row1[11] + ' ' + row1[12]
tables[15].df.iloc[2, 7] = row1[13] + ' ' + row1[14] + ' ' + row1[15]

row2 = tables[15].df.iloc[3, 0].split()
tables[15].df.iloc[3, 0] = row2[0]
tables[15].df.iloc[3, 1] = row2[1]
tables[15].df.iloc[3, 2] = row2[2] + ' ' + row2[12]
tables[15].df.iloc[3, 3] = row2[3] + ' ' + row2[13]
tables[15].df.iloc[3, 4] = row1[2] + row1[3]
tables[15].df.iloc[3, 5] = row2[4] + ' ' + row2[14]
tables[15].df.iloc[3, 6] = row2[5] + ' ' + row2[6] + ' ' + row2[7] + ' ' + row2[8]
tables[15].df.iloc[3, 7] = row2[9] + ' ' + row2[10] + ' ' + row2[11]

# TABLE 16 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[15].df.iloc[5, :6] = tables[15].df.iloc[5, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[15].df.iloc[8, 4].split()[:12]
for i in range(6, 12):
    tables[15].df.iloc[i, 4] = modes[2 * (i - 6)] + modes[2 * (i - 6) + 1]

# TABLE 17 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[16].df.iloc[1, :6] = tables[16].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[16].df.iloc[4, 4].split()[:8]
tables[16].df.iloc[2, 4] = modes[0]
tables[16].df.iloc[3, 4] = modes[1]
tables[16].df.iloc[4, 4] = modes[2] + modes[3]
tables[16].df.iloc[5, 4] = modes[4]
tables[16].df.iloc[6, 4] = modes[5]
tables[16].df.iloc[7, 4] = modes[6] + modes[7]

# TABLE 17 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[16].df.iloc[9, :6] = tables[16].df.iloc[9, 0].split()[:6]
tables[16].df = tables[16].df.drop(11).reset_index(drop=True)

column1 = tables[16].df.iloc[10, 0].split()
tables[16].df.iloc[10, 0:2] = column1[0:2]

tables[16].df.iloc[10, 6] = tables[16].df.iloc[10, 6][2:]
tables[16].df.iloc[11, 6] = "Y " + tables[16].df.iloc[11, 6]

column4 = tables[16].df.iloc[11, 4].split()
tables[16].df.iloc[10:13, 4] = [column4[0], column4[1] + column4[2] + column4[3], column4[4] + column4[5] + column4[6]]

# TABLE 18 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[17].df.iloc[1, :6] = tables[17].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[17].df.iloc[5, 4].split()[:12]
tables[17].df.iloc[2, 4] = modes[0] + modes[1]
tables[17].df.iloc[3, 4] = modes[2] + modes[3]
tables[17].df.iloc[4, 4] = modes[4]
tables[17].df.iloc[5, 4] = modes[5]
tables[17].df.iloc[6, 4] = modes[6] + modes[7]
tables[17].df.iloc[7, 4] = modes[8]
tables[17].df.iloc[8, 4] = modes[9]
tables[17].df.iloc[9, 4] = modes[10] + modes[11]

# TABLE 18 SEM II
# Split "Sec Day Time Loc Mode Cap Exam Staff" into its respective column
tables[17].df.iloc[11, :8] = tables[17].df.iloc[11, 0].split()[:8]

row1 = tables[17].df.iloc[12, 0].split()
row2 = tables[17].df.iloc[13, 0].split()

tables[17].df.iloc[12, 0] = row1[2]
tables[17].df.iloc[12, 1] = row1[3]
tables[17].df.iloc[12, 2] = row1[4]
tables[17].df.iloc[12, 3] = row1[5]
tables[17].df.iloc[12, 4] = row2[0]
tables[17].df.iloc[12, 5] = row1[6]
tables[17].df.iloc[12, 6] = row1[0] + ' ' + row1[7] + ' ' + row1[8] + ' ' + row1[9]
tables[17].df.iloc[12, 7] = row1[10] + ' ' + row1[11] + ' ' + row1[12]

tables[17].df.iloc[13, 0] = row2[4]
tables[17].df.iloc[13, 1] = row2[5]
tables[17].df.iloc[13, 2] = row2[6] + ' ' + row2[15] + ' ' + row2[18]
tables[17].df.iloc[13, 3] = row2[7] + ' ' + row2[16] + ' ' + row2[19]
tables[17].df.iloc[13, 4] = row2[1] + ' ' + row2[2] + ' ' + row2[3]
tables[17].df.iloc[13, 5] = row2[8] + ' ' + row2[17] + ' ' + row2[20]
tables[17].df.iloc[13, 6] = row1[1] + ' ' + row2[9] + ' ' + row2[10] + ' ' + row2[11]
tables[17].df.iloc[13, 7] = row2[12] + ' ' + row2[13] + ' ' + row2[14]

# TABLE 19 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[18].df.iloc[1, :6] = tables[18].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[18].df.iloc[6, 4].split()[:18]
for i in range(2, 11):
    tables[18].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 19 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[18].df.iloc[12, :6] = tables[18].df.iloc[12, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[18].df.iloc[17, 4].split()[:18]
for i in range(13, 22):
    tables[18].df.iloc[i, 4] = modes[2 * (i - 13)] + modes[2 * (i - 13) + 1]

# TABLE 20 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[19].df.iloc[1, :6] = tables[19].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[19].df.iloc[4, 4].split()[:12]
for i in range(2, 8):
    tables[19].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 20 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[19].df.iloc[9, :6] = tables[19].df.iloc[9, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[19].df.iloc[11, 4].split()[:6]
for i in range(10, 13):
    tables[19].df.iloc[i, 4] = modes[2 * (i - 10)] + modes[2 * (i - 10) + 1]

# TABLE 21 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[20].df.iloc[1, :6] = tables[20].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[20].df.iloc[5, 4].split()[:16]
for i in range(2, 10):
    tables[20].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 21 SEM II
# Split "Sec Day Time Loc Mode Cap Exam Staff" into its respective column
tables[20].df.iloc[11, :8] = tables[20].df.iloc[11, 0].split()[:8]

row1 = tables[20].df.iloc[12, 0].split()
tables[20].df.iloc[12, 0] = row1[4]
tables[20].df.iloc[12, 1] = row1[5]
tables[20].df.iloc[12, 2] = row1[6] + ' ' + row1[13]
tables[20].df.iloc[12, 3] = row1[7] + ' ' + row1[14]
tables[20].df.iloc[12, 4] = row1[0] + row1[1]
tables[20].df.iloc[12, 5] = row1[8] + ' ' + row1[15]
tables[20].df.iloc[12, 6] = row1[9]
tables[20].df.iloc[12, 7] = row1[10] + ' ' + row1[11] + ' ' + row1[12]

row2 = tables[20].df.iloc[13, 0].split()
tables[20].df.iloc[13, 0] = row2[0]
tables[20].df.iloc[13, 1] = row2[1]
tables[20].df.iloc[13, 2] = row2[2] + ' ' + row2[9]
tables[20].df.iloc[13, 3] = row2[3] + ' ' + row2[10]
tables[20].df.iloc[13, 4] = row1[2] + row1[3]
tables[20].df.iloc[13, 5] = row2[4] + ' ' + row2[11]
tables[20].df.iloc[13, 6] = row2[5]
tables[20].df.iloc[13, 7] = row2[6] + ' ' + row2[7] + ' ' + row2[8]

# TABLE 22 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[21].df.iloc[1, :6] = tables[21].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[21].df.iloc[4, 4].split()[:12]
for i in range(2, 8):
    tables[21].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 22 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[21].df.iloc[9, :6] = tables[19].df.iloc[9, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[21].df.iloc[16, 4].split()[:28]
for i in range(10, 24):
    tables[21].df.iloc[i, 4] = modes[2 * (i - 10)] + modes[2 * (i - 10) + 1]

# TABLE 23 SEM I
# Split "Sec Day Time Loc Mode Cap Exam Staff" into its respective column
tables[22].df.iloc[1, :8] = tables[22].df.iloc[1, 0].split()[:8]

row1 = tables[22].df.iloc[2, 0].split()
tables[22].df.iloc[2, 0] = row1[4]
tables[22].df.iloc[2, 1] = row1[5]
tables[22].df.iloc[2, 2] = row1[6] + ' ' + row1[13]
tables[22].df.iloc[2, 3] = row1[7] + ' ' + row1[14]
tables[22].df.iloc[2, 4] = row1[0] + row1[1]
tables[22].df.iloc[2, 5] = row1[8] + ' ' + row1[15]
tables[22].df.iloc[2, 6] = row1[9]
tables[22].df.iloc[2, 7] = row1[10] + ' ' + row1[11] + ' ' + row1[12]

row2 = tables[22].df.iloc[3, 0].split()
tables[22].df.iloc[3, 0] = row2[0]
tables[22].df.iloc[3, 1] = row2[1]
tables[22].df.iloc[3, 2] = row2[2] + ' ' + row2[9]
tables[22].df.iloc[3, 3] = row2[3] + ' ' + row2[10]
tables[22].df.iloc[3, 4] = row1[2] + row1[3]
tables[22].df.iloc[3, 5] = row2[4] + ' ' + row2[11]
tables[22].df.iloc[3, 6] = row2[5]
tables[22].df.iloc[3, 7] = row2[6] + ' ' + row2[7] + ' ' + row2[8]

# TABLE 23 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[22].df.iloc[5, :6] = tables[22].df.iloc[5, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[22].df.iloc[10, 4].split()[:20]
for i in range(6, 16):
    tables[22].df.iloc[i, 4] = modes[2 * (i - 6)] + modes[2 * (i - 6) + 1]

# TABLE 24 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[23].df.iloc[1, :6] = tables[23].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[23].df.iloc[6, 4].split()[:18]
for i in range(2, 11):
    tables[23].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 24 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[23].df.iloc[12, :6] = tables[23].df.iloc[12, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[23].df.iloc[17, 4].split()[:18]
for i in range(13, 22):
    tables[23].df.iloc[i, 4] = modes[2 * (i - 13)] + modes[2 * (i - 13) + 1]

# TABLE 25 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[24].df.iloc[1, :6] = tables[24].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[24].df.iloc[4, 4].split()[:10]
for i in range(2, 7):
    tables[24].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 25 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[24].df.iloc[8, :6] = tables[24].df.iloc[8, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[24].df.iloc[11, 4].split()[:10]
for i in range(9, 14):
    tables[24].df.iloc[i, 4] = modes[2 * (i - 9)] + modes[2 * (i - 9) + 1]

# TABLE 26 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[25].df.iloc[1, :6] = tables[25].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[25].df.iloc[6, 4].split()[:18]
for i in range(2, 11):
    tables[25].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 26 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[25].df.iloc[12, :6] = tables[25].df.iloc[12, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[25].df.iloc[16, 4].split()[:16]
for i in range(13, 21):
    tables[25].df.iloc[i, 4] = modes[2 * (i - 13)] + modes[2 * (i - 13) + 1]

# TABLE 27 SEM I
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[26].df.iloc[1, :6] = tables[26].df.iloc[1, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[26].df.iloc[4, 4].split()[:10]
for i in range(2, 7):
    tables[25].df.iloc[i, 4] = modes[2 * (i - 2)] + modes[2 * (i - 2) + 1]

# TABLE 27 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[26].df.iloc[8, :6] = tables[26].df.iloc[8, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[26].df.iloc[10, 4].split()[:6]
for i in range(9, 12):
    tables[26].df.iloc[i, 4] = modes[2 * (i - 9)] + modes[2 * (i - 9) + 1]

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
