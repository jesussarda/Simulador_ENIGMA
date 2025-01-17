# -*- coding: utf-8 -*-

"""
Created on Thu Jan  2 12:13:30 2025

@author: Jesús Sardá
"""

import pickle
from libreria_clases import ROTOR, PANEL, ENIGMA, lee_equipo,  crea_lista_aleatorios

# -----------------------------------------------------------------
#   M A I N
# -----------------------------------------------------------------


if __name__ == '__main__':

    """
    ------------------------------------------------------------------
    Se simula la configuración de una máquina ENIGMA desde el punto de 
    vista de un operador que va a codificar un mensaje para ser 
    trasmitido.
    El operador configura la máquina según parámetros acordados con el 
    operador  receptor, codifica la información de configuración a usar
    para encriptar el mensaje, codigica el mensaje y lo adjunta a la 
    información anterior y envía el nuevo mensaje.  los parámetros 
    encriptados de configuración siguen un formato pre acordado:
    
    ------------------------------------------------------------------

    por ejemplo:
    1-  Como los rotores y selectores están numerados, se pueden convertir
        a sus equivalentes alfabéticos y luego encriptar.
    2-  la configuración del cableado del panel son caracteres alfabéticos
        basta con agruparlos en un formato definido y también encriptarlo.
    3-  El datos encriptados se pueden unir al encriptado del mensaje en
        un orden pre definido, por ejemplo en la cabecera del nuevo mensaje
        (por simplificación del ejemplo) siguiendo algunas reglas.
        Por ejemplo:
        
        1- Los tres primeros caracteres del nuevo mensaje corresponden a 
            la numeración de los rotores.
        2- Los tres caracteres siguientes al giro o seleccón de esos rotores.
        3- El siguiente caracter corresponde al número de cables o puentes 
            usados en el panel.
        4- Los sigientes pares de caracteres son las tuplas de cableado, tantas
            pares como indique el número anterior.
        5- A partir de aqui comienza el mensaje.
        
        Estas reglas pueden definirse de muchas maneras o en forma dinámica para
        evitar ser detectadas por un observador que quera romper el envcriptado.
        
    ------------------------------------------------------------------
    """

    # Se hace una sola vez: a partir aquí comienza un periodo estratégico.
    # Durante ese período se usa siempre la misma configuración,
    # NOTA:
    #   Podria usarse la configuración por defecto de fábrica de la máquina
    #   pero no es estratégicamente conveniente.


    # --------------------------------------------------------------------
    #       Mensaje que se quiere enviar a destino
    # --------------------------------------------------------------------

    mensaje = 'esta es una prueba para el encriptado de la maquina enigma sin usar el panel de conexiones'
    print(f'\tMensaje:    {mensaje}')

    # ---------------------------------------------------------------------
    #       Configuración inicial de de la máquina
    # ---------------------------------------------------------------------

    print(f'\n\tEtapa 1: se obtiene la máquina con todo su equipamiento ')

    configuracion_inicial_enigma = lee_equipo('configuracion_de_fabrica.pkl')

    # Crea la máquina y el mensaje que quiere

    enigma = ENIGMA(configuracion_inicial_enigma)

    cant_rotores =  enigma.cant_rot  # los rotoers que permite malojar la máquina
    cant_opciones = enigma.cant_caj  # de los rotores en la caja, se escogen los que caben en la máqioan
    cant_teclas =   enigma.cant_car  # de los rotores instalados, se selecona la posición

    inicia_periodo_operativo = True

    if inicia_periodo_operativo:

        # =======================================================================
        # configuraion de la maquina según parametros predefinidos y compartidos.

        descripcion = '\n\tEtapa 2: Configurción preacordada.' \
                      '\n\tSe escoge la configuración inical de la máquina.' \
                      '\n\tEsta configuración se envía a los destinatasrios del mensaje' \
                      '\n\tpara que puedan desencriptar la cabecera del mensaje.' \
                      '\n\tSe hace una sola vez durante un periodo de operación predefinido' \
                      '\n\ty luego se cambia por seguridad.\n'
        print(f'{descripcion}')

        rotores =       crea_lista_aleatorios(cant_opciones, cant_rotores)
        print(f'Rotores iniciales escogidos=  {rotores}')

        selectores =    crea_lista_aleatorios(cant_teclas, cant_rotores)
        print(f'Selección inicial de rotores= {selectores}')

        cables =        [('K','Z'), ('F','H'), ('N','C'), ('L', 'E')]  # se scoje cel cableado en el panel
        print(f'Cableado inicial del panel=   {cables}')

        config_inicial = {
            'rotores':      rotores,      # en este caso la numeracion de be comenzar en 1 y no puede ser mayor  que 26
            'selectores':   selectores,
            'cableado':     cables,
         }

        # -----------------------------------------------------------------------
        #   se envia a los destinoatarios (operadores) la informacion de la
        #   configuración incial de la máquina.
        #   NOTA:
        #       Esto se hace una vez en un período de operación largo, a juicio
        #       del comando.

        enigma.guarda_datos_para_destino(config_inicial, 'configuracion_inicial_acordada.json')

    else:
        # -----------------------------------------------------------------------
        #   se lee la informacion de la  configuración incial de la máquina
        #   NOTA:
        #       Esto se hace cada vez durqante un período de operación largo

        descripcion = '\n\tEtapa 2: Uso regular de encriptasdo de mensajes.' \
                      '\n\tSe usa la configuración inical de la máquina para' \
                      '\n\tencripastr la cabecera del código que se ha de enviar ' \
                      '\n\ta los destinatasrios del mensaje.\n'
        print(f'{descripcion}')

        config_inicial = enigma.lee_datos_origen('configuracion_inicial_acordada.json')

        rotores =       config_inicial['rotores']
        selectores =    config_inicial['selectores']
        cables  =       config_inicial['cableado']
        cant_cables =   len(cables)

        print(f'Rotores iniciales escogidos=  {rotores}')
        print(f'Selección inicial de rotores= {selectores}')
        print(f'Cableado inicial del panel=   {cables}')

    # -----------------------------------------------------------------------
    # se reconfigura la máquina para encriptar los datos de configuración
    # inicial que se añadirá al mensaje como la cabecera.

    descripcion = '\n\tEtapa 3: Se cambian los parámetros de la máquina para ' \
                  '\n\tencriptar la cabecera\n'
    print(f'{descripcion}')

    enigma.cambia_rotores(rotores)
    enigma.gira_rotores(selectores)
    enigma.cablea_panel(cables)

    # =======================================================================
    # Codificación de pàrámetros

    lista_codigos = enigma.encripta_configuracion(config_inicial)
    codigo = ''.join(lista_codigos)
    print(f'Configuración cabecera:     {codigo}')

    # =======================================================================
    # A partir de este momento se reconfoigura la máquina cada vez que se se
    # desee enviar un mensje o durante un periodo corto, como a lo largo del
    # día.
    # Codificación de mensaje a enviar

    descripcion = '\n\tEtapa 4: Se escogen los parámetros de la máquina para' \
                  '\n\tencriptar el mensaje, pero no se cambia la máquian aún.\n'
    print(f'{descripcion}')

    rotores = crea_lista_aleatorios(cant_opciones, cant_rotores)
    print(f'Rotores iniciales escogidos=  {rotores}')

    selectores = crea_lista_aleatorios(cant_teclas, cant_rotores)
    print(f'Selección inicial de rotores= {selectores}')

    cables = [('A','D'), ('F','H'), ('N','C'), ('L', 'E')]  # se scoje cel cableado en el panel
    print(f'Cableado inicial del panel=   {cables}')

    config_mensaje = {
        'rotores':      rotores,      # en este caso la numeracion de be comenzar en 1 y no puede ser mayor  que 26
        'selectores':   selectores,
        'cableado':     cables,
     }

    # Se encripta la nueva configuración escogida paraa cabeera usanso la configuración acordada

    descripcion = '\n\tEtapa 5: Se encripta la nueva configuración escogida para encripar el mensaje' \
                  '\n\tpara la cabecera usando al configuración de la máquina preacordada'
    print(f'{descripcion}')

    lista_codigos = enigma.encripta_configuracion(config_mensaje)
    codigo = ''.join(lista_codigos)
    print(f'Configuración cabecera:     {codigo}')

    # enigma.guarda_datos_para_destino(config_mensaje, 'configuracion_del_mensaje')

    descripcion = '\n\tEtapa 6: Se reconfigura la maquina con la configuración escogida para encripar el mensaje'
    print(f'{descripcion}')

    enigma.cambia_rotores(rotores)
    enigma.gira_rotores(selectores)
    enigma.cablea_panel(cables)

    descripcion = '\n\tEtapa 7: Se encripta el mensaje con los nuevos parámetros.\n'
    print(f'{descripcion}')

    codigo = enigma.encripta_texto(mensaje)
    print(f'encriptadpo del mensaje:     {codigo}')

    # =======================================================================
    # se añade el código del mensaje a la cabecera encriptada (opción simple, se
    # puede seguir un formato distinto mas complejo)

    lista_codigos.append(codigo)

    # =======================================================================
    # Envia el codigo junto con la configuración (almacena en disco)

    descripcion = '\n\tEtapa 8: Se añade la cabecera encriptada al mensaje encriptado.\n'
    print(f'{descripcion}')

    mensaje_encriptado = ''.join(lista_codigos)
    print(f'Encriptado completo: {mensaje_encriptado}')

    descripcion = '\n\tEtapa 9: Se envia el mensaje comppleto a los destinatarios por el' \
                  '\n\tmedio escogido: radio, cable, correo, etc.'
    print(f'{descripcion}')

    # Se envía  el mensaje codificado y ensamblado al estino usndo cualquier medio: radio, cable, correo, etc.
    # Aquí  se simula guardándolo en disco.

    enigma.guarda_datos_para_destino(mensaje_encriptado, 'codigo_enviado.json')
