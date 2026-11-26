# -*- coding: utf-8 -*-
"""Shorts v4. Cada vídeo:
 text  : narración exacta (lo que dice la voz)
 hook  : 2 líneas de titular arriba durante el gancho  [(texto, estilo)]  estilo: red|yellow|white
 shots : (frase_ancla, imagen, movimiento)   movimiento: push|pull|left|right|up
         la primera toma de cada ancla cambia en la primera palabra de la frase
 kw    : (frase_ancla, texto, color[, extra])  texto grande que golpea arriba; extra: dict(list=True) acumula
 hits  : palabras (normalizadas) que provocan golpe de cámara
"""
FX = dict(vc_helicoptero_atardecer=(.33, .5), vc_noria_dia=(.72, .5), vc_skyline_noche=(.45, .5), gasolinera_neon=(.7, .5), pitbull_cadena=(.4, .5),
  marina_yates=(.6, .5), jason_manejando_copiloto=(.62, .45), jason_rifle_perro=(.38, .5), vc_torres_agua=(.38, .5), ambrosia_fiesta_lodo=(.5, .5),
  lucia_auto_neon=(.55, .45), lucia_gimnasio=(.48, .45), lucia_checks_cashing=(.48, .45), lucia_persecucion_tunel=(.45, .45), jason_capucha_rifle=(.45, .45),
  jason_pistola_balas_dinero=(.62, .45), jason_hidroavion=(.55, .5), jason_reja_policia=(.53, .45), jl_abrazo_pantano_policia=(.42, .45),
  jl_cubriendose_armas=(.68, .45), jl_convertible_costa=(.65, .45), azotea_coctel_noche=(.37, .45), jl_moto_policia_helicoptero=(.62, .45),
  jl_auto_llamas_bolsas=(.5, .45), jl_escalera_metal=(.45, .45), jl_auto_pistolas=(.6, .45), jl_gimnasio_pelea=(.5, .45), vc_letrero_avion=(.5, .5),
  port_gellhorn_atardecer=(.5, .5), port_gellhorn_motel=(.25, .5), mount_kalaga_canon=(.55, .5), grassrivers_skyline=(.55, .5), leonida_keys_aereo=(.55, .5))

V = {}

V["06"] = dict(slug="consolas_v4", tone="#22E3D6",
 text="¿Tienes PS4 o Xbox One? Solo una de las dos puede jugar GTA 6. El juego sale únicamente para PS5 y Xbox Series X y S. No hay versión de PS4. Pero en Xbox One sí se puede jugar… por la nube. Microsoft confirmó que funciona con Xbox Cloud Gaming desde el día uno, con los gráficos de una Series S. Eso sí: tienes que comprar el juego, necesitas acceso a la nube de Xbox y buen internet, y no está disponible en todos los países. La Series S sí lo corre de forma nativa. ¿Y Nintendo Switch 2? Nada anunciado.",
 hook=[], banner="¿Tu consola puede con *GTA 6*?", v5=True,
 montage=["clip:hands", "lucia_persecucion_tunel", "jl_convertible_costa"],
 music="synth",
 shots=[
  ("Solo una", "jason_manejando_copiloto", "push"),
  ("puede jugar", "clip:playing@1", "push"),
  ("El juego sale", "lucia_auto_neon", "push"),
  ("Xbox Series", "gasolinera_neon", "left"),
  ("No hay versión", "jason_reja_policia", "punch", dict(k="slam", text="SIN|PS4", bg="#FF2D45")),
  ("de PS4", "jason_reja_policia", "punch", dict(k="mono")),
  ("Pero en Xbox", "jl_moto_policia_helicoptero", "push", dict(k="split", img2="jason_reja_policia", a="XBOX ONE ✓", b="PS4 ✗")),
  ("por la nube", "vc_helicoptero_atardecer", "up", dict(k="anim", p="cloud", label="POR LA NUBE", sub="Xbox Cloud Gaming")),
  ("Microsoft confirmó", "azotea_coctel_noche", "push", dict(k="news", src="Según Microsoft", hl="GTA 6 llega a Xbox Cloud Gaming desde el día uno")),
  ("con los gráficos", "marina_yates", "left"),
  ("Eso sí", "jl_cubriendose_armas", "punch"),
  ("tienes que comprar", "clip:money@2", "push"),
  ("necesitas acceso", "jason_capucha_rifle", "push"),
  ("buen internet", "clip:server@3", "push", dict(k="anim", p="wifi", label="BUEN INTERNET")),
  ("no está disponible", "port_gellhorn_motel", "right"),
  ("La Series S", "jl_auto_llamas_bolsas", "push"),
  ("Nintendo Switch", "vc_noria_dia", "pull", dict(k="mono")),
  ("Nada anunciado", "jl_auto_pistolas", "punch", dict(k="slam", text="NADA|ANUNCIADO", bg="#0b0b0b")),
 ],
 kw=[
  ("únicamente", "SOLO PS5 Y SERIES X|S", "yellow"),
  ("comprar el juego", "✔ COMPRAR EL JUEGO", "white", dict(list="NECESITAS:")),
  ("acceso a la nube", "✔ XBOX CLOUD", "white", dict(list="NECESITAS:")),
  ("no está disponible", "⚠️ NO EN TODOS LOS PAÍSES", "white"),
  ("forma nativa", "SERIES S: NATIVO ✅", "green"),
 ],
 hits=["solo", "unicamente", "pero", "eso", "nativa"],
)

V["11"] = dict(slug="17_millones", tone="#FFE14D",
 text="GTA 6 vendió más que muchos juegos en toda su vida… y eso que todavía no salía en México. Diecisiete millones de copias antes del lanzamiento. Más de mil seiscientos millones de dólares, según Sensor Tower. En Metacritic tiene noventa y nueve. Y millones de personas lo vieron en vivo en Twitch. ¿Tú ya lo tienes, o todavía no?",
 hook=[("17 MILLONES 😳", "yellow"), ("ANTES DE SALIR", "red")],
 montage=["jason_pistola_balas_dinero", "jl_boveda_dinero" if False else "lucia_checks_cashing", "vc_skyline_noche"],
 shots=[("y eso que", "vc_letrero_avion", "push"), ("Diecisiete millones", "jl_auto_llamas_bolsas", "punch"), ("antes del lanzamiento", "marina_yates", "right"),
        ("Más de mil", "jason_pistola_balas_dinero", "punch"), ("según Sensor", "azotea_coctel_noche", "left"), ("En Metacritic", "lucia_auto_neon", "push"),
        ("noventa y nueve", "vc_helicoptero_atardecer", "punch"), ("Y millones", "ambrosia_fiesta_lodo", "right"), ("en vivo", "gasolinera_neon", "push"),
        ("¿Tú ya", "jl_convertible_costa", "pull"), ("o todavía no", "jason_pistola_balas_dinero", "push")],
 kw=[("Diecisiete millones", "17 MILLONES DE COPIAS", "yellow"), ("mil seiscientos", "💰 $1,650 MILLONES USD", "green"),
     ("noventa y nueve", "METACRITIC: 99", "yellow"), ("en vivo", "🔴 MILLONES EN VIVO", "red")],
 hits=["diecisiete", "mil", "noventa", "millones"],
)

