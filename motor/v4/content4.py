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
import os as _os

# --- Trabajos de GitHub: jobs/<id>/job.json definen el Short ---
import json as _json, glob as _glob
for _f in _glob.glob(_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))), "jobs", "*", "job.json")):
    _j = _json.load(open(_f, encoding="utf-8"))
    if "texto" not in _j or "shots" not in _j: continue   # trabajos solo para "ver" (sin guion todavía)
    V[_j["id"]] = dict(slug=_j["slug"], tone=_j.get("tone", "#FFD21F"), v5=True, v6=True, v7=True, banner=None,
        hook=[tuple(x) for x in _j.get("hook", [])], song=_j.get("song"), song_start=_j.get("song_start", 0.0), text=_j["texto"],
        montage=_j["montage"], shots=[tuple(x) for x in _j["shots"]], kw=[tuple(x) for x in _j.get("kw", [])], hits=_j.get("hits", []))
