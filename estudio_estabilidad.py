import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Configurar semilla para reproducibilidad
np.random.seed(42)

# Simular datos de estabilidad de un adhesivo industrial
# Tiempo en meses (0 a 24 meses)
tiempo_meses = np.arange(0, 25, 1)

# Condiciones de almacenamiento
# 5°C (refrigeración): degradación muy lenta
# 25°C (ambiente): degradación moderada
# 40°C (acelerado): degradación rápida

# Fuerza de adhesión inicial: 100% (valor normalizado)
# Modelos de degradación (exponencial + ruido)
fuerza_5C = 100 * np.exp(-0.005 * tiempo_meses) + np.random.normal(0, 1, len(tiempo_meses))
fuerza_25C = 100 * np.exp(-0.02 * tiempo_meses) + np.random.normal(0, 1.5, len(tiempo_meses))
fuerza_40C = 100 * np.exp(-0.06 * tiempo_meses) + np.random.normal(0, 2, len(tiempo_meses))

# Viscosidad (mPa·s) - cambio más dramático a altas temperaturas
viscosidad_inicial = 2500
viscosidad_5C = viscosidad_inicial * (1 + 0.001 * tiempo_meses) + np.random.normal(0, 50, len(tiempo_meses))
viscosidad_25C = viscosidad_inicial * (1 + 0.008 * tiempo_meses) + np.random.normal(0, 100, len(tiempo_meses))
viscosidad_40C = viscosidad_inicial * (1 + 0.025 * tiempo_meses) + np.random.normal(0, 150, len(tiempo_meses))

# Crear figura con subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Gráfico 1: Fuerza de Adhesión
ax1.plot(tiempo_meses, fuerza_5C, 'o-', color='#1f77b4', label='5°C (Refrigerado)', linewidth=2, markersize=4)
ax1.plot(tiempo_meses, fuerza_25C, 's-', color='#ff7f0e', label='25°C (Ambiente)', linewidth=2, markersize=4)
ax1.plot(tiempo_meses, fuerza_40C, '^-', color='#d62728', label='40°C (Acelerado)', linewidth=2, markersize=4)

# Línea de especificación mínima (ejemplo: 80% de la fuerza inicial)
ax1.axhline(y=80, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Límite mínimo aceptable (80%)')

ax1.set_xlabel('Tiempo (meses)', fontsize=12)
ax1.set_ylabel('Fuerza de Adhesión (%)', fontsize=12)
ax1.set_title('Estudio de Estabilidad - Fuerza de Adhesión del Adhesivo Industrial', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()
ax1.set_ylim(50, 105)

# Gráfico 2: Viscosidad
ax2.plot(tiempo_meses, viscosidad_5C, 'o-', color='#1f77b4', label='5°C (Refrigerado)', linewidth=2, markersize=4)
ax2.plot(tiempo_meses, viscosidad_25C, 's-', color='#ff7f0e', label='25°C (Ambiente)', linewidth=2, markersize=4)
ax2.plot(tiempo_meses, viscosidad_40C, '^-', color='#d62728', label='40°C (Acelerado)', linewidth=2, markersize=4)

# Límites de especificación para viscosidad (ejemplo: 2000-4000 mPa·s)
ax2.axhline(y=4000, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Límite máximo (4000 mPa·s)')
ax2.axhline(y=2000, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Límite mínimo (2000 mPa·s)')

ax2.set_xlabel('Tiempo (meses)', fontsize=12)
ax2.set_ylabel('Viscosidad (mPa·s)', fontsize=12)
ax2.set_title('Estudio de Estabilidad - Viscosidad del Adhesivo Industrial', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend()

# Añadir anotaciones sobre vida útil
# Para 25°C, encontrar cuando la fuerza cae por debajo de 80%
try:
    idx_vida_util = np.where(fuerza_25C < 80)[0][0]
    vida_util_meses = tiempo_meses[idx_vida_util]
    ax1.annotate(f'Vida útil estimada:\n~{vida_util_meses} meses a 25°C', 
                xy=(vida_util_meses, 80), xytext=(vida_util_meses+3, 85),
                arrowprops=dict(arrowstyle='->', color='black', alpha=0.7),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
                fontsize=10)
except IndexError:
    # Si no hay puntos por debajo de 80, anotar que la vida útil es mayor
    ax1.annotate('Vida útil > 24 meses a 25°C', 
                xy=(20, 82), xytext=(15, 88),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7),
                fontsize=10)

plt.tight_layout()
plt.savefig('estudio_estabilidad.png', dpi=300, bbox_inches='tight')
plt.savefig('estudio_estabilidad.pdf', bbox_inches='tight')
print("Gráfico de estudio de estabilidad guardado como 'estudio_estabilidad.png' y '.pdf'")
plt.show()

# Crear un gráfico adicional con datos tabulares
fig2, ax3 = plt.subplots(figsize=(12, 6))

# Crear tabla de resultados resumidos
condiciones = ['5°C', '25°C', '40°C']
vida_util_estimada = []

for i, fuerza in enumerate([fuerza_5C, fuerza_25C, fuerza_40C]):
    try:
        idx = np.where(fuerza < 80)[0][0]
        vida_util_estimada.append(f'{tiempo_meses[idx]} meses')
    except IndexError:
        vida_util_estimada.append('>24 meses')

# Datos para la tabla
tabla_datos = [
    ['Temperatura', 'Fuerza final (24m)', 'Viscosidad final (24m)', 'Vida útil estimada'],
    ['5°C', f'{fuerza_5C[-1]:.1f}%', f'{viscosidad_5C[-1]:.0f} mPa·s', vida_util_estimada[0]],
    ['25°C', f'{fuerza_25C[-1]:.1f}%', f'{viscosidad_25C[-1]:.0f} mPa·s', vida_util_estimada[1]],
    ['40°C', f'{fuerza_40C[-1]:.1f}%', f'{viscosidad_40C[-1]:.0f} mPa·s', vida_util_estimada[2]]
]

# Crear tabla
tabla = ax3.table(cellText=tabla_datos[1:], colLabels=tabla_datos[0], 
                  cellLoc='center', loc='center', 
                  colWidths=[0.2, 0.25, 0.25, 0.3])
tabla.auto_set_font_size(False)
tabla.set_fontsize(12)
tabla.scale(1, 2)

# Formatear la tabla
for i in range(len(tabla_datos[0])):
    tabla[(0, i)].set_facecolor('#4CAF50')
    tabla[(0, i)].set_text_props(weight='bold', color='white')

ax3.axis('off')
ax3.set_title('Resumen del Estudio de Estabilidad - Adhesivo Industrial', 
              fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('tabla_estabilidad.png', dpi=300, bbox_inches='tight')
plt.savefig('tabla_estabilidad.pdf', bbox_inches='tight')
print("Tabla de estabilidad guardada como 'tabla_estabilidad.png' y '.pdf'")
plt.show() 