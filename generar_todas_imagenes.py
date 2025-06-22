#!/usr/bin/env python3
"""
Script principal para generar todas las imágenes del informe de digitalización
aplicada a la calidad en la industria química.

Este script ejecuta todos los scripts individuales para generar:
- Gráficos de control
- Estudios de estabilidad
- Análisis de conformidad  
- Capacidad de proceso
- Dashboard digital

Autor: Generado para el informe de digitalización en química
Fecha: 2024
"""

import subprocess
import sys
import os

def ejecutar_script(script_name):
    """Ejecuta un script de Python y maneja errores"""
    try:
        print(f"🔄 Ejecutando {script_name}...")
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {script_name} completado exitosamente")
        if result.stdout:
            print(f"   📄 Salida: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando {script_name}: {e}")
        if e.stderr:
            print(f"   🚨 Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ Archivo {script_name} no encontrado")
        return False

def main():
    """Función principal que ejecuta todos los scripts"""
    print("🧪 GENERADOR DE GRÁFICOS - CONTROL DE CALIDAD QUÍMICA")
    print("=" * 60)
    
    # Lista de scripts a ejecutar
    scripts = [
        "grafico_control_basico.py",
        "estudio_estabilidad.py", 
        "capacidad_proceso.py",
        "conformidad_histograma.py",
        "dashboard_simple.py"
    ]
    
    # Ejecutar cada script
    exitos = 0
    for i, script in enumerate(scripts, 1):
        print(f"[{i}/{len(scripts)}] ", end="")
        if ejecutar_script(script):
            exitos += 1
        print()
    
    print("=" * 60)
    print(f"✅ Scripts exitosos: {exitos}/{len(scripts)}")
    if exitos == len(scripts):
        print("🎉 ¡Todas las imágenes generadas exitosamente!")

if __name__ == "__main__":
    main() 