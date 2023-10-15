import pdfplumber
import re

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

for match in matches:
    print(f"Course Code: {match[0]}")
    print(f"Course Name: {match[1]}\n")