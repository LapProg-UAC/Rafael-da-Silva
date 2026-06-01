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

# 2. Testa e Sobrancelhas (Muito relaxadas e arqueadas)
Z += surf(-0.25, 0.48, 0.18, 0.08, 0.06) 
Z += surf(0.25, 0.48, 0.18, 0.08, 0.06)  

# 3. Cavidades dos Olhos
Z -= surf(-0.2, 0.3, 0.12, 0.1, 0.1)
Z -= surf(0.2, 0.3, 0.12, 0.1, 0.1)

# 4. Nariz
Z += surf(0, 0.05, 0.08, 0.3, 0.22) 
Z += surf(0, -0.2, 0.12, 0.12, 0.15) 

# 5. Maçãs do Rosto (Bem altas e projetadas para frente pelo sorriso)
Z += surf(-0.38, -0.05, 0.22, 0.25, 0.18)
Z += surf(0.38, -0.05, 0.22, 0.25, 0.18)

# 6. BOCA COM CURVATURA EXTREMA
# Lábio inferior/centro da boca (Posição mais baixa)
Z += surf(0, -0.58, 0.22, 0.06, 0.08)

# Cantos da boca (Subindo muito em direção às bochechas)
# Note que o y (-0.3) é bem mais alto que o centro (-0.58)
Z += surf(-0.35, -0.32, 0.12, 0.12, 0.18)
Z += surf(0.35, -0.32, 0.12, 0.12, 0.18)

# 7. Queixo
Z += surf(0, -0.8, 0.2, 0.15, 0.1)

# 8. Pescoço e Ombros
Z += 0.15 * np.exp(-( (X**2/2.0) + ((Y+1.0)**2/0.5) ))

# --- RENDERIZAÇÃO ---
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')

color_busto = np.array([0.7, 0.55, 0.5])

def update(frame):
    ax.clear()
    ax.set_facecolor('black')
    
    # A luz oscila para mostrar o relevo da curva do sorriso
    azim_luz = 180 + 30 * np.sin(frame * 2 * np.pi / 40)
    ls = LightSource(azdeg=azim_luz, altdeg=45)
    
    rgb = np.ones(Z.shape + (3,)) * color_busto
    shaded = ls.shade_rgb(rgb, Z, blend_mode='soft', vert_exag=1.5)

    ax.plot_surface(X, Y, Z, facecolors=shaded,
                    linewidth=0, antialiased=True, shade=False)

    ax.view_init(elev=85, azim=-90)
    
    ax.set_xlim(-0.8, 0.8)
    ax.set_ylim(-1.1, 1.0)
    ax.set_zlim(-0.1, 0.8)
    ax.set_axis_off()

print("Esculpindo sorriso com curva acentuada...")
ani = FuncAnimation(fig, update, frames=40, interval=100)

gif_name = "feliz.gif"
ani.save(gif_name, writer="pillow", fps=15)
plt.close()

print(f"Pronto! O rosto feliz está no arquivo '{gif_name}'.")