# analisis-hospitalidad-turismo-ecuador
Proyecto de ciencia de datos que integra web scraping, análisis de sentimiento y modelado de hospitalidad para clasificar y jerarquizar destinos turísticos en Ecuador a partir de reseñas y datos públicos de Booking.com.

El objetivo fue **clasificar y jerarquizar los destinos costeros del Ecuador** (Villamil Playas, Salinas, Montañita, Puerto López, Ayampe, Manta y Atacames) según su **capacidad hotelera** y **nivel de hospitalidad**, utilizando datos obtenidos desde [Booking.com](https://booking.com).

## 🎯 Objetivos del proyecto
- Diseñar una **estrategia de recolección de datos** mediante web scraping.
- Crear un **dataset estructurado** de alojamientos con información sobre precios, puntuaciones, reseñas, servicios, etc.
- Desarrollar una **metodología de clasificación** basada en variables cuantitativas (capacidad, puntuación) y cualitativas (percepciones en reseñas).
- Implementar un **análisis comparativo y ranking final** de destinos.
- Integrar **IA generativa (GPT API)** para interpretar percepciones de clientes.


## 📊 Metodología de análisis
1. **Extracción de datos:**  
   Scraping con `Selenium` y `BeautifulSoup` para obtener títulos, precios, puntuaciones, reseñas y servicios de alojamientos.
2. **Procesamiento:**  
   Limpieza con `pandas`, normalización de precios y puntuaciones, y creación de métricas por destino.
3. **Análisis semántico:**  
   Uso de la **API de OpenAI (GPT-4)** para evaluar hospitalidad y percepciones en reseñas.
4. **Clasificación y ranking:**  
   Ponderación de variables:
