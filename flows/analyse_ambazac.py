import onecode
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import rasterio
import warnings

# Configuration
warnings.filterwarnings('ignore')


def run():
    # ─── DÉCLARATION DES WIDGETS (S'affichent dans l'onglet Input) ───
    # Chaque élément doit avoir une 'key' unique.

    # 1. Sélection des fichiers de données
    f_geo = onecode.file_input(
        key="fichier_geochimie",
        value="data/Points_geochimie_AMBAZAC.geojson",
        label="Points Géochimiques (GeoJSON)"
    )

    f_mnt = onecode.file_input(
        key="fichier_mnt",
        value="data/MNT_25M_AMBAZAC_IMAGE.tif",
        label="MNT (GeoTIFF)"
    )

    # 2. Paramètres d'analyse (Sliders)
    f_mad = onecode.slider(
        key='facteur_mad',
        value=2.0,
        min=1.0,
        max=5.0,
        step=0.1,
        label="Sensibilité Anomalies (MAD)"
    )

    p_au = onecode.slider('poids_au', 0.5, min=0.0, max=1.0, step=0.1, label="Poids Or (Au)")
    p_as = onecode.slider('poids_as', 0.2, min=0.0, max=1.0, step=0.1, label="Poids Arsenic (As)")
    p_w = onecode.slider('poids_w', 0.2, min=0.0, max=1.0, step=0.1, label="Poids Tungstène (W)")

    # ─── LOGIQUE DE TRAITEMENT ───
    onecode.Logger.info(f"Démarrage de l'analyse avec un facteur MAD de {f_mad}")

    # Chargement des données (utilisation de str() pour extraire le chemin du widget)
    data = gpd.read_file(str(f_geo))

    with rasterio.open(str(f_mnt)) as src:
        mnt = src.read(1)
        extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]

    # Exemple de calcul de score simple
    # Note : On accède directement aux valeurs des sliders par leur variable
    data['score'] = (data['Au_ppb'] * p_au) + (data['As_ppm'] * p_as)

    # ─── GÉNÉRATION DES SORTIES (Outputs) ───
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(mnt, cmap='terrain', extent=extent)
    sc = ax.scatter(data.geometry.x, data.geometry.y, c=data['score'], cmap='YlOrRd', s=20)
    plt.colorbar(sc, label='Potentiel Minéral')

    # Sauvegarde conforme pour l'affichage dans l'onglet Output
    output_path = onecode.file_output('carte_ambazac', 'outputs/carte_potentiel.png', make_path=True)
    plt.savefig(output_path)
    plt.close()

    onecode.Logger.info("Analyse terminée. Carte générée dans l'onglet Output.")