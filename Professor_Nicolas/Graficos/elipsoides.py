import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parametric angles
u = np.linspace(0, 2 * np.pi, 60)
v = np.linspace(0, np.pi, 60)
u, v = np.meshgrid(u, v)

# Ellipsoid axes
a, b, c = 3, 2, 1.5

# Concentric scaling
scales = [1.0, 0.9, 0.8, 0.7, 0.6]

# Create figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Update function for animation
def update(frame):
    ax.clear()

    for scale in scales:
        A, B, C = a * scale, b * scale, c * scale
        X = A * np.sin(v) * np.cos(u)
        Y = B * np.sin(v) * np.sin(u)
        Z = C * np.cos(v)

        ax.plot_surface(X, Y, Z, alpha=0.3)

    ax.set_box_aspect([a, b, c])
    ax.set_axis_off()
    ax.view_init(elev=30, azim=frame)

# Animation
ani = FuncAnimation(
    fig,
    update,
    frames=np.linspace(0, 360, 60),
    interval=150
)

gif_path = 'elipsoide.gif'
ani.save(gif_path, writer='pillow', fps=20)
plt.show()