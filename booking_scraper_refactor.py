

"""
Script de web scraping para Booking.com que realiza dos tareas principales:
1. Extrae una lista de alojamientos de una página de resultados de búsqueda.
2. Visita la página de detalle de cada alojamiento para extraer información
   adicional (como la descripción) y todas las reseñas de los usuarios.
Finalmente, guarda todos los datos en un archivo JSON.
"""
import re

import time
import sys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException
)
from bs4 import BeautifulSoup

# --- Configuración Global ---

# NOTA: Esta URL de búsqueda puede caducar o cambiar.
# Contiene parámetros para: Quito, 25-26 Oct 2025, 2 adultos.
# URL_BUSQUEDA = ("https://www.booking.com/searchresults.es.html?label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&ss=General+Villamil&ssne=General+Villamil&ssne_untouched=General+Villamil&highlighted_hotels=1437824&efdco=1&lang=es&src=hotel&dest_id=-932017&dest_type=city&checkin=2025-12-06&checkout=2025-12-07&group_adults=2&no_rooms=1&group_children=0&nflt=price%3DUSD-280-max-1")

# URLS_BUSQUEDA = [
#     "https://www.booking.com/searchresults.es.html?label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&ss=villamil+playas&ssne=General+Villamil&ssne_untouched=General+Villamil&highlighted_hotels=1437824&lang=es&src=searchresults&dest_id=9556342&dest_type=hotel&ac_position=0&ac_click_type=b&ac_langcode=es&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=7eb39c37e1a15e88c35c1cb82502d80f&checkin=2025-12-06&checkout=2025-12-07&group_adults=2&no_rooms=1&group_children=0&nflt=price%3DUSD-280-max-1",
#     "https://www.booking.com/searchresults.es.html?label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&ss=Salinas%2C+Ecuador&ssne=General+Villamil&ssne_untouched=General+Villamil&highlighted_hotels=1437824&lang=es&src=searchresults&dest_id=-932936&dest_type=city&ac_position=1&ac_click_type=b&ac_langcode=es&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=8fac9f25a5a8207ef343e5b218bbc2c7&checkin=2025-12-06&checkout=2025-12-07&group_adults=2&no_rooms=1&group_children=0&nflt=price%3DUSD-68-max-1",
#     "https://www.booking.com/searchresults.es.html?label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&ss=Monta%C3%B1ita%2C+Ruta+del+Sol%2C+Ecuador&ssne=Atacames&ssne_untouched=Atacames&highlighted_hotels=1437824&lang=es&src=searchresults&dest_id=-930965&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=es&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=cd8678f6af32026d&checkin=2025-12-06&checkout=2025-12-07&group_adults=2&no_rooms=1&group_children=0&nflt=price%3DUSD-150-max-1",
#     "https://www.booking.com/searchresults.es.html?label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&ss=Puerto+L%C3%B3pez%2C+Ruta+del+Sol%2C+Ecuador&ssne=Monta%C3%B1ita&ssne_untouched=Monta%C3%B1ita&highlighted_hotels=1437824&lang=es&src=searchresults&dest_id=-932301&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=es&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=fab0901b82ce0c18&checkin=2025-12-06&checkout=2025-12-07&group_adults=2&no_rooms=1&group_children=0&nflt=price%3DUSD-80-max-1",
#     "https://www.booking.com/searchresults.es.html?label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&ss=Ayampe%2C+Ruta+del+Sol%2C+Ecuador&ssne=Puerto+L%C3%B3pez&ssne_untouched=Puerto+L%C3%B3pez&highlighted_hotels=1437824&lang=es&src=searchresults&dest_id=-924536&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=es&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=d8869037d3100502&checkin=2025-12-06&checkout=2025-12-07&group_adults=2&no_rooms=1&group_children=0&nflt=price%3DUSD-100-max-1",
#     "https://www.booking.com/searchresults.es.html?label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&ss=Manta%2C+Ruta+del+Sol%2C+Ecuador&ssne=Ayampe&ssne_untouched=Ayampe&highlighted_hotels=1437824&lang=es&src=searchresults&dest_id=-930612&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=es&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=1e26904c6fba0579&checkin=2025-12-06&checkout=2025-12-07&group_adults=2&no_rooms=1&group_children=0&nflt=price%3DUSD-150-max-1",
#     "https://www.booking.com/searchresults.es.html?label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&ss=Atacames%2C+Esmeraldas%2C+Ecuador&ssne=Manta&ssne_untouched=Manta&highlighted_hotels=1437824&lang=es&src=searchresults&dest_id=-924479&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=es&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=d8869058509a022b&checkin=2025-12-06&checkout=2025-12-07&group_adults=2&no_rooms=1&group_children=0&nflt=price%3DUSD-150-max-1"
# ]

