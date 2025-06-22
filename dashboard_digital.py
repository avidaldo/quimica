import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Configurar semilla para reproducibilidad
np.random.seed(42)

# Crear figura principal del dashboard
fig = plt.figure(figsize=(20, 12))

# Configurar el título principal
fig.suptitle('Dashboard Digital - Sistema de Control de Calidad Industrial', 
             fontsize=20, fontweight='bold', y=0.96)

# Crear layout con GridSpec para un dashboard profesional
gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

# === PANEL 1: Gráfico de Control en Tiempo Real ===
ax1 = fig.add_subplot(gs[0, :2])

# Simular datos de densidad en tiempo real (últimas 24 horas)
horas = 24
tiempo = [datetime.now() - timedelta(hours=24-i) for i in range(horas)]
densidad_actual = 1.00 + 0.008 * np.sin(np.linspace(0, 4*np.pi, horas)) + np.random.normal(0, 0.003, horas)

# Parámetros de control
CL = 1.00
UCL = 1.012
LCL = 0.988

ax1.plot(tiempo, densidad_actual, 'o-', color='#2E86AB', linewidth=2, markersize=6)
ax1.axhline(CL, color='green', linewidth=2, label='LC (1.000)')
ax1.axhline(UCL, color='red', linestyle='--', linewidth=2, label='UCL (1.012)')
ax1.axhline(LCL, color='red', linestyle='--', linewidth=2, label='LCL (0.988)')

# Marcar último punto
ax1.scatter(tiempo[-1], densidad_actual[-1], color='red', s=100, zorder=5)
ax1.annotate(f'ACTUAL:\n{densidad_actual[-1]:.3f} g/cc', 
             xy=(tiempo[-1], densidad_actual[-1]), 
             xytext=(tiempo[-1], densidad_actual[-1] + 0.008),
             arrowprops=dict(arrowstyle='->', color='red'),
             bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8),
             fontweight='bold', ha='center')

ax1.set_title('Control de Densidad - Últimas 24 Horas', fontsize=14, fontweight='bold')
ax1.set_ylabel('Densidad (g/cc)', fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.legend()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=4))

# === PANEL 2: Indicadores KPI ===
ax2 = fig.add_subplot(gs[0, 2])
ax2.axis('off')

# Crear indicadores estilo KPI
kpis = [
    ('Cpk Actual', '1.45', '#28A745', 'EXCELENTE'),
    ('Conformidad', '99.2%', '#FFC107', 'OBJETIVO: 99.5%'),
    ('Lotes Hoy', '24', '#17A2B8', '2 EN PROCESO')
]

y_positions = [0.8, 0.5, 0.2]
for i, (metric, value, color, status) in enumerate(kpis):
    # Cuadro de KPI
    rect = patches.Rectangle((0.1, y_positions[i]-0.1), 0.8, 0.15, 
                           linewidth=2, edgecolor=color, facecolor=color, alpha=0.2)
    ax2.add_patch(rect)
    
    # Texto del KPI
    ax2.text(0.5, y_positions[i], f'{metric}\n{value}', 
             ha='center', va='center', fontsize=14, fontweight='bold')
    ax2.text(0.5, y_positions[i]-0.05, status, 
             ha='center', va='center', fontsize=10, style='italic')

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_title('Indicadores Clave', fontsize=14, fontweight='bold')

# === PANEL 3: Estado de Equipos ===
ax3 = fig.add_subplot(gs[0, 3])
ax3.axis('off')

equipos = [
    ('Reactor A', 'OPERATIVO', '#28A745'),
    ('Sensor pH-01', 'OPERATIVO', '#28A745'),
    ('Bomba B-12', 'MANTENIMIENTO', '#FFC107'),
    ('Mezclador C', 'OPERATIVO', '#28A745')
]

for i, (equipo, estado, color) in enumerate(equipos):
    y_pos = 0.8 - i * 0.2
    circle = patches.Circle((0.2, y_pos), 0.05, color=color)
    ax3.add_patch(circle)
    ax3.text(0.35, y_pos, f'{equipo}\n{estado}', 
             va='center', fontsize=10, fontweight='bold')

ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.set_title('Estado de Equipos', fontsize=14, fontweight='bold')

# === PANEL 4: Histograma de Calidad Reciente ===
ax4 = fig.add_subplot(gs[1, :2])

# Datos de los últimos 100 lotes
datos_recientes = np.random.normal(1.00, 0.005, 100)
counts, bins, patches = ax4.hist(datos_recientes, bins=20, alpha=0.7, color='#2E86AB', edgecolor='black')

# Colorear según especificaciones
LSL, USL = 0.98, 1.02
for i, (count, bin_left, patch) in enumerate(zip(counts, bins[:-1], patches)):
    bin_right = bins[i+1]
    if bin_right <= LSL or bin_left >= USL:
        patch.set_facecolor('red')

