from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

def sobre(page_content):
    site = BeautifulSoup(page_content, 'html.parser')

    conteudo_endereco = site.findAll('p', {'class': 'merchant-details-about__info-data'})

    endereco = conteudo_endereco[0].text
    cidade = conteudo_endereco[1].text
    cep =  conteudo_endereco[2].text[5:]
    cnpj = conteudo_endereco[3].text[6:]
    
    return [endereco,cidade,cep,cnpj]

def horario(page_content):
    site = BeautifulSoup(page_content, 'html.parser')

    dias_horarios = site.findAll('div', {'class': 'merchant-details-schedule__day'})

    list_dias_horarios = []

    for dia_horario in dias_horarios:
        dia = dia_horario.find('span', {'class': 'merchant-details-schedule__day-title-text'}).text
        horario = dia_horario.find('span', {'class': 'merchant-details-schedule__day-schedule'}).text
        list_dias_horarios.append(f'{dia} - {horario}')
    
    return list_dias_horarios


df = pd.read_csv('C:\workspace\scrapy_restaurantes\scrapy_ifood\lojas_ifood.csv', sep=';')
lojas_detalhes = []
rows = df.shape[0]

for i in range(rows):
    nomeloja = df.iloc[i, 0]
    enderecoweb = df.iloc[i, 2]
    
    options = Options()
    options.add_argument('window-size=400,530')
    options.add_argument('--headless')
    service = Service(ChromeDriverManager().install())

    navegador = webdriver.Chrome(service=service, options=options)
    navegador.get(f'{enderecoweb}')

    # Grupo cardápio

    page_content = navegador.page_source

    site = BeautifulSoup(page_content, 'html.parser')

    grupos_cardapio = site.findAll('h2', {'class': 'restaurant-menu-group__title'})

    list_grupos = []

    for grupo in grupos_cardapio:
        nome_grupo = grupo.text
        list_grupos.append(nome_grupo.lower())

    # Ver Mais

    sleep(4)
    if navegador.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div[1]/div/header[2]/div[1]/div/div[2]/button'):
        navegador.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div[1]/div/header[2]/div[1]/div/div[2]/button').click()
        sleep(2)
        try:
            lista_sobre = sobre(navegador.page_source)
        except:
            lista_sobre = ['-','-','-','-']
        # Horario
        if navegador.find_element(By.ID, 'marmita-tab1-1'):
            navegador.find_element(By.ID, 'marmita-tab1-1').click()
            sleep(2)
            try:
                list_dias = horario(navegador.page_source)
            except:
                list_dias = ['-']
        else:
            list_dias = ['-']
    else:
        sleep(6)
        if navegador.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div[1]/div/header[2]/div[1]/div/div[2]/button'):
            navegador.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div[1]/div/header[2]/div[1]/div/div[2]/button').click()
            sleep(2)
            try:
                lista_sobre = sobre(navegador.page_source)
            except:
                lista_sobre = ['-','-','-','-']
            # Horario
            if navegador.find_element(By.ID, 'marmita-tab1-1'):
                navegador.find_element(By.ID, 'marmita-tab1-1').click()
                sleep(2)
                try:
                    list_dias = horario(navegador.page_source)
                except:
                    list_dias = ['-']
            else:
                list_dias = ['-']

    # Fim Ver Mais
    
    lojas_detalhes.append([nomeloja,enderecoweb,lista_sobre[0],lista_sobre[1],lista_sobre[2],lista_sobre[3],list_dias,list_grupos])

    navegador.close()

dados = pd.DataFrame(lojas_detalhes, columns=['NomeLoja','EnderecoWeb','Endereco','Cidade','CEP','CNPJ','Horario','GrupoCardapio'])
dados.to_csv('lojas_detalhes.csv', index=False, sep=';')