# Diccionario con las búsquedas
URLS_BUSQUEDA = {
    "Villamil Playas":"https://www.booking.com/searchresults.es.html?ss=villamil+playas&ssne=General+Villamil&ssne_untouched=General+Villamil&highlighted_hotels=1437824&efdco=1&label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&lang=es&sb=1&src_elem=sb&src=searchresults&dest_id=9556342&dest_type=hotel&ac_position=0&ac_click_type=b&ac_langcode=es&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=1fd93f009411257c4c51838f2eaaa5ed&ac_meta=GiAxZmQ5M2YwMDk0MTEyNTdjNGM1MTgzOGYyZWFhYTVlZCAAKAEyAmVzOg92aWxsYW1pbCBwbGF5YXNAAEoAUAA%3D&checkin=2025-12-13&checkout=2025-12-14&group_adults=2&no_rooms=1&group_children=0"
    ,"Salinas": "https://www.booking.com/searchresults.es.html?ss=Salinas%2C+Ruta+del+Sol%2C+Ecuador&ssne=General+Villamil&ssne_untouched=General+Villamil&highlighted_hotels=1437824&label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&lang=es&sb=1&src_elem=sb&src=searchresults&dest_id=-932937&dest_type=city&ac_position=1&ac_click_type=b&ac_langcode=es&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=a61dea2cd86636752bf56aabfedf141a&ac_meta=GiBhNjFkZWEyY2Q4NjYzNjc1MmJmNTZhYWJmZWRmMTQxYSABKAEyAmVzOgJzYUAASgBQAA%3D%3D&checkin=2025-12-13&checkout=2025-12-14&group_adults=2&no_rooms=1&group_children=0"
    ,"Montañita":"https://www.booking.com/searchresults.es.html?ss=Monta%C3%B1ita%2C+Ruta+del+Sol%2C+Ecuador&ssne=Salinas&ssne_untouched=Salinas&highlighted_hotels=1437824&label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&lang=es&sb=1&src_elem=sb&src=searchresults&dest_id=-930965&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=es&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=d2db52727df2afa30a065b4a4e113c73&ac_meta=GiBkMmRiNTI3MjdkZjJhZmEzMGEwNjViNGE0ZTExM2M3MyAAKAEyAmVzOgVtb250YUAASgBQAA%3D%3D&checkin=2025-12-13&checkout=2025-12-14&group_adults=2&no_rooms=1&group_children=0"
    , "Puerto Lopez":"https://www.booking.com/searchresults.es.html?ss=Puerto+L%C3%B3pez%2C+Ruta+del+Sol%2C+Ecuador&ssne=Monta%C3%B1ita&ssne_untouched=Monta%C3%B1ita&highlighted_hotels=1437824&label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&lang=es&sb=1&src_elem=sb&src=searchresults&dest_id=-932301&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=es&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=64dd2719b5ebb98f6a225d76d83efc0f&ac_meta=GiA2NGRkMjcxOWI1ZWJiOThmNmEyMjVkNzZkODNlZmMwZiAAKAEyAmVzOglwdWVydG8gbG9AAEoAUAA%3D&checkin=2025-12-13&checkout=2025-12-14&group_adults=2&no_rooms=1&group_children=0"
    , "Ayampe":"https://www.booking.com/searchresults.es.html?ss=Ayampe%2C+Ruta+del+Sol%2C+Ecuador&ssne=Puerto+L%C3%B3pez&ssne_untouched=Puerto+L%C3%B3pez&highlighted_hotels=1437824&label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&lang=es&sb=1&src_elem=sb&src=searchresults&dest_id=-924536&dest_type=city&ac_position=1&ac_click_type=b&ac_langcode=es&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=d8e1551c1e9d6ae5de9c96314ca96d19&ac_meta=GiBkOGUxNTUxYzFlOWQ2YWU1ZGU5Yzk2MzE0Y2E5NmQxOSABKAEyAmVzOgNheWFAAEoAUAA%3D&checkin=2025-12-13&checkout=2025-12-14&group_adults=2&no_rooms=1&group_children=0"
    , "Manta":"https://www.booking.com/searchresults.es.html?ss=Manta&ssne=Manta&ssne_untouched=Manta&highlighted_hotels=1437824&efdco=1&label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&lang=es&sb=1&src_elem=sb&src=searchresults&dest_id=-930612&dest_type=city&checkin=2026-01-01&checkout=2026-01-02&group_adults=2&no_rooms=1&group_children=0"
    , "Atacames":"https://www.booking.com/searchresults.es.html?ss=Atacames&ssne=Atacames&ssne_untouched=Atacames&highlighted_hotels=1437824&efdco=1&label=gen173nr-10CAQoggJCDGNpdHlfLTkzMjAxN0gKWARoQYgBAZgBM7gBF8gBDNgBA-gBAfgBAYgCAagCAbgCwNy3yAbAAgHSAiQzMDFiZjYzMy1iMjQxLTRmNjAtOWU4MC1lNDFhZjdmYTM0NTHYAgHgAgE&sid=61e6f1a6c7eaf8b23f09e670ece985e3%22++++++++++++++++%22&aid=304142&lang=es&sb=1&src_elem=sb&src=searchresults&dest_id=-924479&dest_type=city&checkin=2025-11-15&checkout=2025-11-16&group_adults=2&no_rooms=1&group_children=0"    

}

