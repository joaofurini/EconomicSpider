import requests as req #BIBLIOTECA PARA LIDAR COM REQUESTS, IMPORTEI AS REQ POR COSTUME, PODERIA SER USADO COMO REQUESTS
from bs4 import BeautifulSoup #BIBLIOTECA PARA PARSEAR AS PAGINAS QUE RECEBEREMOS
from data import Facebook #DADOS SIGILOSOS DE LOGIN E SENHA PARA O FACEBOOK
from fbchat import Client #BIBLIOTECA PARA ENVIAR MENSAGENS NO FACEBOOK
from fbchat.models import *
import pandas as pd #BIBLIOTECA PARA FORMATACAO DE DADOS
from checagem import Checagem #CLASSE PARA CHECAR RESPOSTAS

#METODO PARA FAZER O LOGIN
def login():
	#INSTANCIA DA CLASSE FACEBOOK
	fb = Facebook()
	#CRIANDO O CLIENTE COM O USUARIO E SENHA DO FACEBOOK
	client = Client(fb.getUser(), fb.getPass())
	return client

def searchUserId(userName, client):
	#PESQUISAR O NOME DO CLIENTE
	users = client.searchForUsers(userName)
	#USER RECEBE O PRIMEIRO NOME CORRESPONDENTE NA LISTA
	user = users[0]
	return user

def sendMessage(message, client, user):
	#ENVIANDO A MENSAGEM, OBTENDO O ID DO USUARIO DESTINO USANDO O USER.UID
	client.send(Message(text= message), thread_id= user.uid, thread_type=ThreadType.USER)


def fetchNews():
	#CRIANDO A URL DA PAGINA QUE PEGAREMOS AS NOTICIAS
	url = 'https://www.infomoney.com.br'
	#USANDO A BIBLIOTECA REQUESTS PARA BUSCAR A URL
	page = req.get(url)
	#USANDO A BIBLIOTECA BEAUTIFULSOUP PARA PARSEAR A PAGINA RECEBIDA
	soup = BeautifulSoup(page.text, 'lxml')
	#BUSCANDO TODOS OS ITENS DA CLASSE ITEM ORDER 
	news = soup.findAll(class_='item order')
	newsList = []
	links = []
	continua = True 

	while continua:
		#CHAMANDO A FUNCAO PARA FAZER O LOGIN
		client = login()
		#DEFININDO O NOEM DO USUARIO QUE BUSCAREMOS O ID
		userName = input('Digite para quem deseja enviar as noticias: ')
		#CHAMANDO A FUNCAO PARA RETORNAR O USUARIO DESEJADO
		user = searchUserId(userName, client)
		#PARA CADA NEW EM NEWS FAZER O SEGUINTE
		for new in news:
			#NOTICIA RECEBE O 'A' EM FORMA DE TEXTO --NOTICIA--
			noticia = new.find('a').text
			#ADICIONA A NOTICIA NA LISTA DE NOTICIAS
			newsList.append(noticia)
			#CHAMANDO A FUNCAO PARA ENVIAR A MENSAGEM PARA O DESTINATARIO
			sendMessage(noticia, client, user)
			#CRIANDO O LINK DAS NOTICIAS
			link ='https://www.infomoney.com.br'+new.find('a')['href']
			#ADICIONANDO O LINK NA LISTA DE LINKS
			links.append(link)
			#CHAMANDO A FUNCAO PARA ENVIAR O LINK PARA O DESTINATARIO
			sendMessage(link, client, user)

		#CHECAR SE O USUARIO DESEJA ENVIAR AS NOTICIAS OBTIDAS PARA MAIS ALGUEM 
		#FOI FEITO DESSA FORMA POIS O FACEBOOK NAO ACEITA QUE ENVIE MENSAGEM PARA MAIS DE UMA PESSOA DE UMA VEZ
		#TENDO QUE SER FEITO O LOGOUT E LOGIN NOVAMENTE ANTES DE ENVIAR PARA OUTRA PESSOA
		resposta = input('Deseja enviar para mais alguem? s/n')
		checaResposta = Checagem()
		checaResposta.check(resposta)
		if resposta == 's':
			client.logout()
		else:
			continua = False

	#USANDO O PANDAS PARA CRIAR O FORMATO DO ARQUIVO 
	df = pd.DataFrame({
		"News": newsList,
		"Links": links
		})
	#ENVIANDO AS NOTICIAS PARA UM ARQUIVO CSV 
	df.to_csv('Noticias')
	print(df)


#CHAMADA DO METODO PRINCIPAL		
fetchNews()







