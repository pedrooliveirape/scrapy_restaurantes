from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_csv('C:\Workspace\scrapy_restaurantes\lojas_detalhes_bruto_nao_apagar.csv', sep=';')
rows = df.shape[0]
pizza_df = pd.DataFrame(columns=['NomeLoja','EnderecoWeb'])
lista_pizza = []

for i in range(rows):
    lista_grupos = df.iloc[i, 7]
    lista_grupos = lista_grupos.replace("'",' ').replace('[','').replace(']','').replace(',','')
    lista_grupos = lista_grupos.split()
    #print(type(lista_grupos))
    for l in lista_grupos:
        lista_temp = []
        if 'pizza' in l:
            lista_temp.append(df.iloc[i, 0])
            lista_temp.append(df.iloc[i, 1])
            lista_pizza.append(lista_temp)

pizza_df = pizza_df.append(lista_pizza, ignore_index=False)
pizza_df.to_csv('lojas_pizza.csv', index=False, sep=';')
