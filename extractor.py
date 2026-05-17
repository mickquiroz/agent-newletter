import feedparser
import re
from datetime import datetime, timedelta, timezone
from dateutil import parser

FEEDS = [
    "https://github.blog/engineering/feed/",
    "https://feed.infoq.com/",
    "https://www.darkreading.com/rss.xml",
    "https://www.hashicorp.com/blog/feed.xml",
    "https://thenewstack.io/feed/"
]

def extraer_imagen(entry):
    """
    Intenta extraer la URL de la imagen principal de la noticia
    buscando en diferentes campos estándar y etiquetas HTML incrustadas.
    """
    if hasattr(entry, 'media_thumbnail') and len(entry.media_thumbnail) > 0:
        return entry.media_thumbnail[0].get('url')
        
    if hasattr(entry, 'media_content') and len(entry.media_content) > 0:
        for media in entry.media_content:
            if 'url' in media and media.get('medium', 'image') == 'image':
                return media['url']
                
    if hasattr(entry, 'links'):
        for link in entry.links:
            if 'image' in link.get('type', ''):
                return link.get('href')

    img_regex = re.compile(r'<img[^>]+src=["\'](.*?)["\']', re.IGNORECASE)

    if hasattr(entry, 'content'):
        for content in entry.content:
            match = img_regex.search(content.get('value', ''))
            if match:
                return match.group(1)
                
    if hasattr(entry, 'summary'):
        match = img_regex.search(entry.summary)
        if match:
            return match.group(1)
            
    if hasattr(entry, 'description'):
        match = img_regex.search(entry.description)
        if match:
            return match.group(1)

    return "" 

def obtener_noticias_recientes(feeds, horas_limite=48):
    noticias_recientes = []
    tiempo_limite = datetime.now(timezone.utc) - timedelta(hours=horas_limite)

    for url in feeds:
        print(f"Extrayendo feed: {url}")
        feed = feedparser.parse(url)
        
        for entry in feed.entries:
            if hasattr(entry, 'published'):
                fecha_pub = parser.parse(entry.published)
            elif hasattr(entry, 'updated'):
                fecha_pub = parser.parse(entry.updated)
            else:
                continue 
            if fecha_pub.tzinfo is None:
                fecha_pub = fecha_pub.replace(tzinfo=timezone.utc)

            if fecha_pub > tiempo_limite:
                url_imagen = extraer_imagen(entry)
                
                descripcion_limpia = entry.description if hasattr(entry, 'description') else ""
                descripcion_limpia = re.sub(r'<[^>]+>', '', descripcion_limpia).strip()

                noticias_recientes.append({
                    "titulo": entry.title,
                    "link": entry.link,
                    "descripcion": descripcion_limpia,
                    "imagen": url_imagen,
                    "fecha": fecha_pub.strftime("%Y-%m-%d %H:%M:%S"),
                    "fuente": feed.feed.title if hasattr(feed.feed, 'title') else url
                })
                
    return noticias_recientes