"""
Created on Thu Jan  2 12:13:30 2025

@author: Jesús Sardá
"""

import random
import json
import pickle

# -----------------------------------------------------------------
#   Funciones auxiliares
# -----------------------------------------------------------------

def lee_equipo(nombre_archivo):
    with open(f'{nombre_archivo}', 'rb') as archivo:
        configuracion_enigma = pickle.load(archivo)
    # configuracion_enigma= {}
    # try:
    #     nombre = nombre_archivo + pkl
    #     with open(f'{nombre}.pkl', 'rb') as archivo:
    #         configuracion_enigma = pickle.load(archivo)
    # except Exception:
    #     print(f'\tEl archivo <{nombre_archivo}.pkl> no existe o no pudo abrirse')
    #     exit()
    return configuracion_enigma

# -----------------------------------------------------------------

def guarda_equipo(datos_configuracion, nombre_archivo):
    try:
        with open(f'{nombre_archivo}', 'wb') as archivo:
            pickle.dump(datos_configuracion, archivo)
    except Exception:
        print(f'\tEl archivo <{nombre_archivo}> no pudo ser creado')

#-----------------------------------------------------------------

def  crea_lista_aleatorios(opciones, cantidad):
    lista_aleatoria = [random.randint(1, opciones) for _ in range(cantidad)]
    return lista_aleatoria

# -----------------------------------------------------------------

class ROTOR():

    # ------------------------------------------------------------------------------------------------------

    def __init__(self,  alfabeto,  nombre= 'rotor', configura= False):
        self.nombre = nombre

        self.alfa = alfabeto
        self.ordinales = list(range(len(self.alfa)))
        self.config =   configura
        self.cableado = self.ordinales
        self.selector = 1

        # Gira el rotor para colocarlo en la selección.

        if self.config:
            self.cableado = self.configura(self.ordinales)
        else:
            self.cableado = self.lee_configuracion(nombre)

    # ------------------------------------------------------------------------------------------------------

    def reinicia_rotor(self):
        self.cableado = self.lee_configuracion(self.nombre)

    # ------------------------------------------------------------------------------------------------------

    def gira_rotor(self, selector):
        lista = self.cableado.copy()
        for i in range(selector):
            inicio = lista.pop(0)
            lista.append(inicio)
        self.selector = selector
        return lista

    # ------------------------------------------------------------------------------------------------------

    def configura(self, ordinales):
        self.lista = ordinales.copy()
        random.shuffle(self.lista)
        self.guarda_configuracion(self.nombre, self.lista)
        return self.lista

    # ------------------------------------------------------------------------------------------------------

    def guarda_configuracion(self, nombre, datos):
        with open(f'{nombre}.json', 'w') as archivo:
            json.dump(datos, archivo)

    # ------------------------------------------------------------------------------------------------------

    def lee_configuracion(self, nombre):
        try:
            with open(f'{nombre}.json', 'r') as archivo:
                datos = json.load(archivo)
        except Exception:
            print(f'\tNo existe el archivo <{nombre}.json>. El rotor se creará pero este rotor no estará codificado')
        return self.cableado


    # ------------------------------------------------------------------------------------------------------

    def muesta_configuracion(self, alfa = True, referencia= True):
        print(f'\tConfiguración de <{self.nombre}>')
        print(f'\t', end = ' ')
        if referencia:
            for char in self.alfa:
                print(f'{char:>2s}', end = ', ')
        print(f'\n\t', end = ' ')
        for ord in self.cableado:
            if alfa:
                print(f'{self.alfa[ord]:>2s}', end = ', ')
            else:
                print(f'{str(ord):>2s}', end=', ')
        print()
        print()

    # ------------------------------------------------------------------------------------------------------

    def procesa(self, ordinal, adelante=True):
        if isinstance(ordinal, int) and ordinal <= len(self.cableado):
            if adelante:
                return self.cableado[ordinal]
            else:
                return self.cableado.index(ordinal)
        else:
            print('\tValor ordinal no es un número entero')

# ------------------------------------------------------------------------------------------------------

class REFLECTOR(ROTOR):

    def __init__(self, alfabeto,  nombre= 'reflector', configura= False):
        super().__init__(alfabeto,  nombre, configura)

# ------------------------------------------------------------------------------------------------------

