
  #! python3
from bs4 import BeautifulSoup
import requests
import json
import tweepy #este modulo hay que instalarlo para correr el bot
import time

#twitter emogis
dinero = '💵'
sube = '📤'
baja = '📥'
reloj = '🕓'
dolar = '💲'
sacoDinero = '💰'
fecha = '🗓'
estadisticas = '📊'
# Authenticate to Twitter
auth = tweepy.OAuthHandler("ADlyvU5OGsujVvPB97T9Vzux3", "dsubK4g0a2JGDzGkZ1geuSK1V1g7MfD2kwTU0MTYRoMAWToGKM")
auth.set_access_token("833044968977682433-wWbzZR42Gy8FdXjK3DmXL2c8RmDBOqc", "30nv0153yX0o1qECobJhcKhez8dMm99tx4feNlLSfcudp")

# Create API object
api = tweepy.API(auth)

historicoToday = [234,590]
historicoBCV = [234,590]

def getOficial(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser') #contenido html de la web
    elementosSoup = soup.find_all('strong') #buscar elementos span con la clase nombre-equipo
    return elementosSoup

def getParalelo(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    elementosSoup = soup.find_all('p')
    dolarToday = (json.loads(elementosSoup[0].text))
    return dolarToday
  
def principe():
      
    #hora actual
    hora = str(time.strftime("%H:%M")) #Formato de 24 horas
    fecha = str(time.strftime("%d/%m/%y"))
    if hora == '13:05' or hora == '17:05':
      dolarOficial = getOficial('http://www.bcv.org.ve/tasas-informativas-sistema-bancario')
      dolarParalelo = getParalelo('https://s3.amazonaws.com/dolartoday/data.json')
      dolar = dolarParalelo['USD']
      dolarBCV = float(dolar['sicad2'])
      dolarToday = float(dolar['dolartoday'])
      historicoToday.append(dolarToday)
      historicoToday.pop(0)
      historicoBCV.append(dolarToday)
      historicoBCV.pop(0)
      statusBCV = ''
      statusToday = ''
      if historicoToday[1] > historicoToday[0]:
            statusToday = sube
      elif historicoToday[1] == historicoToday[0]:
            statusToday = ''
      else:
            statusToday = baja
      
      if historicoBCV[1] > historicoBCV[0]:
            statusBCV = sube
      elif historicoToday[1] == historicoToday[0]:
            statusBCV = ''
      else:
            statusBCV = baja
    
      dolarTodayPretty = "{:,}".format(dolarToday).replace(',','~').replace('.',',').replace('~','.')
      dolarBCVpretty = "{:,}".format(dolarBCV).replace(',','~').replace('.',',').replace('~','.')

      
     
      try:
        api.update_status(f"Actualizacion 📊\n \n🗓 {fecha}\n🕓 {hora}\n💵 Dolartoday: Bs. {dolarTodayPretty} {statusToday}\n💰 Banco Central: Bs. {dolarBCVpretty} {statusBCV}\n")
        print('[+]Estado de Twitter Publicado  Satisfactoriamente')
      except tweepy.TweepError as error:
        if error.api_code == 187:
          # Do something special
          print('Estado de twitter Duplicado')
        else:
          raise error
    else:
          print(f'[-]Hora: {hora} Todavia no es la hora correcta para publicar')
    time.sleep(60) #6 horas en segundos

while True:
      principe()
#Buscar por atributo: 
#soup.find_all("a", attrs={"class": "sister"})
#soup.find_all(id='link2')

