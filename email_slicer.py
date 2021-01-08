import re
import pandas as pd

txt = """
Jack has sent an invoice email to john.d@yahoo.com 
by using his email id jack.small@gmail.com and he also shared
a copy to his boss rosy.blue@amazon.co.uk on the cc part.
"""

# Scraping emails
find_email = re.findall(r'[\w\.-]+@[\w\.-]+', txt)

df = pd.DataFrame(columns=["EmailId", "Domain"])
email = ""
domain = ""

for i in find_email:
    email = i
    domain = re.findall('@+\S+[.in|.com|.uk]', i)[0]
    df = df.append({'EmailId': email, 'Domain': domain}, ignore_index=True)

print(df.head())