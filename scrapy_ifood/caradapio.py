import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup

def pegalinksprod(site):
    lista_html = site.findAll('a', {'data-test-id': 'dish-card-test-id'})#<h3 class="dish-card__description"
    lista_links = []

    for i in lista_html:
        link = i.get('href')
        link = 'https://www.ifood.com.br'+link 
        lista_links.append(link)
    return lista_links


options = Options()
options.add_argument('window-size=400,700')
#options.add_argument('--headless')
service = Service(ChromeDriverManager().install())

enderecoweb = 'https://www.ifood.com.br/delivery/igarassu-pe/pizza-em-casa-jardim-boa-sorte/ec6a3997-c0d3-4598-9e0c-4c43b4fee1f6'
navegador = webdriver.Chrome(service=service, options=options)
navegador.get(enderecoweb)

page_content = navegador.page_source

site = BeautifulSoup(page_content, 'html.parser')

produtos_links = pegalinksprod(site)

