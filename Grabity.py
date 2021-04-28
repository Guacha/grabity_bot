import Bot
import Space
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def inicio(actu, contexto):
    """Función handler para el comando /start"""
    user = actu.message.from_user
    print(f"[{user['id']}]: Un usuario nuevo inició el bot")
    print(f"[{user['id']}]: Nombre de usuario nuevo: {user['username']}")
    contexto.bot.send_message(chat_id=actu.effective_chat.id, text="Bienvenido al bot Grabity, El bot para ver "
                                                                   "constelaciones en tu espacio!")


def desconocido(actu, contexto):
    """Función Handler para un comando desconocido"""
    user = actu.message.from_user
    print(f"[{user['id']}]: El usuario digitó un comando inválido")
    contexto.bot.send_message(chat_id=actu.effective_chat.id, text='No reconocí ese comando, intenta nuevamente o '
                                                                   'revisa que el comando esté escrito '
                                                                   'correctamente.')


def menu_constelaciones(actu, contexto):
    """Función que arroja opciones para visualizar cosas sobre las constelaciones"""
    
    user = actu.message.from_user
    print(f"[{user['id']}]: El usuario pidió ver la lista de constelaciones")
    
    # Definir los botones de opción
    teclado = [[InlineKeyboardButton("Ver constelación", callback_data='const'),
                InlineKeyboardButton("Ver Espacio", callback_data='espacio')],
               [InlineKeyboardButton("Ver todas las constelaciones", callback_data='todo')]]

    # Generar el menú con los botones definidos de arriba
    menu = InlineKeyboardMarkup(teclado)
    actu.message.reply_text('Elige lo que quieras ver: ', reply_markup=menu)


