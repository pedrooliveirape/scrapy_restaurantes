from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

def passofor(rows):
    inicio_li = []
    fim_li = []

    for i in range(0,rows,20):
        inicio_li.append(i)
        fim_li.append(i+20)
    fim_li[-1] = rows
    return [inicio_li, fim_li]

def sobre(navegador):
    navegador.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div[1]/div/header[2]/div[1]/div/div[2]/button').click()
    c = 0
    while c < 10:
        sleep(1)
        page_content = navegador.page_source
        site = BeautifulSoup(page_content, 'html.parser')
        if site.findAll('p', {'class': 'merchant-details-about__info-data'}):
            conteudo_endereco = site.findAll('p', {'class': 'merchant-details-about__info-data'})

            endereco = conteudo_endereco[0].text
            cidade = conteudo_endereco[1].text
            cep =  conteudo_endereco[2].text[5:]
            cnpj = conteudo_endereco[3].text[6:]
            c = 10
        else:
            c += 1
        
    return [endereco,cidade,cep,cnpj]

def horario(navegador):
    navegador.find_element(By.ID, 'marmita-tab1-1').click()
    c = 0
    while c < 10:
        sleep(1)
        page_content = navegador.page_source
        site = BeautifulSoup(page_content, 'html.parser')
        if site.findAll('div', {'class': 'merchant-details-schedule__day'}):
            dias_horarios = site.findAll('div', {'class': 'merchant-details-schedule__day'})

            list_dias_horarios = []

            for dia_horario in dias_horarios:
                dia = dia_horario.find('span', {'class': 'merchant-details-schedule__day-title-text'}).text
                horario = dia_horario.find('span', {'class': 'merchant-details-schedule__day-schedule'}).text
                list_dias_horarios.append(f'{dia} - {horario}')
            c = 10
        else:
            c += 1
    
    return list_dias_horarios

def grupos(navegador):
    c = 0
    while c < 10:
        sleep(1)
        page_content = navegador.page_source
        site = BeautifulSoup(page_content, 'html.parser')

        if site.findAll('h2', {'class': 'restaurant-menu-group__title'}):
            grupos_cardapio = site.findAll('h2', {'class': 'restaurant-menu-group__title'})
            list_grupos = []
            for grupo in grupos_cardapio:
                nome_grupo = grupo.text
                list_grupos.append(nome_grupo.lower())
            c = 10
        else:
            c += 1

    return list_grupos


df = pd.read_csv('C:\workspace\scrapy_restaurantes\scrapy_ifood\lojas_ifood.csv', sep=';')
dados = pd.DataFrame(columns=['NomeLoja','EnderecoWeb','Endereco','Cidade','CEP','CNPJ','Horario','GrupoCardapio'])
lojas_detalhes = []
rows = df.shape[0]
cont = 0
#trange = passofor(rows)

#for c in range(len(trange[0])):    
for i in range(rows):
    nomeloja = df.iloc[i, 0]
    enderecoweb = df.iloc[i, 2]
    
    try: # Tentando configurar a página da loja para abertura
        options = Options()
        options.add_argument('window-size=400,530')
        options.add_argument('--headless')
        service = Service(ChromeDriverManager().install())

        navegador = webdriver.Chrome(service=service, options=options)
    # Abrindo a página
        navegador.get(f'{enderecoweb}')
        
        try: # Tentando scrapy dos GRUPOS DO CARDÁPIO
            lista_de_grupos = grupos(navegador)
        except:
            lista_de_grupos = ['-']

    # Abrindo o VER MAIS
        try: # Tentando scrapy do SOBRE
            lista_sobre = sobre(navegador)
        except:
            lista_sobre = ['-','-','-','-']
        
        try: #Tentando scrapy do HORÁRIO
            list_dias = horario(navegador)
        except:
            list_dias = ['-']

    # Criando a lista bibliotecas para o Data Frame    
        lojas_detalhes.append({'NomeLoja': nomeloja,'EnderecoWeb': enderecoweb,'Endereco': lista_sobre[0],'Cidade': lista_sobre[1],'CEP': lista_sobre[2],'CNPJ': lista_sobre[3],'Horario': list_dias,'GrupoCardapio': lista_de_grupos})
        navegador.close()
    except:
        lojas_detalhes.append([nomeloja,enderecoweb,'-','-','-','-','-','-'])
    cont += 1
    if cont == 5:
        try:
            dados = dados.append(lojas_detalhes, ignore_index=False)
            dados.to_csv('lojas_detalhes_teste.csv', index=False, sep=';')
            lojas_detalhes = []
            cont = 0
        except:
            cont = 0
# Fim do FOR por loja
dados = dados.append(lojas_detalhes, ignore_index=False)
dados.to_csv('lojas_detalhes_teste.csv', index=False, sep=';')
# Fim do FOR por range