V["12"] = dict(slug="huevo_de_pascua", tone="#3DFF6E",
 text="En GTA 6 hay un huevo de pascua… literal. Un jugador subió la torre de radio más alta del juego. La subida tarda como seis minutos. Y arriba, en un nido, había un huevo esperándolo. Rockstar siempre esconde cosas así, en los lugares más absurdos. ¿Tú hasta dónde subirías por un huevo?",
 hook=[("UN HUEVO DE PASCUA", "yellow"), ("LITERAL 🥚", "white")],
 montage=["vc_torres_agua", "mount_kalaga_canon", "vc_helicoptero_atardecer"],
 shots=[("Un jugador", "jl_escalera_metal", "up"), ("la torre", "vc_torres_agua", "up"), ("La subida", "jason_capucha_rifle", "push"),
        ("seis minutos", "grassrivers_skyline", "right"), ("Y arriba", "leonida_keys_aereo", "pull"), ("había un huevo", "vc_noria_dia", "punch"),
        ("Rockstar siempre", "port_gellhorn_atardecer", "left"), ("en los lugares", "ambrosia_fiesta_lodo", "push"), ("¿Tú hasta", "jason_hidroavion", "right"),
        ("por un huevo", "vc_torres_agua", "push")],
 kw=[("torre de radio", "📡 LA TORRE MÁS ALTA", "white"), ("seis minutos", "⏱️ 6 MINUTOS SUBIENDO", "yellow"),
     ("había un huevo", "🥚 UN HUEVO EN UN NIDO", "green"), ("lugares más absurdos", "ROCKSTAR SIENDO ROCKSTAR", "cyan")],
 hits=["literal", "huevo", "nido", "absurdos"],
)

V["13"] = dict(slug="casa_secreta", tone="#FFE14D",
 text="Rockstar nos enseñó GTA 6 en 2021… y nadie se dio cuenta. En GTA San Andreas Definitive Edition apareció una foto de una casa que no estaba en el juego original. Muchos sospechaban que era de GTA 6. Ahora, fans que están mapeando el juego dicen que encontraron esa misma casa en GTA 6, en Belville. Igualita, hasta las plantas y los árboles. Rockstar no lo ha confirmado. ¿Tú crees que fue a propósito?",
 hook=[("GTA 6 EN 2021", "yellow"), ("Y NADIE LO VIO 👀", "red")],
 montage=["port_gellhorn_motel", "vc_skyline_noche", "grassrivers_skyline"],
 shots=[("En GTA San", "vc_noria_dia", "push"), ("apareció una foto", "port_gellhorn_atardecer", "left"), ("que no estaba", "port_gellhorn_motel", "push"),
        ("Muchos sospechaban", "jason_reja_policia", "punch"), ("Ahora, fans", "leonida_keys_aereo", "pull"), ("dicen que encontraron", "grassrivers_skyline", "right"),
        ("en Belville", "vc_torres_agua", "push"), ("Igualita", "marina_yates", "punch"), ("Rockstar no", "jl_abrazo_pantano_policia", "left"),
        ("¿Tú crees", "lucia_auto_neon", "push"), ("a propósito", "port_gellhorn_motel", "push")],
 kw=[("San Andreas", "SAN ANDREAS DEFINITIVE · 2021", "white"), ("foto de una casa", "🏠 UNA CASA MISTERIOSA", "yellow"),
     ("misma casa", "LA MISMA CASA EN GTA 6", "green"), ("Belville", "📍 BELVILLE", "cyan"), ("Igualita", "IGUALITA 🤯", "yellow"),
     ("no lo ha confirmado", "SIN CONFIRMAR", "red")],
 hits=["nadie", "misma", "igualita", "confirmado"],
)

V["14"] = dict(slug="la_gente_enloquecio", tone="#FF2D45",
 text="La gente está haciendo cosas absurdas por GTA 6. En Estados Unidos, el ejército le dio cuatro días libres a soldados que se volvieron a enlistar, para que pudieran jugarlo. En España, un profesor movió un examen para la semana del lanzamiento. Y en una encuesta, ocho de cada diez dijeron que se van a desvelar jugando. ¿Tú faltarías a la escuela o al trabajo?",
 hook=[("LA GENTE", "yellow"), ("ENLOQUECIÓ 🤯", "red")],
 montage=["ambrosia_fiesta_lodo", "jl_gimnasio_pelea", "pitbull_cadena"],
 shots=[("En Estados Unidos", "jason_rifle_perro", "push"), ("el ejército", "jason_capucha_rifle", "punch"), ("a soldados", "jl_cubriendose_armas", "right"),
        ("para que pudieran", "jason_manejando_copiloto", "push"), ("En España", "lucia_checks_cashing", "left"), ("movió un examen", "lucia_gimnasio", "punch"),
        ("Y en una encuesta", "azotea_coctel_noche", "push"), ("ocho de cada", "vc_skyline_noche", "punch"), ("desvelar jugando", "gasolinera_neon", "right"),
        ("¿Tú faltarías", "jl_convertible_costa", "pull"), ("o al trabajo", "ambrosia_fiesta_lodo", "push")],
 kw=[("el ejército", "🪖 4 DÍAS LIBRES PARA JUGAR", "green"), ("un profesor", "📚 MOVIÓ UN EXAMEN", "yellow"),
     ("ocho de cada diez", "8 DE CADA 10 SE DESVELAN", "red"), ("¿Tú faltarías", "¿FALTARÍAS? 🤔", "white")],
 hits=["absurdas", "ejercito", "examen", "ocho"],
)

V["15"] = dict(slug="5_detalles_trailer", tone="#22E3D6",
 text="Cinco detalles del último tráiler de GTA 6 que casi nadie vio. Uno: hay un dragón de Komodo en el pantano… y esos ni siquiera viven en Florida. Dos: en un auto de dos puertas ya puede ir alguien atrás. En GTA 5 no se podía. Tres: los personajes sudan cuando hacen ejercicio. Cuatro: hay por lo menos tres modelos de motos de agua. Y cinco: un letrero marca la gasolina a cuatro veintinueve el galón. ¿Cuál viste tú?",
 hook=[("5 DETALLES", "yellow"), ("QUE NO VISTE 👀", "red")],
 montage=["jl_abrazo_pantano_policia", "jl_convertible_costa", "leonida_keys_aereo"],
 shots=[("Uno: hay", "jl_abrazo_pantano_policia", "push"), ("y esos ni", "grassrivers_skyline", "right"), ("Dos: en", "jl_convertible_costa", "punch"),
        ("En GTA 5", "jason_manejando_copiloto", "left"), ("Tres: los", "lucia_gimnasio", "punch"), ("cuando hacen", "jl_gimnasio_pelea", "push"),
        ("Cuatro: hay", "leonida_keys_aereo", "punch"), ("motos de agua", "marina_yates", "right"), ("Y cinco", "gasolinera_neon", "punch"),
        ("cuatro veintinueve", "port_gellhorn_motel", "push"), ("¿Cuál viste", "jl_abrazo_pantano_policia", "pull")],
 kw=[("Uno: hay", "1 · DRAGÓN DE KOMODO 🦎", "yellow"), ("Dos: en", "2 · PASAJERO ATRÁS 🚗", "yellow"), ("Tres: los", "3 · SUDAN 💦", "yellow"),
     ("Cuatro: hay", "4 · 3 MOTOS DE AGUA 🌊", "yellow"), ("Y cinco", "5 · GASOLINA $4.29 ⛽", "yellow")],
 hits=["uno", "dos", "tres", "cuatro", "cinco"],
)

