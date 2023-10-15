import pdfplumber
import re
import camelot
from IPython.display import display

tables = camelot.read_pdf('https://or.ump.edu.my/or/CourseCatalog/COURSE_CATALOG_IJA.pdf', pages='345-384')

for i in range(len(tables)):
    tables[i].df = tables[i].df.replace('\\n', ' ', regex=True)
    display(tables[i].df)

with pdfplumber.open("COURSE_CATALOG_IJA.pdf") as pdf:
    extracted_text = ''

    for page in pdf.pages:
        text = page.extract_text()
        extracted_text += text

extracted_text = extracted_text \
    .replace("\n", " ") \
    .replace("03-OCT-23 11:09 AM", "") \
    .replace("Pre-Requisite : NO ", "") \
    .replace("Remarks : NO ", "")

pattern = r"Course Code : ([A-Z]{3}\d{4})[\s\S]+?Course Name : (.+?)\d"
matches = re.findall(pattern, extracted_text)
counter = 1

for match in matches:
    print(f"{counter}. Course Code: {match[0]}")
    print(f"Course Name: {match[1]}\n")
    counter += 1
