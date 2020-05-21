import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import os


class Estrella:
    def __init__(self, x, y, z, id_hd, mag_brillo, id_hrv_rev_num, noms=None):
        self.x = x
        self.y = y
        self.z = z
        self.id_hd = id_hd
        self.mag_brillo = mag_brillo
        self.id_hrv_rev_num = id_hrv_rev_num
        self.noms = noms


class Espacio:
    def __init__(self):
        self.starFile = open('stars.txt')
        self.listaEstrellas = []
        self.listaConstelaciones = []
        self.read_estrellas()
        self.read_constelaciones()

    def read_estrellas(self):
        """Método que se encarga de leer el archivo stars.txt y procesar la info de cada linea"""
        for estrella in self.starFile:
            # Partir cada linea en una lista (vector) con máximo 6 particiones, o 7 elementos
            datos_estrella = estrella.split(' ', 6)
            datos_estrella[len(datos_estrella) - 1] = datos_estrella[len(datos_estrella) - 1].rstrip('\n')

            # Solo las estrellas con nombre propio tiene  7 argumentos, luego se deben manejar de forma distinta
            if len(datos_estrella) == 7:
                datos_estrella[6] = datos_estrella[6].split(';')
                datos_estrella[6] = [nom.strip() for nom in datos_estrella[6]]
                star = Estrella(datos_estrella[0], datos_estrella[1], datos_estrella[2], datos_estrella[3],
                                datos_estrella[4], datos_estrella[5], datos_estrella[6])
            else:
                star = Estrella(datos_estrella[0], datos_estrella[1], datos_estrella[2], datos_estrella[3],
                                datos_estrella[4], datos_estrella[5])

            self.listaEstrellas.append(star)

    def read_constelaciones(self):
        """Se encarga de leer cada una de los archivos en \Constelaciones y por cada uno, establecer
         un objeto de tipo constelación"""
        for cons in os.listdir('.\\Constelaciones\\'):
            nom = cons[:-4]
            c = Constelacion(str(nom), self)
            self.listaConstelaciones.append(c)

    def graficar_masivo(self, estrellas, constelaciones):
        """Método que grafica todas las constelaciones, todas las estrellas, o ambos, según se requiera"""
        filename = '.\\Figuras\\Cielo'

        fig, ax = plt.subplots(figsize=(8, 8))

        # Establecer limites de los ejes entre -1 y 1
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)

        # Mostrar divisiones cada 0.2 unidades
        ax.xaxis.set_major_locator(MultipleLocator(0.2))
        ax.yaxis.set_major_locator(MultipleLocator(0.2))

        # Mostrar 4 sub-divisiones por división
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        ax.yaxis.set_minor_locator(AutoMinorLocator(4))

        # Encender el dibujo de ambos ejes, con lineas distintas
        # Los colores están en formato HEX
        ax.grid(which='major', color='#AAAAAA', linestyle='--')
        ax.grid(which='minor', color='#888888', linestyle=':')
        ax.set_facecolor('#111111')
        fig.patch.set_facecolor('#555555')

        # Dibujar lineas centrales para el plano cartesiano
        plt.plot([-1, 1], [0, 0], color='#FFFFFF', linewidth=1)
        plt.plot([0, 0], [-1, 1], color='#FFFFFF', linewidth=1)

        if estrellas:
            filename += '_Estrellas'
            x_estrellas = []
            y_estrellas = []
            b_estrellas = []
            for estrella in self.listaEstrellas:
                x_estrellas.append(float(estrella.x))
                y_estrellas.append(float(estrella.y))
                b_estrellas.append(float(estrella.mag_brillo))

            plt.scatter(x_estrellas, y_estrellas, s=b_estrellas, color='#BBBBBB')

        if constelaciones:
            filename += '_Constelaciones'
            conexiones = []
            for constelacion in self.listaConstelaciones:
                constelacion.get_constelacion()
                for conexion in constelacion.lista_conexiones:
                    par_x = []
                    par_y = []
                    for estrella in constelacion.lista_estrellas:
                        for nom in estrella.noms:
                            if nom in conexion:
                                par_x.append(float(estrella.x))
                                par_y.append(float(estrella.y))
                    conexiones.append([par_x, par_y])

                for conexion in conexiones:
                    plt.plot(conexion[0], conexion[1], color='#CCFF00', linewidth=1)

        filename += '.png'
        plt.savefig(filename)
        return filename

    def get_num_estrellas(self):
        return len(self.listaEstrellas)

    def get_num_constelaciones(self):
        return len(self.listaConstelaciones)