ax4.axvline(LSL, color='red', linestyle='--', linewidth=2, label='LSL')
ax4.axvline(USL, color='red', linestyle='--', linewidth=2, label='USL')
ax4.axvline(1.00, color='green', linestyle=':', linewidth=2, label='Objetivo')

ax4.set_title('Distribución de Calidad - Últimos 100 Lotes', fontsize=14, fontweight='bold')
ax4.set_xlabel('Densidad (g/cc)')
ax4.set_ylabel('Frecuencia')
ax4.legend()
ax4.grid(True, alpha=0.3)

# === PANEL 5: Tendencia de Capacidad ===
ax5 = fig.add_subplot(gs[1, 2:])

# Simular evolución del Cpk en los últimos 30 días
dias = 30
fechas = [datetime.now() - timedelta(days=30-i) for i in range(dias)]
cpk_tendencia = 1.2 + 0.3 * np.sin(np.linspace(0, 2*np.pi, dias)) + np.random.normal(0, 0.05, dias)

ax5.plot(fechas, cpk_tendencia, 'o-', color='#FF6B35', linewidth=2, markersize=4)
ax5.axhline(1.33, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Objetivo Cpk ≥ 1.33')
ax5.axhline(1.0, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Mínimo Aceptable')

ax5.set_title('Evolución de la Capacidad del Proceso (Cpk)', fontsize=14, fontweight='bold')
ax5.set_ylabel('Índice Cpk')
ax5.grid(True, alpha=0.3)
ax5.legend()
ax5.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax5.xaxis.set_major_locator(mdates.DayLocator(interval=5))

# === PANEL 6: Alertas y Notificaciones ===
ax6 = fig.add_subplot(gs[2, :2])
ax6.axis('off')

alertas = [
    ('🟡', '10:45', 'Tendencia al alza detectada en Reactor B', '#FFC107'),
    ('🟢', '09:30', 'Calibración de sensor pH-02 completada', '#28A745'),
    ('🔴', '08:15', 'Límite de control excedido - Lote #A1547', '#DC3545'),
    ('🟢', '07:00', 'Proceso estabilizado después de ajuste', '#28A745'),
]

ax6.text(0.5, 0.95, 'Registro de Alertas del Turno', ha='center', va='top', 
         fontsize=14, fontweight='bold')

for i, (icono, hora, mensaje, color) in enumerate(alertas):
    y_pos = 0.8 - i * 0.15
    ax6.text(0.05, y_pos, f'{icono} {hora}', fontsize=12, fontweight='bold')
    ax6.text(0.2, y_pos, mensaje, fontsize=11, color=color)

ax6.set_xlim(0, 1)
ax6.set_ylim(0, 1)

# === PANEL 7: Métricas de Producción ===
ax7 = fig.add_subplot(gs[2, 2:])

# Datos de producción por turno
turnos = ['Turno 1\n(00-08h)', 'Turno 2\n(08-16h)', 'Turno 3\n(16-24h)']
produccion = [145, 160, 138]  # Lotes producidos
conformidad_turno = [99.3, 98.8, 99.5]  # % de conformidad

# Crear gráfico combinado
ax7_twin = ax7.twinx()

# Barras de producción
bars = ax7.bar(turnos, produccion, alpha=0.7, color='#2E86AB', label='Lotes Producidos')
ax7.set_ylabel('Lotes Producidos', color='#2E86AB', fontsize=12)
ax7.tick_params(axis='y', labelcolor='#2E86AB')

# Línea de conformidad
line = ax7_twin.plot(turnos, conformidad_turno, 'o-', color='#FF6B35', 
                     linewidth=3, markersize=8, label='% Conformidad')
ax7_twin.set_ylabel('Conformidad (%)', color='#FF6B35', fontsize=12)
ax7_twin.tick_params(axis='y', labelcolor='#FF6B35')
ax7_twin.set_ylim(98, 100)

# Añadir valores en las barras
for bar, conf in zip(bars, conformidad_turno):
    height = bar.get_height()
    ax7.text(bar.get_x() + bar.get_width()/2., height + 2,
             f'{int(height)}', ha='center', va='bottom', fontweight='bold')

ax7.set_title('Producción y Conformidad por Turno', fontsize=14, fontweight='bold')
ax7.grid(True, alpha=0.3)

# Añadir línea de referencia para conformidad objetivo
ax7_twin.axhline(99.0, color='red', linestyle='--', alpha=0.7, label='Objetivo 99%')

# === Panel de información del sistema ===
info_text = f"""
SISTEMA DE CONTROL DE CALIDAD v2.1
Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Sensores conectados: 12/12 ✓
Base de datos: Sincronizada ✓
Estado general: OPERATIVO
"""

fig.text(0.02, 0.02, info_text, fontsize=10, style='italic', 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))

plt.savefig('dashboard_digital.png', dpi=300, bbox_inches='tight')
plt.savefig('dashboard_digital.pdf', bbox_inches='tight')
print("Dashboard digital guardado como 'dashboard_digital.png' y '.pdf'")
plt.show() 