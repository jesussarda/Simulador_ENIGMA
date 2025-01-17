# **Simulación de una máquina ENIGMA civil o Militar**

##**Características de la máquina ENIGMA:**

###En el caso civil la configuración seria:
- Tres rotores intercambiables. los rotores son discos con contactos eléctricos en ambas caras conectados por cables internamente.
- Un reflector. también es un disco, pero con contactos eléctricos en una sola cara. Internamente los contactos van conectados por cables puenteados.
- no tiene panel de conexiones. 

La señal eléctrica debido a una tecla pulsada viaja por la secuencia de rotores hasta el reflector y retorna por los mismos rotores en secuencia invertida hasta el bombillo que identifica la letra codificada.
        
           
###En el caso militar tiene:

- Una colección de Hasta ocho posibles rotores intercambiables.
- un reflector.
- tiene un panel de conexiones. 

Dependiendo del componente militar hay distintos modelos y complejidades, siendo la maáquina más compleja la de lus submarinos de la armada, tiene la posibilidad de escoger entre varios rotores, de los cuales solo tres o cuatro se colocan en la máquina, y existe una codificación adicional con  un panel de conexiones manual.  La señal eléctrica de una tecla pulsada viaja por la secuencia de rotores hasta el reflector y retorna por los mismos rotores en secuencia invertida hasta el bombillo que identifica la letra codificada.
        
tiene:
           
NOTAS:
1- La configuración interna de los rotores son cables cruzados y los conexionados son únicos. Se hacen copias idénticas de estos rotores para que tanto el emisor como los receptores tengan la misma máquina. En el equipamiento de enigma viene una caja con más de tres rotores, hasta ocho en el caso de los submarinos de la armada. En la máquina hay alojamiento para tres rotores (cuatro en los últimos modelos para submarinos) y se instalan esos rotores en cualquier orden. Eso cambia el encriptado de la máquina. Los rotores pueden girar para cambiar y aumentar la complejidad del encriptado hasta 26 posiciones (según las letras del teclado), pero pueden girar más de una vez. En este caso el rotor contiguo gira una posición.  Una forma de avisar al operador de destino como configurar su máquina para decodificar el mensaje recibido, es incluir en el mensaje codificado el orden y número de los rotores  así como la posición de giro y el cabledo del panel de conexiones usados para la codificación también encriptado siguiendo unas reglas pre acordadas.

2- La configuración del reflector es básicamente la misma que la de un rotor y al nivel de la codificación se puede interpretaar como un rotor. 

3- El panal e conexiones esta formado por un frente con clavijas, una por cada letra, y una colección de cables de interconexión. Al puentear una letra con otra se intercambia el orden, de tal manera que se puede interpretar como si fuera un rotor que se ha configurado manualmente. No necesariamente todos las letras deben estar puenteadas, puede haber un solo puente.


##Reglas para la simulación:

###secuencia de ejecución:

1- El script ***<crea_enigma.py>*** es la primera rutina que debe ser ejecutada. La razón es que en este script se crean todos elementos que forman la máquina: los rotores, reflector, panel, teclado...
Es el equivalente a fabricar la máquina ENIGMA con todos sus aditamentos. Se hace separado porque al crearse los rotores y el reflector se configura el conexionado interno aleatoriamente. Pero ocurre que la misma configuración deben ser copiadas tanto para el origen y el destino de los mensajes. Es una misma máquina para el emisor como para el receptor y el encriptado no funciona si el la configuración de los rotores y reflector cambia en ambas partes.

2- En el script ***<simula_enigama_origen.py>*** se reconfigura la máquina y se encripta el mensaje. Sin embargo hay una fase del proceso que debe ser acordada con el destino: la configuración de la máquina usada para el encriptado de la información de la configuración de la máquina, que puede cambiar por a cuerdo como regla en periodos acordadaos,  que es a su vez es usada al momento de enviar el mensaje, que puede cambiar diariamente. Esto significa que cuando el emisor envía un mensaje a destino este mensaje contiene internamente tanto la información de la configuración usada para encriptar la información del mensaje como la configuración usada, pero se usan configuraciones distintas de la máquina para una como para la otra.

3- El script ***<simula_enigama_destino.py>*** una vez obtenida la información acordada  de configuración de la máquina que debe ser usada para obtener la configuración de la máquina usada para desencriptar el mensaje que esta contenida en la información recibida.

3- El nombre del rotor es obligatorio al crear la instancia: se usa como identificador de instancia y como nombre de archivo.
4- Por defecto la instancia de clase no crea una configuración de rotores sino que lee una previamente creada, por lo que hay que indicarle explícitamente con un valor de parámetro <configura=true> la primer vez o cuando se desee
cambiar. Si no se indica que se cree, el rotor no tenfra codificaciòn (la salida del rotor sera la misma que la de entrada.

5- Para crear la instancia de del reflector básicamante se usa la misma clase del rotor.
