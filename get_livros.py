from bs4 import BeautifulSoup
import requests
import wget
import os.path

TIMEOUT = 1.5
url = 'https://docs.google.com/spreadsheets/d/1HzdumNltTj2SHmCv3SRdoub8SvpIEn75fa4Q23x0keU/htmlview'
url_default = 'https://link.springer.com/'

def extract_title(content):
    soup = BeautifulSoup(content, 'lxml')
    tag = soup.find('title', text=True) # Tenta encontrar a primeira tag 'title' preenchida

    return tag.string.split('|')[0].strip() if tag else None # retorna o valor dentro da tag

def extract_links(content):
    soup = BeautifulSoup(content, 'lxml')
    links = [] # Cria uma lista que não permite valores repetidos 

    for tag in soup.find_all('div','softmerge-inner'): # Pega todas as tags 'a' que contenham o 'href' preenchido    
        if tag.text.startswith('http://') or tag.text.startswith('https://'): # Se o 'href' começa com http então é link válido            
            links.append(tag.text) # Adiciona a tag na lista

    return links

def extract_link(content):    
    soup = BeautifulSoup(content, 'lxml')
    
    link = soup.find('a', {'data-track-action': 'Book download - pdf'})
    return link['href']

try:
    special_char = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    
    folder = input('Digite o caminho da pasta a ser armazenado: ')
    folder = folder.replace('\\', '/')

    content = requests.get(url, timeout = TIMEOUT).text
    links = extract_links(content)

    for i, cont in enumerate(links):
        try:
            content = requests.get(cont, timeout = TIMEOUT).text
            link = extract_link(content)
            url_completo = url_default + link        

            title = extract_title(content)   

            for char in special_char:
                title = title.replace(char, '')

            filename = folder +'/' + title + '.pdf'    

            if not os.path.isfile(filename):
                print(f'\n {i} - {title}')
                print(filename)
                
                '''
                wget mostra barra de progresso ao fazer o download
                e já grava o arquivo direto no local informado
                '''
                wget.download(url_completo, filename)

                '''
                requests não mostra nada ao realizar o downlaod
                e é necessário gravar manualmente o arquivo
                '''
                # r = requests.get(url_completo).content

                # f = open(filename, 'wb')
                # f.write(r)
                # f.close
        except Exception as err:
            print(f'\nnão foi possível fazer o download, link sem botão download!! \n {err}')
    
    print()
    print()
    print('-' * 40)
    print('FINALIZADO COM SUCESSO'.center(40))
    print('-' * 40)

except Exception as err:
    print(err)
