import requests
from bs4 import BeautifulSoup

url = 'https://apps02.ump.edu.my/semakan/Matric_Card.jsp?std_id=CB20033'

response = requests.get(url)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr', bgcolor='#CCCCCC')

    for row in rows:
        if 'NAMA' in row.get_text():
            name = row.find_all('td')[1].get_text(strip=True).split(": ")[1]
            print("Name:", name)


else:
    print('Failed to retrieve the web page. Status code:', response.status_code)
