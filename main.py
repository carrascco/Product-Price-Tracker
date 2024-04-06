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

from playwright.async_api import async_playwright
import asyncio

async def obtener_precio3(url):
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await page.goto(url)

        # Asegúrate de que el dropdown está presente y haz clic en él
        await page.wait_for_selector('.dropdown-input', timeout=15000)
        await page.click('.dropdown-input')

        # Espera a que el elemento con el ID aparezca. Dado que el ID contiene espacios y caracteres especiales,
        # y `page.waitForSelector` no es adecuado para IDs con espacios, usaremos `page.evaluate` para esperar y hacer clic.
        # Reemplazamos la espera y el clic directos por un bloque evaluate que maneje la espera internamente.
        valor_span = await page.evaluate('''
            async () => {
                const sizeOption = document.getElementById('size_option_001013512219281   :eci');
                if (!sizeOption) {
                    throw new Error('sizeOption not found');
                }
                const child = sizeOption.querySelector('.size-element');
                if (!child) {
                    throw new Error('Child size-element not found');
                }
                child.click();

                // Espera para asegurar que los clics han tenido efecto y el DOM se ha actualizado
                await new Promise(resolve => setTimeout(resolve, 1000)); // Espera 1 segundo

                const spanElement = document.querySelector('.product-detail-price');
                return spanElement ? spanElement.textContent : null; // Devuelve el texto de spanElement o null si no se encuentra
            }
        ''')

        if valor_span:
            print(f"Valor de spanElement: {valor_span}")
        else:
            print("spanElement no encontrado o sin texto.")

        await browser.close()
        return valor_span



async def obtener_precio4(url):
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await page.goto(url)
       
        try:
            # Espera hasta que el elemento con el precio sea visible y obtén su texto
            precio_element = await page.wait_for_selector('.price-sales-standard', state='visible', timeout=10000)
            precio = await precio_element.text_content()

            # Limpiar y retornar el precio
            return precio.strip()
        except Exception as e:
            print(f"No se pudo encontrar el precio. 4: {e}")
            return None


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
url3='https://www.elcorteingles.es/perfumeria/A18380039-chanel-coco-mademoiselle-eau-de-parfum-vaporizador/'
url4='https://www.sephora.es/p/coco-mademoiselle---eau-de-parfum-vaporizador-92482.html?gad_source=1&gclid=Cj0KCQiA5rGuBhCnARIsAN11vgRn_rRsC3GfQUF-Y-XCmSPKB5YR1dVuaLx9boqL9p45g85GnIVumxMaAlM-EALw_wcB'






precio1=obtener_precio1(url1)
precio_str = precio1.replace('€', '').replace('\xa0', '').replace(',', '.')
precio1 = float(precio_str) 
precio2=obtener_precio2(url2)
numero = precio2.split('\xa0')[0].replace(',', '.')   
precio2 = float(numero)

# precio3=obtener_precio3(url3)
precio3=asyncio.run(obtener_precio3(url3))
numero = precio3.split()[0]  
precio3 = float(numero.replace(',', '.')) 

precio4=asyncio.run(obtener_precio4(url4))
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
