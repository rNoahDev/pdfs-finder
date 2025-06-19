import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def telecharger_pdfs(url):

    dossier = r'C:\Users\noahrozier\Documents\page_grp'
    # Créer un dossier de destination si nécessaire
    if not os.path.exists(dossier):
        os.makedirs(dossier)

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
    
    # Filtrer les liens vers des PDF
    pdfs = [urljoin(url, lien['href']) for lien in liens if lien['href'].lower().endswith('.pdf')]

    if not pdfs:
        print("Aucun fichier PDF trouvé.")
        return

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

if __name__ == "__main__":
    url = 'https://ronan.lauvergnat.fr/Enseignements_actuels_RL.html'
    telecharger_pdfs(url)