#

# --- Constantes de Tiempos de Espera (en segundos) ---
ESPERA_INICIAL_PAGINA = 15  # Espera para que cargue la lista de resultados
ESPERA_SCROLL = 3          # Pausa entre cada scroll en la página de resultados
ESPERA_PAGINA_DETALLE = 10 # Espera para que cargue la página de detalle
ESPERA_MODAL_RESEÑAS = 10  # Espera para que aparezca la modal de reseñas

# --- Constantes de Scraping ---
MAX_PAGINAS_RESEÑAS = 3    # Máximo de páginas de reseñas a scrapear por alojamiento
ARCHIVO_SALIDA_JSON = "booking_data.json"


def initialize_driver() -> webdriver.Chrome:
    """
    Inicializa y devuelve una instancia del WebDriver de Chrome.
    Maneja la excepción si ChromeDriver no está instalado o no se encuentra.
    
    @return: Una instancia de webdriver.Chrome o None si falla.
    """
    print("Iniciando el navegador (Chrome)...")
    try:
        # Opciones para ejecutar en modo "headless" (sin interfaz gráfica)
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # driver = webdriver.Chrome(options=options)
        
        driver = webdriver.Chrome()
        driver.maximize_window()
        return driver
    except Exception as e:
        print(f"Error fatal al iniciar Chrome: {e}")
        print("Asegúrate de que Google Chrome y ChromeDriver estén instalados y en tu PATH.")
        sys.exit(1)


