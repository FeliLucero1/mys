#!/usr/bin/env python3
"""
Script de Configuración - Modelo de Simulación
Trabajo Final - Modelos y Simulación
Felipe Lucero

Este script facilita la instalación y configuración del entorno
para ejecutar el modelo de simulación.
"""

import subprocess
import sys
import os
from pathlib import Path

def verificar_python():
    """Verifica que Python esté instalado y sea compatible"""
    print("Verificando versión de Python...")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def crear_entorno_virtual():
    """Crea un entorno virtual para el proyecto"""
    print("\nCreando entorno virtual...")
    
    try:
        # Crear entorno virtual
        subprocess.run([sys.executable, "-m", "venv", "tfi-env"], check=True)
        print("✅ Entorno virtual creado: tfi-env")
        
        # Determinar comando de activación
        if os.name == 'nt':  # Windows
            activate_script = "tfi-env\\Scripts\\activate"
        else:  # Linux/Mac
            activate_script = "source tfi-env/bin/activate"
        
        print(f"📝 Para activar el entorno virtual, ejecuta:")
        print(f"   {activate_script}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear entorno virtual: {e}")
        return False

def instalar_dependencias():
    """Instala las dependencias del proyecto"""
    print("\nInstalando dependencias...")
    
    try:
        # Determinar pip del entorno virtual
        if os.name == 'nt':  # Windows
            pip_cmd = "tfi-env\\Scripts\\pip"
        else:  # Linux/Mac
            pip_cmd = "tfi-env/bin/pip"
        
        # Instalar dependencias
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencias instaladas correctamente")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

def verificar_archivos():
    """Verifica que todos los archivos necesarios estén presentes"""
    print("\nVerificando archivos del proyecto...")
    
    archivos_requeridos = [
        "modelo.py",
        "analisis_datos.py", 
        "requirements.txt",
        "README.md"
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if Path(archivo).exists():
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} (faltante)")
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print(f"\n⚠️  Archivos faltantes: {', '.join(archivos_faltantes)}")
        return False
    
    print("✅ Todos los archivos están presentes")
    return True

def mostrar_instrucciones():
    """Muestra instrucciones de uso"""
    print("\n" + "="*60)
    print("🎉 CONFIGURACIÓN COMPLETADA")
    print("="*60)
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Activa el entorno virtual:")
    if os.name == 'nt':  # Windows
        print("   tfi-env\\Scripts\\activate")
    else:  # Linux/Mac
        print("   source tfi-env/bin/activate")
    
    print("\n2. Ejecuta el modelo de simulación:")
    print("   python modelo.py")
    
    print("\n3. Analiza los datos de Twitter (si tienes tweets_clean.csv):")
    print("   python analisis_datos.py")
    
    print("\n📁 ARCHIVOS GENERADOS:")
    print("   - resultados_simulacion.png: Gráficos de la simulación")
    print("   - analisis_twitter.png: Análisis de datos de Twitter")
    
    print("\n📚 DOCUMENTACIÓN:")
    print("   - README.md: Guía completa del proyecto")
    print("   - modelo.py: Código del modelo de simulación")
    print("   - analisis_datos.py: Análisis de datos reales")

def main():
    """Función principal de configuración"""
    print("🔧 CONFIGURACIÓN DEL PROYECTO")
    print("Modelo de Simulación: Viralización de Errores en Chatbots")
    print("Felipe Lucero - Trabajo Final - Modelos y Simulación\n")
    
    # Verificar Python
    if not verificar_python():
        return
    
    # Verificar archivos
    if not verificar_archivos():
        print("\n⚠️  Algunos archivos están faltantes. Asegúrate de tener todos los archivos del proyecto.")
        return
    
    # Crear entorno virtual
    if not crear_entorno_virtual():
        return
    
    # Instalar dependencias
    if not instalar_dependencias():
        return
    
    # Mostrar instrucciones
    mostrar_instrucciones()

if __name__ == "__main__":
    main() 