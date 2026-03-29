import urllib.request
import os

def download_france_pbf():
    url = "https://download.geofabrik.de/europe/france-latest.osm.pbf"
    local_filename = "france-latest.osm.pbf"
    try:
        file_path, headers = urllib.request.urlretrieve(url, local_filename)
        size_gb = os.path.getsize(file_path) / (1024**3)
        print(f"Succès ! Fichier enregistré : {file_path}")
        print(f"Taille sur disque : {size_gb:.2f} Go")
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")

if __name__ == "__main__":
    download_france_pbf()