import pandas as pd

df = pd.read_csv("C:\workspace\scrapy_restaurantes\Planilha sem título - teste.csv", sep=',')
df.head(5)

cardapio = df.iloc[0, 2]
cardapio = cardapio[1:-1]

produtos = []
inicio = 0
fim = 0
soma = 0
cont = 0

for i in cardapio:
    if soma == 0 and i != '[':
        cont += 1
        continue
    if i == '[':
        if soma == 0:
            inicio = cont
        soma += 1
    if i == ']':
        soma -= 1
        if soma == 0:
            fim = cont+1
            palavra = cardapio[inicio:fim]
            produtos.append(palavra)
    cont += 1

    cont = 0
for i in produtos:
    gr = i[1:-1]
    produtos[cont] = gr
    cont += 1

    virgula = 0
cont = 0
dic_cardapio = {}

for l in produtos:
    pos = l.find("',")
    fim = pos + 1
    prod = l[1:pos]
    itens = l[pos+3:]
    dic_cardapio[prod] = itens
    cont += 1

for k,v in dic_cardapio.items():
    if v[0] == '[':
        valor = v[1:-1]

        grupos = []
        inicio = 0
        fim = 0
        soma = 0
        cont = 0

        for i in valor:
            if soma == 0 and i != '[':
                cont += 1
                continue
            if i == '[':
                if soma == 0:
                    inicio = cont
                soma += 1
            if i == ']':
                soma -= 1
                if soma == 0:
                    fim = cont+1
                    palavra = valor[inicio:fim]
                    grupos.append(palavra)
            cont += 1
        
        dic_cardapio[k] = grupos


for k,lista_grupos in dic_cardapio.items():
    if type(lista_grupos) is list:
        grupo = []        
        for g in lista_grupos:
            dic_itens = {}
            itens_grupo = g[1:-1]
            itens_preco = itens_grupo.split(', ')
            for item in range(0,len(itens_preco),2):
                dic_itens[itens_preco[item].strip("'")] = itens_preco[item+1].strip("'")
            grupo.append(dic_itens)
        dic_cardapio[k] = grupo

for k,v in dic_cardapio.items():
  if type(v) is list:
    nova_list_grupo = []
    for i in v:
      item = i
      novo_dict_interno = {}
      for chave,valor in item.items():
        try:
          resposta = valor.replace('+ R$','').replace(',','.')
          try:
            resposta = float(resposta)
          except:
            resposta = float(0)
        except:
          resposta = float(0)
        novo_dict_interno[chave] = resposta
      nova_list_grupo.append(novo_dict_interno)
    dic_cardapio[k] = nova_list_grupo
  else:
    try:
      resposta = v.replace('+ R$','').replace(',','.')
      try:
        resposta = float(resposta)
      except:
        resposta = float(0)
    except:
      try:
        resposta = float(v)
      except:
        resposta = float(0)
    dic_cardapio[k] = resposta

cont = 0
lista_print = []
for k, v in dic_cardapio.items():
    if type(v) is list:
        lista_print.append('')
        lista_print.append(f'[{k}] ---------- [VVVVVVVVVVV]')
        for p,i in enumerate(v):
            lista_print.append(f'          --- GRUPO {p+1} ---')
            for chave, valor in i.items():
                lista_print.append(f'          {chave} ---------- [{valor}]')
    else:
        lista_print.append('')
        lista_print.append(f'[{k}] ---------- [{v}]')
    cont += 1

    	
with open('C:\Workspace\scrapy_restaurantes\cardapio_boa_pizza.txt', 'w') as arquivo:
    arquivo.write("\n".join(lista_print))

