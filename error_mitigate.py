import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)

page = requests.get('http://finance.yahoo.com', verify=False)

print(page.content)
