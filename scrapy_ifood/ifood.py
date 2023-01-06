from selenium import webdriver
from time import sleep

navegador = webdriver.Chrome('C:/workspace/scrapy_ifood/chromedriver.exe')

navegador.get('https://www.google.com/')
sleep(5)
elemento = navegador.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
sleep(5)
elemento.send_keys('selenium no python')
sleep(5)

#navegador.find_element_by_xpath('//*[@id="__next"]/section[2]/div/form/div/input').send_keys('rua São Francisco de Assis, 110 Cruz de Rebouças, Igarassu')

#sleep(5)

#navegador.find_element_by_xpath('//*[@id="__next"]/section[2]/div/form/button').click()

