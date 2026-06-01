import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LightSource

# --- CONFIGURAÇÕES ---
RES = 150  # Resolução da malha
FRAMES = 36 # Quantidade de quadros (360 graus / 10)

def sculpt(u, v, u_c, v_c, sigma_u, sigma_v, amplitude):
    """ Função para deformar a malha de forma orgânica """
    return amplitude * np.exp(-( (u - u_c*np.pi)**2/(2*sigma_u**2) + (v - v_c)**2/(2*sigma_v**2) ))

# Criar a malha UV
u = np.linspace(0, 2 * np.pi, RES)
v = np.linspace(0, np.pi, RES)
U, V = np.meshgrid(u, v)

# 1. FORMA BÁSICA DO BUSTO
R = np.ones_like(U)
f = 1.5 # Direção frontal (1.5 * PI)

# --- ESCULPINDO FEIÇÕES (Baseado na sua referência) ---
# Nariz: Ponte e ponta definida
R += sculpt(U, V, f, 1.4, 0.07, 0.35, 0.45) 
# Olhos: Cavidades profundas para realismo de luz
R -= sculpt(U, V, f-0.22, 1.25, 0.1, 0.12, 0.25) 
R -= sculpt(U, V, f+0.22, 1.25, 0.1, 0.12, 0.25)
# Mandíbula: Definida e quadrada
R += sculpt(U, V, f-0.45, 2.1, 0.2, 0.4, 0.2)
R += sculpt(U, V, f+0.45, 2.1, 0.2, 0.4, 0.2)
# Maçãs do rosto (Zigomáticos)
R += sculpt(U, V, f-0.35, 1.6, 0.15, 0.25, 0.15)
R += sculpt(U, V, f+0.35, 1.6, 0.15, 0.25, 0.15)
# Queixo e Lábios
R += sculpt(U, V, f, 2.5, 0.15, 0.15, 0.2) # Queixo
R += sculpt(U, V, f, 2.05, 0.2, 0.04, 0.1) # Lábio Sup.

# 2. CONVERSÃO PARA COORDENADAS 3D
X = R * np.cos(U) * np.sin(V)
Y = 1.2 * R * np.sin(U) * np.sin(V)
Z = 1.6 * R * np.cos(V)

# 3. BASE DO PESCOÇO E OMBROS (Achatamento e alargamento)
mask_base = V > 2.6
X[mask_base] *= 2.2 # Alarga para os ombros
Z[mask_base] -= 0.4 # Estabiliza a base

# --- RENDERIZAÇÃO ---
fig = plt.figure(figsize=(8, 8), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ls = LightSource(azdeg=225, altdeg=45) # Luz cinematográfica
color_sculpt = np.array([0.7, 0.65, 0.6]) # Tom de argila/pele

def update(frame):
    ax.clear()
    ax.set_facecolor('black')
    
    # Gerar sombreamento baseado na luz
    rgb = np.ones(Z.shape + (3,)) * color_sculpt
    shaded = ls.shade_rgb(rgb, Z, blend_mode='hsv', vert_exag=0.5)
    
    ax.plot_surface(X, Y, Z, facecolors=shaded, linewidth=0, antialiased=True, shade=False)
    
    ax.view_init(elev=15, azim=frame * 10)
    ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(-2.5, 2)
    ax.set_axis_off()

print("Cinzelando o busto no VS Code... Aguarde.")
ani = FuncAnimation(fig, update, frames=FRAMES, interval=100)

# Salvar o arquivo
gif_name = "busto_realista_3d.gif"
ani.save(gif_name, writer="pillow", fps=12)
plt.close()

print(f"Sucesso! O arquivo '{gif_name}' foi gerado na pasta do seu projeto.")