class PANEL():

    # ------------------------------------------------------------------------------------------------------

    def __init__(self,  alfabeto, lista_cambios, nombre= 'panel', configura= False):
        self.nombre = nombre

        self.alfa = alfabeto
        self.ordinales = list(range(len(self.alfa)))
        self.config =   configura
        self.cableado = self.ordinales
        self.cambios= lista_cambios

        if self.config:
            self.cableado = self.configura(self.cambios)
        else:
            self.cableado = self.lee_configuracion(nombre)

    # ------------------------------------------------------------------------------------------------------

    def configura(self, lista_cambios):
        cableado = self.ordinales.copy()
        for car_origen, car_cambio in lista_cambios:
            ord_origen = self.alfa.index(car_origen.upper())
            ord_cambio = self.alfa.index(car_cambio.upper())
            cableado[ord_origen] = ord_cambio
            cableado[ord_cambio] = ord_origen
        self.guarda_configuracion(self.nombre, cableado)
        self.cableado = cableado
        return cableado

    # ------------------------------------------------------------------------------------------------------

    def guarda_configuracion(self, nombre, datos):
        with open(f'{nombre}.json', 'w') as archivo:
            json.dump(datos, archivo)

    # ------------------------------------------------------------------------------------------------------

    def lee_configuracion(self, nombre):
        try:
            with open(f'{nombre}.json', 'r') as archivo:
                datos = json.load(archivo)
                print(datos)
        except Exception:
            print(f'\tNo existe el archivo <{nombre}.json>. El rotor se creará pero este rotor no estará codificado')
        return self.cableado

    # ------------------------------------------------------------------------------------------------------

    def muesta_configuracion(self, alfa = True, referencia= True):
        print(f'\tConfiguración de <{self.nombre}>')
        print(f'\t', end = ' ')
        if referencia:
            if alfa:
                for char in self.alfa:
                    print(f'{char:>2s}', end = ', ')
            else:
                for ord in self.ordinales:
                    print(f'{str(ord):>2s}', end=', ')
        print(f'\n\t', end = ' ')
        for ord in self.cableado:
            if alfa:
                print(f'{self.alfa[ord]:>2s}', end = ', ')
            else:
                print(f'{str(ord):>2s}', end=', ')
        print()
        print()

    # ------------------------------------------------------------------------------------------------------

    def procesa(self, ordinal, adelante=True):
        if isinstance(ordinal, int) and ordinal <= len(self.cableado):
            if adelante:
                return self.cableado[ordinal]
            else:
               return self.cableado.index(ordinal)
        else:
            print('\tValor ordinal no es un número entero')

#-----------------------------------------------------------------

