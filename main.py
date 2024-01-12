import bs4
from bs4 import BeautifulSoup
from requests.exceptions import ChunkedEncodingError
import requests
from datetime import datetime
import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import threading
import json
from unidecode import unidecode

driver = webdriver.Firefox()
url = 'https://www.linkedin.com/'
driver.get(url)

# Encontrar el campo de formulario por su nombre, ID, selector CSS, Xpath u otro criterio
campo_nombre = driver.find_element(By.NAME,"session_key")
campo_nombre.clear()
campo_nombre.send_keys("sebtionkomo@gmail.com")

campo_contrasena = driver.find_element(By.NAME,"session_password")
campo_contrasena.clear()
campo_contrasena.send_keys("Alexander51600@")

campo_contrasena.send_keys(Keys.RETURN)
time.sleep(15)

# driver.get('https://www.linkedin.com/in/maycol-alexander-canaveri-265a66285/')
driver.get('https://www.linkedin.com/in/arnoldhuete/')
time.sleep(5)

soup = BeautifulSoup(driver.page_source,'html.parser')
sections = soup.find_all("section")

profile_data = {
    "Profile":{
        "name":"",
        "profileAction":"",
        "profileDetails":[]
    },
    "Acerca_De":{
        "description":"",
        "aptitudes":""
    },
    "Experiencia":[],
    "Educacion":{
        "title":"",
        "description":"",
        "year":""
    },
    "Licencia_Y_Certificacion":[],
    "Conocimientos_Y_Aptitudes":[],
    "Idiomas":[],
}

#Profile-Section
profile = sections[2]
name = (profile.find("h1", class_="text-heading-xlarge inline t-24 v-align-middle break-words")).text
profile_data["Profile"]["name"] = name
data_sugestion = (profile.find("div",class_="text-body-medium break-words")).get_text(strip = True)
profile_data["Profile"]["profileAction"] = data_sugestion
otherData = (profile.find("ul",class_="pv-text-details__right-panel")).find_all("span")
for i in otherData:
    profile_data["Profile"]["profileDetails"].append(i.get_text(strip = True))

#Activiti-Section
# activity = sections[4]
# profile_data["Actividad"].append("None")

#AcercaDe-Section
acercaDe = sections[5]
description = (acercaDe.find("div",class_="display-flex ph5 pv3")).get_text(strip=True)
profile_data["Acerca_De"]["description"] = description
aptitudPrincipal = (acercaDe.find("div",class_="display-flex align-items-center t-14 t-normal")).text
profile_data["Acerca_De"]["aptitudes"] = aptitudPrincipal

#EXP-Section
exp = sections[6]
if exp.find("a",class_="optional-action-target-wrapper artdeco-button artdeco-button--tertiary artdeco-button--standard artdeco-button--2 artdeco-button--muted inline-flex justify-center full-width align-items-center artdeco-button--fluid"):
    span_class_name = "pvs-navigation__text"
    span_xpath = f"//span[@class='{span_class_name}']"
    span_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, span_xpath)))
    span_element.click()
    time.sleep(5)
    soupN_Element =  BeautifulSoup(driver.page_source,"html.parser")
    expEl = soupN_Element.find_all("div",class_="display-flex align-items-center mr1 t-bold")
    for i in expEl:
        profile_data["Experiencia"].append(i.get_text(strip=True))
    driver.back()

time.sleep(5)

#Educacion_Section
educacion = sections[7]
title_des = (educacion.find("a",class_="optional-action-target-wrapper display-flex flex-column full-width")).find_all("span")
profile_data["Educacion"]["title"] = title_des[0].get_text(strip=True)
profile_data["Educacion"]["description"] = title_des[1].get_text(strip=True)
profile_data["Educacion"]["year"] = title_des[2].get_text(strip=True)

#Licencia_Y_Certificacion 
license_Sec = sections[8]
if license_Sec.find("a",class_="optional-action-target-wrapper artdeco-button artdeco-button--tertiary artdeco-button--standard artdeco-button--2 artdeco-button--muted inline-flex justify-center full-width align-items-center artdeco-button--fluid"):
    elemento_a = driver.find_element(By.ID,"navigation-index-see-all-licenses-and-certifications")
    elemento_a.click()

    time.sleep(5)
    soupN_Element =  BeautifulSoup(driver.page_source,"html.parser")
    expEl = soupN_Element.find_all("div",class_="display-flex align-items-center mr1 hoverable-link-text t-bold")
    for i in expEl:
        profile_data["Licencia_Y_Certificacion"].append(i.get_text(strip=True))
    driver.back()

#Conocimientos y aptitudes
conociminentoYap = sections[9]
if conociminentoYap.find("a",class_="optional-action-target-wrapper artdeco-button artdeco-button--tertiary artdeco-button--standard artdeco-button--2 artdeco-button--muted inline-flex justify-center full-width align-items-center artdeco-button--fluid"):
    elemento_a = driver.find_element(By.ID,"navigation-index-Mostrar-todas-las-aptitudes-47-")
    elemento_a.click()

    time.sleep(5)
    soupN_Element =  BeautifulSoup(driver.page_source,"html.parser")
    expEl = soupN_Element.find_all("div",class_="display-flex align-items-center mr1 hoverable-link-text t-bold")
    for i in expEl:
        profile_data["Conocimientos_Y_Aptitudes"].append(i.get_text(strip=True))
    driver.back()    

#Idioma Section
idiomaS = sections[10]
language = (idiomaS.find("div",class_="display-flex align-items-center mr1 t-bold")).find_all("span")
for i in language[1:]:
    profile_data["Idiomas"].append(i.get_text(strip=True))

time.sleep(5)
file_name = "extraccionI.json"
with open(file_name, 'w') as archivo_json:
    json.dump(profile_data,archivo_json)

print("Se ha generado el archivo json")

driver.quit()