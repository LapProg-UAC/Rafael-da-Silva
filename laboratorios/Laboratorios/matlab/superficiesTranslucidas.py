import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Grade
x = np.linspace(-5, 5, 150)
y = np.linspace(-5, 5, 150)
X, Y = np.meshgrid(x, y)

# Distância radial
R = np.sqrt(X**2 + Y**2)

# Superfícies
Z1 = np.sin(R)
Z2 = np.cos(R)
Z3 = np.sin(R) + np.cos(R) / 2   # terceira camada

# Figura
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Camada 1: azul -> roxo
ax.plot_surface(
    X, Y, Z1,
    cmap='autumn',
    alpha=0.75,
    edgecolor='none'
)

# Camada 2: azul -> verde
ax.plot_surface(
    X, Y, Z2,
    cmap='winter',
    alpha=0.55,
    edgecolor='none'
)

# Camada 3: vermelho -> laranja
ax.plot_surface(
    X, Y, Z3,
    cmap='gnuplot_r',
    alpha=0.65,
    edgecolor='none'
)

# Labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3 Superfícies com Gradientes de Cor')

plt.show()