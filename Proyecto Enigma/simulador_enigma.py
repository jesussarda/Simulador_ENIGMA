# -*- coding: utf-8 -*-

"""
Created on Thu Jan  2 12:13:30 2025

@author: Jesús Sardá
"""

import pickle
from libreria_clases import ROTOR, PANEL, ENIGMA, lee_equipo
from crea_enigma import reglas

#-----------------------------------------------------------------
#   M A I N
#-----------------------------------------------------------------
    
    
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
               - tiene un panel de conexiones.

        NOTA:   1-  La configuración de los rotores son cables cruzados y son únicos. Evidentemente se 
                    fabrican una sola vez. En la máquina se instalan esos rotores en cualquer orden y eso cambia
                    la codificación de la máquina. 
                2-  Los rotores se puede girar y cambiar así le configuración de las conexiones u por tanto
                    la codificación. De manera que intercambiando los rotores y girando los rotores cambia por
                    completo la codificación de una letra o un mensaje. los rotores están conectados en secuencia
                    de tal manera que si el primer rotor sobrepasa el giro máximo, el sigiente rotor tambien gira
                    en un incremento. Esta configuración es lo que define la clave del código, que tanto el emisor
                    del mensaje como el receptor deben acordar. Una forma de avisar al operador de destino como
                    configurar su máquina es incluir en el mansaje codificado recibido tambien el orden y el tipo
                    de rotores usados para la codificación tambien codificado siguendo unas reglas preacordada.
                3-  La configuración del reflector es básicamente la misma que la de un rotor a nivel
                    de codificación. Fisicamente  los rotores son discos con una entrada en una cara 
                    y una salida en la otra mientras que el reflector es un disco con una sola cara de 
                    entrada/salida. Por tanto el circuito producido por una tecla recorre tantos rotores como
                    haya previo al reflector y retorna en le reflector recorriendo nuevamnete los rotores 
                    a la inversa.
                4-  Una complejidad adicional en la codificación es la del panel de conexiones en las máquians militares
                    que intercambia el orden la las letras manualmente usando puentes electricos entre una letra y otra.
                    Esta configuración debe ser también pre acordada.     
                    
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

    # ---------------------------------------------------------------------
    #       Configuración de la máquina
    # ---------------------------------------------------------------------

    nombre_archivo = 'configuracion_de_fabrica.pkl'
    equipo_enigma = lee_equipo(nombre_archivo)


    enigma = ENIGMA(equipo_enigma)

    mensaje = 'esta es una prueba para el encriptado de la maquina enigma sin usar el panel de conexiones'
    print(f'\tMensaje:    {mensaje}')

    print('\nEtapa 1: Encriptado-Desencriptado Normal')

    # =======================================================================
    # Codificación de mensaje a enviar

    codigo = enigma.encripta_texto(mensaje)
    print(f'\tCòdigo:     {codigo}')

    # =======================================================================
    # Decodificación de mensaje codificado recibido

    recuperado = enigma.desencripta_codigo(codigo)
    print(f'\tRecuperado: {recuperado}\n')

    # enigma.reinicia_rotores()

    # codigo = enigma.encripta_texto(mensaje)
    # print(f'\treinicio:   {codigo}')

    selectores = [4,2,1]
    print(f'paso 2: giro de selectores {selectores}')
    enigma.gira_rotores(selectores)

    codigo = enigma.encripta_texto(mensaje)
    print(f'\tCambio:     {codigo}')

    recuperado = enigma.desencripta_codigo(codigo)
    print(f'\tRecuperado: {recuperado}\n')

    rotores = [3, 6, 2]
    selectores_1 = [40,20,10]
    print(f'\nSelección de giro de rotores {selectores_1}')
    selectores = enigma.analiza_selectores(selectores_1)
    print(f'Mas de un giro en los  rotores se convierten en {selectores}')

    print(f'\npaso 3: cambio de rotores {rotores} y selectores{selectores}')
    enigma.cambia_rotores(rotores)
    enigma.gira_rotores(selectores)

    codigo = enigma.encripta_texto(mensaje)
    print(f'\tCambio sel: {codigo}')

    recuperado = enigma.desencripta_codigo(codigo)
    print(f'\tRecuperado: {recuperado}')

    print(f'\npaso 4: encripta configuración para la cabecera del mensaje')

    config_inicial = {}
    config_inicial['rotores'] = rotores
    config_inicial['selectores'] = selectores
    config_inicial['cableado'] = [('F','J')]
    # config_inicial['cableado'] = []

    norm_codigos = ''
    # lista_codigos, norm_codigos = enigma.encripta_configuracion(config_inicial)
    lista_codigos = enigma.encripta_configuracion(config_inicial)
    # print(f'{norm_codigos}')
    # print(f'{lista_codigos}')
    cabecera = ''.join(lista_codigos)
    print(f'\n\tcabecera:         {cabecera}')

    codigo_enviado = cabecera + codigo
    print(f'\n\tMensaje completo: {codigo_enviado}')

    print(f'\npaso 5: Desencripta configuración a partir de la cabecera del mensaje')
    config_codigo, msg_codificado =   enigma.recupera_configuracion(codigo_enviado, reglas)
    print(f'\n\tConfiguración: {config_codigo}')
    print(f'\tmensaje:       {msg_codificado}')

    recuperado = enigma.desencripta_codigo(msg_codificado)
    print(f'\tRecuperado:    {recuperado}')