V["16"] = dict(slug="guinos_gta_viejos", tone="#FF8A1F",
 text="GTA 6 está lleno de guiños a los GTA viejos. La playera de Jason dice North Fort Law, una base militar del primer GTA, de 1997. Los camiones de Globe Oil vienen de GTA 4. El banco Fleeca regresa de GTA 5. Y hay un arma que hace referencia a la mansión de Tommy Vercetti, de Vice City. ¿Qué personaje viejo te gustaría encontrar?",
 hook=[("GUIÑOS A", "yellow"), ("LOS GTA VIEJOS 👀", "red")],
 montage=["jason_rifle_perro", "vc_letrero_avion", "gasolinera_neon"],
 shots=[("La playera", "jason_capucha_rifle", "push"), ("una base militar", "jason_rifle_perro", "right"), ("Los camiones", "gasolinera_neon", "punch"),
        ("vienen de", "port_gellhorn_atardecer", "left"), ("El banco Fleeca", "lucia_checks_cashing", "punch"), ("Y hay un arma", "jason_pistola_balas_dinero", "push"),
        ("Tommy Vercetti", "vc_skyline_noche", "punch"), ("de Vice City", "vc_letrero_avion", "right"), ("¿Qué personaje", "jl_auto_pistolas", "pull"),
        ("te gustaría", "jason_rifle_perro", "push")],
 kw=[("North Fort Law", "NORTH FORT LAW · GTA 1 (1997)", "yellow"), ("Globe Oil", "⛽ GLOBE OIL · GTA 4", "white"),
     ("Fleeca", "🏦 FLEECA · GTA 5", "green"), ("Tommy Vercetti", "TOMMY VERCETTI 🌴", "cyan")],
 hits=["guinos", "1997", "fleeca", "tommy"],
)

V["17"] = dict(slug="3_cosas_confirmadas", tone="#FFE14D",
 text="Tres cosas que Rockstar confirmó de GTA 6, y que nadie esperaba. Uno: hay un casino en el mapa… pero no se puede apostar. Dos: cuando termina la historia, puedes seguir jugando. Tres: hay zonas del mapa que podrían usarse en el futuro. ¿Más contenido en camino? Rockstar no lo ha dicho. ¿Qué te gustaría que agregaran?",
 hook=[("3 COSAS QUE", "yellow"), ("NADIE ESPERABA", "red")],
 montage=["azotea_coctel_noche", "vc_skyline_noche", "mount_kalaga_canon"],
 shots=[("Uno: hay", "azotea_coctel_noche", "push"), ("pero no se", "jason_pistola_balas_dinero", "punch"), ("Dos: cuando", "jl_convertible_costa", "right"),
        ("puedes seguir", "vc_helicoptero_atardecer", "push"), ("Tres: hay", "mount_kalaga_canon", "punch"), ("que podrían", "grassrivers_skyline", "left"),
        ("¿Más contenido", "leonida_keys_aereo", "pull"), ("Rockstar no", "jason_reja_policia", "push"), ("¿Qué te gustaría", "azotea_coctel_noche", "push")],
 kw=[("Uno: hay", "1 · 🎰 CASINO SIN APUESTAS", "red"), ("Dos: cuando", "2 · SIGUES JUGANDO AL FINAL", "green"),
     ("Tres: hay", "3 · ZONAS PARA EL FUTURO 🗺️", "yellow"), ("Rockstar no", "SIN CONFIRMAR", "white")],
 hits=["uno", "dos", "tres", "apostar"],
)

V["18"] = dict(slug="noventa_y_nueve", tone="#FFE14D",
 text="GTA 6 ya es el juego mejor calificado de la historia. Noventa y nueve en Metacritic. Empata con Zelda: Ocarina of Time, de 1998. Con más de ciento cincuenta reseñas, y ni una sola mixta o negativa. Kotaku dijo que junta lo mejor de todos los juegos de Rockstar. ¿Tú le darías un diez?",
 hook=[("EL MEJOR JUEGO", "yellow"), ("DE LA HISTORIA 🏆", "red")],
 montage=["vc_helicoptero_atardecer", "lucia_auto_neon", "jl_convertible_costa"],
 shots=[("Noventa y nueve", "vc_letrero_avion", "punch"), ("Empata con", "mount_kalaga_canon", "push"), ("de 1998", "grassrivers_skyline", "right"),
        ("Con más de", "azotea_coctel_noche", "push"), ("y ni una", "jl_moto_policia_helicoptero", "punch"), ("Kotaku dijo", "jason_hidroavion", "left"),
        ("todos los juegos", "vc_skyline_noche", "push"), ("¿Tú le darías", "lucia_auto_neon", "pull"), ("un diez", "vc_helicoptero_atardecer", "punch")],
 kw=[("Noventa y nueve", "METACRITIC: 99 🏆", "yellow"), ("Ocarina", "ZELDA OCARINA OF TIME · 1998", "white"),
     ("ni una sola", "0 RESEÑAS NEGATIVAS", "green"), ("Kotaku", "LO MEJOR DE ROCKSTAR", "cyan")],
 hits=["noventa", "empata", "ni", "diez"],
)

V["19"] = dict(slug="casi_rompe_internet", tone="#22E3D6",
 text="GTA 6 casi rompe internet… literalmente. Uno de los nodos de internet más grandes del mundo, DE-CIX, marcó récord de tráfico por las descargas. El juego pesa hasta doscientos doce gigas. Y EA hasta le pidió a los jugadores de Madden que no lo borraran para hacerle espacio. ¿Qué juego borraste tú?",
 hook=[("GTA 6 CASI", "yellow"), ("ROMPE INTERNET 🌐", "red")],
 montage=["vc_skyline_noche", "gasolinera_neon", "lucia_persecucion_tunel"],
 shots=[("Uno de los", "grassrivers_skyline", "pull"), ("marcó récord", "vc_skyline_noche", "punch"), ("por las descargas", "lucia_persecucion_tunel", "push"),
        ("El juego pesa", "jl_auto_llamas_bolsas", "punch"), ("Y EA", "jl_gimnasio_pelea", "right"), ("que no lo borraran", "jason_reja_policia", "push"),
        ("para hacerle", "jl_escalera_metal", "left"), ("¿Qué juego", "vc_skyline_noche", "push")],
 kw=[("marcó récord", "📈 RÉCORD DE TRÁFICO", "green"), ("doscientos doce", "212 GB 😳", "yellow"), ("Madden", "EA: NO BORRES MADDEN 😭", "red")],
 hits=["literalmente", "record", "doscientos", "madden"],
)

V["20"] = dict(slug="trece_anos", tone="#FF2E88",
 text="Trece años. Eso esperamos entre GTA 5 y GTA 6. GTA 5 salió en 2013, en PlayStation 3. En ese tiempo salieron dos generaciones nuevas de consolas, y GTA 5 se vendió en las tres. Hoy, por fin, empieza otra historia. ¿Cuántos años tenías tú cuando salió GTA 5?",
 hook=[("13 AÑOS", "yellow"), ("DE ESPERA ⏳", "red")],
 montage=["vc_helicoptero_atardecer", "port_gellhorn_atardecer", "vc_letrero_avion"],
 shots=[("Eso esperamos", "jl_convertible_costa", "push"), ("GTA 5 salió", "vc_noria_dia", "left"), ("en PlayStation", "port_gellhorn_motel", "push"),
        ("En ese tiempo", "grassrivers_skyline", "right"), ("y GTA 5", "jason_manejando_copiloto", "push"), ("Hoy, por fin", "vc_letrero_avion", "punch"),
        ("empieza otra", "jl_abrazo_pantano_policia", "pull"), ("¿Cuántos años", "lucia_auto_neon", "push"), ("cuando salió", "vc_helicoptero_atardecer", "push")],
 kw=[("en 2013", "GTA 5 · 2013 · PS3", "white"), ("dos generaciones", "PS3 → PS4 → PS5", "cyan"), ("empieza otra", "GTA 6 · 2026 🌴", "yellow")],
 hits=["trece", "2013", "hoy"],
)

