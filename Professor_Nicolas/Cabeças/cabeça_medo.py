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

# 2. Testa e Sobrancelhas (MEDO - Altas no centro e próximas)
# Parte interna das sobrancelhas elevada e junta
Z += surf(-0.12, 0.52, 0.1, 0.08, 0.12) # Interna Esq
Z += surf(0.12, 0.52, 0.1, 0.08, 0.12)  # Interna Dir
# Parte externa caindo levemente
Z += surf(-0.35, 0.45, 0.15, 0.07, 0.04) 
Z += surf(0.35, 0.45, 0.15, 0.07, 0.04)  

# 3. Cavidades dos Olhos (Arregalados - mais largos e profundos)
Z -= surf(-0.2, 0.32, 0.15, 0.12, 0.15)
Z -= surf(0.2, 0.32, 0.15, 0.12, 0.15)

# 4. Nariz
Z += surf(0, 0.05, 0.08, 0.3, 0.22) 
Z += surf(0, -0.2, 0.12, 0.12, 0.15) 

# 5. Maçãs do Rosto (Tensas e baixas)
Z += surf(-0.35, -0.1, 0.2, 0.2, 0.05)
Z += surf(0.35, -0.1, 0.2, 0.2, 0.05)

# 6. BOCA COM MEDO (Esticada horizontalmente e entreaberta)
# Abertura da boca (oval horizontal)
Z -= surf(0, -0.52, 0.22, 0.08, 0.15)
# Tensão nos cantos da boca puxando para baixo/fora
Z -= surf(-0.3, -0.6, 0.1, 0.1, 0.06)
Z -= surf(0.3, -0.6, 0.1, 0.1, 0.06)

# 7. Queixo (Caído pela mandíbula aberta)
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
    
    # Luz oscilante para dar dramaticidade ao rosto assustado
    azim_luz = 180 + 20 * np.sin(frame * 2 * np.pi / 40)
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

print("Esculpindo rosto com expressão de medo...")
ani = FuncAnimation(fig, update, frames=40, interval=100)

gif_name = "medo.gif"
ani.save(gif_name, writer="pillow", fps=15)
plt.close()

print(f"Pronto! O arquivo '{gif_name}' foi gerado.")