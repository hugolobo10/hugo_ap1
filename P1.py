import pandas as pd
df = pd.read_csv("ncr_ride_bookings.csv")

# 1 - Quantas corridas estão com Status da Corrida como Completada ("Completed") no dataset? 
completadas = df[df['Booking Status'] == "Completed"]
("Quantidade de corridas completadas:", len(completadas))


# 2 - Qual a proporção em relação ao total de corridas?
total = len(df)
proporcao = len(completadas) / total
("Proporção de completadas:", proporcao)


# 3 - Calcule a média e mediana da Distância percorrida por cada Tipo de veículo.
media_por_veiculo = df.groupby('Vehicle Type')['Ride Distance'].mean()
mediana_por_veiculo = df.groupby('Vehicle Type')['Ride Distance'].median()

("Média por tipo de veículo:")
(media_por_veiculo)
("Mediana por tipo de veículo:")
(mediana_por_veiculo)


# 4 - Qual o Metodo de Pagamento mais utilizado pelas bicicletas ("Bike") ?
bikes = df[df['Vehicle Type'] == 'Bike']
mais_usado = bikes['Payment Method'].value_counts().idxmax()
print("Método de pagamento mais usado para Bike:", mais_usado)


# 5 - Faca um merge com ncr_ride_regions.xlsx pela coluna ("Pickup Location") para pegar as regioes das corrifas.
# e verifique qual a Regiao com o maior Valor da corrida?
df_regioes = pd.read_excel("ncr_ride_regioes.xlsx")
df_merge = pd.merge(df, df_regioes, on="Pickup Location", how = "left")

valor_por_regiao = df_merge.groupby('Region')['Booking Value'].sum()
regiao_top = valor_por_regiao.idxmax()



# 6 - O IPEA disponibiliza uma API pública com diversas séries econômicas. 
# Para encontrar a série de interesse, é necessário primeiro acessar o endpoint de metadados.
# Acesse o endpoint de metadados: "http://www.ipeadata.gov.br/api/odata4/Metadados"
# e filtre para encontrar as séries da Fipe relacionadas a venda de imoveis (“venda”).
# Dica Técnica, filtre atraves das coluna FNTSIGLA: df["FNTSIGLA"].str.contains() 
# e depois SERNOME: df["SERNOME"].str.contains() 
import requests
url_meta = "http://www.ipeadata.gov.br/api/odata4/Metadados"
resp = requests.get(url_meta)
meta = resp.json()

df_meta = pd.DataFrame(meta['value'])


df_fipe = df_meta[df_meta['FNTSIGLA'].str.contains("FIPE", na=False)]
df_venda = df_fipe[df_fipe['SERNOME'].str.contains("venda", case=False, na=False)]

(df_venda[['SERCODIGO', 'SERNOME']])
codigo = "SERCODIGO	SERNOME"  
url_valores = f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{codigo}')"
resp_val = requests.get(url_valores)
valores = resp_val.json()
df_valores = pd.DataFrame(valores['value'])

df_valores['DATA'] = pd.to_datetime(df_valores['DATA'])
print(df_valores.head())



# Descubra qual é o código da série correspondente.
# Usando o código encontrado, acesse a API de valores: f"http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{CODIGO_ENCONTRADO}')"
# e construa um DataFrame pandas com as datas (DATA) e os valores (VALVALOR).
# Converta a coluna de datas para o formato adequado (pd.to_datetime())

# 7 -  Monte um gráfico de linha mostrando a evolução das vendas ao longo do tempo.
# Dica: você pode usar a biblioteca matplotlib para gerar o gráfico.
import matplotlib.pyplot as plt

plt.plot(df_valores['DATA'], df_valores['VALVALOR'])
plt.title("Evolução das Vendas de Imóveis")
plt.xlabel("Data")
plt.ylabel("Valor")
plt.show()




