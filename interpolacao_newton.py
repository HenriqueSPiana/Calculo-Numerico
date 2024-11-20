import requests
import matplotlib.pyplot as plt
import numpy as np




# a curva de interpolação de Newton apresentada no gráfico tem um comportamento bastante irregular e até mesmo estranho em algumas regiões. Isso se deve a algumas características do método de interpolação polinomial de Newton:
# Sensibilidade aos dados: O polinômio de Newton é muito sensível aos valores dos dados de entrada. Pequenas variações nos valores de temperatura podem causar grandes oscilações na curva interpolada.
# Efeito Runge: Quando os pontos de dados estão distribuídos de forma equidistante, o polinômio de Newton tende a apresentar oscilações indesejadas nas extremidades do intervalo, fenômeno conhecido como Efeito de Runge.
# Natureza global: O polinômio de Newton é um ajuste global, o que significa que qualquer alteração em um ponto de dados afeta todo o polinômio, resultando em oscilações e comportamentos inesperados.
# Esses fatores, combinados com a natureza irregular dos dados de temperatura, levaram ao surgimento dessa curva de interpolação bastante sinuosa e, em alguns trechos, até contraintuitiva.

# Substitua pela sua chave de API
api_key = 'a028c8064bc076acec15cb9c480538c6'  # Atualize a chave aqui

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

# Função para calcular as diferenças divididas de Newton
def diferenças_divididas(x, y):
    n = len(x)
    coef = np.array(y, dtype=float)  # Inicializa os coeficientes com os valores de y

    for j in range(1, n):
        for i in range(n-1, j-1, -1):
            coef[i] = (coef[i] - coef[i-1]) / (x[i] - x[i-j])

    return coef

# Função para calcular o polinômio de Newton em um ponto
def polinomio_newton(x, coef, x_values):
    n = len(coef)
    resultado = coef[n-1]
    for k in range(n-2, -1, -1):
        resultado = coef[k] + (x_values - x[k]) * resultado
    return resultado

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

    # Calcular as diferenças divididas de Newton
    coef = diferenças_divididas(x_values, y_values)

    # Gerando os valores interpolados usando o polinômio de Newton
    x_interp = np.linspace(0, len(horas)-1, 100)  # Gerando 100 pontos para suavizar
    y_interp = polinomio_newton(x_values, coef, x_interp)

    # Plotando os dados
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, 'o', label="Dados Reais")  # Pontos reais
    plt.plot(x_interp, y_interp, '-', label="Curva Interpolada (Newton)")  # Curva interpolada
    plt.xticks(x_values, horas, rotation=45)  # Exibindo as horas no eixo X
    plt.xlabel('Hora')
    plt.ylabel('Temperatura (°C)')
    plt.title('Temperatura ao Longo do Tempo (Interpolação Polinomial de Newton)')
    plt.legend()
    plt.grid(True)

    # Ajustando os limites do eixo y para um intervalo mais adequado
    min_temp = min(y_values)
    max_temp = max(y_values)
    plt.ylim(min_temp - 1, max_temp + 1)  # Ajustando os limites para o intervalo de temperaturas reais
    plt.tight_layout()
    plt.show()
else:
    print("Não foi possível coletar os dados corretamente.")
