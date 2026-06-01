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

# --- CONSTRUINDO O "MAN FACE" (ROBLOX STYLE) ---
# 1. Base da Cabeça (Ligeiramente mais larga no topo)
Z = 0.42 * np.exp(-( (X**2/0.55) + ((Y-0.2)**2/0.8) ))

# 2. SOBRANCELHAS (O segredo do olhar)
# Sobrancelha esquerda (Mais reta e baixa)
Z += surf(-0.3, 0.45, 0.18, 0.05, 0.08)
# Sobrancelha direita (Mais arqueada e alta - Estilo Man Face)
Z += surf(0.3, 0.50, 0.18, 0.08, 0.10)

# 3. OLHOS (Semicerrados e marcantes)
# Cavidades mais horizontais e estreitas
Z -= surf(-0.25, 0.32, 0.15, 0.06, 0.08)
Z -= surf(0.25, 0.32, 0.15, 0.06, 0.08)

# 4. NARIZ (Ponte chiseled e firme)
Z += surf(0, 0.05, 0.07, 0.3, 0.22) 
Z += surf(0, -0.2, 0.12, 0.1, 0.15) 

# 5. MAÇÃS DO ROSTO (Acentuadas no lado do sorriso)
Z += surf(-0.35, -0.1, 0.18, 0.18, 0.05) # Lado neutro
Z += surf(0.38, 0.0, 0.22, 0.25, 0.12)  # Lado que sobe (sorriso)

# 6. BOCA "SMUG" (O Sorriso icônico)
# Lado Esquerdo da boca: Linha neutra/reta
Z += surf(-0.15, -0.48, 0.15, 0.03, 0.06)
# Lado Direito da boca: CURVA ACENTUADA PARA CIMA
Z += surf(0.3, -0.32, 0.12, 0.1, 0.20)
# Centro da boca conectando os dois
Z += surf(0, -0.45, 0.2, 0.04, 0.04)

# 7. QUEIXO MASCULINO (Largo e esculpido)
Z += surf(0, -0.8, 0.25, 0.18, 0.12)

# 8. Pescoço e Ombros
Z += 0.15 * np.exp(-( (X**2/2.0) + ((Y+1.0)**2/0.5) ))

# --- RENDERIZAÇÃO ---
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')

# Cor de pele clássica ou "estátua"
color_busto = np.array([0.75, 0.6, 0.5])

def update(frame):
    ax.clear()
    ax.set_facecolor('black')
    
    # Luz dramática vindo de cima/diagonal para marcar o maxilar
    azim_luz = 180 + 20 * np.sin(frame * 2 * np.pi / 40)
    ls = LightSource(azdeg=azim_luz, altdeg=50)
    
    rgb = np.ones(Z.shape + (3,)) * color_busto
    shaded = ls.shade_rgb(rgb, Z, blend_mode='soft', vert_exag=1.5)

    ax.plot_surface(X, Y, Z, facecolors=shaded,
                    linewidth=0, antialiased=True, shade=False)

    # Ângulo de câmera frontal clássico
    ax.view_init(elev=85, azim=-90)
    
    ax.set_xlim(-0.8, 0.8)
    ax.set_ylim(-1.1, 1.0)
    ax.set_zlim(-0.1, 0.8)
    ax.set_axis_off()

print("Esculpindo o lendário Man Face...")
ani = FuncAnimation(fig, update, frames=40, interval=100)

gif_name = "roblox.gif"
ani.save(gif_name, writer="pillow", fps=15)
plt.close()

print(f"Pronto! O 'Man Face' foi replicado no arquivo '{gif_name}'.")