def opciones(actu, contexto):
    """Función Handler para los botones Inline de Telegram"""
    
    user = actu.message.from_user
    print(f"[{user['id']}]: El usuario presionó un botón")
    print(f"[{user['id']}]: {actu.callback_query}")
    
    # El Callback Query es el objeto que contiene la información de la respuesta que el usuario
    # envía al presionar un botón
    info = actu.callback_query
    global constelacion_actual, espacio

    # Verificar si la cadena respuesta empieza por un símbolo específico para saber en que parte del menú va
    # El # representa las respuestas que vienen del menú para elegir constelación
    if info.data[0] == '#':
        constelacion_actual = info.data

        # Definimos un teclado especial con los botones para el menú
        teclado = [[InlineKeyboardButton("Sólo constelación", callback_data='$solo_constelacion'),
                    InlineKeyboardButton("Ver todo", callback_data='$ver_todo')]]

        # Lo convertimos en un objeto que telegram pueda recibir
        # El metodo InlineKeyboardMarkup recibe un arreglo 2D donde el arreglo exterior
        # define las filas de botones, y los arreglos internos definen las columnas de botones
        menu = InlineKeyboardMarkup(teclado)

        info.edit_message_text('Cómo deseas ver a {}: '.format(constelacion_actual),
                               reply_markup=menu)

    # El $ representa las repsuestas para elegir si ver solo la constelación
    # o la constelación con todas las estrellas
    elif info.data[0] == '$':
        # Obtener el nombre sin el símbolo
        c = Space.Constelacion(constelacion_actual[1:], espacio)
        c.get_constelacion()

        if info.data[1:] == 'solo_constelacion':
            file = c.graficar_constelacion(False)
        else:
            file = c.graficar_constelacion(True)

        contexto.bot.send_message(chat_id=actu.effective_chat.id, text=c.get_info_constelacion())
        contexto.bot.send_photo(chat_id=actu.effective_chat.id, photo=open(file[2:], 'rb'), caption='Aquí tienes la '
                                                                                                    'constelación '
                                                                                                    '{}'.format(
            constelacion_actual))

    # El & representa respuestas del menú para ver tdo el espacio
    elif info.data[0] == '&':
        if info.data[1:] == 'solo_constelacion':
            info.edit_message_text(text='Aquí tienes todas las constelaciones observables que tengo registradas:')
            file = espacio.graficar_masivo(False, True)
            num = espacio.get_num_constelaciones()
            contexto.bot.send_photo(
                chat_id=actu.effective_chat.id, photo=open(file[2:], 'rb'),
                caption='Actualmente tengo {} constelaciones observables en mi base de datos!'.format(num)
            )

        elif info.data[1:] == 'todas':
            info.edit_message_text(text='Aquí tienes todas las estrellas y constelaciones observables que tengo registradas:')
            file = espacio.graficar_masivo(True, True)
            num_e = espacio.get_num_estrellas()
            num_c = espacio.get_num_constelaciones()
            contexto.bot.send_photo(
                chat_id=actu.effective_chat.id, photo=open(file[2:], 'rb'),
                caption='Actualmente tengo {} estrellas y {} constelaciones observables '
                        'en mi base de datos!'.format(num_e, num_c)
            )

    # Si la respuesta no tiene símbolo, proviene del menú principal
    else:
        if info.data == 'const':
            lista_const = []
            for s in espacio.listaConstelaciones:
                lista_const.append([InlineKeyboardButton(s.nom, callback_data='#' + s.nom)])

            markup = InlineKeyboardMarkup(lista_const)
            info.edit_message_text(
                text="Muy bien, ahora elige la constelación que desees ver de las constelaciones que "
                     "tengo disponibles", reply_markup=markup)
        elif info.data == 'espacio':
            info.edit_message_text(text='Aquí tienes todas las estrellas observables que tengo registradas:')
            file = espacio.graficar_masivo(True, False)
            num = espacio.get_num_estrellas()
            contexto.bot.send_photo(
                chat_id=actu.effective_chat.id, photo=open(file[2:], 'rb'),
                caption='Actualmente tengo {} estrellas observables en mi base de datos!'.format(num)
            )
        elif info.data == 'todo':
            teclado = [[InlineKeyboardButton('Solo Estrellas de constelación', callback_data='&solo_constelacion')],
                       [InlineKeyboardButton('Ver todas las estrellas', callback_data='&todas')]]
            markup = InlineKeyboardMarkup(teclado)
            info.edit_message_text(
                text="Deseas ver solo las estrellas que hagan parte de constelaciones o todas las estrellas del espacio"
                     " observable?",
                reply_markup=markup)


def mensaje_ayuda(actu, cont):
    """Handler de comando para el comando de ayuda /help"""
    
    user = actu.message.from_user
    print(f"[{user['id']}]: El usuario pidió ver la ayuda")
    
    cont.bot.send_message(chat_id=actu.effective_chat.id,
                          text='Bienvenido a Grabity! Tengo un único comando principal, '
                               'que es el comando /visualizar, úsalo para ver todas '
                               'las opciones')


# Bloque principal de código

# Token identificador para la API de Telegram, el token aquí mostrado es token único para Grabity
# Soy consciente de que dejar esto abierto es un riesgo de seguridad, pero honestamente no podría importarme menos
bot_token = "1230627739:AAF4UmYLIKPm_YMv9WivIs55LbEMnpRvxAs"

# Creamos un objeto espacio, sobre el que el bot va a trabajar
espacio = Space.Espacio()
global constelacion_actual
# Creamos un objeto bot, que va a tener los handlers y el dispatcher
# No uso herencia porque... no
grabity = Bot.Bot(bot_token)
grabity.add_handler(CommandHandler('start', inicio))
grabity.add_handler(CommandHandler('visualizar', menu_constelaciones))
grabity.add_handler(CommandHandler('help', mensaje_ayuda))
grabity.add_handler(MessageHandler(Filters.command, desconocido))
grabity.add_handler(CallbackQueryHandler(opciones))

grabity.start(CommandHandler('start', inicio))
