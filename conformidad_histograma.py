import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Configurar semilla para reproducibilidad
np.random.seed(42)

# Definir límites de especificación para pH
LSL_pH = 6.8  # Límite inferior de especificación
USL_pH = 7.2  # Límite superior de especificación
TARGET_pH = 7.0  # Valor objetivo

# Generar datos de 3 escenarios diferentes
# Escenario 1: Proceso centrado y con buena capacidad (100% conforme)
data_conforme = np.random.normal(7.0, 0.05, 200)

# Escenario 2: Proceso descentrado (algunos no conformes)
data_descentrado = np.random.normal(7.15, 0.08, 200)

# Escenario 3: Proceso con alta variabilidad (muchos no conformes)
data_variable = np.random.normal(7.0, 0.12, 200)

# Función para calcular conformidad
def calcular_conformidad(data, lsl, usl):
    conformes = np.sum((data >= lsl) & (data <= usl))
    no_conformes = len(data) - conformes
    porcentaje_conforme = (conformes / len(data)) * 100
    return conformes, no_conformes, porcentaje_conforme

# Crear figura con subplots
fig, axes = plt.subplots(3, 1, figsize=(12, 15))

scenarios = [
    ('Proceso Conforme (Centrado y Capaz)', data_conforme, '#2ca02c'),
    ('Proceso Descentrado', data_descentrado, '#ff7f0e'),
    ('Proceso con Alta Variabilidad', data_variable, '#d62728')
]

for i, (title, data, color) in enumerate(scenarios):
    ax = axes[i]
    
    # Calcular estadísticas de conformidad
    conformes, no_conformes, porcentaje_conforme = calcular_conformidad(data, LSL_pH, USL_pH)
    
    # Crear histograma
    counts, bins, patches = ax.hist(data, bins=25, density=False, alpha=0.7, 
                                   color=color, edgecolor='black', linewidth=0.5)
    
    # Colorear barras según conformidad
    for j, (count, bin_left, patch) in enumerate(zip(counts, bins[:-1], patches)):
        bin_right = bins[j+1]
        bin_center = (bin_left + bin_right) / 2
        if bin_center < LSL_pH or bin_center > USL_pH:
            patch.set_facecolor('red')
            patch.set_alpha(0.8)
    
    # Añadir curva normal teórica
    x_curve = np.linspace(data.min(), data.max(), 100)
    # Escalar la curva normal para que coincida con el histograma
    mean_data = np.mean(data)
    std_data = np.std(data, ddof=1)
    y_curve = stats.norm.pdf(x_curve, mean_data, std_data) * len(data) * (bins[1] - bins[0])
    ax.plot(x_curve, y_curve, 'k-', linewidth=2, alpha=0.8, label='Distribución teórica')
    
    # Líneas de especificación
    ax.axvline(LSL_pH, color='red', linestyle='--', linewidth=2, label=f'LSL = {LSL_pH}')
    ax.axvline(USL_pH, color='red', linestyle='--', linewidth=2, label=f'USL = {USL_pH}')
    ax.axvline(TARGET_pH, color='green', linestyle=':', linewidth=2, alpha=0.7, label=f'Objetivo = {TARGET_pH}')
    ax.axvline(mean_data, color='blue', linestyle='-', linewidth=2, alpha=0.7, 
               label=f'Media = {mean_data:.2f}')
    
    # Sombrear área de conformidad
    x_fill = np.linspace(LSL_pH, USL_pH, 100)
    y_fill = stats.norm.pdf(x_fill, mean_data, std_data) * len(data) * (bins[1] - bins[0])
    ax.fill_between(x_fill, 0, y_fill, alpha=0.2, color='green', label='Zona de conformidad')
    
    # Configurar el gráfico
    ax.set_title(f'{title}\n{conformes} conformes ({porcentaje_conforme:.1f}%) | {no_conformes} no conformes ({100-porcentaje_conforme:.1f}%)', 
                fontsize=14, fontweight='bold')
    ax.set_xlabel('pH', fontsize=12)
    ax.set_ylabel('Frecuencia', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=10)
    ax.set_xlim(6.4, 7.6)

plt.suptitle('Análisis de Conformidad - pH de Solución Química', 
             fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('conformidad_histograma.png', dpi=300, bbox_inches='tight')
plt.savefig('conformidad_histograma.pdf', bbox_inches='tight')
print("Gráfico de conformidad guardado como 'conformidad_histograma.png' y '.pdf'")
plt.show()

# Gráfico adicional: Comparación de tasas de conformidad
fig2, ax = plt.subplots(figsize=(10, 6))

# Datos para el gráfico de barras
escenarios = ['Proceso Centrado\ny Capaz', 'Proceso\nDescentrado', 'Proceso con Alta\nVariabilidad']
conformidad_porcentajes = []
no_conformidad_porcentajes = []

for _, data, _ in scenarios:
    _, _, porcentaje_conforme = calcular_conformidad(data, LSL_pH, USL_pH)
    conformidad_porcentajes.append(porcentaje_conforme)
    no_conformidad_porcentajes.append(100 - porcentaje_conforme)

x = np.arange(len(escenarios))
width = 0.35

# Crear barras apiladas
bars1 = ax.bar(x, conformidad_porcentajes, width, label='Conformes', color='#2ca02c', alpha=0.8)
bars2 = ax.bar(x, no_conformidad_porcentajes, width, bottom=conformidad_porcentajes, 
               label='No Conformes', color='#d62728', alpha=0.8)

# Añadir etiquetas en las barras
for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
    # Etiqueta para conformes
    height1 = bar1.get_height()
    if height1 > 5:  # Solo mostrar si hay suficiente espacio
        ax.text(bar1.get_x() + bar1.get_width()/2., height1/2,
               f'{height1:.1f}%', ha='center', va='center', fontweight='bold', color='white')
    
    # Etiqueta para no conformes
    height2 = bar2.get_height()
    if height2 > 5:  # Solo mostrar si hay suficiente espacio
        ax.text(bar2.get_x() + bar2.get_width()/2., height1 + height2/2,
               f'{height2:.1f}%', ha='center', va='center', fontweight='bold', color='white')

ax.set_xlabel('Tipo de Proceso', fontsize=12)
ax.set_ylabel('Porcentaje (%)', fontsize=12)
ax.set_title('Comparación de Tasas de Conformidad por Tipo de Proceso', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(escenarios)
ax.legend()
ax.set_ylim(0, 100)

# Añadir línea de referencia del 95% (objetivo típico)
ax.axhline(y=95, color='orange', linestyle='--', alpha=0.7, linewidth=2, 
           label='Objetivo 95% conformidad')
ax.legend()

plt.tight_layout()
plt.savefig('comparacion_conformidad.png', dpi=300, bbox_inches='tight')
plt.savefig('comparacion_conformidad.pdf', bbox_inches='tight')
print("Gráfico de comparación de conformidad guardado como 'comparacion_conformidad.png' y '.pdf'")
plt.show() 