# ---- capas variadas (pattern interrupts) para 11–20 ----
def _lay(vid, anchor, lay):
    sh = V[vid]["shots"]
    for i, s in enumerate(sh):
        if s[0] == anchor: sh[i] = (s[0], s[1], s[2], lay); return
    raise KeyError((vid, anchor))
def _rmkw(vid, *anchors):
    V[vid]["kw"] = [k for k in V[vid]["kw"] if k[0] not in anchors]

_lay("11", "Diecisiete millones", dict(k="count", **{"from": 0}, to=17, suf=" M", label="COPIAS ANTES DE SALIR"))
_lay("11", "Más de mil", dict(k="count", **{"from": 0}, to=1650, pre="$", suf=" M", label="DÓLARES"))
_lay("11", "según Sensor", dict(k="news", src="Según Sensor Tower", hl="GTA 6 supera los 1,600 millones de dólares antes de salir"))
_lay("11", "noventa y nueve", dict(k="slam", text="99|METACRITIC", bg="#0b0b0b"))
_lay("11", "en vivo", dict(k="cine"))
_rmkw("11", "Diecisiete millones", "mil seiscientos", "noventa y nueve")

_lay("12", "Un jugador", dict(k="cine"))
_lay("12", "seis minutos", dict(k="count", **{"from": 0}, to=6, suf=" MIN", label="SUBIENDO LA TORRE"))
_lay("12", "había un huevo", dict(k="slam", text="UN HUEVO|LITERAL", bg="#3DFF6E"))
_lay("12", "Rockstar siempre", dict(k="card"))
_rmkw("12", "seis minutos", "había un huevo")

_lay("13", "apareció una foto", dict(k="card"))
_lay("13", "Muchos sospechaban", dict(k="mono"))
_lay("13", "dicen que encontraron", dict(k="news", src="Según fans que mapean el juego", hl="La casa de la foto de 2021 está en Belville, GTA 6"))
_lay("13", "Igualita", dict(k="slam", text="IGUALITA", bg="#FFE14D"))
_lay("13", "Rockstar no", dict(k="mono"))
_rmkw("13", "Igualita", "misma casa")

_lay("14", "el ejército", dict(k="news", src="Según Kotaku", hl="Soldados de EE. UU. reciben días libres para jugar GTA 6"))
_lay("14", "movió un examen", dict(k="card"))
_lay("14", "ocho de cada", dict(k="count", **{"from": 0}, to=8, suf="/10", label="SE VAN A DESVELAR"))
_rmkw("14", "el ejército", "ocho de cada diez")

_lay("15", "y esos ni", dict(k="mono"))
_lay("15", "cuando hacen", dict(k="card"))
_lay("15", "cuatro veintinueve", dict(k="count", **{"from": 0}, to=4.29, dec=2, pre="$", label="EL GALÓN"))

_lay("16", "una base militar", dict(k="count", **{"from": 2026}, to=1997, label="EL PRIMER GTA"))
_lay("16", "Los camiones", dict(k="card"))
_lay("16", "El banco Fleeca", dict(k="slam", text="FLEECA|GTA 5", bg="#0b0b0b"))
_lay("16", "Tommy Vercetti", dict(k="cine"))

_lay("17", "pero no se", dict(k="slam", text="SIN|APUESTAS", bg="#FF2D45"))
_lay("17", "puedes seguir", dict(k="cine"))
_lay("17", "que podrían", dict(k="card"))
_lay("17", "Rockstar no", dict(k="mono"))

_lay("18", "Noventa y nueve", dict(k="count", **{"from": 0}, to=99, label="METACRITIC"))
_lay("18", "Con más de", dict(k="count", **{"from": 0}, to=150, pre="+", label="RESEÑAS"))
_lay("18", "y ni una", dict(k="slam", text="0|NEGATIVAS", bg="#3DFF6E"))
_lay("18", "Kotaku dijo", dict(k="news", src="Según Kotaku", hl="Junta lo mejor de todos los juegos de Rockstar"))
_rmkw("18", "Noventa y nueve", "ni una sola", "Kotaku")

_lay("19", "marcó récord", dict(k="news", src="Según DE-CIX", hl="Récord de tráfico de internet por las descargas de GTA 6"))
_lay("19", "El juego pesa", dict(k="count", **{"from": 0}, to=212, suf=" GB", label="DE DESCARGA"))
_lay("19", "Y EA", dict(k="card"))
_lay("19", "que no lo borraran", dict(k="slam", text="NO BORRES|MADDEN", bg="#FF2D45"))
_rmkw("19", "marcó récord", "doscientos doce", "Madden")

_lay("20", "Eso esperamos", dict(k="count", **{"from": 0}, to=13, label="AÑOS DE ESPERA"))
_lay("20", "GTA 5 salió", dict(k="mono"))
_lay("20", "en PlayStation", dict(k="mono"))
_lay("20", "Hoy, por fin", dict(k="slam", text="HOY|EMPIEZA", bg="#FF2E88"))
_lay("20", "empieza otra", dict(k="cine"))
_rmkw("20", "empieza otra")

# ---- versión 2: guiones con frases puente, estilo de tendencia (v5), clips y animaciones ----
import re as _re, os as _os
_txt = open(_os.path.join(_os.path.dirname(__file__), "..", "out", "ZONA_GTA_guiones_11_al_20_v3.txt"), encoding="utf-8").read()
for _m in _re.finditer(r"──────── (\d+) · [^\n]*\n(.+?)\n", _txt):
    V[_m.group(1)]["text"] = _m.group(2).strip()

def _ren(vid, old, new):
    v = V[vid]
    v["shots"] = [((new,) + s[1:]) if s[0] == old else s for s in v["shots"]]
    v["kw"] = [((new,) + k[1:]) if k[0] == old else k for k in v["kw"]]
def _set(vid, anchor, img=None, lay="keep", move=None):
    sh = V[vid]["shots"]
    for i, s in enumerate(sh):
        if s[0] == anchor:
            L = s[3] if len(s) > 3 else None
            if lay != "keep": L = lay
            t = (s[0], img or s[1], move or s[2]) + ((L,) if L else ()); sh[i] = t; return
    raise KeyError((vid, anchor))

BANNERS = {"11": "¿Ya tienes *GTA 6*?", "12": "¿Subirías por *un huevo*?", "13": "¿Fue a *propósito*?", "14": "¿Faltarías por *GTA 6*?",
           "15": "¿Cuál de estos *viste*?", "16": "¿Notaste *estos guiños*?", "17": "¿Qué le *agregarías*?", "18": "¿Le darías *un 10*?",
           "19": "¿Qué juego *borraste*?", "20": "¿Cuántos años *tenías*?"}
for _k, _b in BANNERS.items():
    V[_k].update(banner=_b, v5=True, hook=[], music="synth")

_ren("12", "Y arriba", "Y cuando"); _ren("13", "Ahora, fans", "Y ahora viene"); _ren("14", "Y en una encuesta", "Y lo más fuerte")
_ren("15", "Y cinco", "Y el cinco"); _ren("16", "Y hay un arma", "Pero hay un detalle"); _ren("17", "Tres: hay", "Y la tres")
_ren("18", "Con más de", "más de ciento"); _ren("19", "Y EA", "Y lo más chistoso"); _ren("20", "En ese tiempo", "Y piénsalo")