# 8 - Crie o grafico do bitcoin (ticker: "btc") atraves da api preco-diversos
# Pegue o periodo compreendido entre 2001 a 2025
# Monte um gráfico de linha mostrando a evolução do preco de fechamento
# import requests
# token = ""
# headers = {'Authorization': 'Bearer {}'.format(token)}
# params = {
# 'ticker': 'ibov',
# 'data_ini': '2023-01-01',
# 'data_fim': '2023-09-01'
# }
# response = requests.get('https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params, headers=headers)




# 9 - Você tem acesso à API do Laboratório de Finanças, que fornece dados do Planilhão em formato JSON. 
# A autenticação é feita via JWT Token no cabeçalho da requisição.
# Acesse a API no endpoint: https://laboratoriodefinancas.com/api/v1/planilhao
# passando como parâmetro a data (por exemplo, "2025-09-23").
# Construa um DataFrame pandas a partir dos dados recebidos.
# Selecione a empresa do setor de "tecnologia" que apresenta o maior ROC (Return on Capital) nessa data.
# Exiba o ticker da empresa, setor e o valor do ROC correspondente.
# import requests
# token = ""
# headers = {'Authorization': 'JWT {}'.format(token)}
# params = {
# 'data_base': '2023-01-02'
# }
# response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMzg5NzAyLCJpYXQiOjE3NTg3OTc3MDIsImp0aSI6ImE3MmY3ZjE3NmE5MjRhMzNiZjFjNjRhZTQ4MjQwOWJkIiwidXNlcl9pZCI6IjkzIn0.xL7LxWS7-5fZMUsryAvRva7NAs7" \
"qE6hhgkqWDDPR-Gw"
headers = {'Authorization': f'JWT {token}'}
params = {'data_base': '2023-01-02'}

resp = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao', params=params, headers=headers)
df_planilhao = pd.DataFrame(resp.json())

df_tec = df_planilhao[df_planilhao['setor'] == 'tecnologia']
empresa_top = df_tec.loc[df_tec['ROC'].idxmax(), ['ticker', 'setor', 'ROC']]
(empresa_top)



# 10 - A API do Laboratório de Finanças fornece informações de balanços patrimoniais de empresas listadas na B3.
# Acesse o endpoint: https://laboratoriodefinancas.com/api/v1/balanco
# usando a empresa Gerdau ("GGBR4") e o período 2025/2º trimestre (ano_tri = "20252T").
# O retorno da API contém uma chave "balanco", que é uma lista com diversas contas do balanço.
# Localize dentro dessa lista a conta cuja descrição é “Ativo Total” e "Lucro Liquido".
# Calcule o Return on Assets que é dados pela formula: ROA = Lucro Liquido / Ativo Totais

# import requests
# token = ""
# headers = {'Authorization': 'JWT {}'.format(token)}
# params = {'ticker': 'PETR4', 
#           'ano_tri': '20231T'
#           }
# response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMzg5NzAyLCJpYXQiOjE3NTg3OTc3MDIsImp0aSI6ImE3MmY3ZjE3NmE5MjRhMzNiZjFjNjRhZTQ4MjQwOWJkIiwidXNlcl9pZCI6IjkzIn0.xL7LxWS7-5fZMUsryAvRva7NAs7" \
"qE6hhgkqWDDPR-Gw")
headers = {'Authorization': 'JWT {}'.format(token)}
#####
params = {'ticker': 'GGBR4', 'ano_tri': '20231T'}
resp = requests.get('https://laboratoriodefinancas.com/api/v1/balanco', params=params, headers=headers)
dados = resp.json()['balanco']

df_balanco = pd.DataFrame(dados)

ativo_total = df_balanco.loc[df_balanco['descricao'] == 'Ativo Total', 'valor'].iloc[0]
lucro_liquido = df_balanco.loc[df_balanco['descricao'] == 'Lucro Liquido', 'valor'].iloc[0]

ROA = lucro_liquido / ativo_total
print("ROA:", ROA)

