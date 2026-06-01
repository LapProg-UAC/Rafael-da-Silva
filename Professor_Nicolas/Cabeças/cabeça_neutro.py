import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LightSource

# --- CONFIGURAÇÕES ---
RES = 300  # Resolução alta para suavidade
x = np.linspace(-1, 1, RES)
y = np.linspace(-1.3, 1.2, RES)
X, Y = np.meshgrid(x, y)

def surf(x0, y0, sx, sy, amp):
    """ Cria volumes suaves (Gaussianas) para as feições """
    return amp * np.exp(-( ((X-x0)**2/(2*sx**2)) + ((Y-y0)**2/(2*sy**2)) ))

# --- CONSTRUINDO O ROSTO ---
# 1. Base da Cabeça (Um ovo suave)
Z = 0.4 * np.exp(-( (X**2/0.5) + ((Y-0.2)**2/0.8) ))

# 2. Testa e Sobrancelhas (Expressão NEUTRA)
# Sobrancelhas "pesadas" e caídas no centro
Z += surf(-0.2, 0.4, 0.15, 0.07, 0.08) # Esq
Z += surf(0.2, 0.4, 0.15, 0.07, 0.08)  # Dir
# Vinco de preocupação entre as sobrancelhas
Z -= surf(0, 0.45, 0.05, 0.1, 0.05)

# 3. Cavidades dos Olhos (Buracos suaves)
Z -= surf(-0.2, 0.3, 0.12, 0.1, 0.1)
Z -= surf(0.2, 0.3, 0.12, 0.1, 0.1)

# 4. Nariz (Mais largo e humano, não pontiagudo)
Z += surf(0, 0.05, 0.08, 0.3, 0.22) # Ponte do nariz
Z += surf(0, -0.2, 0.12, 0.12, 0.15) # Ponta do nariz e narinas

# 5. Maçãs do Rosto
Z += surf(-0.35, 0.0, 0.2, 0.2, 0.05)
Z += surf(0.35, 0.0, 0.2, 0.2, 0.05)

# 6. BOCA NEUTRA (Cantos horizontais)
# Lábio superior
Z += surf(0, -0.45, 0.18, 0.04, 0.06)
# "Puxando" os cantos da boca para baixo para parecer chateado
Z -= surf(-0.2, -0.55, 0.08, 0.08, 0.05)
Z -= surf(0.2, -0.55, 0.08, 0.08, 0.05)

# 7. Queixo
Z += surf(0, -0.75, 0.2, 0.15, 0.1)

# 8. Pescoço e Ombros (Base do busto)
Z += 0.15 * np.exp(-( (X**2/2.0) + ((Y+1.0)**2/0.5) ))

# --- RENDERIZAÇÃO ---
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')

# Cor de "estátua de carne"
color_busto = np.array([0.7, 0.55, 0.5])

def update(frame):
    ax.clear()
    ax.set_facecolor('black')
    
    # Luz vindo da diagonal superior para criar sombras nos olhos e boca
    # A luz se move suavemente para dar efeito 3D
    azim_luz = 180 + 30 * np.sin(frame * 2 * np.pi / 40)
    ls = LightSource(azdeg=azim_luz, altdeg=45)
    
    rgb = np.ones(Z.shape + (3,)) * color_busto
    shaded = ls.shade_rgb(rgb, Z, blend_mode='soft', vert_exag=1.5)

    # Plotar a superfície
    # A câmera está configurada para olhar de frente (elev=90)
    surf_plot = ax.plot_surface(X, Y, Z, facecolors=shaded,
                                linewidth=0, antialiased=True, shade=False)

    # Câmera: Olhando diretamente de cima (que agora é a frente do rosto)
    ax.view_init(elev=85, azim=-90)
    
    # Limites para focar no rosto
    ax.set_xlim(-0.8, 0.8)
    ax.set_ylim(-1.1, 1.0)
    ax.set_zlim(-0.1, 0.8)
    ax.set_axis_off()

print("Esculpindo rosto neutro frontal...")
ani = FuncAnimation(fig, update, frames=40, interval=100)

# Salvar
gif_name = "neutro.gif"
ani.save(gif_name, writer="pillow", fps=15)
plt.close()

print(f"Pronto! O arquivo '{gif_name}' foi gerado.")