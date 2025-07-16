class encuestado:
    def __init__(self, id, nombre, experticia, opinion):
        self.id = id
        self.nombre = nombre
        self.experticia = experticia
        self.opinion = opinion


class Pregunta:
    def __init__(self, id_pregunta):
        self.id_pregunta = id_pregunta
        self.encuestados = [] 
        self.promedio_opinion = 0
        self.promedio_experticia = 0
        self.moda = None
        self.mediana = None
        self.extremismo = 0
        self.consenso = 0


class Tema:
    def __init__(self, nombre):
        self.nombre = nombre
        self.root_preguntas = ABBPreguntas()
        self.promedio_opinion = 0
        self.promedio_experticia = 0
        self.total_encuestados = 0

class NodoABBPregunta:
    def __init__(self, pregunta):
        self.pregunta = pregunta
        self.izquierda = None
        self.derecha = None


class ABBPreguntas:
    def __init__(self):
        self.raiz = None

    def insertar(self, pregunta):
        self.raiz = self._insertar_recursivo(self.raiz, pregunta)

    def _insertar_recursivo(self, nodo, pregunta):
        if nodo is None:
            return NodoABBPregunta(pregunta)

        # Criterio de ordenamiento:
        # Primero por promedio de opinión (mayor primero),
        # luego promedio de experticia, luego número de encuestados
        p1 = pregunta
        p2 = nodo.pregunta

        if (p1.promedio_opinion > p2.promedio_opinion or
            (p1.promedio_opinion == p2.promedio_opinion and p1.promedio_experticia > p2.promedio_experticia) or
            (p1.promedio_opinion == p2.promedio_opinion and
             p1.promedio_experticia == p2.promedio_experticia and
             len(p1.encuestados) > len(p2.encuestados))):
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, pregunta)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, pregunta)

        return nodo

    def recorrer_inorden(self):
        preguntas_ordenadas = []
        self._recorrer_inorden(self.raiz, preguntas_ordenadas)
        return preguntas_ordenadas

    def _recorrer_inorden(self, nodo, lista):
        if nodo:
            self._recorrer_inorden(nodo.izquierda, lista)
            lista.append(nodo.pregunta)
            self._recorrer_inorden(nodo.derecha, lista)


### NODO DEL ARBOL BINARIO DE BUSQUEDA EN TEMA
class NodoABBTema:
    def __init__(self, tema):
        self.tema = tema
        self.izquierda = None
        self.derecha = None



class ABBTemas:
    def __init__(self):
        self.raiz = None

    def insertar(self, tema):
        self.raiz = self._insertar_recursivo(self.raiz, tema)

    def _insertar_recursivo(self, nodo, tema):
        if nodo is None:
            return NodoABBTema(tema)

        t1 = tema
        t2 = nodo.tema

        if (t1.promedio_opinion > t2.promedio_opinion or
            (t1.promedio_opinion == t2.promedio_opinion and t1.promedio_experticia > t2.promedio_experticia) or
            (t1.promedio_opinion == t2.promedio_opinion and
             t1.promedio_experticia == t2.promedio_experticia and
             t1.total_encuestados > t2.total_encuestados)):
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, tema)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, tema)

        return nodo

    def recorrer_inorden(self):
        temas_ordenados = []
        self._recorrer_inorden(self.raiz, temas_ordenados)
        return temas_ordenados

    def _recorrer_inorden(self, nodo, lista):
        if nodo:
            self._recorrer_inorden(nodo.izquierda, lista)
            lista.append(nodo.tema)
            self._recorrer_inorden(nodo.derecha, lista)
