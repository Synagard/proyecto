#Juego de trivia
#
#11/24   C&S

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import random


definiciones = {
    "Cálculo I": [
        {"_pregunta": "¿Qué es un límite?", "respuesta": "Valor al que se aproxima una función"},
        {"_pregunta": "¿Qué es una derivada?", "respuesta": "Tasa de cambio instantánea"}
    ],
    "Mecánica I": [
        {"_pregunta": "¿Qué es la velocidad?", "respuesta": "Cambio de posición en el tiempo"},
        {"_pregunta": "¿Qué es la aceleración?", "respuesta": "Cambio de velocidad en el tiempo"}
    ]
}
"""
deberíamos añadir más definiciones y más ramos pq igual son re pocos yo creo que asi esta bien, la idea es que mostremos como funciona el programa porque lo otro es solo añadir
cantidad y va a funcionar igual
Weno
"""

def ocultar(definicion):
    palabras = definicion.split()
    return "   ".join(
        palabra if len(palabra) == 2 else  
        "".join(
            letra if i == 0 or i == len(palabra) - 1 else "_ "
            for i, letra in enumerate(palabra)
        ).strip()
        for palabra in palabras
    )


definiciones["Mixtas"] = definiciones["Cálculo I"] + definiciones["Mecánica I"]
random.shuffle(definiciones["Mixtas"])  