class Constelacion:

    def __init__(self, nom, espacio):
        self.lista_estrellas = []
        self.lista_conexiones = []
        self.nom = nom
        self.constelacion = open('.\\Constelaciones\\' + nom + '.txt')
        self.espacio = espacio

    def get_constelacion(self):
        """Obtener la constelación del archivo obtenido en el constructor
        Genera el vector de conexiones que contiene las coordenadas de
        las lineas y el vector estrellas que contiene las coordenadas y
        luminosidades de las estrellas"""

        # Vector de cadenas, simplemente contendrá los nombres de las
        # estrellas que ya han sido agregadas
        noms_estrellas = []
        for line in self.constelacion:
            conexion = line.split(',')
            conexion[1] = conexion[1].rstrip('\n')
            for estrella in conexion:
                if noms_estrellas.count(estrella) == 0:
                    noms_estrellas.append(estrella)
                    for existente in self.espacio.listaEstrellas:
                        # Si la estrella en cuestión tiene nombre propio
                        if existente.noms is not None:
                            # Verificamos si el nombre de la estrella que buscamos
                            # aparece en la lista de nombres de la estrella
                            cont = existente.noms.count(estrella)
                            if cont != 0:
                                self.lista_estrellas.append(existente)
                                break
            self.lista_conexiones.append(conexion)  # Agregamos la conexión a la lista de conexiones

    def graficar_constelacion(self, show_espacio):
        fig, ax = plt.subplots(figsize=(8, 8))

        # Establecer limites de los ejes entre -1 y 1
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)

        # Mostrar divisiones cada 0.2 unidades
        ax.xaxis.set_major_locator(MultipleLocator(0.2))
        ax.yaxis.set_major_locator(MultipleLocator(0.2))

        # Mostrar 4 sub-divisiones por división
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        ax.yaxis.set_minor_locator(AutoMinorLocator(4))

        # Encender el dibujo de ambos ejes, con lineas distintas
        # Los colores están en formato HEX
        ax.grid(which='major', color='#AAAAAA', linestyle='--')
        ax.grid(which='minor', color='#888888', linestyle=':')
        ax.set_facecolor('#111111')
        fig.patch.set_facecolor('#555555')

        # Dibujar lineas centrales para el plano cartesiano
        plt.plot([-1, 1], [0, 0], color='#FFFFFF', linewidth=1)
        plt.plot([0, 0], [-1, 1], color='#FFFFFF', linewidth=1)

        # Estas listas contienen las coordenadas de cada estrella
        coord_x = []
        coord_y = []

        # El brillo de cada estrella determina que tan grande se ve esta
        brillo = []

        # Contiene los pares de coordenadas x, y entre los cuales se dibuja
        # una linea
        conexiones = []

        if show_espacio:
            for estrella in self.espacio.listaEstrellas:
                coord_x.append(float(estrella.x))
                coord_y.append(float(estrella.y))
                brillo.append(float(estrella.mag_brillo))
        else:
            for estrella in self.lista_estrellas:
                coord_x.append(float(estrella.x))
                coord_y.append(float(estrella.y))
                brillo.append(float(estrella.mag_brillo))

        for conexion in self.lista_conexiones:
            par_x = []
            par_y = []
            for estrella in self.lista_estrellas:
                for nom in estrella.noms:
                    if nom in conexion:
                        par_x.append(float(estrella.x))
                        par_y.append(float(estrella.y))
            conexiones.append([par_x, par_y])

        for conexion in conexiones:
            plt.plot(conexion[0], conexion[1], color='#CCFF00', linewidth=1)

        plt.scatter(coord_x, coord_y, s=brillo, color='#BBBBBB')

        # plt.show()
        filename = '.\\Figuras\\' + self.nom
        if show_espacio:
            filename += '_full-cielo'
        else:
            filename += '_solo-constelacion'

        filename += '.png'

        plt.savefig(filename)

        return filename
