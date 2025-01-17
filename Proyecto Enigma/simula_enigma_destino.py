# -*- coding: utf-8 -*-

"""
Created on Thu Jan  2 12:13:30 2025

@author: Jesús Sardá
"""

import pickle
from libreria_clases import ROTOR, PANEL, ENIGMA, lee_equipo

# -----------------------------------------------------------------
#   M A I N
# -----------------------------------------------------------------


if __name__ == '__main__':

    """
     ------------------------------------------------------------------
     Se simula la configuración de una máquina ENIGMA desde el punto de 
     vista un operador que va a decodificar un codigo recibido.
     El operador configura ionicialmente la máquina segun parámetros 
     acordados con el operador en el origen.
     ------------------------------------------------------------------
     """

    # ---------------------------------------------------------------------
    #       Configuración bàsica de de la máquina
    # ---------------------------------------------------------------------

    print('-'*80)
    print(f'\n\tEtapa 1: Se prepara la máquina con todo su equipamiento\n')

    configuracion_inicial_enigma = lee_equipo('configuracion_de_fabrica.pkl')

    # Crea la máquina y el mensaje que quiere

    enigma = ENIGMA(configuracion_inicial_enigma)

    # -----------------------------------------------------------------------
    #   se lee la informacion de la configuración incial de la máquina
    #   NOTA:
    #       Esto se hace cada vez para decodificar los parametros de configuración

    print('-'*80)
    descripcion = '\n\tEtapa 2: Uso regular de encriptasdo de mensajes.' \
                  '\n\tSe usa la configuración inical de la máquina para' \
                  '\n\tdesencriptar la cabecera del código que se ha de recibir ' \
                  '\n\tdesde el originador del mensaje.\n'
    print(f'{descripcion}')

    config_inicial = enigma.lee_datos_origen('configuracion_inicial_acordada.json')

    rotores =       config_inicial['rotores']
    selectores =    config_inicial['selectores']
    cables  =       config_inicial['cableado']

    print(f'Rotores iniciales escogidos=  {rotores}')
    print(f'Selección inicial de rotores= {selectores}')
    print(f'Cableado inicial del panel=   {cables}')

    # -----------------------------------------------------------------------
    # se reconfigura la máquina para desencriptar los datos de configuración
    # inicial que se encuentra en la cabecera del mensaje

    print('-'*80)
    descripcion = '\n\tEtapa 3: Se cambian los parámetros de la máquina.\n'
    print(f'{descripcion}')

    enigma.cambia_rotores(rotores)
    enigma.gira_rotores(selectores)
    enigma.cablea_panel(cables)

    #-----------------------------------------------------------------------
    # Recibe el mensaje encriptado

    print('-'*80)
    descripcion = '\n\tEtapa 4: Se recibe el mensaje encriptado\n'
    print(f'{descripcion}')

    codigo_recibido= enigma.lee_datos_origen('codigo_enviado.json')
    print(f'mensaje recibido: {codigo_recibido}')

    #-----------------------------------------------------------------------
    #   Reglas para obtener los datos de configuración encriptados a
    #   partir de del mensaje recibido, que contendrá:
    #       - escogencia de los rotores
    #       - posicion, giro o seleccion de los rotores
    #       - cantidad e conexiones en el panel.
    #       - pares de caracteres que forman el cableado.
    #
    #   El formato de las reglas son duplas definif¡das así:
    #       (<posicion en mensaje>, <cantidad de datos>)

    reglas = {
        'loc_rotores':    (0, 3),   # (posiciòn, cantidad)
        'loc_selectores': (3, 3),   # (posiciòn, cantidad)
        'loc_numero':     (6, 1),   # (posiciòn, cantidad)
        'loc_cables':     (7, 0),   # La cantidad se debe calcular# en base a lo anterior
        'loc_codigo':      None,    # Se debe calcular en nbase los dos anterioores
    }


    # -----------------------------------------------------------------------
    # Se separa la cabecera del

    print('-'*80)
    descripcion = '\n\tEtapa 5: Se recupera la configuracion de la máquina ' \
                  '\n\ta partir del encabezado y tambien el mensaje codificado .\n'
    print(f'{descripcion}')

    config_codigo, msg_codificado =   enigma.recupera_configuracion(codigo_recibido, reglas)

    rotores =       config_codigo['rotores']
    selectores =    config_codigo['selectores']
    cables  =       config_codigo['cableado']

    print(f'Rotores obtenidos=   {rotores}')
    print(f'Selección obtenidos= {selectores}')
    print(f'Cableado obtenidos=  {cables}')

    # codigo = config_codigo['codigo']

    print(f'Código recibido:      {msg_codificado}')

    # enigma.reinicia_rotores()

    print('-'*80)
    descripcion = '\n\tEtapa 6: Se reconfigura la máquina para desencriptar el mensaje' \
                  '\n\ty se desencripta el mensaje.\n'
    print(f'{descripcion}')

    enigma.cambia_rotores(rotores)
    enigma.gira_rotores(selectores)
    enigma.cablea_panel(cables)

    # =======================================================================
    # Deodificación de codigo recibido

    mensaje = enigma.desencripta_codigo(msg_codificado)
    print(f'Mensaje:   {mensaje}')

