import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def search_pages(url):
    print(f"Recherche de pages sur le site: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Liste pour stocker les URLs des pages trouvées
        pages_urls = []

        # Recherche de liens vers des pages
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('http'):
                pages_urls.append(href)

        if pages_urls:
            print("Pages trouvées:")
            for page_url in pages_urls:
                print(page_url)
        else:
            print("Aucune page trouvée sur ce site.")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")

def search_zip(url):
    print(f"Recherche de fichiers .zip sur le site: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Liste pour stocker les URLs des fichiers .zip trouvés
        zip_urls = []

        # Recherche de liens pointant vers des fichiers .zip
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.zip'):
                zip_url = urljoin(url, href)
                zip_urls.append(zip_url)

        if zip_urls:
            print("Fichiers .zip trouvés:")
            for zip_url in zip_urls:
                print(zip_url)
                download_zip(zip_url)
        else:
            print("Aucun fichier .zip trouvé sur ce site.")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")

def download_zip(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Extraire le nom du fichier .zip
        filename = url.split('/')[-1]

        # Chemin complet pour enregistrer le fichier dans le répertoire courant
        save_path = os.path.join(os.getcwd(), filename)

        # Écrire le contenu du fichier .zip téléchargé localement
        with open(save_path, 'wb') as file:
            file.write(response.content)

        print(f"Fichier .zip téléchargé avec succès: {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement du fichier .zip: {e}")

def main():
    while True:
        print("\nMenu Principal:")
        print("1. Rechercher des pages sur un site")
        print("2. Rechercher des fichiers .zip sur un site")
        print("3. Quitter")
        choice = input("Choisissez une option: ")

        if choice == '1':
            url = input("Entrez l'URL du site: ")
            search_pages(url)
        elif choice == '2':
            url = input("Entrez l'URL du site: ")
            search_zip(url)
        elif choice == '3':
            print("Quitter...")
            break
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == '__main__':
    main()
