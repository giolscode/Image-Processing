from astroquery.skyview import SkyView
from astropy.io import fits
import matplotlib.pyplot as plt
import os
import numpy as np

def normalize_image_data(data):
    """Normalise les données d'image entre 0 et 1."""
    min_value = np.percentile(data, 1)
    max_value = np.percentile(data, 99)
    normalized_data = (data - min_value) / (max_value - min_value)
    return np.clip(normalized_data, 0, 1)

def download_fits_files(target, surveys, folder="fits_files"):
    """Télécharge les fichiers FITS pour une cible donnée depuis SkyView."""
    os.makedirs(folder, exist_ok=True)
    downloaded_files = []

    for survey in surveys:
        try:
            images = SkyView.get_images(position=target, survey=survey)
            if images:
                file_name = f"{folder}/{target.replace(' ', '_')}_{survey.replace(' ', '_')}.fits"
                fits.writeto(file_name, images[0][0].data, header=images[0][0].header, overwrite=True)
                downloaded_files.append(file_name)
                print(f"Fichier téléchargé : {file_name}")
            else:
                print(f"Aucune donnée trouvée pour {survey}.")
        except Exception as e:
            print(f"Erreur lors du téléchargement pour {survey} : {e}")

    return downloaded_files

def create_warm_rgb_image(target, surveys):
    """Crée une image RGB avec des couleurs chaudes à partir de plusieurs relevés."""
    fits_files = download_fits_files(target, surveys)

    if len(fits_files) < 3:
        print("Erreur : Besoin d'au moins 3 fichiers pour créer une image RGB.")
        return

    red_data = fits.getdata(fits_files[0])
    green_data = fits.getdata(fits_files[1])
    blue_data = fits.getdata(fits_files[2])

    red_data = normalize_image_data(red_data)
    green_data = normalize_image_data(green_data)
    blue_data = normalize_image_data(blue_data)
    
    gamma = 0.8
    red_data = np.power(red_data, gamma)
    green_data = np.power(green_data, gamma)
    blue_data = np.power(blue_data, gamma)

    height, width = red_data.shape
    center_y, center_x = height // 2, width // 2
    y, x = np.ogrid[:height, :width]
    distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    radial_effect = np.exp(-distance / (height / 3))

    red_data += radial_effect * 0.3
    green_data += radial_effect * 0.2
    blue_data += radial_effect * 0.1

    def enhance_edges(data):
        gradient_x = np.abs(np.diff(data, axis=1, append=data[:, -1:]))
        gradient_y = np.abs(np.diff(data, axis=0, append=data[-1:, :]))
        return np.clip(data + gradient_x + gradient_y, 0, 1)

    red_data = enhance_edges(red_data)
    green_data = enhance_edges(green_data)
    blue_data = enhance_edges(blue_data)

    red_data *= 1.5
    green_data *= 1.3
    blue_data *= 0.8
    def brighten_background(data, strength=0.5):
        return np.clip(data + strength * (1 - data), 0, 1)

    red_data = brighten_background(red_data)
    green_data = brighten_background(green_data)
    blue_data = brighten_background(blue_data)

    rgb_image = np.stack([red_data, green_data, blue_data], axis=-1)

    def enhance_saturation(image, intensity=1.6):
        mean_intensity = image.mean(axis=-1, keepdims=True)
        return np.clip(mean_intensity + intensity * (image - mean_intensity), 0, 1)

    rgb_image = enhance_saturation(rgb_image)

    plt.figure(figsize=(10, 10))
    plt.imshow(rgb_image, origin='lower')
    plt.axis('off')
    plt.title(f"{target} - Image RGB avec couleurs chaudes")
    plt.show()

if __name__ == "__main__":
    target_name = "Andromeda Galaxy"
    survey_list = ["2MASS-K", "2MASS-H", "2MASS-J"]
    create_warm_rgb_image(target_name, survey_list)
