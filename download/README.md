# Descarga de datos del HMI


Se descargan datos mediante la librería Fido (toca tener instalar instalado los paquetes sunpy, drms, zeep).

Para ello, escribir en la terminal

-  ```pip install sunpy drms zeep```

Es recomendable tener instalado [anaconda](https://www.anaconda.com/products/distribution).


## Librerías 

- sunpy
- astropy


```python
from sunpy.net import Fido         # Para descargar datos
from sunpy.net import attrs as a   # Para seleccionar observable físico
import astropy.units as u          # Para trabajar en unidades adecuadas
```

## Acceso base de datos

El formato temporal para descargar los archivos es:

```python
    a.Time('año/mes/día hh:mm:ss')
```

Así queda:

```python
result = Fido.search(a.Time('2011/07/30 02:08:00', '2011/07/30 02:10:00'),
                     a.Instrument.hmi, a.Physobs.intensity)
```

Para descargar otros observables:
```python
    a.Instrument.hmi, a.Physobs.los_velocity
    a.Instrument.hmi, a.Physobs.los_magnetic_field
    a.Instrument.aia, a.Wavelength(171*u.angstrom) #131, 94, 304 Å...
```

## Descarga de archivos


Ahora se descargan los datos del servidor.

En `path` colocar la carpeta donde se descargan las imágenes.

`max_conn` es el número máximo de archivos para descargar en paralelo



```python
downloaded_file = Fido.fetch(result, path='~/hmi/{file}', max_conn=50)
```

---

# Descompresión fits

Dado que el servidor de donde se descargan los datos maneja grandes cantidades de información, los archivos suelen estar comprimidos. 
En este caso, el algoritmo de compresión que se usa es *The Rice compression algorithm*. Se muestra como descomprimirlos.

Para ello, se puede descargar cfitsio desde los repositorios de Linux:

- Ubuntu/Debian/Mint: `sudo apt install cfitsio`
- Arch Linux/Manjaro: `sudo pacman -Syu cfitsio`
- Fedora: `sudo dnf install cfitsio`

Luego, acceder a la carpeta donde están los datos descargados y abrir una terminal allí.
En dicha terminal escribir las siguientes líneas:

```bash
    rename '.fits' '.fits.fz' *.fits   # Para renombrarlos
    funpack -E 1 -v *.fits.fz          # Para descomprimir
    rm *.fz                            # Para eliminar los .fz
```
