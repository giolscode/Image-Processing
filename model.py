import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import make_lupton_rgb, AsinhStretch, PercentileInterval, ImageNormalize
import numpy as np

class FitsModel:
    
    def __init__(self):
        self.red_filter = None
        self.green_filter = None
        self.blue_filter = None

    def load_fits(self, red, green, blue):
        self.red_filter = red
        self.green_filter = green
        self.blue_filter = blue

    def process_fits(self, output_path="output_rgb.png"):
        if not self.red_filter or not self.green_filter or not self.blue_filter:
            raise ValueError("Les fichiers FITS ne sont pas chargés.")

        # Créer l'image RGB sombre
        rgb_image = create_realistic_dark_rgb_image(self.red_filter, self.green_filter, self.blue_filter, stretch=0.3, dark_factor=0.8)
        plt.imsave(output_path, rgb_image, cmap='gray')
        return output_path
    
def clean_data(data, clip_percentile=99.5): 
    max_value = np.percentile(data, clip_percentile)
    data[data > max_value] = max_value
    data[data < 0] = 0  
    return data

def create_realistic_dark_rgb_image(red_file, green_file, blue_file, stretch=0.3, dark_factor=0.7):
    
    # Charger et nettoyer les données FITS
    pix_red = clean_data(fits.getdata(red_file))
    pix_green = clean_data(fits.getdata(green_file))
    pix_blue = clean_data(fits.getdata(blue_file))

    # Appliquer une normalisation par percentile et un AsinhStretch
    interval = PercentileInterval(99.5) 
    norm_red = ImageNormalize(pix_red, interval=interval, stretch=AsinhStretch())
    norm_green = ImageNormalize(pix_green, interval=interval, stretch=AsinhStretch())
    norm_blue = ImageNormalize(pix_blue, interval=interval, stretch=AsinhStretch())

    # Ajuster les pondérations des canaux pour un rendu plus réaliste
    scaled_red = norm_red(pix_red) * 1.3  
    scaled_green = norm_green(pix_green) * 1.0  
    scaled_blue = norm_blue(pix_blue) * 0.3  

    # Réduire l'intensité globale pour un effet plus équilibré
    scaled_red *= dark_factor
    scaled_green *= dark_factor
    scaled_blue *= dark_factor

    # Normalisation finale pour garantir que les valeurs sont dans [0, 1]
    scaled_red = np.clip(scaled_red, 0, 1)
    scaled_green = np.clip(scaled_green, 0, 1)
    scaled_blue = np.clip(scaled_blue, 0, 1)

    # Créer l'image RGB
    rgb_image = np.stack((scaled_red, scaled_green, scaled_blue), axis=-1)
    
    return rgb_image