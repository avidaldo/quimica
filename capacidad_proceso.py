import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Configurar semilla para reproducibilidad
np.random.seed(42)

# Definir límites de especificación
LSL = 0.98  # Límite de especificación inferior
USL = 1.02  # Límite de especificación superior
TARGET = (LSL + USL) / 2  # Valor objetivo (1.00)

# Crear cuatro escenarios de capacidad de proceso
scenarios = {
    'Proceso Incapaz (Cp<1)': {
        'mean': 1.00,
        'std': 0.015,  # Alta variabilidad
        'color': '#d62728',
        'title': 'Proceso Incapaz\n(Cp < 1.0)'
    },
    'Proceso Justo (Cp≈1)': {
        'mean': 1.00,
        'std': 0.0067,  # Cp ≈ 1
        'color': '#ff7f0e',
        'title': 'Proceso Justo\n(Cp ≈ 1.0)'
    },
    'Proceso Capaz (Cp>1.33)': {
        'mean': 1.00,
        'std': 0.005,  # Cp ≈ 1.33
        'color': '#2ca02c',
        'title': 'Proceso Capaz\n(Cp > 1.33)'
    },
    'Proceso Descentrado': {
        'mean': 1.015,  # Descentrado hacia el límite superior
        'std': 0.005,
        'color': '#9467bd',
        'title': 'Proceso Descentrado\n(Cp≠Cpk)'
    }
}

# Crear figura con subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
axes = axes.ravel()

