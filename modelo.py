"""
Modelo de Simulación: Viralización de Errores en Chatbots
Trabajo Final - Modelos y Simulación
Felipe Lucero

Este modelo simula cómo se propaga la información de errores en chatbots
y cómo esto afecta la carga del sistema y la percepción pública.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Tuple
import random
from collections import defaultdict
import seaborn as sns

# Configuración para gráficos en español
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False

@dataclass
class Usuario:
    """Representa un usuario que puede interactuar con el chatbot"""
    id: int
    tipo: str  # 'normal', 'influencer', 'critico'
    probabilidad_interaccion: float
    probabilidad_compartir: float
    influencia: float  # Factor de multiplicación para viralización
    estado: str = 'inactivo'  # 'inactivo', 'consciente', 'activo'
    
    def __post_init__(self):
        self.tiempo_ultima_interaccion = 0
        self.interacciones_totales = 0
        self.errores_reportados = 0

@dataclass
class Chatbot:
    """Representa el sistema de chatbot"""
    capacidad_maxima: int
    tiempo_respuesta_base: float
    probabilidad_error: float
    capacidad_actual: int = 0
    errores_totales: int = 0
    tiempo_respuesta_actual: float = 0.0
    
    def actualizar_capacidad(self, usuarios_activos: int):
        """Actualiza la capacidad del sistema basado en usuarios activos"""
        self.capacidad_actual = min(usuarios_activos, self.capacidad_maxima)
        # El tiempo de respuesta aumenta exponencialmente con la carga
        factor_carga = self.capacidad_actual / self.capacidad_maxima
        self.tiempo_respuesta_actual = self.tiempo_respuesta_base * (1 + factor_carga**2)
    
    def generar_error(self) -> bool:
        """Determina si el chatbot genera un error"""
        return random.random() < self.probabilidad_error

class ModeloViralizacion:
    """Modelo principal de simulación"""
    
    def __init__(self, 
                 num_usuarios: int = 1000,
                 capacidad_chatbot: int = 100,
                 tiempo_simulacion: int = 100):
        
        self.num_usuarios = num_usuarios
        self.tiempo_simulacion = tiempo_simulacion
        self.tiempo_actual = 0
        
        # Inicializar chatbot
        self.chatbot = Chatbot(
            capacidad_maxima=capacidad_chatbot,
            tiempo_respuesta_base=1.0,
            probabilidad_error=0.01  # 1% de probabilidad de error por defecto
        )
        
        # Inicializar usuarios
        self.usuarios = self._crear_usuarios()
        
        # Métricas de seguimiento
        self.metricas = {
            'usuarios_activos': [],
            'usuarios_conscientes': [],
            'carga_sistema': [],
            'errores_generados': [],
            'tiempo_respuesta': [],
            'percepcion_publica': []
        }
        
        # Eventos de viralización
        self.eventos_viralizacion = []
        
    def _crear_usuarios(self) -> List[Usuario]:
        """Crea la población de usuarios con diferentes características"""
        usuarios = []
        
        for i in range(self.num_usuarios):
            # Distribución de tipos de usuarios
            tipo_rand = random.random()
            if tipo_rand < 0.8:  # 80% usuarios normales
                tipo = 'normal'
                prob_interaccion = random.uniform(0.1, 0.3)
                prob_compartir = random.uniform(0.05, 0.15)
                influencia = random.uniform(1.0, 2.0)
            elif tipo_rand < 0.95:  # 15% usuarios críticos
                tipo = 'critico'
                prob_interaccion = random.uniform(0.4, 0.7)
                prob_compartir = random.uniform(0.3, 0.6)
                influencia = random.uniform(3.0, 8.0)
            else:  # 5% influencers
                tipo = 'influencer'
                prob_interaccion = random.uniform(0.2, 0.5)
                prob_compartir = random.uniform(0.6, 0.9)
                influencia = random.uniform(10.0, 50.0)
            
            usuario = Usuario(
                id=i,
                tipo=tipo,
                probabilidad_interaccion=prob_interaccion,
                probabilidad_compartir=prob_compartir,
                influencia=influencia
            )
            usuarios.append(usuario)
        
        return usuarios
    
    def _simular_interaccion_usuario(self, usuario: Usuario) -> bool:
        """Simula la interacción de un usuario con el chatbot"""
        if random.random() < usuario.probabilidad_interaccion:
            usuario.interacciones_totales += 1
            usuario.tiempo_ultima_interaccion = self.tiempo_actual
            
            # Verificar si el chatbot genera un error
            if self.chatbot.generar_error():
                self.chatbot.errores_totales += 1
                usuario.errores_reportados += 1
                return True  # Se generó un error
        return False
    
    def _simular_propagacion_error(self, usuario_error: Usuario):
        """Simula la propagación de información sobre el error"""
        # Calcular cuántos usuarios se enteran del error
        usuarios_afectados = int(usuario_error.influencia * 
                               usuario_error.probabilidad_compartir * 
                               random.uniform(0.5, 1.5))
        
        # Seleccionar usuarios aleatorios para hacer conscientes
        usuarios_disponibles = [u for u in self.usuarios if u.estado == 'inactivo']
        usuarios_seleccionados = random.sample(
            usuarios_disponibles, 
            min(usuarios_afectados, len(usuarios_disponibles))
        )
        
        for usuario in usuarios_seleccionados:
            usuario.estado = 'consciente'
            self.eventos_viralizacion.append({
                'tiempo': self.tiempo_actual,
                'usuario_origen': usuario_error.id,
                'usuario_afectado': usuario.id,
                'tipo_origen': usuario_error.tipo
            })
    
    def _calcular_percepcion_publica(self) -> float:
        """Calcula la percepción pública basada en errores y carga del sistema"""
        errores_por_usuario = self.chatbot.errores_totales / max(1, sum(u.interacciones_totales for u in self.usuarios))
        carga_relativa = self.chatbot.capacidad_actual / self.chatbot.capacidad_maxima
        
        # La percepción empeora con más errores y mayor carga
        percepcion = 1.0 - (errores_por_usuario * 10) - (carga_relativa * 0.3)
        return max(0.0, min(1.0, percepcion))
    
    def ejecutar_simulacion(self):
        """Ejecuta la simulación completa"""
        print(f"Iniciando simulación con {self.num_usuarios} usuarios por {self.tiempo_simulacion} pasos...")
        
        # Activar algunos usuarios inicialmente para iniciar la simulación
        usuarios_iniciales = random.sample(self.usuarios, min(10, len(self.usuarios)))
        for usuario in usuarios_iniciales:
            usuario.estado = 'consciente'
        
        # Simular un error inicial para activar la viralización
        if usuarios_iniciales:
            usuario_inicial = random.choice(usuarios_iniciales)
            if self._simular_interaccion_usuario(usuario_inicial):
                self._simular_propagacion_error(usuario_inicial)
                usuario_inicial.estado = 'activo'
        
        for tiempo in range(self.tiempo_simulacion):
            self.tiempo_actual = tiempo
            
            # Contar usuarios activos y conscientes
            usuarios_activos = sum(1 for u in self.usuarios if u.estado == 'activo')
            usuarios_conscientes = sum(1 for u in self.usuarios if u.estado == 'consciente')
            
            # Actualizar capacidad del chatbot
            self.chatbot.actualizar_capacidad(usuarios_activos)
            
            # Simular interacciones de usuarios conscientes
            usuarios_conscientes_lista = [u for u in self.usuarios if u.estado == 'consciente']
            for usuario in usuarios_conscientes_lista:
                if self._simular_interaccion_usuario(usuario):
                    # Si se generó un error, propagar la información
                    self._simular_propagacion_error(usuario)
                    # El usuario se vuelve activo (está reportando el error)
                    usuario.estado = 'activo'
            
            # Algunos usuarios activos pueden volver a ser conscientes
            for usuario in self.usuarios:
                if usuario.estado == 'activo' and random.random() < 0.1:
                    usuario.estado = 'consciente'
            
            # Ocasionalmente, algunos usuarios inactivos se vuelven conscientes (efecto de red)
            if tiempo > 0 and tiempo % 5 == 0:  # Cada 5 pasos
                usuarios_inactivos = [u for u in self.usuarios if u.estado == 'inactivo']
                if usuarios_inactivos:
                    # La probabilidad aumenta con el número de usuarios activos
                    prob_activacion = min(0.1, usuarios_activos / 1000)
                    for usuario in usuarios_inactivos:
                        if random.random() < prob_activacion:
                            usuario.estado = 'consciente'
            
            # Registrar métricas
            self.metricas['usuarios_activos'].append(usuarios_activos)
            self.metricas['usuarios_conscientes'].append(usuarios_conscientes)
            self.metricas['carga_sistema'].append(self.chatbot.capacidad_actual / self.chatbot.capacidad_maxima)
            self.metricas['errores_generados'].append(self.chatbot.errores_totales)
            self.metricas['tiempo_respuesta'].append(self.chatbot.tiempo_respuesta_actual)
            self.metricas['percepcion_publica'].append(self._calcular_percepcion_publica())
        
        print("Simulación completada.")
    
    def visualizar_resultados(self):
        """Genera gráficos de los resultados de la simulación"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Simulación: Viralización de Errores en Chatbots', fontsize=16)
        
        tiempo = list(range(self.tiempo_simulacion))
        
        # Gráfico 1: Usuarios activos y conscientes
        axes[0, 0].plot(tiempo, self.metricas['usuarios_activos'], 'r-', label='Usuarios Activos')
        axes[0, 0].plot(tiempo, self.metricas['usuarios_conscientes'], 'b-', label='Usuarios Conscientes')
        axes[0, 0].set_title('Evolución de Usuarios')
        axes[0, 0].set_xlabel('Tiempo')
        axes[0, 0].set_ylabel('Número de Usuarios')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Gráfico 2: Carga del sistema
        axes[0, 1].plot(tiempo, self.metricas['carga_sistema'], 'g-')
        axes[0, 1].set_title('Carga del Sistema')
        axes[0, 1].set_xlabel('Tiempo')
        axes[0, 1].set_ylabel('Carga Relativa')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Gráfico 3: Errores acumulados
        axes[0, 2].plot(tiempo, self.metricas['errores_generados'], 'm-')
        axes[0, 2].set_title('Errores Acumulados')
        axes[0, 2].set_xlabel('Tiempo')
        axes[0, 2].set_ylabel('Número de Errores')
        axes[0, 2].grid(True, alpha=0.3)
        
        # Gráfico 4: Tiempo de respuesta
        axes[1, 0].plot(tiempo, self.metricas['tiempo_respuesta'], 'c-')
        axes[1, 0].set_title('Tiempo de Respuesta')
        axes[1, 0].set_xlabel('Tiempo')
        axes[1, 0].set_ylabel('Tiempo (segundos)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Gráfico 5: Percepción pública
        axes[1, 1].plot(tiempo, self.metricas['percepcion_publica'], 'y-')
        axes[1, 1].set_title('Percepción Pública')
        axes[1, 1].set_xlabel('Tiempo')
        axes[1, 1].set_ylabel('Percepción (0-1)')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Gráfico 6: Análisis de eventos de viralización
        if self.eventos_viralizacion:
            df_eventos = pd.DataFrame(self.eventos_viralizacion)
            tipos_eventos = df_eventos['tipo_origen'].value_counts()
            axes[1, 2].pie(tipos_eventos.values, labels=tipos_eventos.index, autopct='%1.1f%%')
            axes[1, 2].set_title('Eventos de Viralización por Tipo de Usuario')
        
        plt.tight_layout()
        plt.savefig('resultados_simulacion.png', dpi=300, bbox_inches='tight')
        try:
            plt.show()
        except:
            print("Gráfico guardado como 'resultados_simulacion.png'")
            plt.close()
    
    def analizar_escenarios(self):
        """Ejecuta múltiples escenarios para análisis comparativo"""
        escenarios = {
            'Baja viralización': {'prob_error': 0.005, 'influencia_mult': 0.5},
            'Viralización normal': {'prob_error': 0.01, 'influencia_mult': 1.0},
            'Alta viralización': {'prob_error': 0.02, 'influencia_mult': 2.0},
            'Crisis viral': {'prob_error': 0.05, 'influencia_mult': 5.0}
        }
        
        resultados = {}
        
        for nombre, config in escenarios.items():
            print(f"\nEjecutando escenario: {nombre}")
            
            # Configurar escenario
            self.chatbot.probabilidad_error = config['prob_error']
            for usuario in self.usuarios:
                usuario.influencia *= config['influencia_mult']
            
            # Ejecutar simulación
            self.ejecutar_simulacion()
            
            # Guardar resultados
            resultados[nombre] = {
                'max_usuarios_activos': max(self.metricas['usuarios_activos']),
                'max_carga': max(self.metricas['carga_sistema']),
                'errores_finales': self.metricas['errores_generados'][-1],
                'percepcion_final': self.metricas['percepcion_publica'][-1]
            }
            
            # Resetear para siguiente escenario
            self._resetear_simulacion()
        
        return resultados
    
    def _resetear_simulacion(self):
        """Resetea la simulación para ejecutar nuevos escenarios"""
        self.tiempo_actual = 0
        self.chatbot.capacidad_actual = 0
        self.chatbot.errores_totales = 0
        self.chatbot.tiempo_respuesta_actual = 0.0
        
        for usuario in self.usuarios:
            usuario.estado = 'inactivo'
            usuario.tiempo_ultima_interaccion = 0
            usuario.interacciones_totales = 0
            usuario.errores_reportados = 0
            # NO resetear la influencia para mantener los multiplicadores de escenario
        
        self.metricas = {key: [] for key in self.metricas.keys()}
        self.eventos_viralizacion = []

def main():
    """Función principal para ejecutar la simulación"""
    print("=== Modelo de Simulación: Viralización de Errores en Chatbots ===")
    print("Felipe Lucero - Trabajo Final - Modelos y Simulación\n")
    
    # Crear y ejecutar simulación básica
    modelo = ModeloViralizacion(
        num_usuarios=1000,
        capacidad_chatbot=100,
        tiempo_simulacion=100
    )
    
    # Ejecutar simulación básica
    modelo.ejecutar_simulacion()
    modelo.visualizar_resultados()
    
    # Ejecutar análisis de escenarios
    print("\n=== Análisis de Escenarios ===")
    resultados_escenarios = modelo.analizar_escenarios()
    
    # Mostrar resultados comparativos
    print("\nResultados comparativos:")
    print("-" * 80)
    print(f"{'Escenario':<20} {'Max Usuarios':<12} {'Max Carga':<10} {'Errores':<8} {'Percepción':<10}")
    print("-" * 80)
    
    for escenario, datos in resultados_escenarios.items():
        print(f"{escenario:<20} {datos['max_usuarios_activos']:<12} "
              f"{datos['max_carga']:<10.2f} {datos['errores_finales']:<8} "
              f"{datos['percepcion_final']:<10.2f}")
    
    print("\n=== Análisis de Resultados ===")
    print("1. La viralización de errores puede causar saturación rápida del sistema")
    print("2. Los usuarios influyentes multiplican el impacto de los errores")
    print("3. La percepción pública se deteriora exponencialmente con la carga")
    print("4. Medidas de mitigación deberían incluir escalabilidad y moderación")

if __name__ == "__main__":
    main()

