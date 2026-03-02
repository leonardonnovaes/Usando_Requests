import requests  # Biblioteca para fazer requisições HTTP
import pandas as pd  # Biblioteca para manipulação de dados (DataFrame)
from math import ceil  # Função para arredondar números para cima


class DadosRepositorios:
    def __init__(self, owner):
        # Nome do usuário/organização no GitHub (ex: 'amzn', 'netflix')
        self.owner = owner
        
        # URL base da API do GitHub
        self.api_base_url = 'https://api.github.com'
        
        # Token de autenticação (melhor usar variável de ambiente em produção)
        self.access_token = 'seu_Token'
        
        # Headers da requisição (necessário para autenticação e versão da API)
        self.headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'X-GitHub-Api-Version': '2022-11-28'
        }

    def lista_repositorios(self):
        """
        Retorna uma lista com todos os repositórios públicos do owner.
        Cada posição da lista representa uma página retornada pela API.
        """
        repos_list = []

        # Primeiro request para descobrir quantos repositórios públicos existem
        response = requests.get(f'https://api.github.com/users/{self.owner}')
        
        # A API retorna no máximo 30 repositórios por página (default)
        # Então calculamos quantas páginas serão necessárias
        num_pages = ceil(response.json()['public_repos'] / 30)

        # Loop para percorrer todas as páginas
        for page_num in range(1, num_pages + 1):
            try:
                # URL da página específica
                url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'
                
                # Faz requisição autenticada
                response = requests.get(url, headers=self.headers)
                
                # Adiciona o JSON retornado (lista de repositórios da página)
                repos_list.append(response.json())
            
            except:
                # Em caso de erro, adiciona None para manter estrutura
                repos_list.append(None)

        return repos_list

    def nomes_repos(self, repos_list):
        """
        Extrai apenas os nomes dos repositórios da lista de páginas.
        """
        repo_names = []
        
        for page in repos_list:
            for repo in page:
                try:
                    # Pega o campo 'name' de cada repositório
                    repo_names.append(repo['name'])
                except:
                    pass
        
        return repo_names

    def nomes_linguagens(self, repos_list):
        """
        Extrai a linguagem principal de cada repositório.
        """
        repo_languages = []
        
        for page in repos_list:
            for repo in page:
                try:
                    # Campo 'language' indica a principal linguagem usada
                    repo_languages.append(repo['language'])
                except:
                    pass
        
        return repo_languages

    def cria_df_linguagnes(self):
        """
        Cria um DataFrame contendo:
        - Nome do repositório
        - Linguagem principal
        """
        # Obtém todos os repositórios
        repositorios = self.lista_repositorios()
        
        # Extrai nomes
        nomes = self.nomes_repos(repositorios)
        
        # Extrai linguagens
        linguagens = self.nomes_linguagens(repositorios)

        # Cria DataFrame vazio
        dados = pd.DataFrame()
        
        # Adiciona colunas
        dados['repository_name'] = nomes
        dados['linguagens'] = linguagens
        
        return dados
    

# ===============================
# Criando objetos para empresas
# ===============================

# Amazon (usuário oficial no GitHub)
amazon_rep = DadosRepositorios('amzn')
ling_mais_usadas_amzn = amazon_rep.cria_df_linguagnes()

# Netflix
netflix_rep = DadosRepositorios('netflix')
ling_mais_usadas_netflix = netflix_rep.cria_df_linguagnes()

# Spotify
spotify_rep = DadosRepositorios('spotify')
ling_mais_usadas_spotify = spotify_rep.cria_df_linguagnes()

# ===============================
# Salvando os dados em CSV
# ===============================

# Salva cada DataFrame em um arquivo CSV
ling_mais_usadas_amzn.to_csv('dados/linguagens_amazon.csv')
ling_mais_usadas_netflix.to_csv('dados/linguagens_netflix.csv')
ling_mais_usadas_spotify.to_csv('dados/linguagens_spotify.csv')