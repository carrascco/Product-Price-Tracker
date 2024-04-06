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

# def obtener_precio3(url):
   
#     driver = webdriver.Edge(options=options) 
#     driver.get(url)
#     try:
#         tamano_element = WebDriverWait(driver, 20).until(
#             EC.visibility_of_element_located((By.XPATH, '//div[@class="dropdown-input"]'))   
#         )
#         time.sleep(7.5)
#         tamano_element.click()
#     except:
#         print("No se pudo seleccionar el tamaño.")
        
#         driver.quit()
#         exit(1)
    

#     try:
#         parent_div = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, 'size_option_001013512219281   :eci'))
#     )

#         child_div = WebDriverWait(parent_div, 10).until(
#             EC.element_to_be_clickable((By.XPATH, './/div[@role="button"]'))
#         )
#         time.sleep(5)
#         child_div.click()
#     except:
#         print("No se pudo hacer clic en el elemento hijo del div padre.")
#         exit(1)
#     try:
#         precio_element = WebDriverWait(driver, 10).until(
#             EC.visibility_of_element_located((By.CLASS_NAME, 'price-unit--normal')))
#         precio = precio_element.text.strip()
#         return precio
#     except:
#         print("No se pudo encontrar el precio. 3") 
#         exit(1)
# from playwright.sync_api import sync_playwright
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


def obtener_precio32(url):
    with sync_playwright() as p:
        # Inicializa el navegador Edge en modo headless
        browser = p.firefox.launch()
        page = browser.new_page()

        # Abre la URL
        page.goto(url, wait_until='load')

        # try:
        #     # Espera y hace clic en el elemento desplegable de tamaño
        #     page.wait_for_selector('div.dropdown-input', timeout=20000)  # Espera hasta 20 segundos
        #     page.click('div.dropdown-input')

        # except Exception as e:
        #     print("No se pudo seleccionar el tamaño.", str(e))
        #     browser.close()
        #     exit(1)

        # try:
        #     # Espera a que el elemento hijo dentro del div padre sea clickeable y hace clic
        #     # Asegúrate de adaptar el selector al correcto, ya que Playwright maneja los selectores un poco diferente
        #     page.wait_for_selector('#size_option_001013512219281\\:eci', timeout=15000)
        #     page.click('#size_option_001013512219281\\:eci')

        # except Exception as e:
        #     print("No se pudo hacer clic en el elemento hijo del div padre.", str(e))
        #     browser.close()
        #     exit(1)
        valor_span = page.evaluate('''
        (() => {
            var dropdown = document.querySelector('.dropdown-input'); 
            if (dropdown) {
                dropdown.click();
            }

            // Espera un poco después del clic para que el DOM se actualice
            // NOTA: Esto no funcionará como se espera, ya que `setTimeout` no detiene la ejecución en `page.evaluate`
            // Se muestra aquí solo como un concepto; necesitarías manejar la espera de manera diferente.
            setTimeout(() => {}, 1000); // Esto NO funcionará como se espera en page.evaluate()

            var sizeOption = document.getElementById('size_option_001013512219281   :eci'); 
            if (sizeOption) {
                var child = sizeOption.querySelector('.size-element');
                if (child) {
                    child.click(); 
                }
            }

            var spanElement = document.querySelector('.product-detail-price'); 
            return spanElement ? spanElement.textContent : ''; // Devuelve el texto de spanElement o una cadena vacía si no se encuentra
        })();
    ''')
        

        print(valor_span)

        try:
            # Espera a que el elemento del precio sea visible y obtiene su texto
            precio_element = page.wait_for_selector('.price-unit--normal', timeout=10000)
            precio = precio_element.text_content().strip()
            browser.close()
            return precio

        except Exception as e:
            print("No se pudo encontrar el precio.", str(e))
            browser.close()
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
