import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

url = 'https://apps02.ump.edu.my/semakan/Matric_Card.jsp?std_id=CB20033'
base_url = 'https://apps02.ump.edu.my/semakan/'

response = requests.get(url)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('tr', bgcolor='#CCCCCC')
    img_tag = soup.find('img', id='cropbox')

    for row in rows:
        if 'NAMA' in row.get_text():
            name = row.find_all('td')[1].get_text(strip=True).split(": ")[1]
            print("Name:", name)

    if img_tag:

        img_url = base_url + img_tag['src']
        img_response = requests.get(img_url)

        if img_response.status_code == 200:
            image_data = img_response.content
            image = Image.open(BytesIO(image_data))
            image.show()
        else:
            print('Failed to retrieve the image. Status code:', img_response.status_code)

    else:
        print('Image tag not found on the page.')

else:
    print('Failed to retrieve the web page. Status code:', response.status_code)
