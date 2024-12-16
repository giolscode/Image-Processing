import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import ZScaleInterval, ImageNormalize
import numpy as np

def combine_channels(file_paths, weights=None):
    """Combine plusieurs canaux en une seule image avec des pondérations personnalisées."""
    
    if weights is None:
        weights = [1] * len(file_paths)
    
    combined_image = None

    for file_path, weight in zip(file_paths, weights):
        with fits.open(file_path) as hdul:
            data = hdul[1].data if len(hdul) > 1 else hdul[0].data
            if combined_image is None:
                combined_image = np.zeros_like(data, dtype=float)
            combined_image += weight * data

    return combined_image

# Exemple d'utilisation
if __name__ == "__main__":
    print("Combinaison et affichage des canaux...")

    # Fichiers locaux à combiner
    fits_files = [
        "Tarantula_Nebula-oiii.fit",
        "Tarantula_Nebula-halpha.fit",
        "Tarantula_Nebula-sii.fit"
    ]

    # Combinaison des canaux avec des pondérations égales
    combined_image = combine_channels(fits_files, weights=[1, 1, 1])

    # Affichage de l'image combinée
    plt.figure(figsize=(8, 8))
    norm = ImageNormalize(combined_image, interval=ZScaleInterval())
    plt.imshow(combined_image, cmap='viridis', origin='lower', norm=norm)
    plt.colorbar(label='Intensité combinée')
    plt.title('Tarantula Nebula - Image combinée')
    plt.xlabel('Pixel X')
    plt.ylabel('Pixel Y')
    plt.tight_layout()
    plt.show()
