import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime, timedelta

# Configurar semilla para reproducibilidad
np.random.seed(42)

# Crear figura del dashboard
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Dashboard Digital - Sistema de Control de Calidad Industrial', 
             fontsize=18, fontweight='bold')

# === PANEL 1: Gráfico de Control en Tiempo Real ===
# Simular datos de las últimas 12 horas
horas = 12
tiempo = list(range(horas))
densidad = 1.00 + 0.005 * np.sin(np.linspace(0, 2*np.pi, horas)) + np.random.normal(0, 0.002, horas)

ax1.plot(tiempo, densidad, 'o-', color='#2E86AB', linewidth=2, markersize=6)
ax1.axhline(1.00, color='green', linewidth=2, label='LC (1.000)')
ax1.axhline(1.008, color='red', linestyle='--', linewidth=2, label='UCL')
ax1.axhline(0.992, color='red', linestyle='--', linewidth=2, label='LCL')

ax1.set_title('Control de Densidad - Tiempo Real', fontsize=14, fontweight='bold')
ax1.set_xlabel('Tiempo (horas)')
ax1.set_ylabel('Densidad (g/cc)')
ax1.grid(True, alpha=0.3)
ax1.legend()

# === PANEL 2: Indicadores KPI ===
ax2.axis('off')

# Simular KPIs actuales
kpi_data = [
    ('Cpk Actual', '1.42', 'EXCELENTE'),
    ('Conformidad', '99.1%', 'OBJETIVO: 99.5%'),
    ('Lotes Procesados', '18', 'HOY'),
    ('Eficiencia', '94.5%', 'META: 95%')
]

colors = ['#28A745', '#FFC107', '#17A2B8', '#6F42C1']

for i, ((metric, value, status), color) in enumerate(zip(kpi_data, colors)):
    y_pos = 0.85 - i * 0.2
    
    # Cuadro de fondo
    rect = patches.Rectangle((0.05, y_pos-0.08), 0.9, 0.12, 
                           linewidth=2, edgecolor=color, facecolor=color, alpha=0.1)
    ax2.add_patch(rect)
    
    # Texto principal
    ax2.text(0.1, y_pos, metric, fontsize=12, fontweight='bold')
    ax2.text(0.8, y_pos, value, fontsize=14, fontweight='bold', color=color, ha='right')
    ax2.text(0.5, y_pos-0.04, status, fontsize=10, style='italic', ha='center')

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_title('Indicadores Clave de Rendimiento', fontsize=14, fontweight='bold')

# === PANEL 3: Estado de Equipos ===
ax3.axis('off')

equipos = [
    ('Reactor Principal', 'OPERATIVO', '#28A745'),
    ('Sensor pH-01', 'OPERATIVO', '#28A745'),
    ('Bomba Dosificadora', 'MANTENIMIENTO', '#FFC107'),
    ('Mezclador A', 'OPERATIVO', '#28A745'),
    ('Sistema Filtrado', 'OPERATIVO', '#28A745'),
    ('Válvula Control', 'WARNING', '#FF6B35')
]

ax3.set_title('Estado de Equipos Críticos', fontsize=14, fontweight='bold')

for i, (equipo, estado, color) in enumerate(equipos):
    y_pos = 0.9 - i * 0.13
    
    # Indicador circular
    circle = patches.Circle((0.1, y_pos), 0.03, color=color, alpha=0.8)
    ax3.add_patch(circle)
    
    # Texto del equipo
    ax3.text(0.18, y_pos + 0.02, equipo, fontsize=11, fontweight='bold')
    ax3.text(0.18, y_pos - 0.02, estado, fontsize=10, color=color, style='italic')

ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)

# === PANEL 4: Producción por Turno ===
turnos = ['Turno 1', 'Turno 2', 'Turno 3']
produccion = [142, 158, 135]
conformidad = [99.3, 98.7, 99.6]

# Crear gráfico combinado
ax4_twin = ax4.twinx()

# Barras de producción
bars = ax4.bar(turnos, produccion, alpha=0.7, color='#2E86AB', label='Lotes')
ax4.set_ylabel('Lotes Producidos', color='#2E86AB')

# Línea de conformidad
line = ax4_twin.plot(turnos, conformidad, 'o-', color='#FF6B35', 
                     linewidth=3, markersize=8, label='% Conformidad')
ax4_twin.set_ylabel('Conformidad (%)', color='#FF6B35')
ax4_twin.set_ylim(98, 100)

# Añadir valores
for bar, conf in zip(bars, conformidad):
    ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2,
             f'{int(bar.get_height())}', ha='center', fontweight='bold')

ax4.set_title('Producción y Conformidad por Turno', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3)

# Línea objetivo
ax4_twin.axhline(99.0, color='red', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('dashboard_simple.png', dpi=300, bbox_inches='tight')
plt.savefig('dashboard_simple.pdf', bbox_inches='tight')
print("Dashboard simple guardado como 'dashboard_simple.png' y '.pdf'")
plt.show() 