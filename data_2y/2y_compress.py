import pandas as pd
import os

pasta_script = os.path.dirname(os.path.abspath(__file__))

mapeamento_arquivos = {
    'USD.csv': 'USD',
    'EUR.csv': 'EUR',
    'GBP.csv': 'GBP',
    'JPY.csv': 'JPY',
    'CHINA.csv': 'CHINA',
    'CHF.csv': 'CHF',
    'AUD.csv': 'AUD',
    'CAD.csv': 'CAD',
    'KRW.csv': 'KRW',
    'SEK.csv': 'SEK',
    'INDIA.csv': 'INDIA',
    'BRL.csv': 'BRL'
}

#tirei mexico e noruega pq os dados estavam incompletos

lista_dfs = []

print("A iniciar o processamento com alinhamento estrito por Ano-Mês...")

for nome_arquivo, ticker in mapeamento_arquivos.items():
    caminho_completo = os.path.join(pasta_script, nome_arquivo)
    
    if os.path.exists(caminho_completo):
        df = pd.read_csv(caminho_completo)
        
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
        df = df[['Date', 'Price']]
        
        nome_coluna_target = f'RATE_2Y_{ticker}'
        df = df.rename(columns={'Price': nome_coluna_target})
        df.set_index('Date', inplace=True)
        df.index = df.index.to_period('M')
        
        df = df[~df.index.duplicated(keep='last')]
        
        lista_dfs.append(df)
        print(f"{ticker} processado com sucesso.")
    else:
        print(f"Aviso: O ficheiro '{nome_arquivo}' não foi encontrado.")

if len(lista_dfs) > 0:
    df_rates_2y = pd.concat(lista_dfs, axis=1, join='outer')
    
    df_rates_2y.sort_index(inplace=True)

    df_rates_2y.index = df_rates_2y.index.to_timestamp()
    
    caminho_saida = os.path.join(pasta_script, 'rates_2y.csv')
    df_rates_2y.to_csv(caminho_saida)
    
    print("\n--- Processo Concluído com Sucesso ---")
    print(f"O ficheiro unificado e alinhado foi gerado em: {caminho_saida}")
else:
    print("\nErro: Nenhum objeto válido para concatenar.")