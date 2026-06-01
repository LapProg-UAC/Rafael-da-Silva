
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LightSource

# --- CONFIGURAÇÕES ---
RES = 300  
x = np.linspace(-1, 1, RES)
y = np.linspace(-1.3, 1.2, RES)
X, Y = np.meshgrid(x, y)

def surf(x0, y0, sx, sy, amp):
    """ Cria volumes suaves (Gaussianas) para as feições """
    return amp * np.exp(-( ((X-x0)**2/(2*sx**2)) + ((Y-y0)**2/(2*sy**2)) ))

# --- CONSTRUINDO O ROSTO ---
# 1. Base da Cabeça
Z = 0.4 * np.exp(-( (X**2/0.5) + ((Y-0.2)**2/0.8) ))

# 2. Testa e Sobrancelhas (SURPRESO - Muito altas e arqueadas)
Z += surf(-0.25, 0.55, 0.15, 0.08, 0.08) # Esq
Z += surf(0.25, 0.55, 0.15, 0.08, 0.08)  # Dir

# 3. Cavidades dos Olhos (Mais abertas)
Z -= surf(-0.2, 0.3, 0.15, 0.12, 0.12)
Z -= surf(0.2, 0.3, 0.15, 0.12, 0.12)

# 4. Nariz (Inalterado)
Z += surf(0, 0.05, 0.08, 0.3, 0.22) 
Z += surf(0, -0.2, 0.12, 0.12, 0.15) 

# 5. Maçãs do Rosto (Puxadas para baixo pela mandíbula)
Z += surf(-0.35, -0.2, 0.2, 0.2, 0.04)
Z += surf(0.35, -0.2, 0.2, 0.2, 0.04)

# 6. BOCA EM "O" (Buraco profundo e oval)
# Subtração de volume para criar o interior da boca aberta
Z -= surf(0, -0.55, 0.12, 0.18, 0.25)
# Pequeno relevo ao redor para simular os lábios esticados
Z += surf(0, -0.55, 0.15, 0.22, 0.04)

# 7. Queixo (Ligeiramente mais baixo para acompanhar a boca)
Z += surf(0, -0.85, 0.2, 0.15, 0.08)

# 8. Pescoço e Ombros
Z += 0.15 * np.exp(-( (X**2/2.0) + ((Y+1.0)**2/0.5) ))

# --- RENDERIZAÇÃO ---
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')

color_busto = np.array([0.7, 0.55, 0.5])

def update(frame):
    ax.clear()
    ax.set_facecolor('black')
    
    azim_luz = 180 + 30 * np.sin(frame * 2 * np.pi / 40)
    ls = LightSource(azdeg=azim_luz, altdeg=45)
    
    rgb = np.ones(Z.shape + (3,)) * color_busto
    shaded = ls.shade_rgb(rgb, Z, blend_mode='soft', vert_exag=1.5)

    surf_plot = ax.plot_surface(X, Y, Z, facecolors=shaded,
                                linewidth=0, antialiased=True, shade=False)

    ax.view_init(elev=85, azim=-90)
    
    ax.set_xlim(-0.8, 0.8)
    ax.set_ylim(-1.1, 1.0)
    ax.set_zlim(-0.1, 0.8)
    ax.set_axis_off()

print("Esculpindo rosto surpreso...")
ani = FuncAnimation(fig, update, frames=40, interval=100)

gif_name = "surpreso.gif"
ani.save(gif_name, writer="pillow", fps=15)
plt.close()

print(f"Pronto! O arquivo '{gif_name}' foi gerado.")