class Juego(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trivia de Física y Matemáticas")
        self.setGeometry(100, 100, 600, 400)

        self.estructura = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.estructura)
        self.setCentralWidget(self.central_widget)

        self.iniciar_interfaz()

    def iniciar_interfaz(self):
        self.limpiar()  
        self.estructura.addWidget(QLabel("Bienvenidos a la Trivia de Física y Matemáticas"))

        _comenzar = QPushButton("Jugar")
        _comenzar.clicked.connect(self.ramas)
        self.estructura.addWidget(_comenzar)

        _instrucciones = QPushButton("Instrucciones")
        _instrucciones.clicked.connect(self.mostrar_instrucciones)
        self.estructura.addWidget(_instrucciones)

        _salir = QPushButton("Salir")
        _salir.clicked.connect(self.close)
        self.estructura.addWidget(_salir)

    def mostrar_instrucciones(self):
        instrucciones = """
        Instrucciones del Juego:
        
        1. Selecciona la rama de conocimiento (Física, Matemáticas o Mixtas).
        2. Elige el tema dentro de la rama seleccionada.
        3. Se te presentará una pregunta con una definición oculta. 
        4. Debes escribir la respuesta correcta y presionar "Verificar". ¡Recuerda usar los tildes!
        5. Tienes 3 intentos para responder correctamente cada pregunta.
        6. Si aciertas todas las preguntas, ¡ganas el juego! Si te quedas sin intentos, pierdes y serás humillado.
        """
        
        QMessageBox.information(self, "Instrucciones", instrucciones)

    def ramas(self):
        self.limpiar()
        label = QLabel("Selecciona una rama:")
        self.estructura.addWidget(label)

        _fisica = QPushButton("Física")
        _fisica.clicked.connect(lambda: self.mostrar_seleccion_seccion("Física"))
        self.estructura.addWidget(_fisica)

        _matematicas = QPushButton("Matemáticas")
        _matematicas.clicked.connect(lambda: self.mostrar_seleccion_seccion("Matemáticas"))
        self.estructura.addWidget(_matematicas)

        _mixta = QPushButton("Mixtas")
        _mixta.clicked.connect(lambda: self.iniciar("Mixtas"))
        self.estructura.addWidget(_mixta)

        _atras = QPushButton("Atrás")
        _atras.clicked.connect(self.iniciar_interfaz)
        self.estructura.addWidget(_atras)

    def mostrar_seleccion_seccion(self, rama):
        self.limpiar()
        label = QLabel(f"Selecciona un tema de {rama}:")
        self.estructura.addWidget(label)

        if rama == "Física":
            _mecanica1 = QPushButton("Mecánica I")
            _mecanica1.clicked.connect(lambda: self.iniciar("Mecánica I"))
            self.estructura.addWidget(_mecanica1)
        elif rama == "Matemáticas":
            _calculo1 = QPushButton("Cálculo I")
            _calculo1.clicked.connect(lambda: self.iniciar("Cálculo I"))
            self.estructura.addWidget(_calculo1)

        _atras = QPushButton("Atrás")
        _atras.clicked.connect(self.ramas)
        self.estructura.addWidget(_atras)

    def iniciar(self, seccion):
        self.limpiar()

        if seccion == "Mixtas":
            self._preguntas = definiciones["Mixtas"]
        else:
            self._preguntas = definiciones.get(seccion, [])

        self._pregunta_actual = 0
        self.vidas = 3
        self.aciertos = 0 

        if not self._preguntas:
            QMessageBox.information(self, "Sin _preguntas", f"No hay _preguntas en la sección {seccion}.")
            self.ramas()
            return

        self.mostrar__pregunta()

    def mostrar__pregunta(self):
        self.limpiar()

        _pregunta = self._preguntas[self._pregunta_actual]
        d_oculta = ocultar(_pregunta["respuesta"])

        _prgt = QLabel(_pregunta["_pregunta"])
        _prgt.setFont(QFont("Helvetica", 14))
        self.estructura.addWidget(_prgt)

        _definicion = QLabel(d_oculta)
        _definicion.setFont(QFont("Helvetica", 12))
        self.estructura.addWidget(_definicion)

        self.entrada_respuesta = QLineEdit()
        self.estructura.addWidget(self.entrada_respuesta)

        _verificar = QPushButton("Verificar")
        _verificar.clicked.connect(self.verificar_respuesta)
        self.estructura.addWidget(_verificar)

        _atras = QPushButton("Atrás")
        _atras.clicked.connect(self.ramas)
        self.estructura.addWidget(_atras)

    def verificar_respuesta(self):
        r_ingresada = self.entrada_respuesta.text().strip()
        r_correcta = self._preguntas[self._pregunta_actual]["respuesta"]

        if r_ingresada.lower() == r_correcta.lower():
            self.aciertos += 1  
            self._pregunta_actual += 1  
            if self._pregunta_actual < len(self._preguntas):
                self.mostrar__pregunta()  
            else:
                self.resultado(True)  
        else:
            self.vidas -= 1
            if self.vidas > 0:
                QMessageBox.warning(self, "Incorrecto", f"Respuesta incorrecta. Te quedan {self.vidas} intentos.")
            else:
                self.resultado(False)

    def resultado(self, acierto):
        self.limpiar()

        # lobo auuuuuuu
        if self.aciertos == len(self._preguntas):
            label = QLabel("¡Ganaste! Respondiste todas las _preguntas correctamente.")
            _sonido = "lobo.ogg"
            imagen = "V.jpg"
            _reiniciar = QPushButton("Reiniciar juego")
            _reiniciar.clicked.connect(self.ramas)
            self.estructura.addWidget(_reiniciar)
        else:
            label = QLabel("¡Perdiste!") #XDDDD es muy chistoso este audio
            _sonido = "gato.ogg"
            imagen = "F.jpg"
            _reiniciar = QPushButton("Reiniciar juego")
            _reiniciar.clicked.connect(self.ramas)
            self.estructura.addWidget(_reiniciar)
#podriamos cambiarlo por trompetas
#Me gusta más el gato LKJHASKJFLHASF
        label.setFont(QFont("Helvetica", 16))
        self.estructura.addWidget(label)

        imagen_label = QLabel()
        pixmap = QPixmap(imagen)
        imagen_label.setPixmap(pixmap)
        self.estructura.addWidget(imagen_label)

        self.reproducir_sonido(self.ruta_archivo(_sonido))

    def ruta_archivo(self, archivo):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(directorio_actual, archivo)
        return ruta_archivo

    def reproducir_sonido(self, archivo):
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(archivo)))
        self.player.play()

    def limpiar(self):
        for i in reversed(range(self.estructura.count())):
            widget = self.estructura.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    interfaz = Juego()
    interfaz.show()
    sys.exit(app.exec_())

#si apretamos el botón de volver a atrás, aparecen pestañas infinitas xddd Ya lo arreglé
