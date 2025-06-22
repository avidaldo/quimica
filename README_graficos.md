# Scripts de Generación de Gráficos - Control de Calidad en Industria Química

Este directorio contiene los scripts de Python y las imágenes generadas para ilustrar didácticamente los conceptos de control de calidad en la industria química.

## Scripts de Python Disponibles

### 1. `grafico_control_basico.py`
**Propósito**: Genera un gráfico de control estadístico básico que muestra un proceso estable que posteriormente sufre una desviación.

**Imágenes generadas**:
- `grafico_control_basico.png`
- `grafico_control_basico.pdf`

**Conceptos ilustrados**:
- Límites de control (UCL, LCL, LC)
- Límites de especificación (USL, LSL)
- Proceso estable vs. proceso fuera de control
- Detección de causas especiales

### 2. `estudio_estabilidad.py`
**Propósito**: Simula un estudio de estabilidad de un adhesivo industrial bajo diferentes condiciones de temperatura.

**Imágenes generadas**:
- `estudio_estabilidad.png`
- `tabla_estabilidad.png`
- `estudio_estabilidad.pdf`
- `tabla_estabilidad.pdf`

**Conceptos ilustrados**:
- Evolución de propiedades en el tiempo
- Efecto de la temperatura en la degradación
- Determinación de vida útil
- Condiciones de almacenamiento óptimas

### 3. `capacidad_proceso.py`
**Propósito**: Demuestra diferentes niveles de capacidad de proceso mediante histogramas y cálculo de índices Cp/Cpk.

**Imágenes generadas**:
- `capacidad_proceso.png`
- `interpretacion_cpk.png`
- `tabla_capacidad.png`
- `capacidad_proceso.pdf`
- `interpretacion_cpk.pdf`
- `tabla_capacidad.pdf`

**Conceptos ilustrados**:
- Índices Cp y Cpk
- Relación entre capacidad y defectos (PPM)
- Proceso centrado vs. descentrado
- Criterios de interpretación de capacidad

### 4. `conformidad_histograma.py`
**Propósito**: Muestra histogramas de diferentes procesos y su nivel de conformidad con las especificaciones.

**Imágenes generadas**:
- `conformidad_histograma.png`
- `comparacion_conformidad.png`
- `conformidad_histograma.pdf`
- `comparacion_conformidad.pdf`

**Conceptos ilustrados**:
- Análisis de conformidad
- Distribución de datos vs. especificaciones
- Comparación de tasas de conformidad
- Impacto del centrado y variabilidad

### 5. `dashboard_simple.py`
**Propósito**: Simula un dashboard digital de control de calidad industrial con múltiples paneles informativos.

**Imágenes generadas**:
- `dashboard_simple.png`
- `dashboard_simple.pdf`

**Conceptos ilustrados**:
- Integración digital de control de calidad
- KPIs en tiempo real
- Monitoreo de equipos
- Visualización de datos de producción

## Requisitos de Software

Para ejecutar los scripts necesitas:

```bash
pip install numpy matplotlib scipy
```

## Ejecución de los Scripts

```bash
# Para generar todas las imágenes:
python3 grafico_control_basico.py
python3 estudio_estabilidad.py
python3 capacidad_proceso.py
python3 conformidad_histograma.py
python3 dashboard_simple.py
```

## Formato de Salida

Cada script genera imágenes en dos formatos:
- **PNG**: Para visualización en pantalla y documentos digitales (alta resolución, 300 DPI)
- **PDF**: Para impresión y documentos profesionales (formato vectorial)

## Uso Didáctico

Estas imágenes están diseñadas para:

1. **Docentes**: Ilustrar conceptos teóricos en clases de química industrial y análisis de datos
2. **Estudiantes**: Visualizar la aplicación práctica de métodos estadísticos en la industria
3. **Profesionales**: Comprender la implementación digital de sistemas de calidad

## Personalización

Los scripts incluyen parámetros ajustables para:
- Cambiar los límites de especificación
- Modificar la variabilidad de los procesos
- Ajustar colores y estilos de los gráficos
- Simular diferentes escenarios industriales

## Integración en Documentos

Las imágenes pueden referenciarse en documentos Markdown usando:

```markdown
![Descripción](nombre_imagen.png)
```

O en LaTeX usando:
```latex
\includegraphics[width=\textwidth]{nombre_imagen.pdf}
``` 