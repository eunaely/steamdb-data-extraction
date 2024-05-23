import requests
from bs4 import BeautifulSoup
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Configurações do BigQuery
credentials = service_account.Credentials.from_service_account_file('path/to/your/service-account-file.json')
project_id = 'your-gcp-project-id'
dataset_id = 'your_dataset_id'
table_id = 'your_table_id'

# URL da SteamDB para vendas
url = 'https://steamdb.info/sales/'

# Requisição HTTP para obter a página
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extração dos dados (ajuste conforme a estrutura da página)
data = []
for row in soup.select('table#sales-table tr'):
    cols = row.find_all('td')
    if len(cols) > 0:
        data.append({
            'name': cols[0].get_text(strip=True),
            'discount': cols[1].get_text(strip=True),
            'price': cols[2].get_text(strip=True),
            'cut': cols[3].get_text(strip=True)
        })

# Transformar os dados em DataFrame
df = pd.DataFrame(data)

# Carregar os dados no BigQuery
client = bigquery.Client(credentials=credentials, project=project_id)
table_ref = client.dataset(dataset_id).table(table_id)
job = client.load_table_from_dataframe(df, table_ref)
job.result()

print(f'Loaded {job.output_rows} rows into {dataset_id}:{table_id}.')