V["11"]["montage"][0] = "clip:money"; _set("11", "Y millones", "clip:neon", None, "push")
_set("12", "la torre", lay=dict(k="anim", p="tower", label="LA TORRE MÁS ALTA")); _set("12", "Y cuando", "clip:egg", None, "push")
_set("14", "movió un examen", "clip:exam@2", None, "push"); _set("14", "desvelar jugando", "clip:sleep@2", None, "push")
_set("15", "Uno: hay", "clip:komodo@1", None, "push")
_set("17", "Uno: hay", lay=dict(k="anim", p="slots", label="CASINO SIN APUESTAS")); _set("17", "pero no se", lay=None, move="punch")
V["17"]["kw"] = [k for k in V["17"]["kw"] if k[0] != "Uno: hay"]
_set("19", "Uno de los", "clip:server@2", None, "push"); _set("19", "marcó récord", lay=dict(k="anim", p="globe", label="RÉCORD DE TRÁFICO", sub="DE-CIX"))
_set("19", "El juego pesa", lay=dict(k="anim", p="download", label="212 GB", sub="DE DESCARGA"))
_set("20", "Eso esperamos", lay=dict(k="anim", p="calendar", **{"from": 2013}, to=2026, label="13 AÑOS DE ESPERA"))


# ---- versión 3: 4 temas nuevos del día del lanzamiento (11, 16, 17, 20) ----
V["11"] = dict(slug="nueva_zelanda_2millones", tone="#FFE14D", v5=True, hook=[], music="synth", banner="¿Tú fingiste vivir en *Nueva Zelanda*?",
 text=V["11"]["text"],
 montage=["clip:playing", "leonida_keys_aereo", "vc_skyline_noche"],
 shots=[("solo para jugar", "jl_convertible_costa", "push"),
        ("Según Kotaku", "vc_letrero_avion", "push", dict(k="news", src="Según Kotaku", hl="2.1 millones fingieron vivir en Nueva Zelanda para jugar GTA 6 antes")),
        ("un millón y", "clip:hands@2", "push", dict(k="count", **{"from": 0}, to=1.5, dec=1, suf=" M", label="XBOX · ESTADOS UNIDOS")),
        ("dieciocho horas", "lucia_auto_neon", "push", dict(k="count", **{"from": 0}, to=18, suf=" H", label="ANTES QUE TODOS")),
        ("Y en Reino", "vc_skyline_noche", "push", dict(k="count", **{"from": 0}, to=600, suf=" MIL", label="REINO UNIDO")),
        ("Y lo más", "jason_reja_policia", "punch"),
        ("no ha anunciado", "jl_moto_policia_helicoptero", "push"),
        ("¿Tú lo hiciste", "clip:neon@1", "push"),
        ("como todos", "clip:playing", "push")],
 kw=[("no ha anunciado", "SIN BANEOS… POR AHORA", "red")],
 hits=["dos", "curioso", "baneos"])

V["16"] = dict(slug="lo_que_rockstar_quito", tone="#FF2D45", v5=True, hook=[], music="synth", banner="¿Qué te dolió *más*?",
 text=V["16"]["text"],
 montage=["jl_auto_pistolas", "vc_noria_dia", "ambrosia_fiesta_lodo"],
 shots=[("y una dolió", "jason_reja_policia", "punch"),
        ("Rob Nelson", "azotea_coctel_noche", "push", dict(k="news", src="Según Kotaku", hl="Rockstar cortó contenido de GTA 6 por falta de tiempo")),
        ("La primera", "vc_noria_dia", "push"),
        ("Disney World", "vc_helicoptero_atardecer", "right"),
        ("La segunda", "jl_gimnasio_pelea", "punch", dict(k="slam", text="LOS|DARDOS", bg="#FF2D45")),
        ("Y él mismo", "jason_capucha_rifle", "push"),
        ("fue polémico", "jl_cubriendose_armas", "punch", dict(k="mono")),
        ("¿Cuál te", "lucia_auto_neon", "push"),
        ("gustado más", "jl_auto_pistolas", "push")],
 kw=[("La primera", "1 · ZONA ESTILO DISNEY 🎢", "yellow"), ("fue polémico", "«POLÉMICO»", "white")],
 hits=["quito", "dolio", "segunda", "polemico"])

V["17"] = dict(slug="capturas_lavadas_hdr", tone="#22E3D6", v5=True, hook=[], music="synth", banner="¿A ti también te *pasó*?",
 text=V["17"]["text"],
 montage=["lucia_auto_neon", "gasolinera_neon", "vc_skyline_noche"],
 shots=[("no es tu", "lucia_auto_neon", "push", dict(k="split", img2="lucia_auto_neon", fa="saturate(.35) contrast(.62) brightness(1.35)", fb="none", a="ASÍ SE VE ✗", b="ASÍ DEBE VERSE ✓")),
        ("Le está pasando", "clip:neon@2", "push"),
        ("La solución", "gasolinera_neon", "punch", dict(k="slam", text="APAGA|EL HDR", bg="#22E3D6")),
        ("En Xbox", "clip:hands@1", "push"),
        ("y reinicia", "vc_skyline_noche", "push"),
        ("En PS5", "clip:playing@2", "push"),
        ("Y listo", "jl_convertible_costa", "punch"),
        ("Guarda este", "vc_helicoptero_atardecer", "push"),
        ("¿A ti", "lucia_auto_neon", "push")],
 kw=[("En Xbox", "XBOX: HDR + AUTO HDR ✗", "white"), ("y reinicia", "🔄 REINICIA", "yellow"), ("En PS5", "PS5: HDR ✗", "white"),
     ("colores normales", "✅ COLORES NORMALES", "green"), ("Guarda este", "📌 GUÁRDALO", "yellow")],
 hits=["solucion", "listo", "guarda"])

V["20"] = dict(slug="gta6_mundo_real", tone="#FF2E88", v5=True, hook=[], music="synth", banner="¿Comprarías algo de *GTA 6*?",
 text=V["20"]["text"],
 montage=["vc_letrero_avion", "lucia_checks_cashing", "vc_skyline_noche"],
 shots=[("Heinz sacó", "gasolinera_neon", "push", dict(k="news", src="Según Kotaku", hl="Heinz lanza Gorge, la cátsup que GTA 6 parodiaba")),
        ("la marca", "lucia_checks_cashing", "push"),
        ("Y en Miami", "vc_skyline_noche", "right"),
        ("con el logo", "vc_letrero_avion", "push"),
        ("se agotaron", "vc_helicoptero_atardecer", "push", dict(k="count", **{"from": 0}, to=90, suf=" MIN", label="Y SE AGOTARON")),
        ("Ya las revenden", "clip:money@1", "push"),
        ("¿Tú comprarías", "ambrosia_fiesta_lodo", "push"),
        ("algo de", "vc_letrero_avion", "push")],
 kw=[("la marca", "🍅 GORGE: CÁTSUP REAL", "red"), ("Y en Miami", "🏀 PLAYERAS VICE CITY", "white"), ("Ya las revenden", "💸 REVENTA: CIENTOS DE USD", "green")],
 hits=["real", "agotaron", "revenden"])
# v3b: guion 12 nuevo (huevo al parabrisas)
_ren("12", "Rockstar siempre", "Y si lo"); _ren("12", "en los lugares", "Rockstar sabía")
V["12"]["kw"] = [k for k in V["12"]["kw"] if k[0] != "lugares más absurdos"] + [("parabrisas", "🚗 DIRECTO AL PARABRISAS", "cyan")]