class ENIGMA():

    # ------------------------------------------------------------------------------------------------------

    def __init__(self, configuracion):

        self.caja =         configuracion['caja_rotores']
        self.alfa =         configuracion['alfabeto']
        self.rotores =      configuracion['rotores']
        self.reflector =    configuracion['reflector']
        self.panel =        configuracion['panel']

        self.cant_car = len(self.alfa)
        self.cant_rot = len(self.rotores)
        self.cant_caj = len(self.caja)

    # ------------------------------------------------------------------------------------------------------

    def lee_numeracion_rotores(self):
        ord_rotores = []
        for rotor in self.rotores:
            ord = self.caja.index(rotor)
            ord_rotores.append(ord+1)
        return ord_rotores

    # ------------------------------------------------------------------------------------------------------

    def invierte_rotores(self, rotores):
        inverso = rotores.copy()
        inverso.reverse()
        return inverso

    # ------------------------------------------------------------------------------------------------------

    def cambia_rotores(self, lista_cambios):
        if len(lista_cambios) == self.cant_rot:
            val_min = min(lista_cambios)
            val_max = max(lista_cambios)
            if val_max <= self.cant_caj:
                if val_min > 0:
                    nuevos = []
                    for ind in lista_cambios:
                        nuevos.append(self.caja[ind-1])
                    self.rotores = nuevos
                    return self.rotores
                else:
                    print(f'\t*** ERROR *** La numeración de los rotores comienzan en 1')
                    exit()
            else:
                print(f'\t*** ERROR *** Se pide un rotor {max(lista_cambios)} que no existe, solo hay {self.cant_caj} rotores en caja')
                exit()
        else:
            print(f'\t*** ERROR *** La cantidad de rotores debe ser {self.cant_rot}')
            exit()

    # ------------------------------------------------------------------------------------------------------

    def reinicia_rotores(self):
        for rotor in self.rotores:
            rotor.reinicia_rotor()
        return self.rotores

    # ------------------------------------------------------------------------------------------------------

    def gira_rotores(self, selectores):
        selectores = self.analiza_selectores(selectores)
        for i, rotor in enumerate(self.rotores):
            rotor.cableado = rotor.gira_rotor(selectores[i])
        self.selectores = selectores
        return self.rotores

    # ------------------------------------------------------------------------------------------------------

    def analiza_selectores(self, selectores):
        if len(selectores) == self.cant_rot:
            for i, selector in enumerate(selectores):
                if selector > self.cant_car:
                    selectores[i] = selector % self.cant_car
                    selectores[i + 1] += selector // self.cant_car
            return selectores
        else:
            print(f'\t**ERROR**. el número de selectores ({len(selectores)}) debe concidir con el de rotores ({self.cant_rot})')
            exit()

    # ------------------------------------------------------------------------------------------------------

    def cablea_panel(self, lista_conexiones):
        self.panel.configura(lista_conexiones)

    # ------------------------------------------------------------------------------------------------------
    # *** ESTE EES EL CORAZÓN DE LA CLASE  <++

    def codifica(self, car, adelante =True):
        valor = self.tecla(car.upper())

        if not adelante:
            valor = self.panel.procesa(valor, adelante)     # para mantener la secuancia
        for rotor in self.rotores:
            valor = rotor.procesa(valor, adelante)
        valor = self.reflector.procesa(valor, adelante)
        for rotor in reversed(self.rotores):
            valor = rotor.procesa(valor,  adelante)
        if adelante:
            valor = self.panel.procesa(valor, adelante)     # para mantener la secuancia
        cod = self.bombilla(valor)
        return cod

    # ------------------------------------------------------------------------------------------------------

    def encripta_texto(self, mensaje):
        encriptado = []
        for car in mensaje:
            cod = self.codifica(car)
            encriptado.append(cod)
        codificado = ''.join(encriptado)
        return codificado

    # ------------------------------------------------------------------------------------------------------

    def desencripta_codigo(self, codigo):
        decriptado = []
        for cod in codigo:
            car = self.codifica(cod, adelante=False)
            decriptado.append(car)
        recuperado = ''.join(decriptado)
        return recuperado

    # ------------------------------------------------------------------------------------------------------

    def guarda_datos_para_destino(self, codigo, nombre_archivo):
        with open(f'{nombre_archivo}', 'w') as archivo:
            json.dump(codigo, archivo)

    # ------------------------------------------------------------------------------------------------------

    def lee_datos_origen(self, nombre_archivo):
        with open(f'{nombre_archivo}', 'r') as archivo:
            datos = json.load(archivo)
        return datos

    # ------------------------------------------------------------------------------------------------------

    def tecla(self,car):
        if isinstance(car, str):
            if car in self.alfa:
                return self.alfa.index(car)
            else:
                print(f'\t**ERROR**. El carácter no está en el teclado')
        else:
            print('\t**ERROR**. El carácter no es alfabético')
        exit()

    # ------------------------------------------------------------------------------------------------------

    def bombilla(self,valor):
        if isinstance(valor, int):
            return self.alfa[valor]
        else:
            print('\tValor no es un número entero')

    # --------------------------------------------------------------------

    def encripta_configuracion(self, configuracion):

        rotores =       configuracion['rotores']
        selectores =    configuracion['selectores']
        cableado =      configuracion['cableado']


        car_rotores = []
        for ord in rotores:
            car_rotores.append(self.alfa[ord - 1])
        norm_rotores = ''.join(car_rotores)
        encr_rotores = self.encripta_texto(norm_rotores)

        car_selector = []
        for ord in selectores:
            car_selector.append(self.alfa[ord - 1])
        norm_selector = ''.join(car_selector)
        encr_selector = self.encripta_texto(norm_selector)

        num_cable = len(cableado)
        norm_num = self.alfa[num_cable]
        encr_num = self.encripta_texto(norm_num)

        car_cable = []
        for par in cableado:
            car_cable.append(''.join(par))
        norm_cable = ''.join(car_cable)
        encr_cable = self.encripta_texto(norm_cable)

        return [encr_rotores, encr_selector, encr_num, encr_cable]

    # --------------------------------------------------------------------

    def recupera_configuracion(self, codigo, reglas):

        config = {}
        for clave, regla in reglas.items():

            if clave == 'loc_rotores':
                pos, cant = regla
                dato = codigo[pos:pos + cant]
                desencriptado = self.desencripta_codigo(dato)
                tmp  = []
                for car in desencriptado:
                    tmp.append(self.alfa.index(car)+1)
                config['rotores'] = tmp

            elif clave == 'loc_selectores':
                pos, cant = regla
                dato = codigo[pos:pos + cant]
                desencriptado = self.desencripta_codigo(dato)
                tmp  = []
                for car in desencriptado:
                    tmp.append(self.alfa.index(car)+1)
                config['selectores'] = tmp

            elif clave == 'loc_numero':
                pos, cant = regla
                dato = codigo[pos:pos + cant]
                desencriptado = self.desencripta_codigo(dato)
                num = self.alfa.index(desencriptado)

            elif clave == 'loc_cables':
                pos, cant = regla
                cant = num*2
                dato = codigo[pos:pos + cant]
                desencriptado = self.desencripta_codigo(dato)
                tmp = []
                for i in range(0, cant, 2):
                    par = desencriptado[i:i+1], desencriptado[i+1:i+2]
                    tmp.append(par)
                config['cableado'] = tmp

            elif clave == 'loc_codigo':
                pos = pos+cant
                msg_codificado = codigo[pos:]

        return config, msg_codificado