def scrape_listings_from_search_page(driver: webdriver.Chrome, url: str) -> list[dict]:
    """
    Navega a la URL de búsqueda, hace scroll para cargar todos los resultados
    y extrae la información básica de cada propiedad.
    
    @param driver: La instancia del WebDriver de Selenium.
    @param url: La URL de la página de resultados de búsqueda.
    @return: Una lista de diccionarios, donde cada uno representa una propiedad.
    """
    print(f"Navegando a la URL de búsqueda...")
    driver.get(url)

    # Espera explícita: espera hasta que la primera "property card" sea visible
    try:
        Wait(driver, ESPERA_INICIAL_PAGINA).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="property-card"]'))
        )
        print("Página de resultados cargada.")
    except TimeoutException:
        print("La página tardó demasiado en cargar o no se encontraron propiedades.")
        print("Posibles causas: CAPTCHA, bloqueo de IP o selectores obsoletos.")
        return []

    # Scroll hasta el final de la página para cargar todos los resultados dinámicos
    print("Haciendo scroll para cargar todos los alojamientos...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(ESPERA_SCROLL)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Se llegó al final de la página
        last_height = new_height

    print("Extrayendo contenido HTML...")
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    listings = soup.find_all('div', {'data-testid': 'property-card'})#obtener lista de las propiedades de todos los alojamientos
    print(f"--- Se encontraron {len(listings)} propiedades ---")

    properties_data = []
    for listing in listings:
        try:
            # Título
            name_elem = listing.find('div', {'data-testid': 'title'})
            title = name_elem.get_text(strip=True) if name_elem else "Nombre no disponible"

            # Precio
            price_elem = listing.find('span', {'data-testid': 'price-and-discounted-price'})
            price = price_elem.get_text(strip=True) if price_elem else "Precio no disponible"

            # URL a la página de detalle
            link_elem = listing.find('a', {'data-testid': 'availability-cta-btn'})
            detail_url = link_elem.get('href') if link_elem else ""
            
            # Puntuación numérica
            rating_value = "Sin puntuación"
            score_div = listing.select_one('div[data-testid="review-score"] > div[aria-hidden="true"]')
            if score_div:
                rating_value = score_div.get_text(strip=True)

            span_element = listing.select_one('span[class*="fff1944c52 d4d73793a3"]')
            beach_distance = "Sin calificación"
            if span_element:
                beach_distance = span_element.get_text(strip=True)

            # Distancia del centro
            span_element = listing.find('span', {'data-testid': 'distance'})
            distance = span_element.get_text(strip=True) if span_element else "Distancia no disponible"

            # Características (ej: "1 cama doble")
            features_text = ""
            features_list = listing.select('ul > li > span')
            if features_list:
                # Une todos los textos de características encontrados
                features_text = " ".join([s.get_text(strip=True) for s in features_list if s.get_text(strip=True) and '•' not in s.get_text()])

            # Política de pago
            payment_policy = ""
            policy_div = listing.find('div', {'data-testid': 'payment-policy-tags'})
            if policy_div:
                payment_policy = policy_div.get_text(" ", strip=True)

            properties_data.append({
                "title": title,
                "price": price,
                "rating": rating_value,
                "distance": distance,
                "features": features_text,
                "payment_policy": payment_policy,
                "url": detail_url,
                "beach_distance": beach_distance
            })
        except Exception as e:
            print(f"Error extrayendo datos de una propiedad: {e}")
            continue

    return properties_data
                                                                                       

def scrape_detail_page_data(driver: webdriver.Chrome) -> dict:
    """
    Extrae datos adicionales (descripción, ubicación) desde la página de detalle.
    Asume que el driver ya está en la página correcta.
    
    @param driver: La instancia del WebDriver de Selenium.
    @return: Un diccionario con la información extraída.
    """
    detail_data = {
        "description": "Descripción no disponible",
        "location": "Ubicación (lat,lng) no disponible",
        "services": "Servicios no disponibles",
        "pointService": "Puntaje de Servicios no disponibles"
    }

    # Espera a que el elemento de descripción esté presente
    try:
        desc_elem = Wait(driver, ESPERA_PAGINA_DETALLE).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p[data-testid="property-description"]'))
        )
        # Obtener el HTML de la página de detalle
        detail_html = driver.page_source
        detail_soup = BeautifulSoup(detail_html, 'html.parser')

        # Extraer descripción
        desc_elem_soup = detail_soup.find('p', {'data-testid': 'property-description'})
        if desc_elem_soup:
            detail_data["description"] = desc_elem_soup.get_text(" ", strip=True)

        # Extraer coordenadas del mapa
        map_link = detail_soup.select_one('a#map_trigger_header_pin')
        if map_link and map_link.get('data-atlas-latlng'):
            detail_data["location"] = map_link.get('data-atlas-latlng')

        # Extraer servicios (amenities)
        services_list = detail_soup.find('div', {'data-testid': 'property-most-popular-facilities-wrapper'})
        services = []


        # ahora puedes seguir trabajando solo con esa parte
        for li in detail_soup.find_all("li"):
            name_span = li.select_one("span.f6b6d2a959")
            if name_span:
                services.append(name_span.get_text(strip=True))
        detail_data["services"] = services[:-1]

        # Extraer puntaje de servicios
        score_div = detail_soup.find("div", string=re.compile("Puntuación"))
        if score_div:
            text = score_div.get_text(strip=True)
            match = re.search(r"Puntuación:\s*([\d,\.]+)", text)
            if match:
                puntuacion = match.group(1).replace(",", ".")  # convertir coma a punto si quieres float
                detail_data["pointService"] = puntuacion
                print(puntuacion)





    except TimeoutException:
        print("  -> No se pudo encontrar la descripción en la página de detalle (posible timeout).")
    except Exception as e:
        print(f"  -> Error extrayendo datos del detalle: {e}")

    return detail_data