# ---- versión 4: material real (clips del tráiler, huevo, playeras, capturas) ----
FX.update(casa_gta6=(.62, .5), casa_sa=(.72, .5), gorge=(.52, .5), decix_tabla=(.5, .5), madden_tweet=(.5, .5), metacritic99=(.7, .3),
          hdr_lavada=(.5, .5), dardos_lucia=(.5, .5), soldado_moto=(.45, .4), profe_correo1=(.5, .5), profe_correo2=(.5, .5),
          metacritic_crop=(.5, .5), profe_examen=(.5, .5), profe_top=(.5, .5), madden_crop=(.5, .5), profe_mail=(.5, .5))

def _v(vid, **kw): V[vid].update(kw)

_v("11", montage=["clip:nz@1", "clip:nz@4.6", "clip:tr40@0.3"],
 shots=[("solo para jugar", "clip:nz@7.6", "push"),
        ("Según Kotaku", "vc_letrero_avion", "push", dict(k="news", src="Según Kotaku", hl="2.1 millones fingieron vivir en Nueva Zelanda para jugar GTA 6 antes")),
        ("un millón y", "clip:tr40@0.2", "push", dict(k="count", **{"from": 0}, to=1.5, dec=1, suf=" M", label="XBOX · ESTADOS UNIDOS")),
        ("cambiaron su región", "clip:nz@0.2", "push"),
        ("dieciocho horas", "clip:tr46@2.5", "push", dict(k="count", **{"from": 0}, to=18, suf=" H", label="ANTES QUE TODOS")),
        ("Y en Reino", "clip:tr11@0.4", "push", dict(k="count", **{"from": 0}, to=600, suf=" MIL", label="REINO UNIDO")),
        ("Y lo más", "clip:tr46@1.1", "punch"),
        ("no ha anunciado", "clip:tr52@0.2", "push"),
        ("¿Tú lo hiciste", "clip:nz@5.2", "push"),
        ("como todos", "clip:tr26@0.1", "push")])

_v("12", montage=["clip:egg_throw@7", "clip:egg_nest@1.5", "clip:egg_tower@2"],
 shots=[("Un jugador", "clip:egg_climb@0", "push", dict(k="cine")),
        ("la torre de radio", "clip:egg_tower@2.4", "up"),
        ("La subida", "clip:egg_climb@4", "push", dict(k="count", **{"from": 0}, to=6, suf=" MIN", label="SUBIENDO LA TORRE")),
        ("Y cuando", "clip:egg_climb@6.8", "push"),
        ("en un nido", "clip:egg_nest@0.8", "push"),
        ("había un huevo", "clip:egg_nest@4.5", "punch"),
        ("Y si lo", "clip:egg_throw@1.2", "push"),
        ("desde la torre", "clip:egg_throw@4", "push"),
        ("se activa", "clip:egg_throw@6.2", "push"),
        ("el huevo cae", "clip:egg_throw@7.8", "push"),
        ("en el parabrisas", "clip:egg_car@4.6", "punch"),
        ("Rockstar sabía", "clip:egg_car@6.4", "push"),
        ("¿Tú hasta", "clip:egg_top@1.5", "push")],
 kw=[("torre de radio", "📡 LA TORRE MÁS ALTA", "white"), ("había un huevo", "🥚 UN HUEVO… LITERAL", "green"),
     ("en el parabrisas", "🚗 DIRECTO AL PARABRISAS", "cyan")],
 hits=["literal", "huevo", "escena", "parabrisas"])

_v("13", montage=["casa_sa", "casa_gta6", "clip:tr02@2.3"],
 shots=[("En GTA San", "casa_sa", "push"),
        ("apareció una foto", "casa_sa", "push", dict(k="shot", src="casa_sa", z=1.1, zx=.75, zy=.6)),
        ("que no estaba", "casa_sa", "push", dict(k="mono")),
        ("Muchos sospechaban", "clip:tr11@5.3", "push"),
        ("Y ahora viene", "clip:tr02@2.2", "pull"),
        ("dicen que encontraron", "casa_gta6", "push"),
        ("en Belville", "casa_gta6", "right"),
        ("Igualita", "casa_sa", "punch", dict(k="split", img2="casa_gta6", fx2=.62, a="SAN ANDREAS · 2021", b="GTA 6 · 2026")),
        ("Y adentro", "clip:tr26@3.4", "push", dict(k="mono")),
        ("sabe que vive", "clip:tr60@4.3", "push"),
        ("Rockstar no", "casa_gta6", "pull", dict(k="mono")),
        ("¿Tú crees", "casa_gta6", "push")],
 kw=[("San Andreas", "SAN ANDREAS DEFINITIVE · 2021", "white"), ("misma casa", "LA MISMA CASA EN GTA 6", "green"),
     ("en Belville", "📍 BELVILLE", "cyan"), ("sabe que vive", "🕵️ SABE QUE ES UN VIDEOJUEGO", "yellow"), ("no lo ha confirmado", "SIN CONFIRMAR", "red")],
 hits=["nadie", "misma", "igualita", "videojuego"])

_v("14", montage=["clip:heat@3", "clip:tr26@1.4", "clip:tr40@4.2"],
 shots=[("En Estados Unidos", "clip:tr26@1.2", "push"),
        ("el ejército", "soldado_moto", "push", dict(k="news", src="Según Kotaku", hl="43 soldados se reenlistaron a cambio de días libres para jugar GTA 6")),
        ("cuatro días libres", "clip:tr26@1.9", "push", dict(k="count", **{"from": 0}, to=4, suf=" DÍAS", label="LIBRES PARA JUGAR")),
        ("para que pudieran", "soldado_moto", "push"),
        ("En España", "profe_mail", "push", dict(k="shot", src="profe_mail", z=1.12, zx=.3, zy=.75, zt=.9,
                                                  hl=[[.49, .64, .41, .11], [.05, .76, .29, .11]])),
        ("para la semana", "clip:exam@2", "push"),
        ("Y lo más fuerte", "clip:tr40@4.2", "punch"),
        ("ocho de cada", "clip:sleep@2", "push", dict(k="count", **{"from": 0}, to=8, suf="/10", label="SE VAN A DESVELAR")),
        ("desvelar jugando", "clip:tr11@5.3", "push"),
        ("¿Tú faltarías", "clip:tr40@0.3", "pull"),
        ("o al trabajo", "clip:tr66@6.2", "push")],
 kw=[("un profesor", "📚 MOVIÓ UN EXAMEN", "yellow"), ("¿Tú faltarías", "¿FALTARÍAS? 🤔", "white")],
 hits=["absurdas", "ejercito", "examen", "ocho"])

_v("15", montage=["clip:tr26@1.3", "clip:tr52@4.4", "clip:tr02@0.2"],
 shots=[("Uno: hay", "clip:tr26@1.2", "push"),
        ("en el pantano", "clip:komodo@1", "punch"),
        ("y esos ni", "clip:komodo@4", "push", dict(k="mono")),
        ("Dos: en", "clip:tr18@0.2", "push"),
        ("ya puede ir", "clip:tr18@1.5", "right"),
        ("En GTA 5", "clip:tr18@2.3", "push", dict(k="mono")),
        ("Tres: los", "clip:tr52@4.2", "push"),
        ("cuando hacen", "clip:tr52@5.1", "punch"),
        ("Cuatro: hay", "clip:tr02@0.05", "push"),
        ("motos de agua", "clip:tr02@0.5", "right"),
        ("Y el cinco", "clip:tr_keys@0.1", "punch"),
        ("cuatro veintinueve", "clip:tr_keys@0.4", "push", dict(k="count", **{"from": 0}, to=4.29, dec=2, pre="$", label="EL GALÓN")),
        ("¿Cuál viste", "clip:tr26@0.1", "pull")],
 kw=[("Uno: hay", "1 · DRAGÓN DE KOMODO 🦎", "yellow"), ("Dos: en", "2 · PASAJERO ATRÁS 🚗", "yellow"), ("Tres: los", "3 · SUDAN 💦", "yellow"),
     ("Cuatro: hay", "4 · 3 MOTOS DE AGUA 🌊", "yellow"), ("Y el cinco", "5 · GASOLINA ⛽", "yellow")],
 hits=["uno", "dos", "tres", "cuatro", "cinco"])

