import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style

# Configurar estilo para mayor legibilidad
plt.style.use('default')
plt.rcParams.update({'font.size': 12})

# Configurar semilla para reproducibilidad
np.random.seed(42)

# Generar datos simulados de densidad (en g/cc):
# 20 datos iniciales con media 1.00 (proceso estable)
# 10 datos posteriores con media 1.03 (proceso desviado)
data_estable = np.random.normal(1.00, 0.005, 20)
data_inestable = np.random.normal(1.03, 0.008, 10)
data = np.concatenate([data_estable, data_inestable])

# Calcular límites de control basados en la fase estable
CL = data_estable.mean()  # Línea Central
sigma = data_estable.std(ddof=1)  # Desviación estándar
UCL = CL + 3*sigma  # Límite de Control Superior
LCL = CL - 3*sigma  # Límite de Control Inferior

# Límites de especificación
LSL, USL = 0.98, 1.02

# Crear el gráfico
fig, ax = plt.subplots(figsize=(12, 8))

# Datos
x = np.arange(1, len(data) + 1)
ax.plot(x, data, 'o-', color='#2E86AB', markersize=6, linewidth=2, label='Densidad medida')

# Líneas de control
ax.axhline(CL, color='#28A745', linewidth=2, label=f'Línea Central (CL = {CL:.3f})')
ax.axhline(UCL, color='#DC3545', linestyle='--', linewidth=2, label=f'UCL = {UCL:.3f}')
ax.axhline(LCL, color='#DC3545', linestyle='--', linewidth=2, label=f'LCL = {LCL:.3f}')

# Límites de especificación
ax.axhline(USL, color='#6F42C1', linestyle=':', linewidth=2, label=f'USL = {USL}')
ax.axhline(LSL, color='#6F42C1', linestyle=':', linewidth=2, label=f'LSL = {LSL}')

# Zonas de control (opcional)
ax.fill_between(x, LCL, UCL, alpha=0.1, color='green', label='Zona de control')
ax.fill_between(x, LSL, USL, alpha=0.05, color='purple', label='Zona de especificación')

# Marcar puntos fuera de control
puntos_fuera = data > UCL
if np.any(puntos_fuera):
    ax.scatter(x[puntos_fuera], data[puntos_fuera], color='red', s=100, marker='x', 
               linewidth=3, label='Fuera de control', zorder=5)

# Línea vertical para separar fases
ax.axvline(x=20.5, color='orange', linestyle='-', alpha=0.7, linewidth=2)
ax.text(10, 1.035, 'Proceso Estable', fontsize=14, ha='center', 
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))
ax.text(25, 1.035, 'Proceso Desviado', fontsize=14, ha='center',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7))

# Configuración del gráfico
ax.set_xlabel('Número de muestra (orden temporal)', fontsize=14)
ax.set_ylabel('Densidad (g/cc)', fontsize=14)
ax.set_title('Gráfico de Control - Densidad de Producto Químico', fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left', fontsize=10)

# Ajustar layout y guardar
plt.tight_layout()
plt.savefig('grafico_control_basico.png', dpi=300, bbox_inches='tight')
plt.savefig('grafico_control_basico.pdf', bbox_inches='tight')
print("Gráfico de control básico guardado como 'grafico_control_basico.png' y '.pdf'")
plt.show() 