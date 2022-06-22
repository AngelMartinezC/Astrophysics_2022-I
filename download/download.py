from sunpy.net import Fido, attrs as a
import astropy.units as u

# Se selecciona la fecha en que se quiere descargar la imagen
result = Fido.search(a.Time('2011/07/30 02:08:00', '2011/07/30 02:10:00'),
                     a.Instrument.hmi, a.Physobs.intensity)

# Se realiza la descarga de imágenes en paralelo
downloaded_file = Fido.fetch(result, path='~/hmi/{file}', max_conn=10)
print(downloaded_file)