_v("16", montage=["dardos_lucia", "clip:darts@1", "clip:tr40@4.2"],
 shots=[("y una dolió", "clip:darts@2", "punch"),
        ("Rob Nelson", "dardos_lucia", "push", dict(k="news", src="Según VGC", hl="Rockstar explica por qué quitó cosas de GTA 6: «No tenemos tiempo ilimitado»")),
        ("La primera", "vc_noria_dia", "push"),
        ("Disney World", "vc_helicoptero_atardecer", "right"),
        ("La segunda", "clip:darts_bar@0.5", "punch"),
        ("Y él mismo", "clip:darts@4", "push"),
        ("fue polémico", "clip:darts@6", "punch", dict(k="mono")),
        ("¿Cuál te", "dardos_lucia", "push"),
        ("gustado más", "clip:tr40@0.3", "push")],
 kw=[("La primera", "1 · ZONA ESTILO DISNEY 🎢", "yellow"), ("La segunda", "2 · LOS DARDOS 🎯", "yellow"), ("fue polémico", "«POLÉMICO»", "white")],
 hits=["quito", "dolio", "segunda", "polemico"])

_set("17", "no es tu", "hdr_lavada", dict(k="split", img2="hdr_lavada", fa="none", fb="contrast(1.45) saturate(1.55) brightness(.8)", a="ASÍ SE VE ✗", b="ASÍ DEBE VERSE ✓"))
_set("17", "Le está pasando", "hdr_lavada", None, "push")
V["17"]["montage"] = ["hdr_lavada", "clip:tr40@0.3", "clip:tr46@0.2"]

_v("18", montage=["clip:tr40@0.3", "metacritic_crop", "clip:tr52@0.2"])
_set("18", "Noventa y nueve", "metacritic_crop", dict(k="shot", src="metacritic_crop", z=1.18, zx=.88, zy=.55, ring=[.80, .46, .18, .21]))
_set("18", "Empata con", "clip:tr66@0.2", None, "push")
_set("18", "más de ciento", "metacritic_crop", dict(k="shot", src="metacritic_crop", z=1.12, zx=.2, zy=.6, hl=[[.025, .57, .46, .08]]))
_set("18", "todos los juegos", "clip:tr46@2.5", None, "push")
_set("18", "¿Tú le darías", "clip:tr40@0.3", None, "pull")
_set("18", "un diez", "clip:tr66@6.2", None, "punch")

_v("19", montage=["clip:server@2", "madden_crop", "clip:tr46@0.2"])
_set("19", "marcó récord", "decix_tabla", dict(k="shot", src="decix_tabla", z=1.1, zx=.7, zy=.75, ring=[.655, .68, .11, .13]))
_set("19", "Y lo más chistoso", "madden_crop", dict(k="shot", src="madden_crop", z=1.1, zx=.25, zy=.5, hl=[[.015, .43, .47, .11], [.32, .81, .26, .09]]))
_set("19", "¿Qué juego", "clip:tr46@0.2", None, "push")

_v("20", montage=["gorge", "clip:heat@3", "clip:tr40@0.3"])
_set("20", "Heinz sacó", "gorge", dict(k="shot", src="gorge", z=1.08, zx=.52, zy=.55))
_set("20", "la marca", "gorge", None, "push")
_set("20", "Y en Miami", "clip:heat@0.5", None, "push")
_set("20", "con el logo", "clip:heat@4", None, "right")
_set("20", "se agotaron", "clip:heat@7", None, "push")
_set("20", "¿Tú comprarías", "clip:tr40@0.3", None, "pull")
# v4b: ajustes tras revisar fotogramas
FX.update(decix_crop=(.5, .5), madden_crop2=(.5, .5))
V["18"]["montage"] = ["clip:tr40@0.3", "clip:tr66@6.2", "clip:tr52@0.2"]
V["19"]["montage"] = ["clip:server@2", "clip:tr46@6.2", "clip:tr46@0.2"]
_set("19", "marcó récord", "decix_crop", dict(k="shot", src="decix_crop", z=1.35, zx=.72, zy=.6, zt=.8, ring=[.675, .5, .1, .2]))
_set("19", "Y lo más chistoso", "madden_crop2", dict(k="shot", src="madden_crop2", z=1.25, zx=.4, zy=.55, zt=.9, hl=[[.01, .44, .86, .13], [.36, .86, .3, .1]]))
_set("14", "En España", "profe_mail", dict(k="shot", src="profe_mail", z=1.4, zx=.4, zy=.72, zt=.9, hl=[[.49, .64, .41, .11], [.05, .76, .29, .11]]))
_set("14", "Y lo más fuerte", "clip:heat@6", None, "punch")
_set("14", "desvelar jugando", "clip:tr60@3.1", None, "push")
V["14"]["montage"] = ["clip:heat@3", "clip:tr26@1.4", "clip:sleep@1"]
_set("13", "Muchos sospechaban", "clip:tr60@3.1", None, "push")
_set("12", "se activa", "clip:egg_throw@5.6", None, "push")
_set("15", "En GTA 5", "clip:tr18@0.9", None, "push")
_set("15", "Cuatro: hay", "clip:tr02@0~0.55", None, "push")
_set("15", "motos de agua", "clip:tr02@2.3", None, "right")
_set("19", "marcó récord", "decix_crop", dict(k="shot", src="decix_crop", z=1.18, zx=.62, zy=.6, zt=.8, ring=[.655, .47, .125, .23]))
_set("19", "Y lo más chistoso", "madden_crop2", dict(k="shot", src="madden_crop2", z=1.2, zx=.42, zy=.55, zt=.9, ring=[.0, .41, .9, .17]))
V["14"]["kw"] = [k for k in V["14"]["kw"] if k[0] != "un profesor"]
_set("16", "y una dolió", "dardos_lucia", None, "punch")
V["16"]["montage"] = ["dardos_lucia", "clip:darts@1", "clip:tr46@2.6"]

