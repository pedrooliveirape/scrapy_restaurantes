import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup

def pegalinksprod(site):
    lista_html = site.findAll('a', {'data-test-id': 'dish-card-test-id'})
    lista_produtos = []

    for i in lista_html:
        lista_info = []
        link = i.get('href')
        link = 'https://www.ifood.com.br'+link
        nomeproduto = i.find('h3', {'class':'dish-card__description'}).text
        lista_info = [link,nomeproduto]
        lista_produtos.append(lista_info)
    return lista_produtos

def abrirproduto(link, nomeproduto):
    options = Options()
    options.add_argument('window-size=400,700')
    options.add_argument('--headless')
    service = Service(ChromeDriverManager().install())

    enderecoweb = link
    navegador = webdriver.Chrome(service=service, options=options)
    navegador.get(enderecoweb)

    page_content = navegador.page_source

    site = BeautifulSoup(page_content, 'html.parser')

    navegador.close()

    nomeproduto = nomeproduto

    if site.find('section', {'class': 'garnish-choices__list'}):
        list_garnish_choices = site.findAll('section', {'class': 'garnish-choices__list'})
        lista_itens = []
        for l in list_garnish_choices:
            content_garnish_choices = l.findAll('label', {'class': 'garnish-choices__label'})
            itens = []
            lista_itens.append(itens)
            for i in content_garnish_choices:
                label_garnish_choices = i
                try:
                    nomeitem = label_garnish_choices.p.contents[0]
                except:
                    nomeitem = '-'
                #try:
                #    detalhesitem = label_garnish_choices.find('span', {'class': 'garnish-choices__option-details'}).text
                #except:
                #    detalhesitem = '-'
                try:
                    precoitem = label_garnish_choices.find('span', {'class': 'garnish-choices__option-price'}).text
                except:
                    precoitem = '-'
                itens.append(nomeitem)
                itens.append(precoitem)
        precoitensproduto = lista_itens
    else:
        #try:
        #    detalhesproduto = site.find('p', {'class': 'dish-content__container dish-content__details'}).text
        #except:
        #    detalhesproduto = '-'
        try:
            precoitensproduto = site.find('div', {'class': 'dish-price'}).text
        except:
            precoitensproduto = '-'
    return [nomeproduto,precoitensproduto]

def lojacardapio(enderecoweb):
    options = Options()
    options.add_argument('window-size=400,700')
    options.add_argument('--headless')
    service = Service(ChromeDriverManager().install())

    #endweb = 'https://www.ifood.com.br/delivery/abreu-e-lima-pe/turma-da-pizza-caetes-ii/c847fcf9-4227-4c28-89df-517e66d44a8b'
    endweb = enderecoweb
    navegador = webdriver.Chrome(service=service, options=options)
    navegador.get(endweb)

    page_content = navegador.page_source

    site = BeautifulSoup(page_content, 'html.parser')

    produtos_links = pegalinksprod(site)

    navegador.close()

    lista_produtos_itens = []

    for i in produtos_links:
        sair = False
        while sair is False: 
            resposta = input('\033[0;30;47m'+f'ABRIR O PRODUTO [{i[1]}]? DIGITE S OU N:'+'\033[0;0m'+' ')
            if resposta == 's' or resposta == 'S':
                produto = abrirproduto(i[0],i[1])
                lista_produtos_itens.append(produto)
                sair = True
            elif resposta == 'n' or resposta == 'N':
                res2 = input('\033[0;31;43m'+'IGNORAR ESTE PRODUTO! CONFIRMAR? DIGITE S OU N:'+'\033[0;0m'+' ').lower()
                if res2 == 's':
                    sair = True


    return lista_produtos_itens


df_lojas_pizza = pd.read_csv('C:\Workspace\scrapy_restaurantes\lojas_pizza.csv', sep=';')
df = pd.DataFrame(columns=['NomeLoja','EnderecoWeb','Cardapio'])
rows = df_lojas_pizza.shape[0]

for i in range(rows):
    print(df_lojas_pizza.iloc[i, 0])
    nomerestaurante = df_lojas_pizza.iloc[i, 0]
    restauranteweb = df_lojas_pizza.iloc[i, 1]
    restaurante_cardapio = lojacardapio(restauranteweb)
    linha = df.shape[0]
    df.loc[linha] = [nomerestaurante,restauranteweb,restaurante_cardapio]
    df.to_csv('pizzarias_cardapio.csv', index=False, sep=';')

df.drop_duplicates(subset ="EnderecoWeb", keep = False, inplace = True)
df.to_csv('pizzarias_cardapio.csv', index=False, sep=';')
