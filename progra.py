# Juego de trivia
# 11/24   C&S

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QMessageBox, QInputDialog
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



# preg. mixtas
definiciones["Mixtas"] = definiciones["Cálculo I"] + definiciones["Mecánica I"]
random.shuffle(definiciones["Mixtas"])

# Ocultar def
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
        self.estructura.addWidget(QLabel(" " * 48 + "Bienvenidos a la Trivia de Física y Matemáticas"))

        _comenzar = QPushButton("Jugar")
        _comenzar.clicked.connect(self.ramas)
        self.estructura.addWidget(_comenzar)

        _instrucciones = QPushButton("Instrucciones")
        _instrucciones.clicked.connect(self._instrucciones)
        self.estructura.addWidget(_instrucciones)

        _salir = QPushButton("Salir")
        _salir.clicked.connect(self.close)
        self.estructura.addWidget(_salir)

    def _instrucciones(self):
        instrucciones = """
        Instrucciones del Juego:

        1. Selecciona la rama de conocimiento (Física, Matemáticas o Mixtas).
        2. Elige el tema dentro de la rama seleccionada.
        3. Ingresa el número de preguntas que deseas responder.
        4. Responde las preguntas correctamente para ganar. Tienes 3 intentos por pregunta.
        """
        QMessageBox.information(self, "Instrucciones", instrucciones)

    def ramas(self): #seleccionar el area
        self.limpiar()
        label = QLabel(" " * 70 + "Selecciona una rama:")
        self.estructura.addWidget(label)

        _fisica = QPushButton("Física")
        _fisica.clicked.connect(lambda: self._seccion("Física"))
        self.estructura.addWidget(_fisica)

        _matematicas = QPushButton("Matemáticas")
        _matematicas.clicked.connect(lambda: self._seccion("Matemáticas"))
        self.estructura.addWidget(_matematicas)

        _mixta = QPushButton("Mixtas")
        _mixta.clicked.connect(lambda: self.iniciar("Mixtas"))
        self.estructura.addWidget(_mixta)

        _atras = QPushButton("Atrás")
        _atras.clicked.connect(self.iniciar_interfaz)
        self.estructura.addWidget(_atras)

    def _seccion(self, rama): #bifurcación de areas
        self.limpiar()
        label = QLabel(" " * 60 + f"Selecciona un tema de {rama}:")
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

    def elegir_numero_preguntas(self, seccion):
        """Permite al usuario elegir el número de preguntas."""
        total_preguntas = len(definiciones[seccion])
        if total_preguntas == 0:
            QMessageBox.warning(self, "Sin preguntas", f"No hay preguntas en la sección {seccion}.")
            self.ramas()
            return None

        num_preguntas, ok = QInputDialog.getInt(
            self,
            "Número de preguntas",
            f"Selecciona el número de preguntas (1-{total_preguntas}):",
            min=1, max=total_preguntas, step=1
        )

        if ok:
            return num_preguntas
        else:
            self.ramas()
            return None

    def iniciar(self, seccion):
        self.limpiar()


        if seccion not in definiciones:
            QMessageBox.warning(self, "Error", f"La sección {seccion} no existe.")
            self.ramas()
            return

        num_preguntas = self.elegir_numero_preguntas(seccion)

        if num_preguntas is None:
            return

    #preg. aleatorias
        self._preguntas = random.sample(definiciones[seccion], min(num_preguntas, len(definiciones[seccion])))
        self._pregunta_actual = 0
        self.vidas = 3
        self.aciertos = 0

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
            label = QLabel(" " * 2 + "¡Ganaste! Respondiste todas las preguntas correctamente.")
            _sonido = "lobo.ogg"
            imagen = "V.jpg"
        else:
            label = QLabel(" " * 50 + "¡Perdiste!")
            _sonido = "gato.ogg" #XDDDD es muy chistoso este audio
            imagen = "F.jpg"

        label.setFont(QFont("Helvetica", 16))
        self.estructura.addWidget(label)

        imagen_label = QLabel()
        pixmap = QPixmap(imagen)
        imagen_label.setPixmap(pixmap)
        self.estructura.addWidget(imagen_label)

        self.reproducir_sonido(self.ruta_archivo(_sonido))

        _reiniciar = QPushButton("Reiniciar juego")
        _reiniciar.clicked.connect(self.ramas)
        self.estructura.addWidget(_reiniciar)
#podriamos cambiarlo por trompetas
#Me gusta más el gato LKJHASKJFLHASF
    def ruta_archivo(self, archivo):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(directorio_actual, archivo)
        return ruta_archivo

    def reproducir_sonido(self, archivo):
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(archivo)))
        self.player.play()

    def limpiar(self):
        while self.estructura.count():
            widget = self.estructura.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Juego()
    ventana.show()
    sys.exit(app.exec_())

#si apretamos el botón de volver a atrás, aparecen pestañas infinitas xddd Ya lo arreglé
