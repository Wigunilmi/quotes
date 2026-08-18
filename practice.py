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

#
#

# Assuming 'df' is already created (e.g., df = pd.DataFrame({'The quotes': text, 'Authors': authors}))

# Open an ExcelWriter session using 'openpyxl' so we can edit formatting/layout settings
with pd.ExcelWriter("output.xlsx", engine="openpyxl") as writer:
    
    # 1. Write the DataFrame to 'Sheet1' and hide row numbers (index=False)
    df.to_excel(writer, index=False, sheet_name="Sheet1")
    
    # 2. Access the actual worksheet tab object so Python can change column properties
    ws = writer.sheets["Sheet1"]
    
    # 3. Loop through each column name in your table (e.g., 'The quotes', then 'Authors')
    for column in df.columns:
        
        # .get_loc() gets column position (0, 1...). We add 1 because Excel starts at 1, not 0.
        col_index = df.columns.get_loc(column) + 1
        
        # Convert index number to an Excel letter (e.g., 1 -> 'A', 2 -> 'B')
        column_letter = get_column_letter(col_index)

        # Find the max character count between the data rows and the column header itself
        max_len = max(
            df[column].astype(str).map(len).max(), # Convert all values to text -> get length of each -> grab highest
            len(str(column))                        # Get character length of the column header name
        )

        # Apply calculated width to the Excel column letter, adding +2 spaces for extra visual padding
        ws.column_dimensions[column_letter].width = max_len + 2