# ---------------- v6: sistema automático (canción real, sin whoosh) ----------------
FX.update(pw_calle_frente=(.5, .5), pw_calle_atras=(.5, .5), pw_casa=(.5, .5), pw_arranca=(.5, .5), pw_entrada=(.5, .5), pw_garaje_arriba=(.45, .5), pw_mapa=(.72, .5), pw_alarma=(.68, .5), pw_jason_lucia=(.55, .5), pw_garaje_jason=(.62, .5))
V["21"] = dict(slug="carro_paul_walker", tone="#3DFF6E", v5=True, v6=True, hook=[], banner="El carro de *Paul Walker* 💚",
 song="musica/see_you_again.mp3", song_start=10.3,
 text="Rockstar escondió el carro de Paul Walker en GTA 6. El Eclipse verde de la primera de Rápido y Furioso. Está guardado en el garaje de una casa en Vespucci Island, en Vice City. Nadie te lo vende y ninguna misión te lo da: te metes a la casa, apagas la alarma, abres el garaje y es tuyo. Y abre la cajuela, porque ahí hay otra referencia, pero de Toy Story. Desde que empieza el juego lo puedes tener.",
 montage=["pw_garaje_arriba", "pw_calle_frente", "pw_garaje_jason"],
 shots=[("Rockstar escondió", "pw_garaje_arriba", "push", dict(k="shot", src="pw_garaje_arriba", z=1.15, zx=.4, zy=.55)),
        ("de Paul Walker", "pw_calle_frente", "push", dict(k="shot", src="pw_calle_frente", z=1.12, zx=.5, zy=.55)),
        ("El Eclipse verde", "pw_calle_atras", "push", dict(k="shot", src="pw_calle_atras", z=1.1, zx=.45, zy=.6)),
        ("de la primera", "pw_garaje_arriba", "pull"),
        ("Está guardado", "pw_garaje_jason", "push"),
        ("en Vespucci Island", "pw_mapa", "push", dict(k="shot", src="pw_mapa", z=1.3, zx=.62, zy=.2, ring=[.56, .08, .16, .22])),
        ("Nadie te lo vende", "pw_casa", "push", dict(k="shot", src="pw_casa", z=1.08, zx=.5, zy=.5)),
        ("te metes a la casa", "pw_casa", "push"),
        ("apagas la alarma", "pw_alarma", "push", dict(k="shot", src="pw_alarma", z=1.12, zx=.62, zy=.55)),
        ("abres el garaje", "pw_garaje_jason", "push"),
        ("y es tuyo", "pw_arranca", "punch", dict(k="shot", src="pw_arranca", z=1.12, zx=.5, zy=.6)),
        ("Y abre la cajuela", "pw_calle_atras", "push"),
        ("pero de Toy Story", "pw_garaje_arriba", "punch", dict(k="shot", src="pw_garaje_arriba", z=1.2, zx=.65, zy=.45)),
        ("Desde que empieza", "pw_jason_lucia", "push"),
        ("lo puedes tener", "pw_calle_frente", "push", dict(k="shot", src="pw_calle_frente", z=1.15, zx=.5, zy=.55))],
 kw=[("Paul Walker", "PAUL WALKER 🕊️", "green"), ("Vespucci Island", "📍 VESPUCCI ISLAND", "yellow"),
     ("Toy Story", "🐍 TOY STORY EN LA CAJUELA", "cyan"), ("Desde que empieza", "GRATIS DESDE EL INICIO", "green")],
 hits=["escondio", "tuyo", "toy"])

# ---------------- v7: gameplay real a pantalla completa (estilo Shorts top) ----------------
V["21"] = dict(slug="carro_paul_walker", tone="#3DFF6E", v5=True, v6=True, v7=True, banner=None,
 hook=[("EL CARRO DE", "white"), ("PAUL WALKER", "yellow")],
 song="musica/see_you_again.mp3", song_start=10.3,
 text="Rockstar escondió el carro de Paul Walker en GTA 6, y mucha gente todavía no lo sabe. Es el Eclipse verde de la primera de Rápido y Furioso. Idéntico. Está en Vespucci Island, en Vice City. Te brincas la barda, rompes la puerta, apagas la alarma… y ahí está. Nadie te lo vende. Ninguna misión te lo da. Es tuyo desde el principio del juego. Y abre la cajuela, porque Rockstar escondió otra referencia… pero de Toy Story.",
 montage=["clip:pw_hero@2.6", "clip:pw_front@3.6", "clip:pw_garage_in@0.1"],
 shots=[("de Paul Walker", "clip:pw_hero@4.6", "push"),
        ("y mucha gente", "clip:pw_front@1", "push"),
        ("Es el Eclipse", "clip:pw_drive1@1", "push"),
        ("de la primera", "pw_real", "push", dict(k="split", img2="pw_game", a="EN LA VIDA REAL", b="EN GTA 6", fx2=.5)),
        ("Está en Vespucci", "clip:pw_map@0.3", "push"),
        ("en Vice City", "clip:pw_drive3@1", "push"),
        ("Te brincas la barda", "clip:pw_fence@0.5", "push"),
        ("rompes la puerta", "clip:pw_kick@1.6", "push"),
        ("apagas la alarma", "clip:pw_dark@3.9", "push", dict(k="focus", fx=.42, fy=.3, r=170)),
        ("y ahí está", "clip:pw_reveal@2.5", "punch"),
        ("Nadie te lo vende", "clip:pw_garage_in@1", "push"),
        ("Ninguna misión", "clip:pw_exit@1", "push"),
        ("Es tuyo", "clip:pw_drive2@1", "push"),
        ("desde el principio", "clip:pw_drive1@5", "push"),
        ("Y abre la cajuela", "clip:pw_garage2@3", "push"),
        ("otra referencia", "clip:pw_garage_in@5", "push"),
        ("pero de Toy Story", "clip:pw_hero@2.6", "punch")],
 kw=[("Vespucci Island", "📍 VESPUCCI ISLAND", "yellow"),
     ("brincas la barda", "1. BRINCA LA BARDA", "white", dict(list="CÓMO SACARLO:")),
     ("rompes la puerta", "2. ROMPE LA PUERTA", "white", dict(list="CÓMO SACARLO:")),
     ("apagas la alarma", "3. APAGA LA ALARMA", "white", dict(list="CÓMO SACARLO:")),
     ("Toy Story", "🐍 TOY STORY", "cyan")],
 hits=["identico", "esta", "story"])

FX.update(pw_real=(.45, .55), pw_game=(.5, .5))

# ---- 22 · ¿Real o GTA 6? (Ocean Drive) ----
V["22"] = dict(slug="real_o_gta6", tone="#FFD21F", v5=True, v6=True, v7=True, banner=None,
 hook=[("¿MIAMI", "white"), ("O GTA 6?", "yellow")],
 song="musica/blinding_lights.mp3", song_start=11.0,
 text=open("voces_ext/22.txt", encoding="utf-8").read().strip() if _os.path.exists("voces_ext/22.txt") else "",
 montage=["clip:od1@0", "clip:od1@1.0", "clip:od2@0.3"],
 shots=[("Fíjate bien", "clip:od1@2.2", "push"), ("Los carros", "clip:od2@0", "push"), ("Es GTA 6", "clip:od3@0", "punch"),
        ("Lo subió", "clip:ar1@0", "push"), ("y engañó", "clip:ar2@0", "push"),
        ("Ahora fíjate", "clip:cmp1@0", "hold"), ("con los mismos", "clip:cmp2@0", "hold"), ("Tú le hubieras", "clip:od1@0.3", "punch")],
 kw=[("Es Ocean Drive", "📍 OCEAN DRIVE, VICE CITY", "yellow"), ("hasta Rockstar", "ROCKSTAR LO COMPARTIÓ", "cyan")],
 hits=["gta", "este", "atinado"])

# --- Trabajos de GitHub: jobs/<id>/job.json definen el Short ---
import json as _json, glob as _glob
for _f in _glob.glob(_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))), "jobs", "*", "job.json")):
    _j = _json.load(open(_f, encoding="utf-8"))
    V[_j["id"]] = dict(slug=_j["slug"], tone=_j.get("tone", "#FFD21F"), v5=True, v6=True, v7=True, banner=None,
        hook=[tuple(x) for x in _j.get("hook", [])], song=_j.get("song"), song_start=_j.get("song_start", 0.0), text=_j["texto"],
        montage=_j["montage"], shots=[tuple(x) for x in _j["shots"]], kw=[tuple(x) for x in _j.get("kw", [])], hits=_j.get("hits", []))
