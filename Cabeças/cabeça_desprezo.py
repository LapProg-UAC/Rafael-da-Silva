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

# 2. Testa e Sobrancelhas (Assimetria: sobrancelha direita levemente arqueada)
Z += surf(-0.25, 0.45, 0.15, 0.07, 0.06) # Esq
Z += surf(0.25, 0.50, 0.15, 0.08, 0.09)  # Dir (Mais alta)

# 3. Cavidades dos Olhos
Z -= surf(-0.2, 0.3, 0.12, 0.1, 0.1)
Z -= surf(0.2, 0.32, 0.12, 0.1, 0.08)

# 4. Nariz
Z += surf(0, 0.05, 0.08, 0.3, 0.22) 
Z += surf(0, -0.2, 0.12, 0.12, 0.15) 

# 5. Maçãs do Rosto (Lado direito bem mais alto acompanhando a boca)
Z += surf(-0.35, -0.1, 0.2, 0.2, 0.04)  # Esq
Z += surf(0.35, 0.05, 0.22, 0.25, 0.15) # Dir (Bem projetada)

# 6. BOCA COM CANTO MUITO ELEVADO (Desprezo Acentuado)
# Lábio central
Z += surf(0, -0.48, 0.2, 0.04, 0.06)
# Canto esquerdo: Neutro/Caído
Z -= surf(-0.28, -0.55, 0.1, 0.1, 0.05)
# Canto direito: ELEVAÇÃO EXTREMA
# Subimos o y para -0.25 (quase na linha do nariz) e aumentamos a amp para 0.25
Z += surf(0.3, -0.25, 0.12, 0.12, 0.25)

# 7. Queixo
Z += surf(0, -0.75, 0.2, 0.15, 0.1)

# 8. Pescoço e Ombros
Z += 0.15 * np.exp(-( (X**2/2.0) + ((Y+1.0)**2/0.5) ))

# --- RENDERIZAÇÃO ---
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')

color_busto = np.array([0.7, 0.55, 0.5])

def update(frame):
    ax.clear()
    ax.set_facecolor('black')
    
    # Luz oscilante para destacar o vinco profundo no canto da boca
    azim_luz = 180 + 45 * np.sin(frame * 2 * np.pi / 40)
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

print("Acentuando o canto da boca no desprezo...")
ani = FuncAnimation(fig, update, frames=40, interval=100)

gif_name = "desprezo.gif"
ani.save(gif_name, writer="pillow", fps=15)
plt.close()

print(f"Pronto! O desprezo acentuado está no arquivo '{gif_name}'.")