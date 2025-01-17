# -*- coding: utf-8 -*-

"""
Created on Thu Jan  2 12:13:30 2025

@author: Jesús Sardá
"""

from libreria_clases import ROTOR, REFLECTOR, PANEL, ENIGMA, guarda_equipo

"""
    -----------------------------------------------------------------
    Este script equivale a la fabricación y almacenamiento en una caja 
    del juego de rotores y deflector que se entregaba tanto al emisor 
    como al receptor junto con la máquina ENIGMA.
    -----------------------------------------------------------------

    Sobre el alfabeto en el teclado:
    ---------------------------------
    
          La máquina enigma no tenia símbolos ni números en el teclado.
    Sin embargo no hay restricciones para ampliarlos.
    Se ha colocado sólo el espacio en blanco.
    
    Sobre los rotores y reflector:
    ---------------------------------
    
          Cada rotor es un disco con la misma cantidad de cotactos, en este
    caso 26, uno por cada letra del alfabeto. Intrnamente los contantos
    de la cara delantera se conectan con la rasera en forma aleatoria
    pero se hacen copias identicas para la ENIGMA dde origen y para el
    destino.
    Lo mismo ocurre con el reflector, con la diferencia de que sólo tiene
    contactos en una sola cara y el cableado en entre esos contactos.
    El reflector ya viene instalado en la máquina.
    
    Sobre el panel de conexiones:
    ---------------------------------
          Está colocado en la parte frontal de la máquina, Hay tantoas 
    contactos como letras del alfabeto. y se usa un cable o puente que 
    conecta una letra con otra de tal manera que si se cablea la letra 
    'C' y la letra 'K'  al pulsar la letra 'C' apraece codificado con 
    'K'. Es el equivalente a un rotor, pero con el cableado interno 
    configurable manualmente, no aleatoriamente.
     
    =======================
        OJO, IMPORTANTE:
    =======================
    
    Cada vez que se ejecuta este script, cambia la configuración del 
    cabeado de todos los rotores y del reflector, porque el cableado
    se escoje en forma aleatoria. Se debe ejecutar una sóla vez y enviar 
    copia a los operadores de origen y destino.
    
-----------------------------------------------------------------
"""
#------------------------------------------------------------------
#   Alfabeto del teclado en la máquina

alfabeto = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
    'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y',
    'Z', ' ']

#------------------------------------------------------------------
#   Reglas para recuperar la cabecera del mensaje encriptado
#   la configuración de la máquina

reglas = {
    'loc_rotores':      (0, 3),  # (posiciòn, cantidad)
    'loc_selectores':   (3, 3),  # (posiciòn, cantidad)
    'loc_numero':       (6, 1),  # (posiciòn, cantidad)
    'loc_cables':       (7, 0),  # La cantidad se debe calcular# en base a lo anterior
    'loc_codigo':       None,  # Se debe calcular en nbase los dos anterioores
}

if __name__ == '__main__':

    """
    -------------------------------------------------------------------
       Configuración de una  máquina ENIGMA civil o Militar
    ---------------------------------------------------------------------
    En el caso civil la configuración serìa:
        La señal electrica de una tecla pulsada viaja por la secuencia de
        rotores hasta el reflector y retorna por los mismos rotores en secuencia
        invertida hasta el bombillo que identigica la latra codificada.
        Configuración:
            - tres rotores intercambiables.
            - un reflector.
            - no tine panel de conexiones. 
           
    En el caso militar, dependiendo de la fuerza, sindo la mas compleja
        la de armada, tirne la posibilidad de escoger entre rotores, de los cuales 
        sólo tres se colocan en la màquna, y existe una codificaciòn adicional con 
        un panel dconexiones manual.
        La señal electrica de una tecla pulsada viaja por la secuencia de
        rotores hasta el reflector y retorna por los mismos rotores en secuencia
        invertida hasta el bombillo que identigica la latra codificada.
        tiene:
           - 0cho posibles rotores intercambiables.
           - un reflector.
           - tinee un panel de conexiones.
           
    NOTA:   1-  La configuración de los rotores son cables cruzados y son únicos. Evidentemente se 
            fabrican una sola vez. En la máquina se instalan esos rotores en cualquer orden y eso cambia
            la codificación de la máquina. Una forma de avisar al operador de destino como configurar su
            máquinaes es incluir en el mansaje codificado recibido tambien el orden y el tipo de rotores
            usados para la codificación tambien codificado siguendo unas reglas preacordada.
            2-  La configuración del reflector es básicamente la misma que la de un rotor a nivel
                de codificación. Fisicamente  los rotores son discos con una entrada en una cara 
                y una salida en la otra mientras que el reflector es un disco con una sola cara de 
                entrada/salida.
            En el programa:
            3-  El nombre del rotor es obligatorio al crear la instancia: se usa como identificador
                de instancia y como nombre de archivo.
            4-  Por defecto la instancia de clase no crea una configuración de rotor, sino que lee una
                previamente creada, por lo que hay que indicarle explicitamente  con 
                un valor de parámetro <configura=true> la primer vez o cuando se desee
                cambiar. Si no se indica que se cree, el rotor no tenfra codificaciòn (la salida del
                rotor sera la misma que la de entrada.
            5-  Oara crear la instancia de del reflector se usa la misma clase del rotor.
                 
------------------------------------------------------------------
    """

    rot1 = ROTOR( alfabeto, 'rotor 1', configura= True )
    rot2 = ROTOR( alfabeto, 'rotor 2', configura= True )
    rot3 = ROTOR( alfabeto, 'rotor 3', configura= True )
    rot4 = ROTOR( alfabeto, 'rotor 4', configura= True )
    rot5 = ROTOR( alfabeto, 'rotor 5', configura= True )
    rot6 = ROTOR( alfabeto, 'rotor 6', configura= True )
    rot7 = ROTOR( alfabeto, 'rotor 7', configura= True )
    rot8 = ROTOR( alfabeto, 'rotor 8', configura= True )

    reflector = REFLECTOR( alfabeto, 'reflector', configura= True )

    cambios_panel = []
    panel = PANEL(alfabeto, cambios_panel, 'panel', configura= True)

    configuracion_inicial_enigma = {
        'alfabeto':     alfabeto,               # Alfabeto del teclado de la máquina
        'caja_rotores': [rot1, rot2, rot3, rot4, rot5, rot6, rot7, rot8],
        'rotores':      [rot1, rot2, rot3],     # Tres rotores es la caatidad estandar.
        'reflector':    reflector,
        'panel':        panel
    }

    # Guardar la lista de objetos en un archivo

    nota =  'NOTA:\n\t\tCopias de este equipo debe ser ditribuidas al comando emisor de la orden o mensaje a codificar ' \
                 '\n\t\ty a los receptores de órdenes codificadas. '

    nombre_archivo = 'configuracion_de_fabrica.pkl'
    guarda_equipo(configuracion_inicial_enigma, nombre_archivo)
    print(f'\tLa estructura del equipo para la máquina ENIGMA ha sido configurada de fábrica y los datos guardados en el archivo <{nombre_archivo}>.\n\t{nota}')
