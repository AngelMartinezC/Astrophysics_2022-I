# Importación librerías
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
from sunpy.map import Map

# Increase font
plt.rcParams.update({'font.size': 13})


# -- Se abre una imagen FITS. Esta consiste en un array de datos (números)
# -- acompañados de información asociada al archivo (header).

# -- Acá va el nombre de la imagen
mapa = Map("hmi.ic_45s.2011.07.30_01_25_30_TAI.continuum.fits")

image = mapa.data              # Se seleccionan únicamente los datos
rsun  = mapa.meta["RSUN_OBS"]  # Radio del Sol
scale = mapa.meta["CDELT1"]    # Resolución
xc    = mapa.meta['CRPIX1']    # Centro del disco solar en pixeles en x
yc    = mapa.meta['CRPIX2']    # Centro del disco solar en pixeles en y
naxis = mapa.meta['NAXIS1']    # Número de píxeles en la dirección x
date  = mapa.meta['DATE-OBS']  # Fecha de observación

# -- Se crea un array con los ángulos entre -90° y 90°
ANGLE = np.linspace(-np.pi/2,np.pi/2,1000)

def model1(tao):
    """
    Calcula la gráfica de intensidad teórica con oscurecimiento del limbo 
    para un caso sencillo de un cuerpo emitiendo radiación.
    **Inputs**:
        tao {float} -- Optical thickness: profundidad óptica.
    **Outputs**:
        {list} -- Lista con los valores del la intensidad como función del 
        ángulo.
    """
    # -- Se crea una lista vacía para agregar los valores de la intensidad
    TEO = []
    # Intensidad específica para el centro del disco solar promedio:
    I0 = np.mean(image[int(yc)-10:int(yc)+10,int(xc)-10:int(xc)+10]) 
    for theta in ANGLE:
        f = I0*np.exp(-tao*(1/np.cos(theta)-1))
        TEO.append(f)
    return TEO

def model2(tao,B1,B2):
    """
    Calcula la gráfica de intensidad teórica con oscurecimiento del limbo 
    para una atmósfera que tanto emite radiación como también la absorbe.
    **Inputs**:
        tao {float} -- Optical thickness: profundidad óptica.
        B1 {float} -- Intensidad específica de cuerpo negro.
        B2 {float} -- Planckiana, función fuente de la atmósfera (suposición).
    **Outputs**:
        {list} -- Lista con los valores del la intensidad como función del 
        ángulo.
    """
    # -- Se crea una lista vacía para agregar los valores de la intensidad
    TEO = [] 
    # Intensidad específica para el centro del disco solar promedio:
    I0 = np.mean(image[int(yc)-10:int(yc)+10,int(xc)-10:int(xc)+10]) 
    for theta in ANGLE:
        # Intensidad como función del ángulo theta:
        f1 = I0*((B1-B2)*np.exp(-tao/np.cos(theta))+B2)
        f2 = ((B1-B2)*np.exp(-tao)+B2)
        TEO.append(f1/f2)
    return TEO

def model3(u,v):
    """
    Calcula la gráfica de intensidad teórica con oscurecimiento del limbo 
    para una función fuente como función de la profundidad.
    **Inputs**:
        u {float} -- Primer coeficiente de oscurecimiento del limbo.
        y {float} -- Segundo coeficiente de oscurecimiento del limbo.
    **Outputs**:
        {list} -- Lista con los valores del la intensidad como función del 
        ángulo. 
    """
    a0 = 1-u-v
    a1 = u
    a2 = v/2
    # -- Se crea una lista vacía para agregar los valores de la intensidad
    TEO = [] 
    # Intensidad específica para el centro del disco solar promedio:
    I0 = np.mean(image[int(yc)-10:int(yc)+10,int(xc)-10:int(xc)+10]) 
    for theta in ANGLE:
        f = I0*(a0 + a1*np.cos(theta) + 2*a2*(np.cos(theta))**2)
        TEO.append(f)
    return TEO




# ---------------------------------------------------------
# -- GRÁFICA --------


# -- Se crea un array de datos con los píxeles de la imagen
pixel = np.arange(0,naxis,1)

# -- La siguiente lista consta de los valores de la intensidad del continuo
# -- para una línea horizontal centrada en y=yc y que tiene un ancho de
# -- 20 píxeles.
line = [np.mean(image[i,int(xc)-10:int(xc)+10]) for i in pixel] 

