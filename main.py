import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


global precio_global
global precio_anterior

global response
global precio1
global precio2
global precio3
global precio4

global urlLowest

options = Options()
options.headless = True

def obtener_precio1(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    precio_element = soup.find('span', {'id': 'product-price-35237'})
    if precio_element:
        precio = precio_element.text.strip()
        return precio
    else:
        print('No se pudo encontrar el precio. 1')
        exit(1)
    
def obtener_precio2(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    div_100ml = soup.find('div', string='100 ml')
    if div_100ml:
        
        precio_element = div_100ml.find_next('span', {'class': 'product-price__extended-content-units'})
        
        if precio_element:
            precio = precio_element.text.strip()
            precio = precio.split('/')[0].strip()
            return precio
    print('No se pudo encontrar el precio. 2')
    exit(1)

def obtener_precio3(url):

    driver = webdriver.Firefox(options=options) 
    driver.get(url)
    try:
        tamano_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="dropdown-input"]'))   
        )
        time.sleep(3.5)
        tamano_element.click()
    except:
        print("No se pudo seleccionar el tamaño.")
        
        driver.quit()
        exit(1)
    

    try:
        parent_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'size_option_001013512219281   :eci'))
    )

        child_div = WebDriverWait(parent_div, 10).until(
            EC.element_to_be_clickable((By.XPATH, './/div[@role="button"]'))
        )
        time.sleep(2)
        child_div.click()
    except:
        print("No se pudo hacer clic en el elemento hijo del div padre.")
        exit(1)
    try:
        precio_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'price-unit--normal')))
        precio = precio_element.text.strip()
        return precio
    except:
        print("No se pudo encontrar el precio. 3") 
        exit(1)

def obtener_precio4(url):

    driver = webdriver.Firefox(options=options)  # Necesitarás descargar el WebDriver correspondiente a tu navegador
    driver.get(url)
   
    try:
        precio_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'price-sales-standard'))
        )

        # Obtener el precio del elemento
        precio = precio_element.text.strip()

        # Imprimir el precio
        return precio
    except:
        print("No se pudo encontrar el precio. 4")
        exit(1)


def lowestPrice(price1,price2,price3,price4):
    global urlLowest
    lowest = min(price1, price2, price3, price4)
    if lowest == price1:
        urlLowest = url1
        return lowest
    if lowest == price2:
        urlLowest = url2
        return lowest
    if lowest == price3:
        urlLowest = url3
        return lowest
    
    urlLowest = url4
    return lowest

def comparar_precio(lowestActualPrice):
    global precio_anterior
    with open("precio", "r") as archivo:
        precio_anterior = archivo.read()
        if lowestActualPrice != float(precio_anterior):
            
            return True

def enviar_correo(nuevo_precio):
    remitente="miguelcdo10@gmail.com"

    mensaje = EmailMessage()
    mensaje['From'] = remitente
    mensaje['To'] = os.getenv('EMAIL_RECEIVER')
    mensaje['Subject'] = "¡Nuevo precio mínimo encontrado en el seguimiento de tu producto!"

    cuerpo_mensaje = f"El precio del producto ha cambiado. "
    cuerpo_mensaje += f"Antes costaba {precio_anterior} €...<br> "
    cuerpo_mensaje+= f"<b>¡El nuevo precio mínimo es: {nuevo_precio} €!</b>"
    cuerpo_mensaje += f"<br><br>Lo puedes encontrar en {urlLowest}"
    mensaje.set_content(cuerpo_mensaje, subtype='html') 

    smtp=smtplib.SMTP_SSL('smtp.gmail.com',465)
    smtp.ehlo()
    smtp.login(remitente, os.getenv('EMAIL_API'))
    smtp.sendmail(remitente, os.getenv('EMAIL_RECEIVER'), mensaje.as_string())
    smtp.close()

   

url1 = 'https://www.druni.es/coco-mademoiselle-chanel-eau-parfum-vaporizador'
url2='https://www.douglas.es/es/p/1000722295?variant=103896'
url3='https://www.elcorteingles.es/perfumeria/A18380039-chanel-coco-mademoiselle-eau-de-parfum-vaporizador/?parentCategoryId=997.4374515011&color=default'
url4='https://www.sephora.es/p/coco-mademoiselle---eau-de-parfum-vaporizador-92482.html?gad_source=1&gclid=Cj0KCQiA5rGuBhCnARIsAN11vgRn_rRsC3GfQUF-Y-XCmSPKB5YR1dVuaLx9boqL9p45g85GnIVumxMaAlM-EALw_wcB'






precio1=obtener_precio1(url1)
precio_str = precio1.replace('€', '').replace('\xa0', '').replace(',', '.')
precio1 = float(precio_str) 
precio2=obtener_precio2(url2)
numero = precio2.split('\xa0')[0].replace(',', '.')   
precio2 = float(numero)

precio3=obtener_precio3(url3)
numero = precio3.split()[0]  
precio3 = float(numero.replace(',', '.')) 

precio4=obtener_precio4(url4)
numero = precio4.split()[0]  
precio4 = float(numero.replace(',', '.'))  



lowest=lowestPrice(precio1,precio2,precio3,precio4)
if comparar_precio(lowest):
    print('El precio del producto ha cambiado.')
    with open("precio", "w") as archivo:
        archivo.write(str(lowest))
    enviar_correo(lowest)
    print('El nuevo precio del producto se ha guardado en el archivo "precio".')
else:
    print('El precio del producto no ha cambiado.')
