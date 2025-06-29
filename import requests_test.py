import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin


def pagefilter(url, liens):
    page = [
        urljoin(url, lien['href'])
        for lien in liens
        if lien.get('href') and '.html' in lien['href'].lower() and 'Enseignement' in lien['href']
    ]

    if page:
        print("Des pages ont été trouvées :", len(page))
    else:
        print("Aucune page trouvée")

    return page


def pdffilter(url, liens):
    pdfs = [
        urljoin(url, lien['href'])
        for lien in liens
        if lien.get('href') and lien['href'].lower().endswith('.pdf')
    ]

    if not pdfs:
        print("Aucun fichier PDF trouvé.")
    return pdfs


def liensfinder(url):
    try:
        reponse = requests.get(url)
        reponse.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return []

    soup = BeautifulSoup(reponse.content, 'html.parser')
    liens = soup.find_all('a', href=True)
    return liens


def pdfdownload(pdfs, dossier):
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
allSeenPages = set([])

def boucle(newFoundPages):
    newpages = []
    currentpages = set([])
    for k in newFoundPages:
        liens = liensfinder(k)
        kpages = pagefilter(k , liens)
        for j in kpages:
            if not allSeenPages.__contains__(j):
                currentpages.add(j)



    
    # for q in range(len(currentpages)):
    #     alrin = 0
    #     for p in range(len(newFoundPages)):
    #         if currentpages[q] == newFoundPages[p]:
    #             alrin = 1
    #     for n in range(len(newpages)):
    #         if currentpages[q] == newpages[n]:
    #             alrin = 1
    #     if alrin == 0:
    #         print(len(currentpages))
    #         newpages.append(currentpages[q])
    #print(q)
    #print(newpages)
    if list(currentpages) != []:
        for r in currentpages:
            allSeenPages.add(r)
        print(len(currentpages))
        print("blublublu",list(currentpages))
        boucle(list(currentpages))
    else:
        print("blébléblé")
        print("\n".join(list((allSeenPages))))
    #     return
    #print(kpages)
    return




def telecharger_pdfs(url):
    
    dossier = r'C:\Users\noahrozier\Documents\page_grp'
    if not os.path.exists(dossier):
        os.makedirs(dossier)

    liens = liensfinder(url)
    if not liens:
        return
    
    apages = pagefilter(url, liens)
    pdfs = pdffilter(url, liens)
    allSeenPages.add(url)
    boucle([url])


    if pdfs:
        pdfdownload(pdfs, dossier)


if __name__ == "__main__":
    #url = 'https://ronan.lauvergnat.fr/Enseignements_actuels_RL.html'
    url ='https://ronan.lauvergnat.fr/index.html'
    telecharger_pdfs(url)