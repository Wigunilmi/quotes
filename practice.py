import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl.utils import get_column_letter
#connect with the site through url link
url='https://quotes.toscrape.com./'

response=requests.get(url)

#searching for boxes that have title or whatever
#<div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
soup=BeautifulSoup(response.text,'html.parser')
quotes=soup.find_all('div',class_='quote')
print(len(quotes))

text=[]
authors=[]
for quote in quotes:
    mytag=quote.find('span',class_='text')
    qtext=mytag.text
    text.append(qtext)
    myta=quote.find('small',class_='author')
    qauthor=myta.text
    authors.append(qauthor)
    
df=pd.DataFrame({
    'The quotes':text,
    'Authors': authors
})
with pd.ExcelWriter("output.xlsx", engine="openpyxl") as writer:
    

    df.to_excel(writer, index=False, sheet_name="Sheet1")
    ws = writer.sheets["Sheet1"]
    for column in df.columns:
        col_index = df.columns.get_loc(column) + 1
        column_letter = get_column_letter(col_index)

        max_len = max(
            df[column].astype(str).map(len).max(),
            len(str(column))
        )

        ws.column_dimensions[column_letter].width = max_len + 2
