import pandas as pd
import plotly.graph_objects as go
import igraph as ig
import os

# Cargar la información de pares desde el archivo CSV
data_path = 'data/data_binance/pair_information/binance_all_pairs.csv'
info_pares = pd.read_csv(data_path).set_index('symbol').T.to_dict()

# Listas de monedas fiat para AEs y EMDEs
aes_fiat_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CZK']
emdes_fiat_currencies = ['BRL', 'ARS', 'NGN', 'TRY', 'MXN', 'ZAR', 'PLN', 'RUB', 'RON', 'UAH']

# Colores personalizados
colors = {
    'BTC': '#F7931A',   # Naranja para Bitcoin
    'USDT': '#26A17B',  # Verde para Tether
    'AES': '#AA322F',   # Rojo oscuro para AEs
    'EMDES': '#6FA5E2', # Azul pastel para EMDEs
    'OTHERS': '#d6d6d6' # Gris para otras criptomonedas
}

crypto_label_color = '#A9A9A9'  # Gris un poco más oscuro para etiquetas de criptomonedas

# Extraer los vertices y las aristas a partir de 'info_pares'
vertices = set()
edges = []

for symbol, details in info_pares.items():
    base_currency = details['base_currency']
    quote_currency = details['quote_currency']
    vertices.add(base_currency)
    vertices.add(quote_currency)
    edges.append((base_currency, quote_currency))

# Convertir el conjunto de vertices a una lista
vertices = list(vertices)

# Crear el grafo en igraph
G_ig = ig.Graph()
G_ig.add_vertices(vertices)
G_ig.add_edges(edges)

# Filtrar nodos con grado menor que 1
low_degree_nodes = [v.index for v in G_ig.vs if G_ig.degree(v) < 1]
G_ig.delete_vertices(low_degree_nodes)

# Recalcular el PageRank después de eliminar los nodos de bajo grado
pagerank = G_ig.pagerank()
max_pagerank = max(pagerank)

# Exagerar las diferencias aplicando una transformación exponencial al PageRank
min_size = 1  # Tamaño mínimo para nodos con solo 1 conexión
mid_size = 10 # Tamaño para nodos con 2 conexiones
max_size = 40 # Tamaño máximo para nodos con más conexiones y alto PageRank

# Asignar tamaños basados en el número de conexiones y PageRank
vertex_sizes = []
for i in range(len(G_ig.vs)):
    degree = G_ig.degree(i)
    if degree == 1:
        vertex_sizes.append(min_size)
    elif degree == 2:
        vertex_sizes.append(mid_size)
    else:
        vertex_sizes.append(min_size + (pagerank[i] / max_pagerank) ** 0.3 * (max_size - min_size))

# Encontrar las criptomonedas con los 5 mayores valores de PageRank
top_5_cryptos = sorted(range(len(pagerank)), key=lambda i: pagerank[i], reverse=True)[:5]

# Asignar colores a los nodos y etiquetas: AEs, EMDEs y criptomonedas
vertex_colors = []
label_colors = []
vertex_shapes = []
vertex_borders = []

for i in range(len(G_ig.vs)):
    name = G_ig.vs[i]['name']
    
    if name == 'BTC':
        vertex_colors.append(colors['BTC'])
        label_colors.append(colors['BTC'])
        vertex_borders.append(colors['BTC'])  # Borde del mismo color para BTC
    elif name == 'USDT':
        vertex_colors.append(colors['USDT'])
        label_colors.append(colors['USDT'])
        vertex_borders.append(colors['USDT'])  # Borde del mismo color para USDT
    elif name in aes_fiat_currencies:
        vertex_colors.append(colors['AES'])
        label_colors.append(colors['AES'])
        vertex_borders.append(colors['AES'])  # Borde del mismo color para AEs
    elif name in emdes_fiat_currencies:
        vertex_colors.append(colors['EMDES'])
        label_colors.append(colors['EMDES'])
        vertex_borders.append(colors['EMDES'])  # Borde del mismo color para EMDEs
    else:
        vertex_colors.append(colors['OTHERS'])
        label_colors.append(crypto_label_color)  # Usar color de etiqueta para otras cryptos
        vertex_borders.append('rgba(0,0,0,0)')  # Borde transparente para otras criptomonedas

    vertex_shapes.append(
        'triangle-up' if name in aes_fiat_currencies or name in emdes_fiat_currencies else 'circle'
    )

# Asignar etiquetas a las monedas fiat y a las criptomonedas en el top 5 de PageRank
vertex_labels = [
    G_ig.vs[i]['name'] if G_ig.vs[i]['name'] in aes_fiat_currencies or G_ig.vs[i]['name'] in emdes_fiat_currencies or i in top_5_cryptos else ''
    for i in range(len(G_ig.vs))
]

# Definir tamaños de las etiquetas basados en PageRank
min_font_size = 8
max_font_size = 18
vertex_label_sizes = [min_font_size + (pr / max_pagerank) ** 0.3 * (max_font_size - min_font_size) for pr in pagerank]

# Aplicar el layout con mayor número de iteraciones
layout = G_ig.layout_fruchterman_reingold(niter=10000)

# Extraer las posiciones del layout y ajustar para aristas curvas
Xn = [layout[k][0] for k in range(len(G_ig.vs))]
Yn = [layout[k][1] for k in range(len(G_ig.vs))]
Xe = []
Ye = []
for edge in G_ig.es:
    x_mid = (layout[edge.source][0] + layout[edge.target][0]) / 2
    y_mid = (layout[edge.source][1] + layout[edge.target][1]) / 2
    Xe += [layout[edge.source][0], x_mid, layout[edge.target][0], None]
    Ye += [layout[edge.source][1], y_mid, layout[edge.target][1], None]

# Graficar usando Plotly
trace1 = go.Scatter(
    x=Xe,
    y=Ye,
    mode='lines',
    line=dict(color='rgb(240, 240, 240)', width=1),  # Líneas de color gris claro
    hoverinfo='none'
)

trace2 = go.Scatter(
    x=Xn,
    y=Yn,
    mode='markers+text',
    name='ntw',
    marker=dict(
        symbol=vertex_shapes,
        size=vertex_sizes, 
        color=vertex_colors,
        line=dict(width=[2 if color != 'rgba(0,0,0,0)' else 0 for color in vertex_borders], color=vertex_borders)
    ),
    text=vertex_labels,
    textposition='top center',
    textfont=dict(color=label_colors, size=vertex_label_sizes),  # Usar tamaños de fuente basados en PageRank
    hoverinfo='text'
)

# Ajuste del layout
layout_plot = go.Layout(
    showlegend=False,
    autosize=True,  # Activar autosize para que el gráfico sea adaptable
    margin=dict(l=25, r=25, b=25, t=25),  # Márgenes pequeños para maximizar el espacio
    hovermode='closest',
    xaxis=dict(showline=False, zeroline=False, showgrid=False, showticklabels=False),
    yaxis=dict(showline=False, zeroline=False, showgrid=False, showticklabels=False)
)

# Crear la figura
fig = go.Figure(data=[trace1, trace2], layout=layout_plot)

# Guardar el gráfico en la carpeta correspondiente
output_dir = 'outputs/graphs/color/'
os.makedirs(output_dir, exist_ok=True)  # Crear la carpeta si no existe
fig.write_html(os.path.join(output_dir, "fig_f1.html"))

# Mostrar el gráfico
fig.show()
