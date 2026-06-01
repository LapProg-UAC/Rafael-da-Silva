import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LightSource

# --- CONFIGURAÇÕES ---
RES = 400  
x = np.linspace(-1, 1, RES)
y = np.linspace(-1, 1, RES)
X, Y = np.meshgrid(x, y)

def ponto_gauss(x0, y0, sigma, amp):
    """ Cria um ponto de volume arredondado """
    return amp * np.exp(-( (X-x0)**2 + (Y-y0)**2 ) / (2 * sigma**2))

# --- ESCULPINDO AS PRESAS (FANGS) ---
Z = np.zeros_like(X)

def desenhar_presa(x_offset, direcao):
    global Z
    # Criamos a presa usando 50 "camadas" que vão diminuindo
    passos = 60
    for i in range(passos):
        t = i / passos  # de 0 a 1
        
        # Equação da curva (parábola suave)
        curr_y = 0.6 - t * 1.1             # Vai de 0.6 até -0.5
        curr_x = x_offset + direcao * (t**2) * 0.2 # Curva para dentro
        
        # Afilamento: sigma e amp diminuem com t
        curr_sigma = 0.08 * (1 - t*0.9)
        curr_amp = 0.4 * (1 - t*0.8)
        
        # Adiciona o volume usando o máximo para manter a superfície lisa
        Z = np.maximum(Z, ponto_gauss(curr_x, curr_y, curr_sigma, curr_amp))

# Desenha presa esquerda e direita
desenhar_presa(-0.4, 1)  # x_offset = -0.4, curva para a direita (1)
desenhar_presa(0.4, -1)  # x_offset = 0.4, curva para a esquerda (-1)

# --- DEFINIÇÃO DE CORES ---
color_base = np.array([0.0, 0.0, 0.0]) # Preto absoluto
color_fang = np.array([1.0, 1.0, 1.0]) # Branco puro

# Criar mapa RGB (Branco onde houver relevo, preto no fundo)
Z_mask = np.clip(Z * 10, 0, 1) # Sensibilidade alta para pintar a ponta fina
rgb_map = (1 - Z_mask[..., None]) * color_base + Z_mask[..., None] * color_fang

# --- RENDERIZAÇÃO ---
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')

def update(frame):
    ax.clear()
    ax.set_facecolor('black')
    
    # Luz dramática vindo de cima para brilhar no "marfim" das presas
    azim_luz = 180 + 30 * np.sin(frame * 2 * np.pi / 40)
    ls = LightSource(azdeg=azim_luz, altdeg=45)
    
    shaded = ls.shade_rgb(rgb_map, Z, blend_mode='soft', vert_exag=2.0)

    ax.plot_surface(X, Y, Z, facecolors=shaded,
                    linewidth=0, antialiased=True, shade=False)

    # Vista levemente inclinada para ver a curvatura e a ponta
    ax.view_init(elev=60, azim=-90)
    
    ax.set_xlim(-0.8, 0.8)
    ax.set_ylim(-0.8, 0.8)
    ax.set_zlim(0, 0.5)
    ax.set_axis_off()

print("Esculpindo presas de cobra venenosa...")
ani = FuncAnimation(fig, update, frames=40, interval=50)

gif_name = "snake_fangs_3d.gif"
ani.save(gif_name, writer="pillow", fps=20)
plt.close()

print(f"Pronto! As presas foram geradas no arquivo '{gif_name}'.")