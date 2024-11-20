import requests
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d  # Importando para interpolação linear
from scipy import interpolate  # Para interpolação polinomial

api_key = 'a028c8064bc076acec15cb9c480538c6'  
# Este código realiza a coleta de dados de temperatura de uma cidade específica, utilizando a API do OpenWeatherMap, 
# e então aplica a interpolação polinomial cúbica para suavizar a curva de temperatura ao longo do tempo.
# Essa abordagem utiliza a interpolação polinomial cúbica, que tende a gerar uma curva mais suave e regular do que a interpolação polinomial de Newton apresentada anteriormente. 
# Essa técnica é comumente utilizada para suavizar e interpolar dados com variações bruscas, como os dados de temperatura.


# Função para coletar dados da API
def coleta_dados(cidade, chave_api):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={chave_api}&units=metric'
    response = requests.get(url)
    dados = response.json()

    # Verificando o código de erro na resposta
    if dados.get("cod") != "200":
        print(f"Erro na API: {dados.get('message')}")
        return [], []  # Retorna listas vazias se houver erro

    # Se a chave 'list' existe, prosseguir com o processamento dos dados
    horas = [item['dt_txt'] for item in dados['list']]  # Extraindo as horas
    temperaturas = [item['main']['temp'] for item in dados['list']]  # Extraindo as temperaturas
    return horas, temperaturas

# Coletando os dados
cidade = "São Paulo"  # Defina a cidade desejada
horas, temperaturas = coleta_dados(cidade, api_key)

# Verificando se as temperaturas estão variando
if horas and temperaturas:  # Verifica se as listas não estão vazias
    print("Temperaturas coletadas:")
    for hora, temp in zip(horas, temperaturas):
        print(f"{hora}: {temp}°C")

    # Convertendo as horas para valores numéricos (em horas)
    x_values = np.arange(len(horas))  # Índices para as horas
    y_values = temperaturas  # Temperaturas

    # Interpolação Polinomial de grau 3
    poly_func = interpolate.interp1d(x_values, y_values, kind='cubic')  # Interpolação cúbica
    x_interp = np.linspace(0, len(horas)-1, 100)  # Gerando 100 pontos para suavizar
    y_interp = poly_func(x_interp)

    # Plotando os dados
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, 'o', label="Dados Reais")  # Pontos reais
    plt.plot(x_interp, y_interp, '-', label="Curva Interpolada (Polinomial)")  # Curva interpolada
    plt.xticks(x_values, horas, rotation=45)  # Exibindo as horas no eixo X
    plt.xlabel('Hora')
    plt.ylabel('Temperatura (°C)')
    plt.title('Temperatura ao Longo do Tempo (Interpolação Polinomial)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("Não foi possível coletar os dados corretamente.")
