from lxml import html
import requests



# Define the start and end of the XPath range
start = 2
end = 24

# Initialize an empty list to store the URLs
urls = []

for j in range(1, 50):
    base_url = "https://www.arabam.com/ikinci-el/motosiklet?page="+str(j)
    page = requests.get(base_url)
    tree = html.fromstring(page.content)
    for i in range(start, end + 1):
        # Construct the XPath expression
        xpath_expr = f'/html/body/div[2]/div[2]/div[3]/div/div[2]/div[2]/div[2]/table/tbody/tr[{i}]/td[2]/a/@href'

        # Use the XPath expression to find the link
        result = tree.xpath(xpath_expr)

        # If a link was found, add it to the list
        if result:
            urls.append(result[0])

# save the url list to a file txt file
with open('urls.txt', 'w') as f:
    for url in urls:
        f.write(url + '\n')

urls = ['https://www.arabam.com' + url for url in urls]
with open('urls.txt', 'w') as f:
    for url in urls:
        f.write(url + '\n')