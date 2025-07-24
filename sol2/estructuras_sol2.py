class Encuestado:
    def __init__(self, id, nombre, experticia, opinion):
        self.id = id
        self.nombre = nombre
        self.experticia = experticia
        self.opinion = opinion


# Nodo para lista doble de preguntas
class NodoPregunta:
    def __init__(self, pregunta):
        self.pregunta = pregunta
        self.anterior = None
        self.siguiente = None


class Pregunta:
    def __init__(self, id_pregunta):
        self.id_pregunta = id_pregunta
        self.encuestados = []
        self.promedio_opinion = 0
        self.promedio_experticia = 0
        self.mediana = None
        self.moda = None
        self.extremismo = 0
        self.consenso = 0


class ListaPreguntas:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def insertar_ordenado(self, pregunta):
        nuevo = NodoPregunta(pregunta)
        if self.cabeza is None:
            self.cabeza = self.cola = nuevo
            return

        actual = self.cabeza
        while actual:
            p1 = pregunta
            p2 = actual.pregunta

            if (p1.promedio_opinion > p2.promedio_opinion or
                (p1.promedio_opinion == p2.promedio_opinion and p1.promedio_experticia > p2.promedio_experticia) or
                (p1.promedio_opinion == p2.promedio_opinion and
                 p1.promedio_experticia == p2.promedio_experticia and
                 len(p1.encuestados) > len(p2.encuestados))):
                break
            actual = actual.siguiente

        if actual is None:
            self.cola.siguiente = nuevo
            nuevo.anterior = self.cola
            self.cola = nuevo
        elif actual.anterior is None:
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo
        else:
            anterior = actual.anterior
            anterior.siguiente = nuevo
            nuevo.anterior = anterior
            nuevo.siguiente = actual
            actual.anterior = nuevo

    def recorrer_ordenado(self):
        preguntas = []
        actual = self.cabeza
        while actual:
            preguntas.append(actual.pregunta)
            actual = actual.siguiente
        return preguntas


# Nodo para lista enlazada de temas
class NodoTema:
    def __init__(self, tema):
        self.tema = tema
        self.siguiente = None


class Tema:
    def __init__(self, nombre):
        self.nombre = nombre
        self.lista_preguntas = ListaPreguntas()
        self.promedio_opinion = 0
        self.promedio_experticia = 0
        self.total_encuestados = 0


class ListaTemas:
    def __init__(self):
        self.cabeza = None

    def insertar(self, tema):
        nuevo = NodoTema(tema)
        if self.cabeza is None:
            self.cabeza = nuevo
            return

        actual = self.cabeza
        anterior = None
        while actual:
            t1 = tema
            t2 = actual.tema

            if (t1.promedio_opinion > t2.promedio_opinion or
                (t1.promedio_opinion == t2.promedio_opinion and t1.promedio_experticia > t2.promedio_experticia) or
                (t1.promedio_opinion == t2.promedio_opinion and
                 t1.promedio_experticia == t2.promedio_experticia and
                 t1.total_encuestados > t2.total_encuestados)):
                break
            anterior = actual
            actual = actual.siguiente

        if anterior is None:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
        else:
            anterior.siguiente = nuevo
            nuevo.siguiente = actual

    def recorrer(self):
        temas = []
        actual = self.cabeza
        while actual:
            temas.append(actual.tema)
            actual = actual.siguiente
        return temas
