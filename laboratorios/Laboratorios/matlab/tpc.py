import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from bokeh.plotting import figure, show
from bokeh.io import output_notebook

t = np.linspace(-0.10, 6.05, 500)

y1 = np.sin(t)
y2 = np.cos(t)

df = pd.DataFrame({
    't': t,
    'sin(t)': y1,
    'cos(t)': y2
})


corr = df[['sin(t)', 'cos(t)']].corr()
print("Correlation matrix:\n", corr)


plt.figure()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".3f")
plt.title('Correlation Matrix (~0.052 esperado)')
plt.show()


fig = go.Figure()

fig.add_trace(go.Scatter(x=t, y=y1, mode='lines', name='sin(t)'))
fig.add_trace(go.Scatter(x=t, y=y2, mode='lines', name='cos(t)'))

fig.update_layout(
    title='Plotly Interactive Plot',
    xaxis_title='t',
    yaxis_title='Amplitude'
)

fig.show()

output_notebook()

p = figure(title="Bokeh Interactive Plot",
           x_axis_label='t',
           y_axis_label='Amplitude',
           width=700, height=400)

p.line(t, y1, legend_label="sin(t)")
p.line(t, y2, legend_label="cos(t)")

p.legend.location = "top_left"

show(p)