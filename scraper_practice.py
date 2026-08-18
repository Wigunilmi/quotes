
# 1. Bring in our tools (requests for downloading, bs4 for parsing, csv for saving)
import requests 
from bs4 import BeautifulSoup
import csv

# 2. Set the target URL and download the raw HTML of the page
url = 'https://books.toscrape.com/'
response = requests.get(url)

# 3. Feed the downloaded page text into the BeautifulSoup parser
soup = BeautifulSoup(response.text, 'html.parser')

# 4. Tell the parser to find all the repeating "business card" boxes on the page
books = soup.find_all('article', class_='product_pod')

# 5. Open a new CSV file safely, preventing blank rows and weird character crashes
with open('leads.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # 6. Write the top header row first so the columns have names
    writer.writerow(["Book Title"])
    
    # 7. Loop through every single book box we found in step 4
    for book in books:
        
        # a. Look inside the current box, find the <h3>, then find the <a> tag inside it
        link_tag = book.find('h3').find('a')
        
        # b. Extract the full title from the hidden attribute, ignoring the visible cut-off text
        extracted_title = link_tag['title'] 
        
        # c. Write that extracted text into the CSV as a brand new row
        writer.writerow([extracted_title])

# 8. Print diagnostics to the terminal so we know what happened behind the scenes
print("Status Code:", response.status_code)
print("Total books found:", len(books))