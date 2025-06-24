import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def pagefilter(liens) :
    # Filtrer les liens vers une autre page
    page = [urljoin(url, lien['href']) for lien in liens if lien .get('href') and '.html' in lien['href'] .lower()and lien['href'].__contains__('Enseignement')]

    if len(page)>0:
        print("Des pages ont été trouvées :")
        print(len(page))

    elif not page:
        print("aucune page trouvée")
        return

def pdffilter(liens) :
    # Filtrer les liens vers des PDF
    pdfs = [urljoin(url, lien['href']) for lien in liens if lien['href'].lower().endswith('.pdf')]

    if not pdfs:
        print("Aucun fichier PDF trouvé.")
        return
def liensfinder(url):
    # Télécharger le contenu de la page
    try:
        reponse = requests.get(url)
        reponse.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return

    # Parser le HTML
    soup = BeautifulSoup(reponse.content, 'html.parser') 

    # Chercher tous les liens
    liens = soup.find_all('a', href=True)
    return
def pdfdownload(pdfs):
 # Télécharger chaque PDF
    for pdf_url in pdfs:
        nom_fichier = os.path.join(dossier, os.path.basename(pdf_url))
        try:
            print(f"Téléchargement de {pdf_url}...")
            reponse_pdf = requests.get(pdf_url)
            reponse_pdf.raise_for_status()
            with open(nom_fichier, 'wb') as f:
                f.write(reponse_pdf.content)
            print(f"Enregistré sous {nom_fichier}")
        except requests.RequestException as e:
            print(f"Erreur lors du téléchargement de {pdf_url} : {e}")
            return
        return