for i, (scenario_name, params) in enumerate(scenarios.items()):
    ax = axes[i]
    
    # Generar datos
    data = np.random.normal(params['mean'], params['std'], 1000)
    
    # Calcular índices de capacidad
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    
    Cp = (USL - LSL) / (6 * std)
    Cpu = (USL - mean) / (3 * std)
    Cpl = (mean - LSL) / (3 * std)
    Cpk = min(Cpu, Cpl)
    
    # Calcular porcentaje fuera de especificación
    outside_spec = np.sum((data < LSL) | (data > USL)) / len(data) * 100
    
    # Crear histograma
    counts, bins, patches = ax.hist(data, bins=30, density=True, alpha=0.7, 
                                  color=params['color'], edgecolor='black', linewidth=0.5)
    
    # Colorear barras según especificación
    for j, (count, bin_left, patch) in enumerate(zip(counts, bins[:-1], patches)):
        bin_right = bins[j+1]
        if bin_right <= LSL or bin_left >= USL:
            patch.set_facecolor('red')
            patch.set_alpha(0.8)
    
    # Añadir curva normal teórica
    x_curve = np.linspace(data.min(), data.max(), 100)
    y_curve = stats.norm.pdf(x_curve, mean, std)
    ax.plot(x_curve, y_curve, 'k-', linewidth=2, alpha=0.8, label='Distribución teórica')
    
    # Líneas de especificación
    ax.axvline(LSL, color='red', linestyle='--', linewidth=2, label=f'LSL = {LSL}')
    ax.axvline(USL, color='red', linestyle='--', linewidth=2, label=f'USL = {USL}')
    ax.axvline(TARGET, color='green', linestyle=':', linewidth=2, alpha=0.7, label=f'Objetivo = {TARGET}')
    ax.axvline(mean, color='blue', linestyle='-', linewidth=2, alpha=0.7, label=f'Media = {mean:.3f}')
    
    # Configurar el gráfico
    ax.set_title(params['title'], fontsize=14, fontweight='bold')
    ax.set_xlabel('Densidad (g/cc)', fontsize=12)
    ax.set_ylabel('Densidad de probabilidad', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Añadir texto con índices
    textstr = f'Cp = {Cp:.2f}\nCpk = {Cpk:.2f}\nFuera de spec: {outside_spec:.1f}%'
    props = dict(boxstyle='round', facecolor='white', alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
           verticalalignment='top', bbox=props)
    
    # Leyenda solo en el primer subplot
    if i == 0:
        ax.legend(loc='upper right', fontsize=9)
    
    # Ajustar límites del eje x para mostrar todo el rango relevante
    ax.set_xlim(0.95, 1.05)

plt.suptitle('Análisis de Capacidad de Proceso - Diferentes Escenarios', 
             fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('capacidad_proceso.png', dpi=300, bbox_inches='tight')
plt.savefig('capacidad_proceso.pdf', bbox_inches='tight')
print("Gráfico de capacidad de proceso guardado como 'capacidad_proceso.png' y '.pdf'")
plt.show()

# Crear un gráfico adicional mostrando la interpretación de los índices
fig2, ax = plt.subplots(figsize=(12, 8))

# Datos para la interpretación de Cpk
cpk_values = [0.5, 0.67, 1.0, 1.33, 1.67, 2.0]
defect_rates = [133614, 44565, 2700, 63, 0.57, 0.002]  # PPM (partes por millón)
capability_levels = ['Inadecuado', 'Pobre', 'Aceptable', 'Capaz', 'Muy Capaz', 'Excelente']
colors = ['#d62728', '#ff4500', '#ffa500', '#32cd32', '#228b22', '#006400']

# Crear gráfico de barras
bars = ax.bar(range(len(cpk_values)), defect_rates, color=colors, alpha=0.7, edgecolor='black')

# Configurar escala logarítmica para el eje y
ax.set_yscale('log')

# Etiquetas
ax.set_xlabel('Índice Cpk', fontsize=14)
ax.set_ylabel('Defectos por Millón (PPM)', fontsize=14)
ax.set_title('Relación entre Índice Cpk y Tasa de Defectos', fontsize=16, fontweight='bold')

# Configurar ticks del eje x
ax.set_xticks(range(len(cpk_values)))
ax.set_xticklabels([f'{cpk:.2f}' for cpk in cpk_values])

# Añadir etiquetas en las barras
for i, (bar, rate, level) in enumerate(zip(bars, defect_rates, capability_levels)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height * 1.5,
           f'{rate:g} PPM\n({level})', 
           ha='center', va='bottom', fontsize=10, fontweight='bold')

# Añadir líneas de referencia
ax.axhline(y=1000, color='orange', linestyle='--', alpha=0.7, label='1000 PPM (Objetivo común)')
ax.axhline(y=100, color='green', linestyle='--', alpha=0.7, label='100 PPM (Objetivo excelencia)')

ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
plt.savefig('interpretacion_cpk.png', dpi=300, bbox_inches='tight')
plt.savefig('interpretacion_cpk.pdf', bbox_inches='tight')
print("Gráfico de interpretación Cpk guardado como 'interpretacion_cpk.png' y '.pdf'")
plt.show()

# Crear tabla resumen de criterios de capacidad
fig3, ax = plt.subplots(figsize=(12, 6))

# Datos para la tabla
tabla_datos = [
    ['Índice Cpk', 'Nivel de Capacidad', 'Defectos (PPM)', 'Interpretación', 'Recomendación'],
    ['< 0.67', 'Inadecuado', '> 44,565', 'Proceso incapaz', 'Rediseño necesario'],
    ['0.67 - 1.00', 'Pobre', '2,700 - 44,565', 'Proceso marginal', 'Mejora urgente'],
    ['1.00 - 1.33', 'Aceptable', '63 - 2,700', 'Proceso aceptable', 'Mejora continua'],
    ['1.33 - 1.67', 'Capaz', '0.57 - 63', 'Proceso capaz', 'Mantener control'],
    ['> 1.67', 'Excelente', '< 0.57', 'Proceso Six Sigma', 'Replicar en otros procesos']
]

# Crear tabla
tabla = ax.table(cellText=tabla_datos[1:], colLabels=tabla_datos[0], 
                cellLoc='center', loc='center',
                colWidths=[0.15, 0.2, 0.2, 0.2, 0.25])
tabla.auto_set_font_size(False)
tabla.set_fontsize(11)
tabla.scale(1, 2)

# Formatear encabezados
for i in range(len(tabla_datos[0])):
    tabla[(0, i)].set_facecolor('#2E86AB')
    tabla[(0, i)].set_text_props(weight='bold', color='white')

# Colorear filas según el nivel de capacidad
row_colors = ['#ffcccb', '#ffd700', '#98fb98', '#90ee90', '#32cd32']
for i in range(1, len(tabla_datos)):
    for j in range(len(tabla_datos[0])):
        tabla[(i, j)].set_facecolor(row_colors[i-1])

ax.axis('off')
ax.set_title('Criterios de Interpretación de la Capacidad de Proceso (Cpk)', 
             fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('tabla_capacidad.png', dpi=300, bbox_inches='tight')
plt.savefig('tabla_capacidad.pdf', bbox_inches='tight')
print("Tabla de capacidad guardada como 'tabla_capacidad.png' y '.pdf'")
plt.show() 