def scrape_reviews_from_modal(driver: webdriver.Chrome, max_pages: int) -> list[dict]:
    """
    Busca y hace click en "leer todas las reseñas", luego extrae las reseñas
    desde la modal, manejando el scroll y la paginación dentro de ella.
    
    Asume que el driver ya está en la página de detalle del alojamiento.
    
    @param driver: La instancia del WebDriver de Selenium.
    @param max_pages: El número máximo de páginas de reseñas a scrapear.
    @return: Una lista de diccionarios, donde cada uno representa una reseña.
    """
    reviews = []

    # 1) Click al botón 'Leer todas las reseñas'
    try:
        btn_read_reviews = Wait(driver, ESPERA_MODAL_RESEÑAS).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="fr-read-all-reviews"]'))
        )
        # Usar JavaScript para hacer click evita problemas con elementos superpuestos
        driver.execute_script("arguments[0].click();", btn_read_reviews)
    except (TimeoutException, ElementClickInterceptedException):
        print("  -> No se encontró el botón de 'Leer todas las reseñas' o no es clickeable.")
        return reviews  # No hay reseñas o el botón no se encontró

    # 2) Esperar a que la modal de reseñas aparezca
    try:
        modal = Wait(driver, ESPERA_MODAL_RESEÑAS).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                '[data-testid="fr-reviews-modal"], div[role="dialog"]' # Selectores comunes
            ))
        )
    except TimeoutException:
        print("  -> La modal de reseñas no apareció después de hacer click.")
        return reviews

    # --- Funciones auxiliares anidadas (solo se usan aquí) ---
    def parse_visible_reviews() -> list[dict]:
        """Parsea las reseñas actualmente visibles en el DOM de la modal."""
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Busca las tarjetas de reseña dentro de la modal
        containers = soup.select('div[data-testid="fr-reviews-modal"] div[data-testid="review-card"], div[role="dialog"] div[data-testid="review-card"]')
        
        parsed_list = []
        for card in containers:
            title_elem = card.find('h4', {'data-testid': 'review-title'})
            date_elem = card.find('span', {'data-testid': 'review-date'}) 
            review_pos_elem = card.find('div', {'data-testid': 'review-positive-text'})
            review_neg_elem = card.find('div', {'data-testid': 'review-negative-text'})

            parsed_list.append({
                "title": title_elem.get_text(strip=True) if title_elem else "",
                "date": date_elem.get_text(strip=True) if date_elem else "",
                "negative_feedback": review_neg_elem.get_text(strip=True) if review_neg_elem else "",
                "positive_feedback": review_pos_elem.get_text(strip=True) if review_pos_elem else ""
            })
        return parsed_list

    def scroll_modal_completely():
        """Hace scroll dentro de la modal para cargar reseñas (lazy-load)."""
        last_height = -1
        for _ in range(15):  # Límite de seguridad de 15 scrolls
            try:
                # Obtenemos la altura actual del contenido de la modal
                current_height = driver.execute_script("return arguments[0].scrollHeight;", modal)
                # Hacemos scroll hasta el fondo de la modal
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", modal)
                time.sleep(1.5) # Pausa para que cargue el nuevo contenido
                
                new_height = driver.execute_script("return arguments[0].scrollHeight;", modal)
                
                # Si la altura no cambia, significa que llegamos al final
                if new_height == last_height or new_height == current_height:
                    break
                last_height = new_height
            except Exception:
                break # Salir si la modal desaparece o hay error

    def click_next_page() -> bool:
        """Busca el botón 'Página siguiente' y hace click si existe."""
        try:
            # Selector para el botón de paginación (puede cambiar)
            next_button = modal.find_element(By.CSS_SELECTOR, "button[aria-label='Página siguiente']")
            if next_button.is_enabled():
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(1.5) # Esperar a que cargue la nueva página
                return True
        except NoSuchElementException:
            # No se encontró el botón, significa que es la última página
            return False
        except Exception:
            # Otro error (ej: botón no interactuable)
            return False
        return False
    # --- Fin de funciones auxiliares ---

    # 3) Bucle principal de extracción de reseñas
    collected_titles = set() # Usar un set para evitar duplicados si el parseo se repite

    for page in range(1, max_pages + 1):
        print(f"  -> Extrayendo reseñas (Página {page}/{max_pages})...")
        
        # Primero, hacer scroll para cargar todo el contenido lazy-load de esta página
        scroll_modal_completely()
        
        # Segundo, parsear todas las reseñas visibles
        current_page_reviews = parse_visible_reviews()
        
        new_reviews_found = 0
        for review in current_page_reviews:
            # Añadir solo si no la hemos visto antes (control por título)
            if review['title'] not in collected_titles:
                reviews.append(review)
                collected_titles.add(review['title'])
                new_reviews_found += 1
        
        # Tercero, intentar pasar a la siguiente página
        if not click_next_page():
            print("  -> No hay más páginas de reseñas.")
            break # Salir del bucle si no hay botón "siguiente"

    # 4) Cerrar la modal de reseñas (opcional, pero buena práctica)
    try:
        # Busca un botón de cierre común
        close_btn = modal.find_element(By.CSS_SELECTOR, 'button[aria-label="Cerrar"]')
        driver.execute_script("arguments[0].click();", close_btn)
    except Exception:
        pass # No es crítico si no se puede cerrar

    return reviews


