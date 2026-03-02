import requests
import base64

class ManipulaRepositorios:
    def __init__(self, username):
        self.username = username
        self.api_base_url = 'https://api.github.com'
        self.access_token = 'seu_token'
        self.headers = headers = {
        'Authorization': 'Bearer ' + self.access_token,  # espaço depois de Bearer
        'X-GitHub-Api-Version': '2022-11-28'}
    def criar_repo(self, nome_repo):
        data = {
            'name': nome_repo,
            'description': 'Repositório com dados de algumas empresas',
            'private': False
        }
        response = requests.post(f"{self.api_base_url}/user/repos", json=data, headers=self.headers)
        print(f'status_code criação do repositorio: {response.status_code}')
    def add_arquivo(self, nome_repo, nome_arquivo, caminho_arquivo):
        with open(caminho_arquivo, 'rb') as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content)

        url = f"{self.api_base_url}/repos/{self.username}/{nome_repo}/contents/{nome_arquivo}"
        data = {
            'message': 'Adicionando arquivo',
            'content': encoded_content.decode('utf-8')
        }
        response = requests.put(url, json=data, headers=self.headers)
        print(f'status_code adição do arquivo: {response.status_code}')

novo_repo = ManipulaRepositorios('leonardonnovaes')

nome_repo = 'linguagens-repositorios-empresas'
novo_repo.criar_repo(nome_repo)

novo_repo.add_arquivo(nome_repo, 'linguagens_amazon.csv', 'dados/linguagens_amazon.csv')
novo_repo.add_arquivo(nome_repo, 'linguagens_netflix.csv', 'dados/linguagens_netflix.csv')
novo_repo.add_arquivo(nome_repo, 'linguagens_spotify.csv', 'dados/linguagens_spotify.csv')