import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LightSource

# --- CONFIGURAÇÕES ---
RES = 400  
x = np.linspace(-1.2, 1.2, RES)
y = np.linspace(-1, 1, RES)
X, Y = np.meshgrid(x, y)

def segmento(x1, y1, x2, y2, sigma, amp):
    dx, dy = x2 - x1, y2 - y1
    l2 = dx**2 + dy**2
    if l2 == 0: return amp * np.exp(-((X-x1)**2 + (Y-y1)**2) / (2 * sigma**2))
    t = ((X - x1) * dx + (Y - y1) * dy) / l2
    t = np.clip(t, 0, 1)
    dist_sq = (X - (x1 + t * dx))**2 + (Y - (y1 + t * dy))**2
    return amp * np.exp(-dist_sq / (2 * sigma**2))

# --- ESCULPINDO 9 2 6 ---
Z = np.zeros_like(X)
S = 0.05  
A = 0.25  

def add_seg(z_layer, x1, y1, x2, y2):
    return np.maximum(z_layer, segmento(x1, y1, x2, y2, S, A))

# Coordenadas dos números (9, 2, 6)
# 9
Z = add_seg(Z, -0.9, 0.5, -0.5, 0.5); Z = add_seg(Z, -0.9, 0.5, -0.9, 0.0)
Z = add_seg(Z, -0.5, 0.5, -0.5, -0.5); Z = add_seg(Z, -0.9, 0.0, -0.5, 0.0)
# 2
Z = add_seg(Z, -0.2, 0.5, 0.2, 0.5); Z = add_seg(Z, 0.2, 0.5, 0.2, 0.0)
Z = add_seg(Z, -0.2, 0.0, 0.2, 0.0); Z = add_seg(Z, -0.2, 0.0, -0.2, -0.5)
Z = add_seg(Z, -0.2, -0.5, 0.2, -0.5)
# 6
Z = add_seg(Z, 0.5, 0.5, 0.9, 0.5); Z = add_seg(Z, 0.5, 0.5, 0.5, -0.5)
Z = add_seg(Z, 0.5, 0.0, 0.9, 0.0); Z = add_seg(Z, 0.9, 0.0, 0.9, -0.5)
Z = add_seg(Z, 0.5, -0.5, 0.9, -0.5)

# --- DEFINIÇÃO DE CORES ---
color_base = np.array([0.15, 0.15, 0.18]) # Cinza chumbo escuro
color_num  = np.array([1.0, 0.8, 0.1])    # Dourado vibrante

# Criar o mapa RGB baseado na altura Z
# Normalizamos Z entre 0 e 1 para usar como máscara de cor
Z_mask = (Z / A)
Z_mask = np.clip(Z_mask, 0, 1)

# Interpolação Linear entre as duas cores: (1-mask)*Base + mask*Num
rgb_map = (1 - Z_mask[..., None]) * color_base + Z_mask[..., None] * color_num

# --- RENDERIZAÇÃO ---
fig = plt.figure(figsize=(10, 8), facecolor='black')
ax = fig.add_subplot(111, projection='3d')

def update(frame):
    ax.clear()
    ax.set_facecolor('black')
    
    # Luz giratória
    azim_luz = frame * (360 / 40)
    ls = LightSource(azdeg=azim_luz, altdeg=45)
    
    # Aplicar sombreamento ao mapa de cores que criamos
    # shaded = ls.shade_rgb(MAPA_DE_CORES, ALTURA, ...)
    shaded = ls.shade_rgb(rgb_map, Z, blend_mode='soft', vert_exag=1.5)

    ax.plot_surface(X, Y, Z, facecolors=shaded,
                    linewidth=0, antialiased=True, shade=False)

    ax.view_init(elev=55, azim=-90)
    
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-0.8, 0.8)
    ax.set_zlim(0, 0.5)
    ax.set_axis_off()

print("Colorindo base e números separadamente...")
ani = FuncAnimation(fig, update, frames=40, interval=50)

gif_name = "926_duas_cores.gif"
ani.save(gif_name, writer="pillow", fps=20)
plt.close()

print(f"Pronto! O arquivo '{gif_name}' foi gerado com cores distintas.")