fig, ax = plt.subplots(figsize=(9,6))
plt.subplots_adjust(left=0.30,right=0.98, bottom=0.33, top=0.94)
norm = 2*ANGLE/np.pi  # Radio normalizado del Sol
tao = 0.5  # Valores aleatorios de tao, B1 y B2
B1  = 1
B2  = 0.7
u = 0.1
v = 0.2
s1 = model1(tao)
s2 = model2(tao,B1,B2)
s3 = model3(u,v)
#s1 = model2(tao,B1+0.1,B2+0.1)
# -- A continuación, se centran los datos en el eje x de tal forma que 
# -- queden centrados en el cero
plt.plot((pixel-xc)/(rsun/scale),line,'tab:grey',alpha=0.6,lw=2,
        label='Corte a x=%d píxeles'%int(xc))
m, = ax.plot(norm, s1, lw=2.5, color='red'      )#, label='Modelo 1')
l, = ax.plot(norm, s2, lw=2.5, color='tab:blue' )#, label='Modelo 2')
p, = ax.plot(norm, s3, lw=2.5, color='tab:green')#, label='Modelo 3')
plt.title('HMI Continuum '+date)
plt.legend(loc=8)
plt.grid()
plt.xticks([-1,-0.5,0,0.5,1],[0,0.5,1,0.5,0])
plt.xlabel(r"$\mu = \cos \theta$")
plt.ylabel("Intensidad [# cuentas]")


# -- Se realizan los sliders. 

axcolor = 'lightgoldenrodyellow'
rax = plt.axes((0.01,0.52,0.15,0.15))
check = CheckButtons(rax, ('Modelo 1', 'Modelo 2', 'Modelo 3'), 
        (True, True, True))
c = ['r', 'tab:blue', 'tab:green']    
#[rec.set_facecolor(c[i]) for i, rec in enumerate(check.rectangles)]
for i, rec in enumerate(check.rectangles):
    rec.set_facecolor(c[i]) 
    rec.set_alpha(0.6)

axtao = plt.axes([0.08, 0.03, 0.35, 0.03], facecolor=axcolor)
axB2  = plt.axes([0.08, 0.09, 0.35, 0.03], facecolor=axcolor)
axB1  = plt.axes([0.08, 0.15, 0.35, 0.03], facecolor=axcolor)
stao = Slider(axtao, r"$\tau_\nu$", 0.01, 2.0, valinit=tao)
sB1 = Slider(axB1, r'$B_{\nu,1}$', 0.0, 7.0, valinit=B1)
sB2 = Slider(axB2, r'$B_{\nu,2}$', 0.0, 7.0, valinit=B2)

axtao = plt.axes([0.55, 0.15, 0.35, 0.03], facecolor=axcolor)
ttao = Slider(axtao, r"$\tau_\nu$", 0.01, 2.0, valinit=tao, color='red')

axu = plt.axes([0.55, 0.08, 0.35, 0.03], facecolor=axcolor)
axv = plt.axes([0.55, 0.03, 0.35, 0.03], facecolor=axcolor)
m3u = Slider(axu, r"$u'$", -0.50, 1.0, valinit=u, color='tab:green')
m3v = Slider(axv, r"$v'$", -0.50, 1.0, valinit=v, color='tab:green')

def update(val):
    tao = stao.val
    tao1 = ttao.val
    B1 = sB1.val
    B2 = sB2.val
    u = m3u.val
    v = m3v.val
    l.set_ydata(model2(tao,B1,B2))
    m.set_ydata(model1(tao1))
    p.set_ydata(model3(u,v))
    fig.canvas.draw_idle()
stao.on_changed(update)
ttao.on_changed(update)
sB1.on_changed(update)
sB2.on_changed(update)
m3u.on_changed(update)
m3v.on_changed(update)
resetax = plt.axes([0.02, 0.225, 0.1, 0.05])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.875')
def reset(event):
    stao.reset()
    sB1.reset()
    sB2.reset()
    ttao.reset()
    m3u.reset()
    m3v.reset()
button.on_clicked(reset)

#rax = plt.axes([0.02, 0.5, 0.12, 0.15], facecolor=axcolor)
#radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)
#def colorfunc(label):
#    l.set_color(label)
#    fig.canvas.draw_idle()
#radio.on_clicked(colorfunc)


def check_on_clicked(label):
    if label == 'Modelo 1':
        m.set_visible(not m.get_visible())
        update(update)
    elif label == 'Modelo 2':
        l.set_visible(not l.get_visible())
        update(update)
    elif label == 'Modelo 3':
        p.set_visible(not p.get_visible())
        update(update)
    plt.draw()
check.on_clicked(check_on_clicked)



plt.show()

