from astropy.io import fits
import matplotlib.pyplot as plt

data = fits.getdata('Tarantula_Nebula-oiii.fit')


plt.imshow(data, cmap='gray')
plt.colorbar()
plt.show()