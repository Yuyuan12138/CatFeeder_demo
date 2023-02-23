import requests

img_src = 'https://img2.bemfa.com/56f71a52764261ad9220aa61dd823f1d-a1250fc1ecf0c3aaf458c4ee0bc88b66-1675922959.jpg'
response = requests.get(img_src)
with open("C:/Users/13595/Desktop/cat_4.jpg",'wb') as file_obj:
    file_obj.write(response.content)
