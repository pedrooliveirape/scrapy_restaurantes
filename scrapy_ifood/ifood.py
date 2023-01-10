from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_csv('C:\workspace\scrapy_restaurantes\scrapy_ifood\lojas_ifood.csv', sep=';')
lojas_detalhes = []
rows = df.shape[0]

for i in range(1):
    nomeloja = df.iloc[i, 0]
    enderecoweb = df.iloc[i, 2]
    
    options = Options()
    options.add_argument('window-size=400,530')
    service = Service(ChromeDriverManager().install())

    navegador = webdriver.Chrome(service=service, options=options)
    navegador.get(f'{enderecoweb}')
