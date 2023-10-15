import pdfplumber
import re

with pdfplumber.open("COURSE_CATALOG_IJA.pdf") as pdf:
    extracted_text = ''

    for page in pdf.pages:
        text = page.extract_text()
        extracted_text += text

extracted_text.replace("\n", " ").replace("03-OCT-23 11:09 AM", "")

pattern = r"Course Code : (\w+)\s+((?:(?!Course Code :).)*)Course Name : (.+?)\n"
matches = re.findall(pattern, extracted_text, re.DOTALL)

for match in matches:
    course_code, extra_text, course_name = match
    print(f"Course Code: {course_code}\nCourse Name: {course_name}\n")
