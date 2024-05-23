import gspread
from google.auth.transport.requests import AuthorizedSession

# Configuração da API do Google Sheets
gc = gspread.service_account(filename='path/to/your/service-account-file.json')
spreadsheet_id = 'your-google-sheets-id'
sheet_name = 'Sheet1'  # Nome da aba do Google Sheets

# Autenticação e acesso ao Google Sheets
sh = gc.open_by_key(spreadsheet_id)
worksheet = sh.worksheet(sheet_name)

# Autenticação no BigQuery
bq_session = AuthorizedSession(credentials)

# Consulta SQL para obter os dados do BigQuery
query = f'SELECT * FROM `{project_id}.{dataset_id}.{table_id}`'
df = pd.read_gbq(query, project_id=project_id, credentials=credentials)

# Carregar os dados no Google Sheets
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

print('Dados carregados com sucesso no Google Sheets.')