def save_to_json(data: list[dict], filename: str):
    """
    Guarda la lista de datos en un archivo JSON.
    
    @param data: La lista de diccionarios a guardar.
    @param filename: El nombre del archivo de salida.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\nResultados guardados exitosamente en '{filename}'")
    except IOError as e:
        print(f"\nError al guardar el archivo JSON: {e}")


def main():
    """
    Función principal que orquesta el proceso de scraping.
    """
    driver = initialize_driver()

    
    if not driver:
        return # Salir si el driver no se pudo inicializar

    all_properties_data = []

    try:
        # --- PASO 1: Obtener la lista de propiedades de la página de búsqueda ---

        for ciudad, url in URLS_BUSQUEDA.items():
            print(f"\n=== Procesando destino: {ciudad} ===")

            city_data = scrape_listings_from_search_page(driver, url)

            # Agregar campos que identifiquen la ciudad y la URL original
            for prop in city_data:
                prop["destino"] = ciudad
                prop["search_url"] = url

            # Añadir todos los resultados a la lista general
            all_properties_data.extend(city_data)


        # print(all_properties_data)
        
        if not all_properties_data:
            print("No se encontraron propiedades en la página de búsqueda. Terminando.")
            return

        print(f"\n--- Resumen inicial: {len(all_properties_data)} propiedades encontradas ---")
        for i, listing in enumerate(all_properties_data[:5], 1): # Muestra las primeras 5
            print(listing)
            #print(f"  {i}. {listing['title']} ({listing['price']})")
        if len(all_properties_data) > 5:
            print("  ...")
        
        # --- PASO 2: Iterar sobre cada propiedad para obtener detalles y reseñas ---
        print("\nIniciando scraping de las páginas de detalle (esto puede tardar)...")
    
        for i, listing in enumerate(all_properties_data, 1):
            print(f"\n--- Procesando Alojamiento {i}/{len(all_properties_data)}: {listing['title']} ---")
            
            if not listing['url'] or not listing['url'].startswith("http"):
                print("  -> URL no válida o no encontrada, saltando.")
                continue
            
            try:
                # Navegar a la página de detalle
                driver.get(listing['url'])
                
                # Extraer datos de la página (descripción, ubicación)
                detail_data = scrape_detail_page_data(driver)
                listing.update(detail_data) # Fusiona los datos nuevos al diccionario
                
                # Extraer reseñas desde la modal
                reviews = scrape_reviews_from_modal(driver, max_pages=MAX_PAGINAS_RESEÑAS)
                listing["reviews"] = reviews
                print(f"  -> Se encontraron {len(reviews)} reseñas.")

            except Exception as e:
                print(f"  -> ERROR INESPERADO al procesar {listing['title']}: {e}")
                print("  -> Saltando al siguiente alojamiento.")
                continue # Continuar con el siguiente listado
        
        # --- PASO 3: Guardar todos los resultados ---
        print("\nScraping de detalles completado.")
        save_to_json(all_properties_data, ARCHIVO_SALIDA_JSON)
        
    except Exception as e:
        print(f"\nHa ocurrido un error crítico en el script: {e}")
    finally:
        # Asegurarse de que el navegador se cierre siempre
        print("Cerrando el navegador...")
        driver.quit()
        print("Proceso finalizado.")


# --- Punto de entrada del script ---
if __name__ == "__main__":
    main()