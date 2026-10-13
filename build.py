"""Genera una landing por sede a partir de template.html.

Uso:  python build.py            -> crea sedes/<slug>/index.html (una carpeta por sede)
La sede queda fija: sin selector, con su nombre visible y su Place ID de reseña.
Cada carpeta es autosuficiente (logo y favicon incrustados): se puede publicar
como raíz de su propio subdominio.
"""
import base64, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'sedes')

tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()

# Sedes tomadas del CONFIG de la plantilla (única fuente de verdad)
SEDE_RE = re.compile(r"\{slug:'([^']+)',\s*n:'([^']+)',\s*placeId:'([^']+)'\}")
sedes = SEDE_RE.findall(tpl)
assert sedes, 'No se encontraron sedes en template.html'

fav = base64.b64encode(open(os.path.join(HERE, 'favicon.ico'), 'rb').read()).decode()

def sub_once(s, a, b):
    assert a in s, 'No encontrado en la plantilla: ' + a[:60]
    return s.replace(a, b, 1)

def build(slug, nombre, place):
    s = tpl
    # título y favicon incrustado
    s = sub_once(s, '<title>La Rueda · Gracias por visitarnos</title>', '<title>La Rueda %s · Gracias por visitarnos</title>' % nombre)
    s = sub_once(s, '<link rel="icon" href="favicon.ico">', '<link rel="icon" href="data:image/x-icon;base64,%s">' % fav)
    # chip de sede bajo el titular
    s = sub_once(s, '.sede-line{', '.sede-chip{display:inline-block;margin-top:12px;padding:6px 14px;border-radius:999px;background:rgba(255,164,0,.16);color:#FFA400;font-weight:700;font-size:14px}\n.sede-line{')
    s = sub_once(s, '<h1>Gracias por <span>visitarnos</span></h1>', '<h1>Gracias por <span>visitarnos</span></h1>\n  <span class="sede-chip">📍 Sede %s</span>' % nombre)
    # selector de sede: se conserva oculto (la lógica lo usa) y sin etiqueta ni error visible
    s = sub_once(s, '<label for="sede">¿En qué sede estás?</label>\n      <select id="sede" name="sede" required></select>',
                    '<select id="sede" name="sede" hidden></select>')
    # solo esta sede en el CONFIG, preseleccionada
    a = s.index('  sedes: [')
    b = s.index('  ]', a) + len('  ]')
    s = s[:a] + "  sedes: [\n    {slug:'%s', n:'%s', placeId:'%s'}\n  ]" % (slug, nombre, place) + s[b:]
    s = sub_once(s, "var pre = q.get('sede');", "sedeSel.value = sedes[0].slug;\n  var pre = q.get('sede');")
    # el selector de la tarjeta de reseña ya no hace falta
    s = sub_once(s, '<select id="sede2" aria-label="Elige tu sede" class="hide"></select>', '')
    s = sub_once(s, "var s2 = $('sede2'); s2.innerHTML = sedeSel.innerHTML;\n  s2.addEventListener('change', function(){ sedeSel.value = s2.value; pintarResena(); });\n", '')
    s = sub_once(s, "    $('sede2').classList.toggle('hide', !!s); $('sede2').value = sedeSel.value;\n", '')
    # la sede va en el origen del registro
    s = s.replace("origen: 'optin-qr'", "origen: 'optin-qr-%s'" % slug)
    return s

os.makedirs(OUT, exist_ok=True)
for slug, nombre, place in sedes:
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(build(slug, nombre, place))
    print('ok', slug, '' if place != 'PENDIENTE' else '(placeId PENDIENTE)')
