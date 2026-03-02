import requests  # Para fazer requisições HTTP
import base64    # Necessário porque a API do GitHub exige o conteúdo em Base64


class ManipulaRepositorios:
    def __init__(self, username):
        # Nome do usuário dono do repositório
        self.username = username
        
        # URL base da API do GitHub
        self.api_base_url = 'https://api.github.com'
        
        # Token de autenticação (melhor usar variável de ambiente)
        self.access_token = 'seu_token'
        
        # Cabeçalhos da requisição
        self.headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'X-GitHub-Api-Version': '2022-11-28'
        }

    def criar_repo(self, nome_repo):
        """
        Cria um novo repositório na conta autenticada.
        Endpoint: POST /user/repos
        """
        data = {
            'name': nome_repo,
            'description': 'Repositório com dados de algumas empresas',
            'private': False
        }

        # Envia requisição POST para criar o repositório
        response = requests.post(
            f"{self.api_base_url}/user/repos",
            json=data,
            headers=self.headers
        )

        print(f'status_code criação do repositorio: {response.status_code}')

    def add_arquivo(self, nome_repo, nome_arquivo, caminho_arquivo):
        """
        Adiciona um arquivo ao repositório.
        A API exige que o conteúdo seja enviado em Base64.
        Endpoint: PUT /repos/{owner}/{repo}/contents/{path}
        """

        # Abre o arquivo em modo binário
        with open(caminho_arquivo, 'rb') as file:
            file_content = file.read()

        # Converte o conteúdo para Base64
        encoded_content = base64.b64encode(file_content)

        # URL para adicionar conteúdo
        url = f"{self.api_base_url}/repos/{self.username}/{nome_repo}/contents/{nome_arquivo}"

        data = {
            'message': 'Adicionando arquivo',  # mensagem de commit
            'content': encoded_content.decode('utf-8')  # conteúdo convertido para string
        }

        # Envia requisição PUT para criar o arquivo
        response = requests.put(url, json=data, headers=self.headers)

        print(f'status_code adição do arquivo: {response.status_code}')


# =========================
# EXECUÇÃO
# =========================

novo_repo = ManipulaRepositorios('leonardonnovaes')

nome_repo = 'linguagens-repositorios-empresas'

# Cria o repositório
novo_repo.criar_repo(nome_repo)

# Adiciona arquivos CSV
novo_repo.add_arquivo(nome_repo, 'linguagens_amazon.csv', 'dados/linguagens_amazon.csv')
novo_repo.add_arquivo(nome_repo, 'linguagens_netflix.csv', 'dados/linguagens_netflix.csv')
novo_repo.add_arquivo(nome_repo, 'linguagens_spotify.csv', 'dados/linguagens_spotify.csv')