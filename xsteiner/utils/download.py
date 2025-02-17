import requests
from pathlib import Path

def check_url_validity(url):
    filename = Path(url).name
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == requests.status_codes.codes['ok']:
            print(f'✅ {filename} está disponível.')
        else:
            print(f'❌ {filename} não encontrado (Status: {response.status_code}).')
    except requests.RequestException as e:
        print(f'⚠ Erro ao verificar {filename}: {e}')

def download(url):

    response = requests.get(url)
    if response.status_code == requests.status_codes['ok']:
        data = response.content
        return data
    else:
        raise FileNotFoundError('')

def save(content, filename, folder):
    local = Path(folder, filename)
    with open(local, 'wb') as file:
        file.write(content)
    return True