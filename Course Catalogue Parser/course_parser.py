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
    .replace("Academic Session 2023/2024 ", "")

extracted_text = re.sub(r'Couse Synopsis : .*?Campus', 'Campus', extracted_text, flags=re.DOTALL)

pattern = r"Course Code : ([A-Z]{3}\d{4})[\s\S]+?Course Name : (.+?)\d"
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

# TABLE 6 SEM II
# Split "Sec Day Time Loc Mode Cap" into its respective column
tables[5].df.iloc[5, :6] = tables[5].df.iloc[5, 0].split()[:6]

# Split column "mode" into its respective row
modes = tables[5].df.iloc[11, 4].split()[:24]
for i in range(6, 18):
    tables[5].df.iloc[i, 4] = modes[2 * (i - 6)] + modes[2 * (i - 6) + 1]

# Display each table under its corresponding course code
for i, match in enumerate(matches):
    print(f"{i + 1}. Course Code: {match[0]}")
    print(f"Course Name: {match[1]}\n")

    if i < len(tables):
        table = tables[i]
        table.df = table.df.map(lambda x: x.replace('\n', ' '))
        display(table.df)
