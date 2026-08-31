# -*- coding: utf-8 -*-
"""Basque (batua) strings for rutas-mallabia.

Each entry maps a Spanish source string to its Basque translation. The
generator (src/i18n/make_eu.py) applies them to the Spanish _tail.html
files and REFUSES to run if any key is missing from the source, so a
Spanish text that changes can never silently keep an old translation.

Place names (Trabakua, Zengotitagane, Iturzuri, Zenarruza, Oiz…) are
already Basque and stay as they are.
"""

# Shared across every page.
COMMON = {
    # masthead / chrome
    'Cambiar a tema oscuro': 'Aldatu gai ilunera',
    '<span class="place">Mallabia · Bizkaia</span>':
        '<span class="place">Mallabia · Bizkaia</span>',
    'aria-label="Volver arriba"': 'aria-label="Itzuli gora"',
    'aria-label="Foto ampliada"': 'aria-label="Argazki handitua"',
    'aria-label="Cerrar"': 'aria-label="Itxi"',

    # facts table labels
    '<span class="k">Distancia</span>': '<span class="k">Distantzia</span>',
    '<span class="k">Desnivel +</span>': '<span class="k">Desnibela +</span>',
    '<span class="k">Desnivel</span>': '<span class="k">Desnibela</span>',
    '<span class="k">Superficie</span>': '<span class="k">Azalera</span>',
    '<span class="k">Tipo</span>': '<span class="k">Mota</span>',
    '<span class="k">Actividad</span>': '<span class="k">Jarduera</span>',
    '<span class="k">Salida</span>': '<span class="k">Irteera</span>',
    '<span class="k">Dificultad</span>': '<span class="k">Zailtasuna</span>',

    # facts values
    '<span class="v">Circuito</span>': '<span class="v">Zirkuitua</span>',
    '<span class="v">Ida y vuelta</span>': '<span class="v">Joan-etorria</span>',
    '<span class="v">Pista</span>': '<span class="v">Pista</span>',
    '<span class="v">Sendero</span>': '<span class="v">Bidezidorra</span>',
    '<span class="v">Mixta</span>': '<span class="v">Nahasia</span>',
    '<span class="v">Bici</span>': '<span class="v">Bizikleta</span>',
    '<span class="v">Senderismo</span>': '<span class="v">Oinez</span>',
    '<span class="v">Correr</span>': '<span class="v">Korrika</span>',
    '<span class="v">Fácil</span>': '<span class="v">Erraza</span>',
    '<span class="v">Media</span>': '<span class="v">Ertaina</span>',
    '<span class="v">Difícil</span>': '<span class="v">Zaila</span>',
    '<span class="v">Senderismo &middot; Trail running</span>':
        '<span class="v">Oinez &middot; Trail running</span>',
}

# Shared by the three route pages.
ROUTE = {
    '&larr; Rutas': '&larr; Ibilbideak',
    '<h2>Senderismo y bici</h2>': '<h2>Oinez eta bizikleta</h2>',
    '<h2>Senderismo &middot; Trail running</h2>':
        '<h2>Oinez &middot; Trail running</h2>',
    '<span class="k">Altitud mín.</span>': '<span class="k">Altitudea min.</span>',
    '<span class="k">Altitud m&iacute;n.</span>': '<span class="k">Altitudea min.</span>',
    '<span class="k">Altitud máx.</span>': '<span class="k">Altitudea max.</span>',
    '<span class="k">Altitud m&aacute;x.</span>': '<span class="k">Altitudea max.</span>',
    'perfil real del track': 'trackaren benetako profila',
    '⤢ Ampliar': '⤢ Handitu',
    '&#10530; Ampliar': '&#10530; Handitu',
    'Ver ruta completa en Wikiloc': 'Ikusi ibilbide osoa Wikilocen',
    'Descargar GPX': 'Deskargatu GPX',
    '<b>Distancia</b> y <b>Desnivel</b>, calculados a partir del track GPX real. '
    '<b>Dificultad</b>, estimada a partir de ambos. '
    '<b>Superficie</b> y <b>Tipo</b>, observados sobre el terreno.':
        '<b>Distantzia</b> eta <b>Desnibela</b>, benetako GPX trackatik kalkulatuak. '
        '<b>Zailtasuna</b>, bien arabera zenbatetsia. '
        '<b>Azalera</b> eta <b>Mota</b>, bertatik bertara ikusiak.',
    '<span class="k">Para quién es</span>': '<span class="k">Norentzat</span>',
    '<span class="k">Para qui&eacute;n es</span>': '<span class="k">Norentzat</span>',
    '<p class="eyebrow">Mapa de la ruta</p>': '<p class="eyebrow">Ibilbidearen mapa</p>',
    'Track GPX real sobre': 'Benetako GPX tracka',
    '&middot; tambi&eacute;n en': 'gainean &middot; Wikilocen ere bai:',
    '&larr; Volver a rutas': '&larr; Itzuli ibilbideetara',
    '<b>· Puerto de Trabakua</b>': '<b>· Trabakuko mendatea</b>',
    '<b>&middot; Puerto de Trabakua</b>': '<b>&middot; Trabakuko mendatea</b>',
    'Circuito — vuelve casi al mismo punto': 'Zirkuitua — ia puntu berera itzultzen da',
    'Circuito &mdash; vuelve casi al mismo punto': 'Zirkuitua &mdash; ia puntu berera itzultzen da',
    'data-marker-title="Trabakua (salida y llegada)"':
        'data-marker-title="Trabakua (irteera eta helmuga)"',
    'aria-label="Ampliar mapa"': 'aria-label="Handitu mapa"',
    'data-label-expand="Ampliar mapa"': 'data-label-expand="Handitu mapa"',
    'data-label-collapse="Reducir mapa"': 'data-label-collapse="Txikitu mapa"',
}

HOME = {
    '<span class="brand-name">Rutas en torno al <em>pueblo</em></span>':
        '<span class="brand-name">Herri inguruko <em>ibilbideak</em></span>',

    # feat-panel photos (7 Pago)
    'alt="Corredores subiendo una cresta con los aerogeneradores del Oiz al fondo, dorsal 63 en primer plano"':
        'alt="Korrikalariak kresta batean gora, Oizeko aerosorgailuak atzealdean, 63 dortsala aurrealdean"',
    'alt="Corredor con dorsal de la 7 Pago dando el pulgar hacia arriba en un tramo de bosque, con otro corredor detr&aacute;s y las monta&ntilde;as al fondo, dorsal 37"':
        'alt="Korrikalari bat 7 Pagoko dortsalarekin hatz lodia gora eginez baso-zati batean, beste korrikalari bat atzean eta mendiak atzealdean, 37 dortsala"',

    # hero
    'alt="Bicicleta de montaña junto a un poste de señales en el monte, al atardecer, con Mallabia iluminada al fondo"':
        'alt="Mendiko bizikleta seinale-zutoin baten ondoan mendian, ilunabarrean, Mallabia argiztatuta atzealdean"',
    'alt="Persona con los brazos en alto en la cima de un monte al amanecer, con el foco '
    'frontal encendido y el mar al fondo"':
        'alt="Pertsona bat besoak gora dituela mendi baten gailurrean egunsentian, aurreko '
        'fokua piztuta eta itsasoa atzealdean"',
    '<span>Barrios, montes y pueblos del entorno</span>':
        '<span>Inguruko auzoak, mendiak eta herriak</span>',
    '<h1>Mallabia<br><em>a pie y en bici</em></h1>':
        '<h1>Mallabia<br><em>oinez eta bizikletaz</em></h1>',
    'Rutas por los barrios, montes y pueblos del entorno de Mallabia. '
    'Documentadas sobre el terreno, con datos de verdad, no de folleto.':
        'Mallabia inguruko auzoak, mendiak eta herriak zeharkatzen dituzten ibilbideak. '
        'Bertatik bertara dokumentatuak, benetako datuekin, ez liburuxka batekoak.',

    # readout
    '<span class="k">Recorrido documentado</span>': '<span class="k">Dokumentatutako ibilbidea</span>',
    '<span class="k">Desnivel acumulado</span>': '<span class="k">Metatutako desnibela</span>',
    '<span class="k">Track GPX real</span>': '<span class="k">Benetako GPX tracka</span>',
    '<span class="k">Rutas documentadas</span>': '<span class="k">Dokumentatutako ibilbideak</span>',
    '&Uacute;ltima revisi&oacute;n sobre el terreno: agosto de 2026':
        'Azken berrikuspena bertan: 2026ko abuztuan',

    # mini gallery
    '<p class="eyebrow">Sobre el terreno</p>': '<p class="eyebrow">Bertatik bertara</p>',
    'alt="Composición con tres momentos de las rutas: vista de los montes de Mallabia con una cruz en primer plano, un grupo caminando por un sendero de piedra entre bosque, y una bicicleta de montaña con el foco encendido en una cima de noche"':
        'alt="Ibilbideetako hiru une biltzen dituen konposizioa: Mallabia inguruko mendien bista gurutze bat aurrealdean, taldea harrizko bidezidorretik basoan barrena, eta mendiko bizikleta aurreko fokua piztuta gailur batean gauean"',

    # filters
    '<p class="eyebrow">Rutas documentadas</p>': '<p class="eyebrow">Dokumentatutako ibilbideak</p>',
    'aria-label="Antes de salir y d&oacute;nde aparcar"':
        'aria-label="Irten aurretik eta non aparkatu"',
    'GPS &middot; Importante': 'GPS &middot; Garrantzitsua',
    'Ver como historias &rarr;': 'Ikusi istorio gisa &rarr;',
    '<b>Explorar en el mapa</b><small>Todas las rutas, de un vistazo</small>':
        '<b>Ikusi mapan</b><small>Ibilbide guztiak, begirada batean</small>',
    '<span class="k">Antes de salir</span>': '<span class="k">Irten aurretik</span>',
    '<h2>GPS obligatorio</h2>': '<h2>GPSa nahitaezkoa</h2>',
    'aria-label="Rutas desde Trabakua"': 'aria-label="Trabakuatik abiatzen diren ibilbideak"',
    '<span class="signpost-name">Iturzuri, Zengotitagane subida por la cascada de Gerea</span>':
        '<span class="signpost-name">Iturzuri, Zengotitagane Gereako ur-jauzitik gora</span>',
    '<span class="signpost-name">Zenarruza, San Kristobal y Zengotitagane</span>':
        '<span class="signpost-name">Zenarruza, San Kristobal eta Zengotitagane</span>',
    '<span class="signpost-name">Ur Jauziak Gerea</span>':
        '<span class="signpost-name">Ur Jauziak Gerea</span>',
    '<span class="signpost-name">Trabakua, paseo por el barrio Goita</span>':
        '<span class="signpost-name">Trabakua, Goita auzoko paseoa</span>',
    '<span class="signpost-name">Hiru Txikiak, Urko, Oiz y Egoarbitza desde Ermua</span>':
        '<span class="signpost-name">Hiru Txikiak, Urko, Oiz eta Egoarbitza Ermuatik</span>',
    '<span class="signpost-name">Zengotitagane, Iturzurigana y San Crist&oacute;bal Txiki</span>':
        '<span class="signpost-name">Zengotitagane, Iturzurigana eta San Kristobal Txiki</span>',
    '<span class="signpost-name">Zengotitagane, Askako y San Crist&oacute;bal</span>':
        '<span class="signpost-name">Zengotitagane, Askako eta San Kristobal</span>',
    '<span class="signpost-name">Zengotitagane, Axmakur y Oiz</span>':
        '<span class="signpost-name">Zengotitagane, Axmakur eta Oiz</span>',
    '<span class="signpost-name">Osmagain y Arietzu</span>':
        '<span class="signpost-name">Osmagain eta Arietzu</span>',
    '<span class="signpost-name">Trabakua, Asuntza y Urko</span>':
        '<span class="signpost-name">Trabakua, Asuntza eta Urko</span>',
    '<span class="signpost-name">Trabakua Mendibil</span>':
        '<span class="signpost-name">Trabakua Mendibil</span>',
    '<h2>Trabakua<br><em>Mendibil</em></h2>': '<h2>Trabakua<br><em>Mendibil</em></h2>',
    'Circuito desde Trabakua hasta la cima del Mendibil.':
        'Zirkuitua Trabakuatik Mendibilgo gailurreraino.',
    '<span class="signpost-name">Trabakua, Mendibil, Olamendi y Arteta</span>':
        '<span class="signpost-name">Trabakua, Mendibil, Olamendi eta Arteta</span>',
    '<h2>Trabakua, Mendibil,<br><em>Olamendi y Arteta</em></h2>':
        '<h2>Trabakua, Mendibil,<br><em>Olamendi eta Arteta</em></h2>',
    'Circuito desde Trabakua por Mendibil, Olamendi y Arteta.':
        'Zirkuitua Trabakuatik, Mendibil, Olamendi eta Artetatik igarota.',
    'Las rutas est&aacute;n documentadas directamente sobre el terreno, recorri&eacute;ndolas paso a '
    'paso. La informaci&oacute;n recoge lo m&aacute;s &uacute;til que encontrar&aacute;s por el camino '
    '&mdash;vistas, fuentes de agua, cruces y algunos puntos de referencia&mdash; para ayudarte durante '
    'el recorrido.':
        'Ibilbideak zuzenean bertatik dokumentatuta daude, urratsez urrats eginez. Informazioak bidean '
        'aurkituko duzun baliagarriena jasotzen du &mdash;ikuspegiak, ur-iturriak, bidegurutzeak eta '
        'zenbait erreferentzia-puntu&mdash; ibilbidean zehar laguntzeko.',

    'Las rutas no est&aacute;n se&ntilde;alizadas, por lo que es imprescindible llevar el track cargado '
    'en un GPS, reloj o dispositivo de navegaci&oacute;n. La informaci&oacute;n que encontrar&aacute;s '
    'aqu&iacute; sirve de apoyo y para conocer mejor la ruta, pero no sustituye al track durante el '
    'recorrido.':
        'Ibilbideak ez daude seinalizatuta, beraz ezinbestekoa da trackea GPS, erloju edo '
        'nabigazio-gailu batean kargatuta eramatea. Hemen aurkituko duzun informazioak laguntzeko eta '
        'ibilbidea hobeto ezagutzeko balio du, baina ez du ordezten trackea ibilbidean zehar.',

    'aria-label="Filtrar por actividad"': 'aria-label="Iragazi jardueraren arabera"',
    'aria-label="Filtrar por dificultad"': 'aria-label="Iragazi zailtasunaren arabera"',
    '<span>F&aacute;cil</span>': '<span>Erraza</span>',
    '<span>Media</span>': '<span>Ertaina</span>',
    '<span>Dif&iacute;cil</span>': '<span>Zaila</span>',
    '<span>BTT/e-bike</span>': '<span>BTT/e-bike</span>',
    '<span>Senderismo</span>': '<span>Oinez</span>',
    'data-all-distance="Todos" data-all-desnivel="Todos" data-approx="aprox."':
        'data-all-distance="Guztiak" data-all-desnivel="Guztiak" data-approx="inguru"',
    '<div class="signpost-hub">Zona de salida &middot; Trabakua</div>':
        '<div class="signpost-hub">Irteera-gunea &middot; Trabakua</div>',
    'aria-label="Distancia m&iacute;nima"': 'aria-label="Gutxieneko distantzia"',
    'aria-label="Distancia m&aacute;xima"': 'aria-label="Gehieneko distantzia"',
    'aria-label="Desnivel m&iacute;nimo"': 'aria-label="Gutxieneko desnibela"',
    'aria-label="Desnivel m&aacute;ximo"': 'aria-label="Gehieneko desnibela"',
    '<label>Distancia &middot; <b': '<label>Distantzia &middot; <b',
    '<label>Desnivel &middot; <b': '<label>Desnibela &middot; <b',
    'No hay rutas de este tipo todav&iacute;a.': 'Oraindik ez dago mota honetako ibilbiderik.',
    'Según vayamos documentando más rutas, se añaden aquí.':
        'Ibilbide gehiago dokumentatu ahala, hemen gehituko dira.',

    # route cards
    'alt="Pista de cemento y piedra en la ruta de Trabakua"':
        'alt="Zementuzko eta harrizko pista Trabakuako ibilbidean"',
    '<h2>Asuntza<br><em>bira</em></h2>': '<h2>Asuntza<br><em>bira</em></h2>',
    'Pista entre cemento, piedra y tierra, con un repecho duro al principio —no llega a 300 m—, '
    'un desvío técnico opcional a Aginaga y vistas al Duranguesado desde Berano.':
        'Pista zementu, harri eta lur artean; hasieran 300 metro baino gutxiagoko aldapa gogorra du, '
        'Aginagara desbideratze tekniko aukerakoa, eta Durangaldeko ikuspegi zabalak eskaintzen ditu '
        'Beranotik.',
    'alt="Vista panorámica desde la ruta de Iturzuri, con el valle cubierto de niebla"':
        'alt="Bista panoramikoa Iturzuriko ibilbidetik, harana lainoz estalita"',
    '<h2>Iturzuri, Zengotitagane<br><em>subida por la cascada de Gerea</em></h2>':
        '<h2>Iturzuri, Zengotitagane<br><em>Gereako ur-jauzitik gora</em></h2>',
    'Sendero hasta el punto más alto de Mallabia: cascadas, un dolmen prehistórico y un cresterio '
    'con vistas a ambos lados antes de rodear Zengotitagane por el este.':
        'Bidezidorra Mallabiako punturik altueneraino: ur-jauziak, historiaurreko trikuharri bat '
        'eta gailurrerdi bat bi aldeetara bistak dituena, Zengotitagane ekialdetik inguratu aurretik.',
    'alt="Arroyo entre el bosque durante la subida hacia San Kristobal, ruta de Zenarruza"':
        'alt="Erreka basoan barrena San Kristobalerako igoeran, Zenarruzako ibilbidea"',
    '<h2>Zenarruza, San Kristobal<br><em>y Zengotitagane</em></h2>':
        '<h2>Zenarruza, San Kristobal<br><em>eta Zengotitagane</em></h2>',
    'Circuito largo desde Trabakua: la colegiata cisterciense de Zenarruza, una ermita de pastores '
    'en la ladera del Oiz y el dolmen de Iturzurigana, con dos subidas largas seguidas.':
        'Zirkuitu luzea Trabakuatik: Zenarruzako kolegiata zisterziarra, artzainen ermita bat '
        'Oizen hegalean eta Iturzuriganako trikuharria, bi igoera luze jarraian.',
    'Ver la ruta completa': 'Ikusi ibilbide osoa',

    # parking + trailhead map
    '<p class="eyebrow">D&oacute;nde aparcar</p>': '<p class="eyebrow">Non aparkatu</p>',
    'title="Mapa del puerto de Trabakua"': 'title="Trabakuko mendatearen mapa"',
    'Puerto de Trabakua &middot; 43,2105&deg; N, 2,5461&deg; O':
        'Trabakuko mendatea &middot; 43,2105&deg; N, 2,5461&deg; M',
    'A 5,7 km de Mallabia pueblo, unos 7 min en coche &mdash; casi todas las rutas salen de aqu&iacute;, con buen aparcamiento.':
        'Mallabia herritik 5,7 km-ra, 7 minutu inguru autoz &mdash; ia ibilbide guztiak hemendik ateratzen dira, aparkaleku onarekin.',
    'Justo al lado del aparcamiento hay dos bares: caf&eacute; antes de salir, o cerveza y algo de comer al volver.':
        'Aparkalekuaren ondoan bi taberna daude: kafea irten aurretik, edo garagardoa eta zerbait jateko itzultzean.',
    'C&oacute;mo llegar': 'Nola iritsi',
    '<p class="eyebrow">Salidas desde el puerto</p>': '<p class="eyebrow">Irteerak mendatetik</p>',
    'data-marker-title="Puerto de Trabakua (aparcamiento)"':
        'data-marker-title="Trabakuko mendatea (aparkalekua)"',
    'aria-label="Ampliar mapa"': 'aria-label="Handitu mapa"',
    'data-label-expand="Ampliar mapa"': 'data-label-expand="Handitu mapa"',
    'data-label-collapse="Reducir mapa"': 'data-label-collapse="Txikitu mapa"',
    'BTT/e-bike &middot; Trabakua, Zenarruza, Osma, Zengotitagane, San Crist&oacute;bal, Urregarai, Iruzubieta, Goita, Zaldibar y Maguna':
        'BTT/e-bike &middot; Trabakua, Zenarruza, Osma, Zengotitagane, San Kristobal, Urregarai, Iruzubieta, Goita, Zaldibar eta Maguna',
    'Senderismo &middot; Kalamua, Egoarbitza, Urko, Arietzu, Oiz, Iturzuri, Gerea, Mundioko Koba, Mendibil, Arteta, Hiru Txikiak, 7 Pago 25K y 7 Pago 16K':
        'Oinez &middot; Kalamua, Egoarbitza, Urko, Arietzu, Oiz, Iturzuri, Gerea, Mundioko Koba, Mendibil, Arteta, Hiru Txikiak, 7 Pago 25K eta 7 Pago 16K',
    '<span class="signpost-name">7 Pago Mendi Lasterketa 25km</span>':
        '<span class="signpost-name">7 Pago Mendi Lasterketa 25km</span>',
    '<span class="signpost-name">7 Pago Mendi Lasterketa 16K</span>':
        '<span class="signpost-name">7 Pago Mendi Lasterketa 16K</span>',
    '<h2>7 Pago<br><em>Mendi Lasterketa 25km</em></h2>':
        '<h2>7 Pago<br><em>Mendi Lasterketa 25km</em></h2>',
    '<h2>7 Pago<br><em>Mendi Lasterketa 16K</em></h2>':
        '<h2>7 Pago<br><em>Mendi Lasterketa 16K</em></h2>',
    '<p>El trazado real de la 7 Pago Mendi Lasterketa, con paso por la cima del Oiz.</p>':
        '<p>7 Pago Mendi Lasterketaren benetako ibilbidea, Oizko gailurretik igarota.</p>',
    '<p>El trazado real de la 7 Pago Mendi Lasterketa 16K, por los montes y barrios de Mallabia.</p>':
        '<p>7 Pago Mendi Lasterketako 16K-ko benetako ibilbidea, Mallabiko mendi eta auzoetan barrena.</p>',
    'Toca una ruta en el mapa para ver su informaci&oacute;n.':
        'Sakatu ibilbide bat mapan, bere informazioa ikusteko.',
    'download="Rutas Mallabia - todos los tracks.zip"':
        'download="Herriko ibilbideak - track guztiak.zip"',
    'Descargar todos los tracks (ZIP, un GPX por ruta)':
        'Deskargatu track guztiak (ZIP, GPX bat ibilbide bakoitzeko)',

    # osma card
    'alt="Presa de Aixola, junto a Larrosako Iturri, en la ruta de Osma"':
        'alt="Aixolako presa, Larrosako Iturritik gertu, Osmako ibilbidean"',
    '<h2>Trabakua, Elgeta<br><em>y Argi&ntilde;eta</em></h2>':
        '<h2>Trabakua, Elgeta<br><em>eta Argi&ntilde;eta</em></h2>',
    'Trabakua, Elgeta y Argi&ntilde;eta': 'Trabakua, Elgeta eta Argi&ntilde;eta',
    'Circuito desde Trabakua por ermitas y caser&iacute;os del Duranguesado hasta la Necr&oacute;polis '
    'de Argi&ntilde;eta, veinte sarc&oacute;fagos medievales en Elorrio.':
        'Zirkuitua Trabakuatik, Durangaldeko ermita eta baserrien artean, Argi&ntilde;etako '
        'Nekropoliraino, hogei bat Erdi Aroko hilobi Elorrion.',

    # gerea card
    'alt="Ur Jauziak, la cascada escalonada de Gerea, con el agua bajando entre las rocas"':
        'alt="Ur Jauziak, Gereako ur-jauzi mailakatua, ura harrien artetik jaisten"',
    '<h2>Ur Jauziak<br><em>Gerea</em></h2>': '<h2>Ur Jauziak<br><em>Gerea</em></h2>',
    'Sendero corto y familiar hasta la cascada de Gerea.':
        'Bidezidor laburra eta familiarra Gereako ur-jauziraino.',

    # goita card
    '<h2>Trabakua<br><em>paseo por el barrio Goita</em></h2>':
        '<h2>Trabakua<br><em>Goita auzoko paseoa</em></h2>',
    'Paseo corto y llano por el barrio Goita, con vistas y dos ermitas de camino.':
        'Ibilbide laburra eta laua Goita auzotik, ikuspegiekin eta bi ermitarekin bidean.',
    '<h2>Hiru Txikiak<br><em>Urko, Oiz y Egoarbitza</em></h2>':
        '<h2>Hiru Txikiak<br><em>Urko, Oiz eta Egoarbitza</em></h2>',
    'El recorrido real de la carrera Hiru Txikiak Trail, con salida y meta en Ermua.':
        'Hiru Txikiak Trail lasterketaren benetako ibilbidea, Ermuan irten eta amaituz.',
    'alt="Cruz de hierro y v&eacute;rtice geod&eacute;sico en una cima, con aerogeneradores cerca y un banco de nubes al fondo"':
        'alt="Burdinazko gurutzea eta bertize geodesikoa gailur batean, aerosorgailuak gertu eta hodei-banku bat atzealdean"',
    '<span class="v">Carretera y pista</span>': '<span class="v">Errepidea eta pista</span>',
    '<span class="signpost-name">Asuntza y Mundioko Koba</span>':
        '<span class="signpost-name">Asuntza eta Mundioko Koba</span>',
    '<h2>Mundioko<br><em>Koba</em></h2>': '<h2>Mundioko<br><em>Koba</em></h2>',
    'Circuito desde Trabakua hasta la cueva de Mundioko Koba, pasando por el Collado de Asuntza.':
        'Zirkuitua Trabakuatik Mundioko Kobaraino, Asuntzako lepotik igarota.',
    '<span class="signpost-name">Trabakua, Iturreta e Iruzubieta</span>':
        '<span class="signpost-name">Trabakua, Iturreta eta Iruzubieta</span>',
    '<h2>Trabakua, Iturreta<br><em>e Iruzubieta</em></h2>':
        '<h2>Trabakua, Iturreta<br><em>eta Iruzubieta</em></h2>',
    'Circuito desde Trabakua por Iturreta, Iruzubieta, Arta y Gerea.':
        'Zirkuitua Trabakuatik, Iturreta, Iruzubieta, Arta eta Gereatik igarota.',
    'alt="Atardecer sobre una pista rural cercada, con montes iluminados de naranja al fondo"':
        'alt="Ilunabarra landa-pista itxi batean, mendiak laranja kolorez atzealdean"',

    # zengotitagane card
    'alt="Vistas hacia el Anboto y el Alluitz, con Durango al fondo, desde lo alto de la ruta '
    'de Zengotitagane"':
        'alt="Anboto eta Alluitzerako ikuspegiak, Durango atzealdean, Zengotitaganeko '
        'ibilbidearen goialdetik"',
    '<h2>Zengotitagane, Iturzurigana<br><em>y San Crist&oacute;bal Txiki</em></h2>':
        '<h2>Zengotitagane, Iturzurigana<br><em>eta San Kristobal Txiki</em></h2>',
    'Circuito largo en e-bike desde Trabakua a Zengotitagane e Iturzurigana, con dos ermitas '
    'de camino.':
        'Zirkuitu luzea e-bikez Trabakuatik Zengotitagane eta Iturzuriganaraino, bidean bi '
        'ermitarekin.',

    # sancristobal card
    'alt="Pista junto a los aerogeneradores del parque e&oacute;lico, con niebla cubriendo la '
    'cresta"':
        'alt="Pista eolikoen ondoan, lainoak gailurra estaltzen duela"',
    '<h2>Zengotitagane, Askako<br><em>y San Crist&oacute;bal</em></h2>':
        '<h2>Zengotitagane, Askako<br><em>eta San Kristobal</em></h2>',
    'Circuito largo en e-bike desde Trabakua a Zengotitagane y Askako, con las '
    'ermitas de San Crist&oacute;bal Txiki y San Juan de camino.':
        'Zirkuitu luzea e-bikez Trabakuatik Zengotitagane eta Askakoraino, San '
        'Kristobal Txiki eta San Juan ermitak bidean.',

    # oiz card
    'alt="Aerogeneradores del Oiz reflejados en un charco de la cumbre, con las antenas al '
    'fondo"':
        'alt="Oizeko eolikoak gailurreko putzu batean islatuta, antenak atzealdean"',
    '<h2>Zengotitagane, Axmakur<br><em>y Oiz</em></h2>':
        '<h2>Zengotitagane, Axmakur<br><em>eta Oiz</em></h2>',
    'Ida y vuelta desde Trabakua hasta el Oiz, con dos altos de camino y vistas a la costa '
    'cant&aacute;brica desde la cumbre.':
        'Joan-etorria Trabakuatik Oizeraino, bidean bi goirekin eta kostalde '
        'kantauriarrerako ikuspegiekin gailurretik.',

    # arietzu card
    'alt="Vista del valle desde la ruta, con caser&iacute;os, un prado con caballos y una '
    'pista serpenteando entre los montes"':
        'alt="Haranaren ikuspegia ibilbidetik, baserriekin, zaldiak dituen larre batekin '
        'eta mendien artean bihurgunez betetako pista batekin"',
    '<h2>Osmagain<br><em>y Arietzu</em></h2>': '<h2>Osmagain<br><em>eta Arietzu</em></h2>',
    'Circuito corto desde la Ermita de San Juan, con dos altos de camino y una cruz de '
    'piedra en cada uno.':
        'Zirkuitu laburra San Juan ermitatik, bidean bi goirekin eta bakoitzean harrizko '
        'gurutze batekin.',

    # urko card
    'alt="V&eacute;rtice geod&eacute;sico en la cumbre del Urko, con nubes bajas y las '
    'monta&ntilde;as del entorno al fondo"':
        'alt="Urkoko gailurreko bertize geodesikoa, hodei baxuekin eta inguruko '
        'mendiak atzealdean"',
    '<h2>Trabakua, Asuntza<br><em>y Urko</em></h2>':
        '<h2>Trabakua, Asuntza<br><em>eta Urko</em></h2>',
    'Circuito desde Trabakua por Arandomendi, Urko y el Collado de Asuntza.':
        'Zirkuitua Trabakuatik, Arandomendi, Urko eta Asuntzako lepotik.',

    # iturreta card
    '<span class="signpost-name">Trabakua, Barinaga y Iturreta</span>':
        '<span class="signpost-name">Trabakua, Barinaga eta Iturreta</span>',
    'alt="Manillar de la bicicleta eléctrica en un sendero entre matorral, con los aerogeneradores del Oiz al fondo"':
        'alt="Bizikleta elektrikoaren eskulekua sasi arteko bidezidor batean, Oizeko eolikoak atzealdean"',
    '<h2>Trabakua, Barinaga<br><em>y Iturreta</em></h2>':
        '<h2>Trabakua, Barinaga<br><em>eta Iturreta</em></h2>',
    'Circuito en e-bike desde Trabakua por Barinaga hasta Iturreta y Mendibil.':
        'Zirkuitua e-bikez Trabakuatik, Barinaga, Iturreta eta Mendibiletik igarota.',

    # egoarbitza card
    '<span class="signpost-name">Urko, Egoarbitza y Zengotitagane</span>':
        '<span class="signpost-name">Urko, Egoarbitza eta Zengotitagane</span>',
    'alt="V&eacute;rtice geod&eacute;sico en la cumbre del Urko, con bastones de trekking apoyados y las monta&ntilde;as del entorno al fondo"':
        'alt="Urkoko gailurreko bertize geodesikoa, trekking bastoiak bermatuta eta inguruko mendiak atzealdean"',
    '<h2>Urko, Egoarbitza<br><em>y Zengotitagane</em></h2>':
        '<h2>Urko, Egoarbitza<br><em>eta Zengotitagane</em></h2>',
    'Circuito en e-bike desde Trabakua por Urko, Egoarbitza y Santamañesar hasta Zengotitagane.':
        'Zirkuitua e-bikez Trabakuatik, Urko, Egoarbitza eta Santamañesarretik igarota Zengotitaganeraino.',

    # urregarai card
    '<span class="signpost-name">Iturreta, Markina y Urregarai</span>':
        '<span class="signpost-name">Iturreta, Markina eta Urregarai</span>',
    'alt="Amanecer con luz anaranjada sobre las monta&ntilde;as, al salir de Trabakua"':
        'alt="Egunsentia argi laranjaz mendien gainean, Trabakuatik irtetean"',
    '<h2>Iturreta, Markina<br><em>y Urregarai</em></h2>':
        '<h2>Iturreta, Markina<br><em>eta Urregarai</em></h2>',
    'Circuito en e-bike desde Trabakua por Iturreta, Markina y Urregarai hasta Bolibar.':
        'Zirkuitua e-bikez Trabakuatik, Iturreta, Markina eta Urregaraitik igarota Bolibarreraino.',

    # kalamua card
    '<span class="signpost-name">Urko, Kalamua, San Migel y Mendibil</span>':
        '<span class="signpost-name">Urko, Kalamua, San Migel eta Mendibil</span>',
    'alt="Amanecer entre nubes junto al moj&oacute;n de la cumbre de Urko, km 7,9 de la ruta"':
        'alt="Egunsentia hodeien artean, Urkoko gailurreko mugarriaren ondoan, ibilbideko 7,9 km"',
    '<h2>Urko, Kalamua, San Migel<br><em>y Mendibil</em></h2>':
        '<h2>Urko, Kalamua, San Migel<br><em>eta Mendibil</em></h2>',
    'Circuito en e-bike desde Trabakua por Urko, Kalamua, San Migel, Markina, Iturreta y Mendibil.':
        'Zirkuitua e-bikez Trabakuatik, Urko, Kalamua, San Migel, Markina, Iturreta eta Mendibiletik igarota.',

    # maguna card
    '<span class="signpost-name">Trabakua, Zengotitagane y Maguna</span>':
        '<span class="signpost-name">Trabakua, Zengotitagane eta Maguna</span>',
    'alt="Caballo pastando al atardecer en una cresta, con las monta&ntilde;as al fondo"':
        'alt="Zaldia bazkan ilunabarrean gandor batean, mendiak atzealdean dituela"',
    '<h2>Trabakua, Zengotitagane<br><em>y Maguna</em></h2>':
        '<h2>Trabakua, Zengotitagane<br><em>eta Maguna</em></h2>',
    'Circuito muy largo en e-bike desde Trabakua, con paso por Zengotitagane, el Dolmen de Iturzurigana y Maguna.':
        'Zirkuitu oso luzea e-bikez Trabakuatik, Zengotitagane, Iturzuriganako Trikuharria eta Magunatik igarota.',

    # zaldibar card
    '<span class="signpost-name">Trabakua, Aixola y Berriz</span>':
        '<span class="signpost-name">Trabakua, Aixola eta Berriz</span>',
    'alt="La presa de Aixola entre los &aacute;rboles, con la niebla asomando sobre el agua"':
        'alt="Aixolako presa zuhaitzen artean, lainoa uraren gainean agertzen"',
    '<h2>Trabakua, Aixola<br><em>y Berriz</em></h2>':
        '<h2>Trabakua, Aixola<br><em>eta Berriz</em></h2>',
    'Circuito muy largo en e-bike desde Trabakua, con paso por Aixola, Elgeta y Zaldibar antes de volver por Berriz.':
        'Zirkuitu oso luzea e-bikez Trabakuatik, Aixola, Elgeta eta Zaldibartik igarota, Berriztik itzuli aurretik.',

    # footer
    'Para cualquier duda: <a href="mailto:trabakutik@gmail.com">trabakutik@gmail.com</a>':
        'Edozein zalantzarako: <a href="mailto:trabakutik@gmail.com">trabakutik@gmail.com</a>',
}

TRABAKUA = {
    '<span>Pista</span><span class="sep">/</span><span>Cemento, piedra y tierra</span>':
        '<span>Pista</span><span class="sep">/</span><span>Zementua, harria eta lurra</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    '<h1>Asuntza<br><em>bira</em></h1>': '<h1>Asuntza<br><em>bira</em></h1>',
    'Trabakua, Collado de Asuntza y Ermita de San Juan de Arteta desde Trabakua':
        'Trabakua, Asuntzako lepoa eta San Juan Artetako ermita Trabakuatik',
    'alt="Vistas desde el recorrido de Trabakua, con los montes del Duranguesado al fondo"':
        'alt="Bistak Trabakuako ibilbidetik, Durangaldeko mendiak atzealdean"',
    'alt="Foto ampliada del recorrido de Trabakua"':
        'alt="Trabakuako ibilbidearen argazki handitua"',
    'alt="La pista junto al muro de piedra, con tramos de tierra"':
        'alt="Pista harrizko hormaren ondoan, lurrezko tarteekin"',
    'alt="Vistas al Duranguesado desde la subida, con los aerogeneradores al fondo"':
        'alt="Durangaldeko bistak igoeratik, eolikoak atzealdean"',
    'alt="Manillar de la bici en marcha por la pista de Trabakua"':
        'alt="Bizikletaren manillarra Trabakuako pistan martxan"',
    'alt="Vistas al Duranguesado desde Berano, con caseríos y prados en el valle"':
        'alt="Durangaldeko bistak Beranotik, baserriak eta larreak haranean"',
    # The first Spanish paragraph becomes two in Basque -- the natural break
    # falls after the descent, so the </p><p> is part of the replacement.
    'Se sale desde el Alto de Trabakua. Los primeros metros bajan —poco más de un kilómetro— '
    'hasta un cruce a la izquierda donde se deja el asfalto atrás: desde ahí, todo es pista en '
    'solitario, alternando cemento y tramos de piedra. El primer repecho es el más duro de toda '
    'la ruta —se sube de un tirón—, pero engaña: no llega a los 300 m de distancia. '
    'Lo que viene después se lleva mejor.':
        'Trabakuako Altotik abiatzen gara. Lehen metroek behera egiten dute, kilometro bat pasatxo, '
        'eta berehala iristen gara ezkerrerako bidegurutze batera: han asfaltoa uzten dugu, eta '
        'hortik aurrera pista hutsa da, bakarrik, zementuzko eta harrizko tarteak txandakatuz, '
        'mendiko giro garbian.</p>\n'
        '    <p>Lehen aldapa da ibilbide osoko gogorrena: tiraka igotzen da, etenik gabe. Tranpa '
        'egiten du, ordea: ez da 300 metroko luzerara iristen. Behin gaindituta, ondorengoa askoz '
        'eramangarriagoa da, eta gorputzak berehala hartzen du erritmoa.',
    'Justo después de esas primeras cuestas hay una buena bajada algo técnica —sin riesgo para '
    'quien tenga algo de soltura— hasta hacernos con el camino de subida, en la zona del barrio '
    'Aginaga, sin perder mucha altura. Desde Aginaga se sube por un tramo de pista de cemento '
    'hasta enlazar con el camino de tierra, de vuelta a la pista principal, justo al collado de '
    'Asuntza. Es un tramo opcional: '
    'se puede evitar siguiendo recto, sin desviarse hacia él.':
        'Aldapa horien ostean, jaitsiera tekniko samar bat dator &mdash;trebetasun pixka bat '
        'duenarentzat arriskurik gabe&mdash;, eta oso gozagarria. Jaitsieraren amaieran berriro '
        'berreskuratzen dugu igoeraren bidea, Aginaga auzoaren inguruan, altuera handirik galdu '
        'gabe. Aginagatik zementuzko pista batetik igotzen gara, lurrezko bidearekin lotu arte, '
        'pista nagusira itzultzeko, Asuntzako lepoan bertan. Tarte hori aukerakoa da: nahi izanez '
        'gero, zuzen jarraituta saihestu daiteke.',
    'La pista rueda bien de principio a fin, sin sendero estrecho de por medio, y en las bajadas '
    'hay pendientes suficientes para coger algo de velocidad y disfrutarlas. El camino cruza Berano '
    'Txiki y la parte alta de Berano, con vistas hacia el barrio de Goita y las montañas del '
    'Duranguesado, antes de remontar de nuevo hacia Trabakua — una vuelta rápida y con paisaje.':
        'Pistak oso ondo rodatzen du hasieratik amaieraraino: ez dago bidezidor esturik, eta '
        'jaitsieretan malda nahikoa dago abiadura hartu eta gozatzeko. Bidean Berano Txiki eta '
        'Beranoko goialdea zeharkatzen ditugu, Goita eta Durangaldeko mendietarako ikuspegiekin, '
        'eta hortik Trabakuarantz berriro igotzen gara, buelta azkarra eta paisaiaz betea ixteko.',
    'Terreno de pista (cemento y piedra, con un tramo opcional de tierra), sin sendero estrecho — '
    'apta para bici de montaña convencional, no solo para eléctrica.':
        'Pista-terrenoa (zementua eta harria, eta lurrezko tarte aukerakoa), bidezidor esturik gabe — '
        'mendiko bizikleta arrunterako egokia, ez soilik elektrikorako.',
}

ITURZURI = {
    'download="Iturzuri, Zengotitagane subida por la cascada de Gerea.gpx"': 'download="Iturzuri, Zengotitagane Gereako ur-jauzitik gora.gpx"',
    '<title>Fuente de Iturzuri': '<title>Iturzuriko iturria',
    '<title>Túmulo Probazelaiburu II': '<title>Probazelaiburu II.a tumulua',
    '<title>Zengotitagane': '<title>Zengotitagane',
    '<title>Borda abandonada': '<title>Borda abandonatua',
    '<title>Refugio de montaña': '<title>Mendiko aterpea',
    '<span class="num">1</span>Fuente de Iturzuri': '<span class="num">1</span>Iturzuriko iturria',
    '<span class="num">2</span>Túmulo Probazelaiburu II': '<span class="num">2</span>Probazelaiburu II.a tumulua',
    '<span class="num">4</span>Borda abandonada': '<span class="num">4</span>Borda abandonatua',
    '<span class="num">5</span>Refugio de montaña': '<span class="num">5</span>Mendiko aterpea',
    '<span>Sendero</span><span class="sep">/</span><span>Cascadas, dolmen y cresterio</span>':
        '<span>Bidezidorra</span><span class="sep">/</span><span>Ur-jauziak, trikuharria eta gailurrerdia</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    '<h1>Iturzuri, Zengotitagane<br><em>subida por la cascada de Gerea</em></h1>':
        '<h1>Iturzuri, Zengotitagane<br><em>Gereako ur-jauzitik gora</em></h1>',
    'Iturzuri, Túmulo de Probazelaiburu II y Zengotitagane desde Trabakua':
        'Iturzuri, Probazelaiburu II.a tumulua eta Zengotitagane Trabakuatik',
    'alt="Vista panorámica desde la ruta, con el valle cubierto de niebla y las crestas del Duranguesado al fondo"':
        'alt="Bista panoramikoa ibilbidetik, harana lainoz estalita eta Durangaldeko gailurrak atzealdean"',
    'alt="Foto ampliada del recorrido de Iturzuri"': 'alt="Iturzuriko ibilbidearen argazki handitua"',
    'alt="La cascada de Gerena, primera parada de la ruta"':
        'alt="Gerenako ur-jauzia, ibilbideko lehen geldialdia"',
    'alt="Placa del túmulo prehistórico de Probazelaiburu II, el punto más alto de la ruta"':
        'alt="Probazelaiburu II.a historiaurreko tumuluaren plaka, ibilbideko punturik altuena"',
    'alt="Niebla entre los árboles cerca de la cima"': 'alt="Lainoa zuhaitzen artean gailurretik gertu"',
    'alt="El sendero por el cresterio, con los aerogeneradores al fondo"':
        'alt="Bidezidorra gailurrerditik, eolikoak atzealdean"',
    'alt="Restos junto a un aerogenerador cerca de Zengotitagane"':
        'alt="Hondarrak eoliko baten ondoan Zengotitagane inguruan"',
    'Sale de Trabakua hacia el noreste y, tras cuarenta minutos de subida, llega a la primera '
    'parada: la <b>cascada de Gerena</b>. Sigue subiendo hasta la segunda cascada, la de arriba: '
    'ahí, y solo ahí, se cruza el agua para engancharse a un sendero que sube hacia '
    '<a href="https://7pago.com" target="_blank" rel="noopener noreferrer">7 Pago</a>, '
    'escondido entre cipreses y fácil de perder si no se mira bien por dónde sigue. Después de '
    'unos minutos enganchados al sendero, ya es mucho más fácil seguirlo. Ya en la zona de las '
    'siete hayas milenarias que dan nombre a la carrera de montaña de Mallabia, el camino vuelve '
    'a abrirse antes de llegar a la <b>fuente de Iturzuri</b> (km 4,3 · 831 m) —con agua para '
    'llenar cantimploras. Después de la fuente, ya en terreno abierto, aparecen los <b>túmulos de '
    'Iturzuri</b>: el camino gira con fuerza hacia el sureste y gana los últimos metros hasta el '
    'punto más alto de la ruta, el <b>túmulo de Probazelaiburu II</b> (854 m) —un dolmen '
    'prehistórico donde el horizonte se abre entero, con las crestas del Duranguesado '
    'extendiéndose hasta perderse de vista.':
        'Trabakuatik ipar-ekialderantz ateratzen da bidea, eta berrogei minutuko igoera lasaian, '
        'lehen geldialdia agertzen da: <b>Gerenako ur-jauzia</b>. Handik gora jarraitzen da bigarren '
        'ur-jauziraino, goiko aldera. Tarte horretan bakarrik zeharkatzen da ura, '
        '<a href="https://7pago.com" target="_blank" rel="noopener noreferrer">7 Pago</a> aldera '
        'igotzen den bidezidor estu bati heltzeko; altzifreen artean ezkutatuta doa, eta erraz '
        'galtzen da, ondo begiratu ezean. Baina behin bidezidorra hartuta, minutu gutxiren buruan '
        'bidea garbitzen da eta askoz errazagoa da jarraitzea.</p>\n'
        '    <p>Mallabiako mendi-lasterketaren izena ematen duten mila urteko zazpi pagoen inguruan, '
        'bidea berriro zabaltzen da eta <b>Iturzuriko iturrira</b> iristen da (4,3 km · 831 m). '
        'Bertan badago ura kantinplora betetzeko. Iturriaren ondoren, eremu irekian, <b>Iturzuriko '
        'tumuluak</b> agertzen dira: bideak hego-ekialderantz egiten du indarrez, eta azken metroak '
        'irabazita iristen da ibilbideko punturik altuenera, <b>Probazelaiburu II.a tumulura</b> '
        '(854 m). Historiaurreko trikuharri bat da, eta handik zerumuga zabal-zabalik geratzen da, '
        'Durangaldeko gailurrak begi-bistatik galdu arte.',
    'Desde el túmulo, el camino sigue el <b>cresterio</b> hacia el este, con vistas abiertas a '
    'ambos lados de la loma, hasta la cima de <b>Zengotitagane</b> (km 5,6 · 801 m). Desde aquí se '
    'puede bajar directo a Trabakua —el mismo camino que sube la ruta de <a href="oiz.html">'
    'Zengotitagane, Axmakur y Oiz</a>— y acortar bastante el día, o rodear la montaña por el lado '
    'este para quien quiera alargar la ruta un poco más.':
        'Tumulutik, bideak <b>mendi-lerroan</b> jarraitzen du ekialderantz, bizkarraren bi aldeetara '
        'bistak zabal-zabalik, <b>Zengotitagane</b> gailurreraino (5,6 km · 801 m). Hemendik '
        'zuzenean jaits daiteke Trabakuara —<a href="oiz.html">Zengotitagane, Axmakur eta Oiz</a> '
        'ibilbideak igotzen duen bide bera— eta eguna laburtu, edo mendia ekialdetik inguratzen '
        'jarraitu, bira pixka bat gehiago luzatu nahi duenarentzat.',
    'El descenso empieza hacia el sur, por un tramo escondido entre la vegetación que apenas conoce '
    'nadie, hasta una <b>borda abandonada</b> (km 6,1 · 768 m). Ahí el camino gira hacia el este '
    'para rodear la montaña, bajando hasta un <b>refugio de montaña</b> (km 6,6 · 675 m). Desde el '
    'refugio se sigue perdiendo altura hasta casi tocar la carretera general, ya en el barrio de '
    'Osma —pero justo antes de llegar, el camino gira bruscamente y volvemos en dirección norte '
    'hasta enlazar con el camino de ida, ya muy cerca de Trabakua, para cerrar el círculo.':
        'Jaitsiera hegoalderantz hasten da, ia inork ezagutzen ez duen landaretza trinkoaren '
        'artean, <b>borda zahar</b> bateraino (6,1 km · 768 m). Han bideak ekialderantz egiten du '
        'mendia inguratuz, eta <b>mendiko aterpe</b> batera jaisten da (6,6 km · 675 m). '
        'Aterpetik behera jarraitzen du altuera galtzen, errepide nagusia ia ukitu arte, jada Osma '
        'auzoan. Baina iritsi aurretik, bideak bat-batean biratzen du, eta iparralderantz itzultzen '
        'gara joaneko bidearekin berriro lotu arte, Trabakuatik oso gertu, zirkuitua ixteko.',
    '<h2>Senderismo</h2>': '<h2>Oinez</h2>',
    'Sendero de montaña, no apto para bici. Hay dos tramos que exigen ir atentos: el cruce en la '
    'segunda cascada de Gerena para coger el paso hacia 7 Pago, y la bajada sin marcar hacia el sur '
    'desde Zengotitagane. Quien prefiera un día más corto puede bajar directo a Trabakua desde la '
    'cima, sin rodear el lado este. Hay agua en la fuente de Iturzuri (km 4,3), único punto de la '
    'ruta para llenar cantimploras.':
        'Mendiko bidezidorra, ez da bizikletarako egokia. Bi tartek adi ibiltzea eskatzen dute: '
        'Gerenako bigarren ur-jauziko igarobidea 7 Pago alderantz hartzeko, eta Zengotitagatik '
        'hegoalderantz doan markatu gabeko jaitsiera. Egun laburragoa nahi duenak zuzenean jaits '
        'daiteke Trabakuara gailurretik, ekialdea inguratu gabe. Ura dago Iturzuriko iturrian (4,3 '
        'km), ibilbideko kantinplorak betetzeko puntu bakarra.',
}

ZENARRUZA = {
    'download="Zenarruza, San Kristobal y Zengotitagane.gpx"': 'download="Zenarruza, San Kristobal eta Zengotitagane.gpx"',
    '<title>Monasterio de Zenarruza': '<title>Zenarruzako monasterioa',
    '<title>Ermita San Kristobal': '<title>San Kristobal ermita',
    '<title>Dolmen Iturzurigana': '<title>Iturzuriganako trikuharria',
    '<title>Zengotitagane': '<title>Zengotitagane',
    '<span class="num">1</span>Monasterio de Zenarruza': '<span class="num">1</span>Zenarruzako monasterioa',
    '<span class="num">2</span>Ermita San Kristobal': '<span class="num">2</span>San Kristobal ermita',
    '<span class="num">3</span>Dolmen Iturzurigana': '<span class="num">3</span>Iturzuriganako trikuharria',
    '<span>Pista y asfalto</span><span class="sep">/</span><span>Colegiata, ermita y dolmen</span>':
        '<span>Pista eta asfaltoa</span><span class="sep">/</span><span>Kolegiata, ermita eta trikuharria</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    '<h1>Zenarruza, San Kristobal<br><em>y Zengotitagane</em></h1>':
        '<h1>Zenarruza, San Kristobal<br><em>eta Zengotitagane</em></h1>',
    'Monasterio de Zenarruza, Ermita San Kristobal y Zengotitagane desde Trabakua':
        'Zenarruzako monasterioa, San Kristobal ermita eta Zengotitagane Trabakuatik',
    'alt="Atardecer visto desde la Ermita San Kristobal, km 18,6 de la ruta"':
        'alt="Ilunabarra San Kristobal ermitatik ikusita, ibilbideko 18,6 km"',
    'alt="Foto ampliada del recorrido de Zenarruza"': 'alt="Zenarruzako ibilbidearen argazki handitua"',
    'alt="Arroyo entre el bosque durante la subida hacia San Kristobal, km 15,4"':
        'alt="Erreka basoan barrena San Kristobalerako igoeran, 15,4 km"',
    'alt="Luna llena entre las ramas, de vuelta en Trabakua al cierre del circuito"':
        'alt="Ilargi betea adarren artean, Trabakuara itzultzean zirkuitua ixtean"',
    'alt="Vistas desde la zona alta de la ruta, cerca del Oiz (foto de otro d&iacute;a)"':
        'alt="Bistak ibilbidearen goiko aldetik, Oizetik gertu (beste egun bateko argazkia)"',
    'alt="Bicicleta junto a un aerogenerador entre la niebla, cerca de Zengotitagane, km 27,7"':
        'alt="Bizikleta haizezurrutari lotuta lainoetan, Zengotitaganetik gertu, 27,7 km"',
    'alt="Camino forestal cubierto de hojas de oto&ntilde;o, entre &aacute;rboles con las hojas amarillas y verdes"':
        'alt="Basoko bidea udazkeneko hostoz estalita, hosto horiak eta berdeak dituzten zuhaitzen artean"',
    'alt="Escalera de piedra junto a un &aacute;rbol grande, en la Colegiata de Zenarruza"':
        'alt="Harrizko eskailera zuhaitz handi baten ondoan, Zenarruzako kolegiatan"',
    'alt="La Colegiata de Zenarruza vista desde el prado, con el caser&iacute;o anexo y los montes al fondo"':
        'alt="Zenarruzako kolegiata belardi batetik ikusita, ondoko baserriarekin eta mendiak atzealdean"',
    'alt="Aerogeneradores sobre una cresta de monte, con el atardecer entre nubes al fondo"':
        'alt="Haizezurrutariak mendi-gailurraren gainean, ilunabarra hodeien artean atzealdean"',
    'alt="Subida hacia el Oiz, con las antenas de la cima y aerogeneradores a la izquierda, junto a un caser&iacute;o"':
        'alt="Oizerako igoera, gailurreko antenekin eta haizezurrutariak ezkerrean, baserri baten ondoan"',
    'alt="La Ermita San Kristobal junto a los aerogeneradores del parque e&oacute;lico"':
        'alt="San Kristobal ermita, parke eolikoaren haizezurrutarien ondoan"',
    'Sale de Trabakua hacia el norte y, subiendo y bajando por los altos entre Mallabia y '
    'Ziortza-Bolibar, pierde altura de golpe en el &uacute;ltimo tramo hasta el <b>Monasterio de '
    'Zenarruza</b> (km 9,4 &middot; 287 m) &mdash;colegiata cisterciense fundada en el siglo XI, la '
    '&uacute;nica colegiata de Bizkaia y parada hist&oacute;rica del Camino de Santiago del Norte.':
        'Trabakuatik iparralderantz ateratzen da bidea, eta Mallabia eta Ziortza-Bolibar arteko '
        'goialdeetan gora eta behera ibili ondoren, altuera bat-batean galtzen du azken tartean '
        '<b>Zenarruzako monasterioraino</b> (9,4 km &middot; 287 m) &mdash;XI. mendean sortutako '
        'kolegiata zisterziarra, Bizkaiko kolegiata bakarra eta Iparraldeko Donejakue Bidearen '
        'geldialdi historikoa.',
    'Desde el monasterio el camino gira hacia el oeste-suroeste y sube por la ladera del Oiz durante '
    'casi 9 km, ganando m&aacute;s de 500 m de desnivel &mdash;con un buen tramo llano a media subida '
    'para recuperarse, cruzando un arroyo escondido entre el bosque (km 15,4 &middot; 553 m)&mdash; '
    'hasta la '
    '<b>Ermita San Kristobal</b> (km 18,6 &middot; 797 m), antigua ermita-refugio de pastores con '
    'romer&iacute;a el domingo siguiente al 10 de julio.':
        'Monasteriotik, bideak mendebalde-hego-mendebaldera jotzen du eta Oizen hegaletik igotzen '
        'hasten da ia 9 kilometroan zehar, 500 metro baino gehiagoko desnibela irabaziz. Igoeraren '
        'erdian tarte lau polit bat dago indarrak berreskuratzeko, basoan ezkutatutako erreka baten '
        'ondotik pasatuz (15,4 km &middot; 553 m). Handik gora, bideak <b>San Kristobal '
        'ermitaraino</b> eramaten du (18,6 km &middot; 797 m): artzainen ermita-aterpe zaharra, '
        'uztailaren 10aren hurrengo igandean erromeria egiten duena.',
    'Tras la ermita el camino baja hacia el sur hasta un collado a 605 m (km 22,1) para remontar '
    'despu&eacute;s hacia el este, ganando otra vez altura hasta el punto m&aacute;s alto de toda la '
    'ruta: el <b>Dolmen Iturzurigana</b> (km 26,6 &middot; 863 m). Un kil&oacute;metro m&aacute;s al '
    'este, ya dentro del parque e&oacute;lico del Oiz, se corona <b>Zengotitagane</b> (km 27,7 &middot; 822 m).':
        'Ermitatik, bidea hegoalderantz jaisten da 605 metroko lepo bateraino (22,1 km), eta handik '
        'ekialderantz berriro igotzen da, altuera irabaziz ibilbide osoko punturik altuenera: '
        '<b>Iturzuriganako trikuharria</b> (26,6 km &middot; 863 m). Kilometro bat ekialderago, jada '
        'Oizeko parke eolikoaren barruan, <b>Zengotitagane</b> koroatzen da (27,7 km &middot; 822 m).',
    'Desde Zengotitagane el descenso final va hacia el este-sureste, perdiendo los &uacute;ltimos '
    '400 m de desnivel en poco m&aacute;s de 4 km hasta cerrar el c&iacute;rculo de vuelta en '
    'Trabakua. Una ruta larga, para pedalear hasta saciarse.':
        'Zengotitagandik, azken jaitsiera ekialde-hego-ekialderantz doa, azken 400 metroko desnibela '
        'galduz 4 kilometro pasatxotan, Trabakuan zirkuitua ixteko. Ibilbide luzea, baina ederra; '
        'pedalei gustura eragiteko modukoa.',
    '31,7 km y +1.161 m de desnivel en un solo circuito. Sube '
    'casi sin descanso hasta San Kristobal y vuelve a subir despu&eacute;s del collado hasta el '
    'dolmen: dos tirones largos seguidos.':
        '31,7 km eta +1.161 m-ko desnibela zirkuitu bakarrean. Ia '
        'atsedenik gabe igotzen da San Kristobaleraino eta lepoaren ondoren berriro igotzen da '
        'trikuharriraino: bi tirada luze jarraian.',
}

OSMA = {
    'download="Trabakua, Elgeta y Argiñeta.gpx"': 'download="Trabakua, Elgeta eta Argiñeta.gpx"',
    # waypoint names -- one key covers both the elev-legend span and the
    # matching <title> tooltip, since both contain this exact substring.
    'Ermita de San Juan (1&ordf;)': 'San Juan ermita (1.a)',
    'Ermita de Santa Marina': 'Santa Marina ermita',
    'Larrosako Iturri': 'Larrosako Iturri',
    'Ermita de San Juan (2&ordf;)': 'San Juan ermita (2.a)',
    'Necr&oacute;polis de Argi&ntilde;eta': 'Argi&ntilde;etako Nekropolia',
    'Ermita de San Lorenzo (1&ordf;)': 'San Lorentzo ermita (1.a)',
    'Ermita de San Juan Bautista': 'San Juan Bataiatzailea ermita',
    'San Antonio eliza': 'San Antonio eliza',
    'Ermita de San Miguel': 'San Migel ermita',
    'Berriz': 'Berriz',
    'Ermita de San Lorenzo (2&ordf;)': 'San Lorentzo ermita (2.a)',

    '<span>Pista y asfalto</span><span class="sep">/</span><span>Ermitas y necr&oacute;polis medieval</span>':
        '<span>Pista eta asfaltoa</span><span class="sep">/</span><span>Ermitak eta erdi aroko nekropolia</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    '<h1>Trabakua, Elgeta<br><em>y Argi&ntilde;eta</em></h1>':
        '<h1>Trabakua, Elgeta<br><em>eta Argi&ntilde;eta</em></h1>',
    'Circuito desde Trabakua por Osma y la Necr&oacute;polis de Argi&ntilde;eta':
        'Zirkuitua Trabakuatik, Osma eta Argi&ntilde;etako Nekropolitik',

    'alt="Sarc&oacute;fagos medievales de la Necr&oacute;polis de Argi&ntilde;eta, km 20,1 de la ruta"':
        'alt="Erdi Aroko hilobiak Argi&ntilde;etako Nekropolian, ibilbideko 20,1 km"',
    'alt="Foto ampliada del recorrido de Osma"': 'alt="Osmako ibilbidearen argazki handitua"',
    'alt="Presa de Aixola, junto a Larrosako Iturri, km 11,9 de la ruta"':
        'alt="Aixolako presa, Larrosako Iturritik gertu, ibilbideko 11,9 km"',
    'alt="Fila de sarc&oacute;fagos bajo los &aacute;rboles, Necr&oacute;polis de Argi&ntilde;eta"':
        'alt="Hilobi ilara zuhaitzen azpian, Argi&ntilde;etako Nekropolian"',
    'alt="Inscripci&oacute;n epigr&aacute;fica labrada en un sarc&oacute;fago, Necr&oacute;polis de Argi&ntilde;eta"':
        'alt="Hilobi batean landutako inskripzio epigrafikoa, Argi&ntilde;etako Nekropolian"',
    'alt="Sarc&oacute;fagos bajo los robles de la Necr&oacute;polis de Argi&ntilde;eta, con la ermita al fondo"':
        'alt="Argi&ntilde;etako Nekropoliko hilobiak haritzen azpian, ermita atzealdean"',
    'alt="Sarc&oacute;fagos de piedra de la Necr&oacute;polis de Argi&ntilde;eta, entre el c&eacute;sped y los &aacute;rboles"':
        'alt="Harrizko hilobiak Argi&ntilde;etako Nekropolian, belarraren eta zuhaitzen artean"',

    'Esta ruta sale de Trabakua hacia el suroeste, hasta el barrio de Zengotita (km 1,3 &middot; 412 '
    'm), donde se coge la pista forestal que va hacia Areitio y enlaza con el GR &mdash;que va casi '
    'en llano, en paralelo al monte Arietzu&mdash;, camino del barrio de Goierri (km 5,2 &middot; 319 '
    'm), escondido entre robles. Se sigue ganando altura por esa pista hacia el sureste hasta '
    'dejarla, poco antes de la presa de Aixola, para bajar por un tramo de tierra juget&oacute;n hasta '
    'la propia presa &mdash;quien prefiera no perder desnivel puede seguir por la pista principal, '
    'que llega al mismo punto sin bajar. Despu&eacute;s de la presa, ya al empezar a subir hacia '
    'Elgeta, est&aacute; <b>Larrosako Iturri</b> (km 11,9 &middot; 355 m), punto de agua a mitad de '
    'ruta.':
        'Trabakuatik hego-mendebalderantz ateratzen da bidea, Zengotita auzoraino (1,3 km &middot; '
        '412 m), eta han hartzen da Areitiora doan pista forestala, GRarekin lotzen dena &mdash;ia '
        'lauan doa, Arietzu mendia parez pare jarraituz&mdash;, Goierri auzorantz (5,2 km &middot; '
        '319 m), hariztien artean ezkutatuta.</p>\n'
        '    <p>Handik aurrera, pistak hego-ekialderantz egiten du eta altuera irabazten jarraitzen '
        'da, Aixolako presatik gertu pista utzi arte. Tarte horretan, lurrezko jaitsiera jostagarri '
        'bat dago presaraino &mdash;desnibela galdu nahi ez duenak pista nagusitik jarrai dezake, '
        'puntu berera iristen baita. Presaren ondoren, Elgetarantz igotzen hasten denean, '
        '<b>Larrosako Iturria</b> dago (11,9 km &middot; 355 m), ibilbidearen erdiko ur-puntua.',
    'Desde ah&iacute; sigue subiendo hasta Elgeta, ya en el Duranguesado, y contin&uacute;a entre '
    'curvas '
    'por un tramo '
    'de asfalto hasta el cruce de bajada hacia Elorrio, por el barrio Aldape, antes de bajar de golpe '
    '(km 18,8 &middot; '
    '286 m). Kil&oacute;metro y medio '
    'despu&eacute;s gira hacia el noroeste hasta la <b>Necr&oacute;polis de Argi&ntilde;eta</b> (km '
    '20,1 &middot; 247 m): una veintena de sarc&oacute;fagos de '
    'piedra y cinco estelas labradas en piedra del Oiz, de los siglos VII a IX &mdash;entre la '
    'epigraf&iacute;a cristiana m&aacute;s antigua encontrada en Bizkaia, Bien de Inter&eacute;s '
    'Cultural desde 1931. Las tumbas, repartidas originalmente por distintos barrios de Elorrio, se '
    'agruparon aqu&iacute; en el siglo XIX por orden del p&aacute;rroco Retolaza. Hay tambi&eacute;n '
    'una fuente junto a la necr&oacute;polis para llenar cantimploras.':
        'Handik gora, bideak Elgetara igotzen jarraitzen du, Durangaldeko sarreran, eta bihurgune '
        'artean jarraitzen du asfalto-tarte batean zehar, Aldape auzotik Elorrio aldera jaisten den '
        'bidegurutzera iritsi arte (18,8 km &middot; 286 m).</p>\n'
        '    <p>Kilometro eta erdi geroago, bideak ipar-mendebalderantz egiten du <b>Argi&ntilde;etako '
        'Nekropolira</b> iristeko (20,1 km &middot; 247 m): hogei bat harri-sarkofago eta bost '
        'estela, Oizko harrian landuak, VII&ndash;IX. mendekoak &mdash;Bizkaian aurkitutako epigrafia '
        'kristau zaharrenetakoak, Kultura Ondasun izendatuak 1931tik. Tumbak, jatorriz Elorrioko '
        'auzo desberdinetan sakabanatuta zeudenak, XIX. mendean bildu ziren hemen, Retolaza '
        'parrokoaren aginduz. Nekropoliaren ondoan iturri bat dago kantinplorak betetzeko.',
    'Desde ah&iacute; sigue subiendo hacia el barrio de Mendraca, donde el paisaje se abre en una '
    'panor&aacute;mica amplia hacia Elorrio y varias cumbres, como el Udalaitz, y el camino deja el '
    'asfalto por sendero y pista de tierra (km 22,4 &middot; 312 m). Pasa por <b>San Juan Bautista de '
    'Murgoitio</b> (km 24,3 &middot; 277 m) &mdash;con registros del siglo XVII de tumbas dobles nunca '
    'excavadas, similares a las de Argi&ntilde;eta&mdash; y por el barrio de Olakueta (km 25,8 '
    '&middot; 160 m), donde se pierde altura de golpe. Gira despu&eacute;s '
    'hacia el este, bordeando Zaldibar sin entrar en el pueblo, para subir hasta la <b>Ermita de San '
    'Miguel de Okango</b> (km 28,4 &middot; 227 m), patrona del barrio y con fiestas el 29 de '
    'septiembre entre bolos y morcilla, y baja de nuevo hasta <b>Berriz</b> (km 30,7 &middot; 187 m), '
    'en el valle del Ibaizabal, al pie del Oiz.':
        'Handik gora, bideak Mendraca auzorantz igotzen jarraitzen du, eta paisaia zabaltzen da '
        'Elorrio eta inguruko gailurretara &mdash;tartean Udalaitz&mdash;. Bideak asfaltoa uzten du '
        'bidezidor eta lur-pista bihurtzeko (22,4 km &middot; 312 m). Aurrerago, <b>San Juan '
        'Bautista de Murgoitio</b> (24,3 km &middot; 277 m) igarotzen da &mdash;XVII. mendeko '
        'hilobi bikoitz dokumentatuak ditu, inoiz induskatu ez direnak, Argi&ntilde;etakoen '
        'antzekoak&mdash; eta Olakueta auzotik pasatzen da (25,8 km &middot; 160 m), non altuera '
        'galera handia dago.</p>\n'
        '    <p>Ondoren, bideak ekialderantz egiten du, Zaldibar ingurutik herrira sartu gabe, eta '
        '<b>Okangoko San Migel ermitaraino</b> igotzen da (28,4 km &middot; 227 m), auzoko '
        'zaindaria, irailaren 29an ospatzen diren festekin (bolo-jokoa eta odolkia). Handik berriro '
        'jaisten da <b>Berrizera</b> (30,7 km &middot; 187 m), Ibaizabal ibaiaren haranean, Oiz '
        'mendiaren oinean.',
    'Ya de vuelta, pasa por el barrio de San Lorenzo (Mend&iacute;bil-Sallobente) (km 32,1 &middot; '
    '264 m), antes de subir sin parar los &uacute;ltimos 4,7 km y 143 m de '
    'desnivel de vuelta hasta Trabakua, para cerrar el c&iacute;rculo.':
        'Bueltan, bideak San Lorentzo auzotik igarotzen da (Mend&iacute;bil-Sallobente) (32,1 km '
        '&middot; 264 m), eta azken 4,7 km-etan eta 143 m-ko desnibelean etenik gabe igotzen da '
        'berriro Trabakuara, zirkuitua ixteko.',

    '<p>36,8 km y +1.002 m de desnivel en un solo circuito, entre ermitas y caser&iacute;os del '
    'Duranguesado. Hay agua en Larrosako Iturri (km 11,9) y '
    'junto a la Necr&oacute;polis de Argi&ntilde;eta (km 20,1).</p>':
        '<p>36,8 km eta +1.002 m-ko desnibela zirkuitu bakarrean, Durangaldeko ermita eta baserrien '
        'artean. Ura dago Larrosako Iturrin (11,9 km) eta Argi&ntilde;etako '
        'Nekropolitik gertu (20,1 km).</p>',
}

GEREA = {
    '<title>Primera señal, empiezan las vistas':
        '<title>Lehen seinalea, ikuspegiak hasten dira',
    '<span class="num">1</span>Primera señal, empiezan las vistas':
        '<span class="num">1</span>Lehen seinalea, ikuspegiak hasten dira',
    '<span>Sendero</span><span class="sep">/</span><span>Cascada, aerogeneradores y borda</span>':
        '<span>Bidezidorra</span><span class="sep">/</span><span>Ur-jauzia, eolikoak eta borda</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    'Circuito a la cascada de Gerea desde Trabakua':
        'Zirkuitua Trabakuatik Gereako ur-jauzira',
    'alt="Ur Jauziak, la cascada escalonada de Gerea, con el agua bajando entre las rocas"':
        'alt="Ur Jauziak, Gereako ur-jauzi mailakatua, ura harrien artetik jaisten"',
    'alt="Foto ampliada del recorrido de Ur Jauziak-Gerea"':
        'alt="Ur Jauziak-Gerea ibilbidearen argazki handitua"',
    'alt="Cartel de madera del recorrido, con indicaciones a Ur Jauzia y a Trabakua"':
        'alt="Ibilbidearen egurrezko kartela, Ur Jauziarako eta Trabakuarako seinaleekin"',
    'alt="Aerogeneradores del parque eólico del Oiz vistos desde la ruta"':
        'alt="Oizeko parke eolikoaren aerosorgailuak ibilbidetik ikusita"',
    'alt="Sendero junto a una borda abandonada de tejado rojo, con los aerogeneradores al fondo"':
        'alt="Bidezidorra borda abandonatu baten ondoan, teilatu gorriarekin, eolikoak '
        'atzealdean"',
    'alt="Ur Jauziak en otoño, con el agua cayendo entre musgo y rocas"':
        'alt="Ur Jauziak udazkenean, ura goroldio eta harrien artetik erortzen"',
    'alt="Vistas al barrio de Gerea desde la subida, entre caseríos y montañas"':
        'alt="Gereako auzorako ikuspegiak igoeratik, baserrien eta mendien artean"',
    'alt="Ur Jauziak en diciembre, con el agua cayendo con fuerza entre las rocas"':
        'alt="Ur Jauziak abenduan, ura indarrez harrien artetik erortzen"',
    'Esta ruta sale de Trabakua y sube marcada en parte con pintadas verdes y blancas. Tras unos '
    '40 minutos de subida llega la primera parada: <b>Ur Jauziak</b>, una cascada escalonada '
    'entre rocas y musgo. En invierno el caudal es impresionante; en verano baja mucho y se '
    'queda con poca agua y mucho musgo —sigue siendo bonita, pero merece más la pena el resto '
    'del año.':
        'Ibilbide honek Trabakuatik irten eta gora egiten du, tarte batean berde eta zuriz '
        'margotutako marken bidez seinalizatuta. Berrogei bat minutuko igoeraren ondoren, lehen '
        'geldialdia dator: <b>Ur Jauziak</b>, harri eta goroldio artean mailaka jaisten den '
        'ur-jauzia. Neguan emaria ikaragarria da; udan asko jaisten da eta ur gutxirekin eta '
        'goroldio askorekin geratzen da —hala ere polita da, baina gainerako urte-sasoietan '
        'merezi du gehiago.',
    'Los aerogeneradores del parque eólico del Oiz acompañan casi toda la subida a un lado, con '
    'vistas al barrio de Gerea al otro, y de camino se pasa junto a una borda abandonada, de '
    'tejado rojo medio hundido entre la maleza. El camino sigue subiendo hasta el punto más '
    'alto de la ruta, a 686 m (km 2,95). La subida coincide en gran parte con el recorrido de '
    'la <a href="https://7pago.com" target="_blank" rel="noopener noreferrer">7 Pago Mendi '
    'Lasterketa</a>, la carrera de montaña que se celebra en mayo.':
        'Oizeko parke eolikoaren aerosorgailuek igoera ia osoan egiten dute konpainia alde '
        'batetik, eta bestetik Gereako auzorako ikuspegiak zabaltzen dira, borda abandonatu '
        'baten ondotik pasatuz —teilatu gorri erdi hondoratua sasien artean. Bideak gora '
        'jarraitzen du ibilbideko punturik altuenera iritsi arte, 686 metrotara (2,95 km). '
        'Igoera honek bat egiten du neurri handi batean <a href="https://7pago.com" '
        'target="_blank" rel="noopener noreferrer">7 Pago Mendi Lasterketa</a>ren '
        'ibilbidearekin, maiatzean ospatzen den mendi lasterketa.',
    'Desde ahí empieza el descenso, con varios cruces de caminos seguidos donde conviene ir '
    'atento a la traza del GPS, antes de cerrar el círculo de vuelta a Trabakua.':
        'Handik jaitsiera hasten da, hainbat bide-gurutze jarraian dituela, GPSaren trazari adi '
        'egon behar zaiona, Trabakuara itzuliz zirkulua itxi aurretik.',
    '<h2>Senderismo</h2>': '<h2>Oinez</h2>',
    'Ruta válida para todos los niveles, niños mayores incluidos: 5,7 km y +415 m de desnivel '
    'en un solo circuito, con un buen tramo de subida (unos 40 min) hasta la cascada, con los '
    'aerogeneradores de compañía casi todo el camino. No está señalizada oficialmente más allá '
    'de esas pintadas verdes y blancas, así que conviene llevar el track cargado.':
        'Maila guztietarako baliozko ibilbidea, haur nagusiak barne: 5,7 km eta +415 m-ko '
        'desnibela zirkuitu bakarrean, igoera-tarte on batekin (40 bat minutu) ur-jauziraino, '
        'eolikoak lagun ia bide osoan. Ez dago ofizialki seinalizatuta pintura berde eta '
        'zuri horiez haratago, beraz komeni da tracka kargatuta eramatea.',
}

ZENGOTITAGANE = {
    'download="Zengotitagane, Iturzurigana y San Cristóbal Txiki.gpx"': 'download="Zengotitagane, Iturzurigana eta San Kristobal Txiki.gpx"',
    'alt="Foto ampliada del recorrido de Zengotitagane"':
        'alt="Zengotitagane ibilbidearen argazki handitua"',
    '<span>Carretera y pista</span><span class="sep">/</span>'
    '<span>Zengotitagane, Iturzurigana y ermitas</span>':
        '<span>Errepidea eta pista</span><span class="sep">/</span>'
        '<span>Zengotitagane, Iturzurigana eta ermitak</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    '<h1>Zengotitagane, Iturzurigana<br><em>y San Crist&oacute;bal Txiki</em></h1>':
        '<h1>Zengotitagane, Iturzurigana<br><em>eta San Kristobal Txiki</em></h1>',
    'Circuito desde Trabakua, con las ermitas de San Crist&oacute;bal Txiki y San Juan':
        'Zirkuitua Trabakuatik, San Kristobal Txiki eta San Juan ermitekin',
    'alt="Vistas hacia el Anboto y el Alluitz, con Durango al fondo, desde lo alto de la ruta"':
        'alt="Anboto eta Alluitzerako ikuspegiak, Durango atzealdean, ibilbidearen goialdetik"',
    'alt="V&eacute;rtice geod&eacute;sico en Iturzurigana, el punto m&aacute;s alto de la ruta, '
    'con vistas alrededor"':
        'alt="Vertize geodesikoa Iturzuriganan, ibilbideko punturik altuenean, inguruko '
        'ikuspegiekin"',
    'alt="Una cruz en uno de los altos de la ruta, con el valle y una carretera al fondo"':
        'alt="Gurutze bat ibilbideko goi batean, harana eta errepidea atzealdean"',
    'alt="Aerogeneradores en fila sobre una cresta de monte, con un cielo tormentoso al fondo"':
        'alt="Eoliko ilara mendi-gailurraren gainean, zeru ekaiztsua atzealdean"',
    'Salimos de Trabakua en direcci&oacute;n Osma por carretera. Algo m&aacute;s de 2 km '
    'despu&eacute;s giramos a la derecha para coger la pista que sube hasta <b>Zengotitagane</b> '
    '(km 3,7, 820 m), entre los aerogeneradores del parque e&oacute;lico. Las rampas son muy '
    'duras, casi imposibles de subir con una bici normal &mdash;aunque en sentido contrario, '
    'con esta subida convertida en bajada, s&iacute; se puede hacer la ruta con una bici '
    'normal.':
        'Trabakuatik irten eta Osma norabidean egiten dugu errepidez. 2 km pasatxo geroago '
        'eskuinera jotzen dugu, <b>Zengotitagane</b>raino (3,7 km, 820 m) igotzen duen pista '
        'hartzeko, parke eolikoaren aerosorgailuen artean. Maldak oso gogorrak dira, ia '
        'ezinezkoak bizikleta arrunt batekin igotzeko &mdash;alderantzizko norabidean, ordea, '
        'igoera hori jaitsiera bihurtuta, bai egin daiteke ibilbidea bizikleta arrunt batekin.',
    'Tras Zengotitagane seguimos por la cresta, con vistas a los dos lados &mdash;especialmente '
    'bonitas hacia <b>Iturzurigana</b> (km 4,8, 859 m), el punto m&aacute;s alto de la ruta. '
    'Quien quiera coger agua puede desviarse unos metros a la derecha.':
        'Zengotitagane igaro ondoren gailurraren bidetik jarraitzen dugu, bi aldeetara '
        'ikuspegiekin &mdash;bereziki ederrak <b>Iturzurigana</b>rantz (4,8 km, 859 m), '
        'ibilbideko punturik altuena. Ura hartu nahi duenak eskuinera desbideratu ditzake '
        'metro batzuk.',
    'Empieza entonces la bajada hacia Garai, primero por una pista de cemento y despu&eacute;s '
    'por una de piedra, con un canal de agua acompa&ntilde;ando el camino. Poco despu&eacute;s '
    'giramos a la izquierda para encarar una pista trialera corta pero intensa, hasta '
    'enganchar con la pista de piedra que sube desde Garai hasta la fuente de arriba, en lo '
    'alto. Desde ah&iacute; empezamos a bajar hasta la <b>Ermita de San Crist&oacute;bal '
    'Txiki</b> (km 15,4, 495 m) &mdash;as&iacute; se conoce, para distinguirla de la otra '
    'Ermita de San Crist&oacute;bal, la de arriba, junto a los aerogeneradores.':
        'Orduan hasten da Garairako jaitsiera, lehenengo zementuzko pista batetik eta gero '
        'harrizko batetik, ur-kanal batek bidea lagunduta. Handik pixka batera ezkerrera '
        'jotzen dugu, trial-pista labur baina bizi bati aurre egiteko, Garaitik igotzen den '
        'harrizko pistarekin lotu arte, goiko iturriraino, goi-goian. Handik behera hasten '
        'gara <b>San Kristobal Txiki ermita</b>raino (15,4 km, 495 m) &mdash;horrela ezagutzen '
        'da, eolikoen ondoan dagoen beste San Kristobal ermitatik bereizteko.',
    'Continuamos a toda velocidad cuesta abajo hasta el barrio de San Jos&eacute;. Cruzamos la '
    'carretera general entre Trabakua y Berriz y subimos por la carretera vieja hacia el '
    'barrio de Zengotita, donde est&aacute; la <b>Ermita de San Juan</b> (km 19,6, 400 m), ya '
    'cerca de cerrar el c&iacute;rculo, antes de bajar de vuelta a Trabakua.':
        'Abiadura betean jarraitzen dugu behera San Jos&eacute; auzoraino. Trabakua eta Berriz '
        'arteko errepide nagusia gurutzatzen dugu eta errepide zaharretik gora egiten dugu '
        'Zengotita auzorantz, non dagoen <b>San Juan ermita</b> (19,6 km, 400 m), zirkulua '
        'ixteko zorian, Trabakura jaitsi aurretik.',
    '22,4 km y +1.029 m de desnivel en un solo circuito, con rampas muy duras nada m&aacute;s '
    'salir hacia Zengotitagane &mdash;casi imposibles de subir con una bici normal en este '
    'sentido. Hay '
    'agua cerca de Iturzurigana (km 4,8) y en la zona de Garai, antes de la Ermita de San '
    'Crist&oacute;bal Txiki.':
        '22,4 km eta +1.029 m-ko desnibela zirkuitu bakarrean, malda oso gogorrekin '
        'Zengotitaganerako irteeran bertan &mdash;ia ezinezkoak bizikleta arrunt batekin '
        'igotzeko norabide honetan. Ura badago Iturzuriganatik gertu (4,8 km) eta Garaiko aldean, '
        'San Kristobal Txiki ermitaren aurretik.',
    'Ermita de San Crist&oacute;bal Txiki': 'San Kristobal Txiki ermita',
    'Ermita de San Juan': 'San Juan ermita',
}

OIZ = {
    'download="Zengotitagane, Axmakur y Oiz.gpx"': 'download="Zengotitagane, Axmakur eta Oiz.gpx"',
    'alt="Foto ampliada del recorrido del Oiz"':
        'alt="Oizeko ibilbidearen argazki handitua"',
    '<span>Sendero</span><span class="sep">/</span><span>Zengotitagane, Axmakur y Oiz</span>':
        '<span>Bidezidorra</span><span class="sep">/</span><span>Zengotitagane, Axmakur eta Oiz</span>',
    '<span>Ida y vuelta</span></p>': '<span>Joan-etorria</span></p>',
    '<h1>Zengotitagane, Axmakur<br><em>y Oiz</em></h1>':
        '<h1>Zengotitagane, Axmakur<br><em>eta Oiz</em></h1>',
    'Ida y vuelta desde Trabakua hasta el Oiz':
        'Joan-etorria Trabakuatik Oizeraino',
    'alt="Aerogeneradores del Oiz reflejados en un charco de la cumbre, con las antenas al fondo"':
        'alt="Oizeko eolikoak gailurreko putzu batean islatuta, antenak atzealdean"',
    'alt="Vistas panor&aacute;micas desde el Oiz, con los aerogeneradores y el sol de frente"':
        'alt="Oizetiko ikuspegi panoramikoak, eolikoekin eta eguzkia aurrez aurre"',
    'alt="V&eacute;rtice geod&eacute;sico en el Oiz de noche, con las luces rojas de los '
    'aerogeneradores al fondo"':
        'alt="Vertize geodesikoa Oizen gauez, eolikoen argi gorriak atzealdean"',
    'alt="Atardecer en el Oiz, con la silueta de los aerogeneradores en la cresta"':
        'alt="Ilunabarra Oizen, eolikoen silueta gailur-gerrikoan"',
    'alt="Un reba&ntilde;o de camino al Oiz de noche, con las luces de un pueblo al fondo"':
        'alt="Artalde bat Oizerako bidean gauez, herri baten argiak atzealdean"',
    'alt="Un aerogenerador del Oiz recortado contra la luna, al anochecer"':
        'alt="Oizeko eoliko bat ilargiaren kontra, ilunabarrean"',
    'alt="Atardecer rojizo desde el Oiz"':
        'alt="Ilunabar gorrixka Oiztik"',
    'alt="Caballo junto a una charca de piedras en la cima del Oiz"':
        'alt="Zaldia Oizko gailurreko harrizko putzu baten ondoan"',
    'Salimos de Trabakua y subimos hasta <b>Zengotitagane</b> (km 2,1, 810 m) &mdash;una '
    'subida muy fuerte, aunque corta, casi recta, que sale arriba entre el segundo y el '
    'tercer aerogenerador. A partir de ah&iacute;, hacia el Oiz, la pendiente se '
    'suaviza mucho y se hace muy llevadero.':
        'Trabakua atzean utzita, bidea berehala hasten da gora. Lehen helburua '
        '<b>Zengotitagane</b> da (2,1 km &middot; 810 m), eta tarte horretan igoera oso '
        'zuzena eta gogorra da: laburra izan arren, gorputzak berehala nabaritzen du aldapa. '
        'Gailurrera iristen gara bigarren eta hirugarren haize-errotaren artean, eta hortik '
        'aurrera Oiz aldera dena da lasaiago; maldak leuntzen dira eta aurrera egitea '
        'errazagoa da.',
    'Continuamos por la cresta, con unas vistas preciosas a ambos lados, hasta meternos en '
    'el hayedo que nos lleva a la fuente de Iturzuri; tras cruzarlo, se ve un refugio a un '
    'lado, aunque no pasamos por &eacute;l.':
        'Aurrera jarraitzen dugu mendi-lerroan, bi aldeetara zabaltzen diren ikuspegi '
        'zabalekin. Pixkanaka pago artean sartzen gara, tarte atsegin batean, eta horrek '
        'eramaten gaitu Iturzuriko iturrira. Iturria atzean utzita, aterpe bat ikusten da '
        'alde batean, nahiz eta ibilbideak ez duen bertatik pasatzen.',
    '<b>Axmakur</b> (km 4, 888 m) viene justo despu&eacute;s de la fuente, un repecho de la '
    'cresta conectado con el propio Oiz, con vistas hacia el Duranguesado, Urdaibai y Bilbao.':
        'Handik gertu dator <b>Axmakur</b> (4 km &middot; 888 m), goragune txiki baina polit '
        'bat, Oiz mendiarekin lotuta. Hemendik ikuspegi zabalak irekitzen dira: Durangaldea, '
        'Urdaibai, eta eguna garbi badago, Bilbo ere bai.',
    'La cresta cumbrera del <b>Oiz</b> (km 5,69, 1.025 m) est&aacute; ocupada por antenas y '
    'uno de los parques e&oacute;licos m&aacute;s extensos de Bizkaia &mdash;el primero que '
    'se instal&oacute; en el territorio. Desde ah&iacute; hay vistas a la costa '
    'cant&aacute;brica y, en d&iacute;as claros, hasta los Pirineos. Es uno de los montes '
    '&laquo;bocineros&raquo; de Bizkaia, usados antiguamente para convocar reuniones con el '
    'sonido de una bocina que cruzaba los valles.':
        'Aurrerago iristen gara <b>Oiz</b>ko goialdera (5,69 km &middot; 1.025 m). Antenak '
        'eta Bizkaiko parke eoliko handienetako bat daude bertan &mdash;lurraldean jarri zen '
        'lehenengoa. Tontorretik Kantauri itsasoa ikusten da, eta egun garbi-garbian, '
        'Pirinioak ere bai. Oiz da Bizkaiko mendi &laquo;bozinari&raquo;etako bat: garai '
        'batean, bozina baten soinua haranetan zehar zabaltzen zen biltzarrak deitzeko.',
    'La vuelta es por el mismo camino, de vuelta a Trabakua.':
        'Bueltarako, bide bera hartzen dugu, pago artean berriro jaitsiz, Trabakuara '
        'itzultzeko. Ibilbide osoa azkarra, argia eta paisaiaren poderioz oso gozagarria da.',
    '<h2>Senderismo</h2>': '<h2>Oinez</h2>',
    '11,1 km y +752 m de desnivel en una ruta de ida y vuelta, con dos altos de camino '
    '(Zengotitagane y Axmakur) antes de coronar el Oiz (1.025 m).':
        '11,1 km eta +752 m-ko desnibela joan-etorriko ibilbide batean, bidean bi goirekin '
        '(Zengotitagane eta Axmakur) Oiz gailurreratu aurretik (1.025 m).',
    'Ida y vuelta &mdash; el mismo camino de ida y de vuelta':
        'Joan-etorria &mdash; bide bera joan eta etorrian',
}

ARIETZU = {
    'download="Osmagain y Arietzu.gpx"': 'download="Osmagain eta Arietzu.gpx"',
    'alt="Foto ampliada del recorrido de Arietzu"':
        'alt="Arietzuko ibilbidearen argazki handitua"',
    '<span>Sendero</span><span class="sep">/</span><span>Osmagain y Arietzu</span>':
        '<span>Bidezidorra</span><span class="sep">/</span><span>Osmagain eta Arietzu</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    '<h1>Osmagain<br><em>y Arietzu</em></h1>': '<h1>Osmagain<br><em>eta Arietzu</em></h1>',
    'Circuito desde la Ermita de San Juan': 'Zirkuitua San Juan ermitatik',
    'alt="Vista del valle desde la ruta, con caser&iacute;os, un prado con caballos y una '
    'pista serpenteando entre los montes"':
        'alt="Haranaren ikuspegia ibilbidetik, baserriekin, zaldiak dituen larre batekin '
        'eta mendien artean bihurgunez betetako pista batekin"',
    'alt="Una cruz en uno de los altos de la ruta, entre hierba seca y con vistas a un '
    'monte al fondo"':
        'alt="Gurutze bat ibilbideko goi batean, belar lehorren artean eta mendi bat '
        'atzealdean ikusten dela"',
    'alt="El sendero subiendo entre hierba hacia una loma con &aacute;rboles"':
        'alt="Bidezidorra belar artetik igotzen, arbolez betetako muino batera"',
    'alt="Una cruz de piedra entre pinos, en uno de los altos de la ruta"':
        'alt="Harrizko gurutze bat pinuen artean, ibilbideko goi batean"',
    'alt="El sendero entre musgo y helechos, en un tramo de bosque"':
        'alt="Bidezidorra goroldio eta iratzeen artean, baso-tarte batean"',
    'alt="Una cruz de piedra con vistas al valle y a un monte al fondo, en verano"':
        'alt="Harrizko gurutze bat haranerako eta atzealdeko mendi baterako ikuspegiekin, '
        'udan"',
    'data-marker-title="Ermita de San Juan (salida y llegada)"':
        'data-marker-title="San Juan ermita (irteera eta helmuga)"',
    '<span class="v">Ermita de San Juan</span>': '<span class="v">San Juan ermita</span>',
    'Circuito corto desde la Ermita de San Juan, en el barrio de Zengotita, hasta '
    '<b>Osmagain</b> (km 0,7, 527 m), con una cruz en el alto y muy buenas vistas desde el '
    'cresterío: hacia Berriz y los montes del Duranguesado a un lado, hacia los barrios de '
    'Zengotita y Osma al otro. Este tramo coincide con parte del recorrido de la <a '
    'href="https://7pago.com" target="_blank" rel="noopener noreferrer">7 Pago Mendi '
    'Lasterketa</a>, la carrera de montaña que se celebra en mayo.':
        'Zirkuitu laburra San Juan ermitatik, Zengotita auzoan, <b>Osmagain</b>eraino '
        '(0,7 km, 527 m), goian gurutze batekin eta ikuspegi bikainekin gailurrerditik: '
        'Berriz eta Durangaldeko mendiak alde batetik, eta bestetik Zengotita eta Osma '
        'auzoak. Ibilbidearen zati hau <a href="https://7pago.com" target="_blank" '
        'rel="noopener noreferrer">7 Pago Mendi Lasterketa</a>ren zatia da, maiatzean '
        'ospatzen den mendi lasterketa.',
    'El cresterío sigue hasta <b>Arietzu</b> (km 2,2, 479 m), otra cruz de piedra entre '
    'pinos, antes de cerrar el círculo de vuelta a la ermita.':
        'Gailurrerdiak <b>Arietzu</b>raino jarraitzen du (2,2 km, 479 m), harrizko beste '
        'gurutze bat pinuen artean, ermitara bueltan zirkulua itxi aurretik.',
    '<h2>Senderismo</h2>': '<h2>Oinez</h2>',
    '4,3 km y +235 m de desnivel en un circuito corto, apta para ni&ntilde;os, con dos altos '
    'de camino (Osmagain y Arietzu).':
        '4,3 km eta +235 m-ko desnibela zirkuitu laburrean, haurrentzat egokia, bidean bi '
        'goirekin (Osmagain eta Arietzu).',
    '<b>&middot; Ermita de San Juan</b>': '<b>&middot; San Juan ermita</b>',
}

URKO = {
    'download="Trabakua, Asuntza y Urko.gpx"': 'download="Trabakua, Asuntza eta Urko.gpx"',
    'alt="Foto ampliada del recorrido de Trabakua, Asuntza y Urko"':
        'alt="Trabakua, Asuntza eta Urko ibilbidearen argazki handitua"',
    '<h1>Trabakua, Asuntza<br><em>y Urko</em></h1>':
        '<h1>Trabakua, Asuntza<br><em>eta Urko</em></h1>',
    'alt="V&eacute;rtice geod&eacute;sico en la cumbre del Urko, con nubes bajas y las '
    'monta&ntilde;as del entorno al fondo"':
        'alt="Urkoko gailurreko bertize geodesikoa, hodei baxuekin eta inguruko '
        'mendiak atzealdean"',
    '<span>Sendero</span><span class="sep">/</span><span>Arandomendi, Urko y Collado de Asuntza</span>':
        '<span>Bidezidorra</span><span class="sep">/</span><span>Arandomendi, Urko eta '
        'Asuntzako lepoa</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    'Circuito desde Trabakua, por Arandomendi, Urko y el Collado de Asuntza':
        'Zirkuitua Trabakuatik, Arandomendi, Urko eta Asuntzako lepotik',
    '<title>Collado de Asuntza': '<title>Asuntzako lepoa',
    '<span class="num">3</span>Collado de Asuntza': '<span class="num">3</span>Asuntzako lepoa',
    'alt="Nubes bajas en el valle, con el hayedo en tonos de oto&ntilde;o en primer plano"':
        'alt="Hodei baxuak haranean, pagadia udazkeneko koloreetan aurrean"',
    'alt="Niebla llenando el valle entre las crestas, con estelas de aviones en el cielo"':
        'alt="Lainoak harana betetzen gailurren artean, hegazkinen aztarnekin zeruan"',
    'alt="Amanecer entre estelas de aviones, con nubes bajas cubriendo el valle"':
        'alt="Egunsentia hegazkinen aztarnen artean, hodei baxuek harana estaltzen dutela"',
    'alt="Vista panorámica de las montañas del entorno bajo un cielo despejado, con caseríos y prados en el valle en primer plano"':
        'alt="Inguruko mendien ikuspegi panoramikoa zeru garbi baten azpian, baserriak eta larreak haranean lehen planoan"',
    'alt="Poste de señales y mojón en la cima, con el mar al fondo entre nubes bajas"':
        'alt="Seinaleztapen-zutoina eta mugarria gailurrean, itsasoa atzealdean hodei baxuen artean"',
    'alt="Ovejas y vacas pastando en un prado, con un montón de estiércol y un caserío al fondo"':
        'alt="Ardiak eta behiak larre batean bazkan, simaur-pila batekin eta baserri bat atzealdean"',
    'Se sale desde el Alto de Trabakua. Los primeros metros bajan &mdash;poco m&aacute;s de '
    'un kil&oacute;metro&mdash; hasta un cruce a la izquierda donde se deja el asfalto '
    'atr&aacute;s y empieza una cuesta que por un momento se pone intensa, pero corta; '
    'una vez arriba vemos las indicaciones para el monte Mendibil, entre otras. Desde '
    'ah&iacute;, todo es pista en solitario, alternando cemento y tramos de piedra. Lo '
    'que viene despu&eacute;s se lleva mejor, y el camino ondula entre subidas y bajadas '
    'suaves, hasta llegar a Asuntza.':
        'Trabakuako Altoan hasten gara. Lehen metroek behera egiten dute, kilometro bat '
        'pasatxo, ezkerrerako bidegurutze batera iritsi arte. Han asfaltua uzten dugu, eta '
        'berehala hasten da aldapa: momenturen batean gogortu egiten da, baina laburra da. '
        'Goiko puntura iristean, Mendibilerako seinaleak ageri dira, eta horrek ematen dio '
        'ibilbideari mendiko giroa. Handik aurrera, pista hutsa da, tarteka zementua, '
        'tarteka harria. Ondorengoa eramangarriagoa da, eta bidea uhinka doa, igoera eta '
        'jaitsiera leunen artean, Asuntzara iritsi arte.',
    'Por el camino coronamos <b>Arandomendi</b> (km 6,4 &middot; 686 m), donde la '
    'pendiente da un respiro durante el siguiente kil&oacute;metro, antes de atacar la '
    'cuesta final hacia la cumbre del Urko.':
        'Bidean <b>Arandomendi</b> (6,4 km &middot; 686 m) koronatzen dugu. Gailur horrek '
        'arnasa hartzeko tartea ematen du hurrengo kilometroan, eta gorputzak eskertzen '
        'du, Urkoko azken aldapa gogorrari ekin aurretik.',
    'Poco despu&eacute;s llegamos al punto m&aacute;s alto de la ruta, <b>Urko</b> (km 8, '
    '785 m), con su v&eacute;rtice geod&eacute;sico y vistas a las monta&ntilde;as del '
    'entorno. Es el punto m&aacute;s alto de los municipios de Ermua y Eibar, y su cumbre '
    'marca la frontera entre Bizkaia y Gipuzkoa.':
        'Handik gutxira iristen gara ibilbideko punturik altuenera: <b>Urko</b> (8 km '
        '&middot; 785 m). Bertan dago bertize geodesikoa, eta inguruko mendietara '
        'zabaltzen diren ikuspegi zabalak. Urko da Ermua eta Eibar udalerrien punturik '
        'altuena, eta bere gailurrak Bizkaia eta Gipuzkoaren arteko muga markatzen du. '
        'Gailurrean beti sentitzen da zerbait berezia: haizea, isiltasuna, eta ingurua '
        'begiratzeko gogoa.',
    'Bajamos por un bonito tramo de cresta hasta el <b>Collado de Asuntza</b> (km 10,8 '
    '&middot; 490 m), que separa el Urko del monte Mendibil (613 m), y cogemos la misma '
    'pista de la Asuntza, antes de remontar de nuevo hacia Trabakua.':
        'Gailurretik kresta polit batetik jaisten gara <b>Asuntzako lepo</b>ra (10,8 km '
        '&middot; 490 m), Urko eta Mendibil (613 m) bereizten dituen tartera. Lepoan '
        'pista hartzen dugu berriro, Asuntzako bidea bera, eta hortik Trabakuarantz '
        'igotzen hasten gara, ibilbideari buelta emateko.',
    '<h2>Senderismo</h2>': '<h2>Oinez</h2>',
    '15,3 km y +873 m de desnivel en un circuito con dos altos de camino (Arandomendi y '
    'el Collado de Asuntza) antes y despu&eacute;s de coronar el Urko (785 m). No hay '
    'fuentes en la ruta, as&iacute; que conviene llevar agua &mdash;hay una en el bar de '
    'arriba de Trabakua, junto a los columpios.':
        '15,3 km eta +873 m-ko desnibela zirkuitu batean, bidean bi goirekin (Arandomendi '
        'eta Asuntzako lepoa) Urko gailurra (785 m) egin aurretik eta ondoren. Ez dago '
        'iturririk ibilbidean, beraz komeni da ura eramatea &mdash;bat dago Trabakuko '
        'goiko tabernan, kulunkaren ondoan.',
}

SANCRISTOBAL = {
    'download="Zengotitagane, Askako y San Cristóbal.gpx"': 'download="Zengotitagane, Askako eta San Kristobal.gpx"',
    'alt="Foto ampliada del recorrido de Zengotitagane, Askako y San '
    'Crist&oacute;bal"':
        'alt="Zengotitagane, Askako eta San Kristobal ibilbidearen argazki '
        'handitua"',
    '<span>Carretera y pista</span><span class="sep">/</span>'
    '<span>Zengotitagane, Askako y Garai</span>':
        '<span>Errepidea eta pista</span><span class="sep">/</span>'
        '<span>Zengotitagane, Askako eta Garai</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    '<h1>Zengotitagane, Askako<br><em>y San Crist&oacute;bal</em></h1>':
        '<h1>Zengotitagane, Askako<br><em>eta San Kristobal</em></h1>',
    'Circuito desde Trabakua, por Zengotitagane y Askako, con las ermitas de '
    'San Crist&oacute;bal Txiki y San Juan':
        'Zirkuitua Trabakuatik, Zengotitagane eta Askakotik, San Kristobal '
        'Txiki eta San Juan ermitekin',
    'alt="Pista junto a los aerogeneradores del parque e&oacute;lico, con niebla cubriendo la '
    'cresta"':
        'alt="Pista eolikoen ondoan, lainoak gailurra estaltzen duela"',
    'alt="Pista de tierra con un poste de madera, y el valle del Duranguesado al fondo"':
        'alt="Lur-pista zurezko poste batekin, eta Durangaldeko harana atzealdean"',
    'alt="Un hayedo solitario en la cresta, con vistas al valle entre nubes"':
        'alt="Pagadi bakarti bat gailurrean, haranerako ikuspegiekin hodeien artean"',
    'alt="Descenso por un camino de piedra hacia Garai, con un paso canadiense entre la '
    'niebla"':
        'alt="Jaitsiera harrizko bide batetik Garairantz, pasabide kanadiar batekin '
        'lainoen artean"',
    'alt="Un banco de nubes cubriendo la ladera, cerca de Garai"':
        'alt="Hodei-banku bat magala estaltzen, Garaitik gertu"',
    'alt="Vacas descansando en la loma, con el valle y las monta&ntilde;as al fondo"':
        'alt="Behiak bizkarrean atseden hartzen, harana eta mendiak atzealdean"',
    'alt="Caballos pastando entre &aacute;rboles, con los aerogeneradores del parque e&oacute;lico al fondo"':
        'alt="Zaldiak zuhaitzen artean bazkatzen, parke eolikoaren aerosorgailuak atzealdean"',
    'Salimos de Trabakua en direcci&oacute;n Osma por carretera. Algo m&aacute;s de 2 km '
    'despu&eacute;s giramos a la derecha para coger la pista que sube hasta <b>Zengotitagane</b> '
    '(km 3,7, 810 m), entre los aerogeneradores del parque e&oacute;lico. Las rampas son muy '
    'duras, casi imposibles de subir con una bici normal &mdash;aunque en sentido contrario, '
    'con esta subida convertida en bajada, s&iacute; se puede hacer la ruta con una bici '
    'normal.':
        'Trabakua mendatetik Osmarantz ateratzen gara errepidetik. 2 km pasatxo egin ondoren, '
        'eskuinera biratzen dugu <b>Zengotitagane</b>raino igotzen den pista hartzeko (3,7 km '
        '&middot; 810 m), parke eolikoko haize-errotak artean. Malda oso gogorrak dira, ia '
        'ezinezkoak bizikleta arrunt batekin igotzeko &mdash;baina kontrako noranzkoan, hau '
        'jaitsiera bihurtuta, bai egin daiteke ibilbidea bizikleta arruntarekin.',
    'Tras Zengotitagane seguimos por la cresta hasta <b>Iturzurigana</b> (km 4,8, 858 m), con '
    'vistas a los dos lados. Quien quiera coger agua puede desviarse unos metros a la derecha. '
    'Un poco m&aacute;s adelante, tras cruzar en paralelo a los aerogeneradores la parte alta '
    'del Oiz, bajamos a una pista de cemento en busca de la subida a la zona de la cumbre de '
    '<b>Askako</b> (km 5,7, 681 m), que cruzamos por un precioso sendero semioculto bajo la '
    'vegetaci&oacute;n: parte del trazado cl&aacute;sico del AstoTrail, la exigente carrera de '
    'monta&ntilde;a que organiza el municipio de Garai.':
        'Zengotitaganetik krestan jarraitzen dugu <b>Iturzurigana</b>raino (4,8 km &middot; '
        '858 m), bi aldeetara bistak dituela. Ura hartu nahi duenak eskuinera metro gutxi '
        'batzuk desbideratu daiteke. Pixka bat aurrerago, haize-errotak paraleloan zeharkatuz '
        'Oizko goialdea, zementuzko pista batera jaisten gara, <b>Askako</b> gailur-ingurura '
        'igotzeko (5,7 km &middot; 681 m). Gailur-inguru hori sasipean ezkutatuta doan bide '
        'zoragarri batez zeharkatzen da: AstoTrail lasterketa gogorraren ibilbide klasikoaren '
        'parte, Garaiko udalerriak antolatzen duen mendiko proba ospetsua.',
    'Bajamos entonces hacia Garai por un hayedo precioso, una de las bajadas que m&aacute;s '
    'se disfrutan de toda la ruta. Nada m&aacute;s salir de Garai hay una fuente a mano '
    'izquierda, con agua durante todo el a&ntilde;o.':
        'Handik behera, Garaialdera jaisten gara pago-baso zoragarri baten bidez, ibilbideko '
        'jaitsierarik gozagarrienetako batean. Garaitik irten bezain pronto, iturri bat dago '
        'ezkerrean, urte osoan ura duena.',
    'La subida de Garai hasta la <b>Ermita de San Crist&oacute;bal Txiki</b> (km 20,3, 493 m) '
    'la hacemos por una pista de piedra &mdash;as&iacute; se conoce esta ermita, para '
    'distinguirla de la otra Ermita de San Crist&oacute;bal, la de arriba, junto a los '
    'aerogeneradores.':
        'Garaiko igoera <b>San Kristobal Txiki ermita</b>raino (20,3 km &middot; 493 m) '
        'harrizko pista batetik egiten da, goiko San Kristobal ermitatik bereizteko '
        '&mdash;Oiz aldeko haize-errotak inguruan dituen ermitarekin.',
    'Continuamos a toda velocidad cuesta abajo hasta el barrio de San Jos&eacute;. Cruzamos la '
    'carretera general entre Trabakua y Berriz y subimos por la carretera vieja hacia el '
    'barrio de Zengotita, donde est&aacute; la <b>Ermita de San Juan</b> (km 24,5, 404 m), ya '
    'cerca de cerrar el c&iacute;rculo, antes de bajar de vuelta a Trabakua.':
        'Handik beherantz abiadura handian jaisten gara San Jos&eacute; auzoraino. Trabakua eta '
        'Berriz lotzen dituen errepide nagusia zeharkatu, eta errepide zaharretik igotzen da '
        'Zengotita auzoraino, <b>San Juan ermita</b> dagoen tokira (24,5 km &middot; 404 m), '
        'zirkuitua ixteko puntura iritsi aurretik, Trabakuara berriro jaitsi baino lehen.',
    '26,9 km y +1.248 m de desnivel en un solo circuito, con rampas muy duras nada m&aacute;s '
    'salir hacia Zengotitagane &mdash;casi imposibles de subir con una bici normal en este '
    'sentido. Hay '
    'agua cerca de Iturzurigana (km 4,8) y en una fuente a la salida de Garai, con agua todo '
    'el a&ntilde;o, antes de la Ermita de San Crist&oacute;bal Txiki.':
        '26,9 km eta +1.248 m-ko desnibela zirkuitu bakarrean, malda oso gogorrekin '
        'Zengotitaganerako irteeran bertan &mdash;ia ezinezkoak bizikleta arrunt batekin '
        'igotzeko norabide honetan. Ura badago Iturzuriganatik gertu (4,8 km) eta Garaiko '
        'irteerako iturri batean, urtean zehar beti urarekin, San Kristobal Txiki ermitaren '
        'aurretik.',
    'Ermita de San Crist&oacute;bal Txiki': 'San Kristobal Txiki ermita',
    'Ermita de San Juan': 'San Juan ermita',
}

ITURRETA = {
    '<span>Cemento, piedra y tierra</span><span class="sep">/</span><span>Barinaga, el río e Iturreta</span>':
        '<span>Zementua, harria eta lurra</span><span class="sep">/</span><span>Barinaga, ibaia eta Iturreta</span>',

    '<span>Circuito</span></p>':
        '<span>Zirkuitua</span></p>',

    '<h1>Trabakua, Barinaga<br><em>y Iturreta</em></h1>':
        '<h1>Trabakua, Barinaga<br><em>eta Iturreta</em></h1>',

    'alt="Manillar de la bicicleta eléctrica en un sendero entre matorral, con los aerogeneradores del Oiz al fondo"':
        'alt="Bizikleta elektrikoaren eskulekua sasi arteko bidezidor batean, Oizeko eolikoak atzealdean"',
    'alt="Foto ampliada del recorrido de Trabakua, Barinaga y Iturreta"':
        'alt="Trabakua, Barinaga eta Iturretako ibilbidearen argazki handitua"',
    'alt="Vista del valle desde la ruta, con caseríos y bordas entre prados y bosque"':
        'alt="Haranaren ikuspegia ibilbidetik, baserriak eta bordak larre eta basoen artean"',
    'alt="Pista de cemento en la ladera, con los aerogeneradores del Oiz al fondo"':
        'alt="Zementuzko pista hegalean, Oizeko eolikoak atzealdean"',
    'alt="Pista de cemento entre árboles, con luz de otoño filtrándose entre las hojas"':
        'alt="Zementuzko pista zuhaitzen artean, udazkeneko argia hostoen artetik sartzen"',
    'alt="Vista panorámica del valle con un caserío blanco entre bosque y prados"':
        'alt="Haranaren ikuspegi panoramikoa, baserri zuri bat basoaren eta larreen artean"',
    'alt="Pista de tierra en una zona de monte recién talado, con vistas al valle"':
        'alt="Lurrezko pista, berriki moztutako baso-eremu batean, haranerako ikuspegiekin"',

    'Circuito en e-bike desde Trabakua por Barinaga hasta Iturreta y Mendibil':
        'Zirkuitua e-bikez Trabakuatik, Barinaga, Iturreta eta Mendibiletik igarota',

    'download="Trabakua, Barinaga y Iturreta.gpx"':
        'download="Trabakua, Barinaga eta Iturreta.gpx"',

    '<title>El río':
        '<title>Ibaia',

    '<span class="num">2</span>El río</span>':
        '<span class="num">2</span>Ibaia</span>',


    '19,65 km y +975 m de desnivel en un solo circuito, con una rampa corta pero intensa después de Iturreta —difícil de subir con una bici normal en ese tramo. No hay fuentes de agua en el recorrido: en caso de necesidad, habría que desviarse hasta el pueblo de Barinaga.':
        '19,65 km eta +975 m-ko desnibela zirkuitu bakarrean, Iturreta ondoren malda labur baina bizi batekin —zaila bizikleta arrunt batekin igotzeko tarte horretan. Ez dago ur-iturririk ibilbidean: beharrezkoa balitz, Barinaga herrira desbideratu beharko litzateke.',

    'Se sale desde el Alto de Trabakua. Los primeros metros bajan hasta un cruce donde se deja el asfalto, y todo pasa a ser pista en solitario. El primer repecho —duro, poco más de 300 m— es el que más se nota. Después hay una bajada algo técnica hasta la zona de <b>Aginaga</b> (km 5).':
        'Ibilbidea Trabakuako mendatean hasten da. Lehen metroek behera egiten dute asfaltoa uzten den bidegurutze batera iritsi arte, eta hortik aurrera dena da pista bakarrik. Lehen malda —gogorra, 300 metrotik gutxixeago— da gehien nabaritzen dena. Ondoren, jaitsiera teknikoxka bat dago <b>Aginagako</b> eremuraino (5 km).',

    'En Aginaga se coge la pista de la izquierda, bajando entre caseríos y prados con ganado hasta <b>el río</b> (km 9,2), en el fondo del valle. Ahí se gira a la izquierda y empieza la subida por cemento hacia <b>Iturreta</b> (km 12,5). Una vez arriba, coge otra pista de piedra —varios kilómetros para recuperar piernas— antes de la siguiente subida: corta pero intensa, por pista de tierra, difícil de subir con una bici normal —ahí se le pide a la eléctrica todo lo que da. La subida sigue hasta divisar <b>Mendibil</b> a la izquierda (km 14,5), señal de que se ha llegado a la parte más alta de la ruta.':
        'Aginagan ezkerreko pista hartzen da, baserri eta abere-larreen artean behera eginez <b>ibaira</b> iritsi arte (9,2 km), haranaren hondoan. Han ezkerrera biratzen da eta hasten da zementuzko igoera <b>Iturretarantz</b> (12,5 km). Gainean, harrizko pista hartzen da —kilometro batzuk hankak berreskuratzeko— hurrengo igoeraren aurretik: laburra baina bizia, lurrezko pistatik, zaila bizikleta arrunt batekin igotzeko —hor eskatzen zaio elektrikoari eman dezakeen guztia. Igoerak jarraitzen du <b>Mendibil</b> ezkerrera ikusi arte (14,5 km), ibilbideko puntu altuenera iritsi garenaren seinale.',

    'Baja entonces una pista de tierra para estirar unos cuantos kilómetros más, seguida de un buen tramo de piedra donde se puede dar bastante tralla. Ya abajo del todo, la última subida vuelve hacia Trabakua, con los aerogeneradores del Oiz y el barrio de Gerea como paisaje de fondo, antes de llegar de vuelta a Trabakua, punto de salida y llegada.':
        'Ondoren, lurrezko pista batean behera egiten da kilometro batzuk luzatzeko, eta gero harrizko tarte on bat dator, non tralla franko eman daitekeen. Erabat behean, azken igoerak Trabakuarantz egiten du, Oizeko haize-errotak eta Gereako auzoa atzealde gisa dituela, Trabakuara itzuli arte, irteera eta helmuga puntura.',
}

EGOARBITZA = {
    '<span>Pista, sendero y cresta</span><span class="sep">/</span><span>Urko, Egoarbitza y Zengotitagane</span>':
        '<span>Pista, bidezidorra eta gailurra</span><span class="sep">/</span><span>Urko, Egoarbitza eta Zengotitagane</span>',

    '<span>Circuito</span></p>':
        '<span>Zirkuitua</span></p>',

    '<h1>Urko, Egoarbitza<br><em>y Zengotitagane</em></h1>':
        '<h1>Urko, Egoarbitza<br><em>eta Zengotitagane</em></h1>',

    'Circuito en e-bike desde Trabakua por Urko, Egoarbitza y Santama&ntilde;esar hasta Zengotitagane':
        'Zirkuitua e-bikez Trabakuatik, Urko, Egoarbitza eta Santama&ntilde;esarretik igarota Zengotitaganeraino',

    'download="Urko, Egoarbitza y Zengotitagane.gpx"':
        'download="Urko, Egoarbitza eta Zengotitagane.gpx"',

    '<title>Presa de Aixola &middot; 19,0 km &middot; 312 m</title>':
        '<title>Aixolako presa &middot; 19,0 km &middot; 312 m</title>',
    '<span class="num">4</span>Presa de Aixola</span>':
        '<span class="num">4</span>Aixolako presa</span>',

    '<h2>Senderismo</h2>': '<h2>Oinez</h2>',

    'alt="V&eacute;rtice geod&eacute;sico en la cumbre del Urko, con bastones de trekking apoyados y las monta&ntilde;as del entorno al fondo"':
        'alt="Urkoko gailurreko bertize geodesikoa, trekking bastoiak bermatuta eta inguruko mendiak atzealdean"',
    'alt="Foto ampliada del recorrido de Urko, Egoarbitza y Zengotitagane"':
        'alt="Urko, Egoarbitza eta Zengotitaganeko ibilbidearen argazki handitua"',
    'alt="Ascenso hacia Urko entre &aacute;rboles a contraluz, con el amanecer al fondo"':
        'alt="Urkorako igoera zuhaitzen artean kontraargitan, egunsentia atzealdean"',
    'alt="Amanecer con el sol asomando entre nubes, desde la zona de Urko"':
        'alt="Egunsentia, eguzkia hodeien artetik agertzen, Urko inguruko eremutik"',
    'alt="Vista desde Egoarbitza hacia el embalse de Aixola, entre bosque y pistas forestales"':
        'alt="Egoarbitzatik Aixolako urtegirako ikuspegia, baso eta baso-pisten artean"',
    'alt="Cruz de piedra en un mirador de Santama&ntilde;esar, con el valle y los caser&iacute;os al fondo"':
        'alt="Harrizko gurutzea Santama&ntilde;esarreko begiratoki batean, harana eta baserriak atzealdean"',
    'alt="Cruz de piedra entre &aacute;rboles en Arietxu, con un perro junto a ella"':
        'alt="Harrizko gurutzea zuhaitzen artean Arietxun, txakur bat ondoan duela"',
    'alt="Embalse de Aixola, con la caseta sobre el agua y el bosque alrededor"':
        'alt="Aixolako urtegia, etxola urearen gainean eta basoa inguruan"',
    'alt="Corredores subiendo un sendero entre helechos y un &aacute;rbol cubierto de musgo"':
        'alt="Lasterkariak goraka, sendero batetik iratzeen artean eta goroldioz estalitako zuhaitz baten ondotik"',
    'alt="Corredores subiendo una cresta herbosa y rocosa bajo un cielo despejado"':
        'alt="Lasterkariak gandor belartsu eta harritsu batean gora, zeru garbi baten azpian"',

    'La subida hasta <b>Urko</b> (km 8 &middot; 785 m) es la misma que sube desde Trabakua en la ficha de '
    '<a href="urko.html">Asuntza y Urko</a>: pista de cemento y piedra. Desde la cima empieza la '
    'bajada, coincidiendo con el &uacute;ltimo tramo del acceso que sube desde Ermua: primero sendero, '
    'luego un trozo de carretera y despu&eacute;s un cruce escondido que cuesta encontrar la primera vez, '
    'hasta bajar al barrio de <b>Ama&ntilde;a</b> (km 12 &middot; 171 m), en Eibar.':
        '<b>Urko</b>raino igoera (8. km &middot; 785 m) Trabakuatik igotzen den '
        '<a href="urko.html">Asuntza-Urko</a> fitxako bide berbera da: hormigoizko eta harrizko pista. '
        'Gailurrera iritsita hasten da jaitsiera, Ermutik datorren azken zatiarekin bat eginez: '
        'lehenengo, bide estua; gero, errepide zati bat; eta ondoren, ezkutuan dagoen bidegurutze bat, '
        'lehen aldian topatzea kostatzen dena, <b>Ama&ntilde;a</b>ko auzora jaitsi arte (12. km '
        '&middot; 171 m), Eibarren.',

    'Cruzado Ama&ntilde;a se sube hacia el pol&iacute;gono industrial, y de ah&iacute; arranca el sendero '
    'hasta <b>Egoarbitza</b> (km 16,2 &middot; 722 m): pista al principio, despu&eacute;s media cresta, '
    'empinada y dura, con un tramo final rocoso donde conviene ir con cuidado.':
        'Ama&ntilde;a zeharkatuta, industrialdera igotzen da, eta handik hasten da <b>Egoarbitza</b>rako '
        '(16,2 km &middot; 722 m) bidea: hasieran pista, gero media cresta gogorra eta tentea, eta '
        'amaieran harritza duen zatia, kontu handiz ibiltzea komeni dena.',

    'La bajada hacia la <b>presa de Aixola</b> (km 19) es muy buena: primero sendero, despu&eacute;s '
    'pista. Justo al llegar al camino de la presa merece la pena desviarse a la izquierda unos metros '
    'hasta una fuente con agua todo el a&ntilde;o. Se cruza el frente de la presa y se sube '
    'hacia <b>Santama&ntilde;esar</b> (km 22,6 &middot; 663 m), toda por pista, sin ning&uacute;n misterio.':
        '<b>Aixolako presa</b>ra jaitsiera (19. km) oso ona da: lehenengo bide estua, gero pista. '
        'Presako bidera iritsi bezain pronto, ezkerretara metro gutxi batzuk egitea merezi du, urte '
        'osoan ura duen iturri batera. Presaren aurrealdea zeharkatu, eta <b>Santama&ntilde;esar</b> '
        'aldera igotzen da (22,6 km &middot; 663 m), dena pista, misteriorik gabe.',

    'Luego bajamos hacia <b>Santa Marina</b>, donde hay una ermita y se puede volver a abastecer de '
    'agua. En la ermita se coge la GR, que sube poco a poco hacia '
    '<b>Arietxu</b> (km 28,8 &middot; 483 m), el mismo pico de la ruta de <a href="arietzu.html">Osmagain '
    'y Arietzu</a>, pero llegando por el lado contrario.':
        'Handik <b>Santa Marina</b>ra jaisten gara; han ermita dago eta ura berriz hartzeko aukera. '
        'Ermitan GRa hartzen da, poliki-poliki <b>Arietxu</b>raino igotzen dena (28,8 km &middot; 483 m), '
        '<a href="arietzu.html">Osmagain-Arietzu</a> ibilbideko gailur berbera, baina beste aldetik '
        'iritsita.',

    'Desde Arietxu seguimos por el cresterio hasta m&aacute;s o menos la mitad, y luego bajamos hacia el '
    'barrio de Zengotita, donde hay una fuente con agua '
    'todo el a&ntilde;o. Despu&eacute;s de la fuente empieza la subida hacia <b>Zengotitagane</b> '
    '(km 32,5 &middot; 811 m): todo en pista, subir y subir sin apenas tregua, pero bastante llevadera. '
    'Y de ah&iacute;, casi en vertical hacia Trabakua: la &uacute;ltima bajada tiene buena pendiente, unos 400 m de '
    'desnivel en poco m&aacute;s de 2 km, y se cierra el circuito.':
        'Arietxutik krestan jarraitzen da erdi aldera arte, eta gero Zengotita auzora jaisten da, urte '
        'osoan ura duen iturri bat dagoen tokira. Iturriaren ondoren hasten da <b>Zengotitagane</b>rako '
        'igoera (32,5 km &middot; 811 m): dena pista, etenik ia gabe, baina nahiko eramangarria. Eta '
        'handik, ia bertikalki Trabakuara: azken jaitsierak malda handia dauka, 400 m desnibel 2 km '
        'eskasetan, eta zirkuitua ixten da.',

    '34,1 km y +2.564 m de desnivel en un solo circuito, con cuatro subidas importantes (Urko, '
    'Egoarbitza, Arietxu y Zengotitagane) y tramos de media cresta exigentes. '
    'Hay varios puntos para abastecerse de agua en el recorrido: una fuente junto a '
    'la presa de Aixola, otro en Santa Marina, y una fuente en el barrio de '
    'Zengotita.':
        '34,1 km eta +2.564 m-ko desnibela zirkuitu bakarrean, lau igoera garrantzitsurekin (Urko, '
        'Egoarbitza, Arietxu eta Zengotitagane) eta gailurreko tarte eskatzaileekin. Hainbat '
        'puntutan har daiteke ura ibilbidean: iturri bat Aixolako presaren ondoan, beste bat '
        'Santa Marinan, eta iturri bat Zengotita auzoan.',
}

URREGARAI = {
    '<span>Pista, asfalto y cemento</span><span class="sep">/</span><span>Iturreta, Markina y Urregarai</span>':
        '<span>Pista, asfaltoa eta zementua</span><span class="sep">/</span><span>Iturreta, Markina eta Urregarai</span>',

    '<span>Circuito</span></p>':
        '<span>Zirkuitua</span></p>',

    '<h1>Iturreta, Markina<br><em>y Urregarai</em></h1>':
        '<h1>Iturreta, Markina<br><em>eta Urregarai</em></h1>',

    'Circuito en e-bike desde Trabakua por Iturreta, Markina y Urregarai hasta Bolibar':
        'Zirkuitua e-bikez Trabakuatik, Iturreta, Markina eta Urregaraitik igarota Bolibarreraino',

    'download="Iturreta, Markina y Urregarai.gpx"':
        'download="Iturreta, Markina eta Urregarai.gpx"',

    '<h2>Senderismo</h2>': '<h2>Oinez</h2>',


    'alt="Amanecer con luz anaranjada sobre las monta&ntilde;as, al salir de Trabakua"':
        'alt="Egunsentia argi laranjaz mendien gainean, Trabakuatik irtetean"',
    'alt="Foto ampliada del recorrido de Iturreta, Markina y Urregarai"':
        'alt="Iturreta, Markina eta Urregaraiko ibilbidearen argazki handitua"',
    'alt="Pista junto a un caser&iacute;o de tejado rojo, en el valle cerca de Iturreta"':
        'alt="Pista teilatu gorriko baserri baten ondoan, Iturreta inguruko haranean"',
    'alt="Cascada entre &aacute;rboles, en el bosque cerca de Iturreta"':
        'alt="Ur-jauzia zuhaitzen artean, Iturreta inguruko basoan"',
    'alt="Vista de Bolibar, con la iglesia de piedra y los caser&iacute;os del pueblo"':
        'alt="Bolibarren ikuspegia, harrizko eliza eta herriko baserriak"',

    'Salimos de Trabakua y, despu&eacute;s de bajar 1 km direcci&oacute;n Ermua por carretera general, '
    'dejamos esa carretera para girar a la izquierda: cogemos el mismo camino que sube hacia '
    '<a href="urko.html">Asuntza o hacia Urko</a>. Pasamos junto a '
    'unos chal&eacute;s &mdash;con una puerta corredera de acceso&mdash;, y despu&eacute;s de la siguiente curva '
    'aparece una cuesta bastante pronunciada, hasta donde se acaba el '
    'camino de cemento: ah&iacute; est&aacute; el cruce, donde el '
    'camino de frente va para Urko y Asuntza y nosotros cogemos el de la izquierda. Seguimos sin dejar '
    'esa pista hasta un collado con una se&ntilde;al que marca &laquo;Markina&raquo;, con marcas blancas '
    'y amarillas. Ah&iacute; bajamos por un camino de tierra con la pendiente pronunciada, hasta llegar '
    'al camino de piedra que est&aacute; junto a un caser&iacute;o. Junto al caser&iacute;o '
    'giramos a la izquierda hacia la ermita de '
    '<b>Iturreta</b> (km 6 &middot; 361 m). Pasamos junto a una '
    'fuente antes de volver a subir un peque&ntilde;o tramo para bajar de nuevo hacia Markina, siguiendo las '
    'mismas marcas, con buenas vistas hacia el pueblo y varios caser&iacute;os de Iturreta.':
        'Trabakuatik irten eta, Ermua norabidean 1 km errepidez jaitsi ondoren, errepide hori utzi eta '
        'ezkerrera jotzen dugu: <a href="urko.html">Asuntzarako edo Urkorako</a> igotzen den bide bera '
        'hartzen dugu. Txalet batzuen '
        'ondotik pasatzen gara —sarrerako ate irristakor batekin—, eta hurrengo bihurgunearen '
        'ondoren aldapa nahiko pikoa agertzen da, zementuzko bidea amaitzen '
        'den arte: hor dago bidegurutzea, non Urko eta Asuntzarako bidea aurrez aurre doan eta guk '
        'ezkerrekoa hartzen dugun. Pista '
        'hori utzi gabe jarraitzen dugu lepo batera arte, non &laquo;Markina&raquo; markatzen duen '
        'seinale bat aurkituko dugun, marka zuri eta horiekin. Han lur-bide batetik jaisten gara malda '
        'pikoarekin, harrizko bidera iritsi arte, baserri baten ondoan dagoena. '
        'Baserriaren ondoan ezkerrera jotzen '
        'dugu <b>Iturretako ermitarantz</b> (6 km '
        '&middot; 361 m). Iturri baten ondotik pasatzen gara, berriro igo aurretik tarte labur batean, '
        'Markinarantz berriro jaisteko, marka berberei jarraituz, herrirako eta Iturretako hainbat '
        'baserritarako ikuspegi onekin.',

    'Ya en <b>Markina</b> (km 12 &middot; 79 m) volvemos a abastecernos de agua, en una fuente grande '
    'junto a la iglesia del Carmen. Cruzamos el pueblo hacia la salida, pasando junto a unas escuelas, '
    'y cogemos de nuevo un camino de barrio que sube sin descanso hacia <b>Urregarai</b> (km 16 '
    '&middot; 573 m), en los alrededores de Santa Eufemia. El &uacute;ltimo repecho es precioso, junto '
    'a un caser&iacute;o-granja con muchos pastos. Arriba est&aacute; el refugio de Urregarai, con una '
    'fuente y una bolera enfrente.':
        '<b>Markinan</b> (12 km &middot; 79 m) berriro ur hornitzen gara, Karmen elizaren ondoko iturri '
        'handi batean. Herria zeharkatzen dugu irteera aldera, eskola batzuen ondotik pasatuz, eta '
        'berriro auzo-bide bat hartzen dugu, atsedenik gabe <b>Urregairantz</b> igotzen duena (16 km '
        '&middot; 573 m), Santa Eufemia inguruan. Azken aldapa ederra da, larre asko dituen '
        'baserri-granja baten ondoan. Goian Urregairako aterpea dago, iturri batekin eta aurrean '
        'bolatoki bat.',

    'Bajamos por el camino de asfalto que zigzaguea hasta la carretera general, la cruzamos y, un poco '
    'm&aacute;s adelante, giramos a la derecha para seguir por una pista de tierra hacia el barrio de '
    'Zeinka, desde donde se baja a <b>Bolibar</b> (km 22,3 &middot; 173 m) en un santiam&eacute;n. '
    'Cogemos la carretera que va hacia la Colegiata de <a href="zenarruza.html">Zenarruza</a>, pero '
    'antes de empezar a subir hacia ella dejamos el asfalto para subir por una cuesta empinada de '
    'cemento hacia <b>Muniozguren</b> (km 25,5 &middot; 496 m), a los pies del monte Oiz.':
        'Errepide nagusira bihurgune-bihurgunean jaisten den asfaltozko bidetik jaisten gara, '
        'zeharkatu eta, pixka bat aurrerago, eskuinera jotzen dugu Zeinka auzorantz doan lur-pista '
        'batetik jarraitzeko, handik <b>Bolibarrera</b> jaisten gara istant batean (22,3 km &middot; '
        '173 m). <a href="zenarruza.html">Zenarruza</a>ko kolegiatarantz doan errepidea hartzen dugu, '
        'baina hara igotzen hasi baino lehen, asfaltoa uzten dugu zementuzko aldapa pikotik '
        '<b>Muniozgurenerantz</b> igotzeko (25,5 km &middot; 496 m), Oiz mendiaren oinean.',

    'Ya solo queda bajar hacia Trabakua, por el barrio de Gerena, para cerrar el circuito.':
        'Trabakuarantz jaistea besterik ez zaigu geratzen, Gerena auzotik, zirkuitua ixteko.',

    '30,5 km y +1.163 m de desnivel en un solo circuito, con dos subidas importantes (Urregarai y '
    'Muniozguren) y tramos de pista, asfalto y cemento empinado. '
    'Hay varios puntos para abastecerse de agua en el recorrido: una fuente en Iturreta, otra junto a '
    'la iglesia del Carmen en Markina, y una tercera en el refugio de Urregarai.':
        '30,5 km eta +1.163 m-ko desnibela zirkuitu bakarrean, bi igoera garrantzitsurekin (Urregarai '
        'eta Muniozguren) eta pista, asfalto eta zementu pikoko tarteekin. Hainbat '
        'puntutan har daiteke ura ibilbidean: iturri bat Iturretan, beste bat Markinako Karmen '
        'elizaren ondoan, eta hirugarren bat Urregairako aterpean.',
}

KALAMUA = {
    '<span>Pista, asfalto y cemento</span><span class="sep">/</span><span>Urko, Kalamua, San Migel y Mendibil</span>':
        '<span>Pista, asfaltoa eta zementua</span><span class="sep">/</span><span>Urko, Kalamua, San Migel eta Mendibil</span>',

    '<span>Circuito</span></p>':
        '<span>Zirkuitua</span></p>',

    '<h1>Urko, Kalamua, San Migel<br><em>y Mendibil</em></h1>':
        '<h1>Urko, Kalamua, San Migel<br><em>eta Mendibil</em></h1>',

    'Circuito en e-bike desde Trabakua por Urko, Kalamua, San Migel, Markina, Iturreta y Mendibil':
        'Zirkuitua e-bikez Trabakuatik, Urko, Kalamua, San Migel, Markina, Iturreta eta Mendibiletik igarota',

    'download="Urko, Kalamua, San Migel y Mendibil.gpx"':
        'download="Urko, Kalamua, San Migel eta Mendibil.gpx"',

    '<h2>Senderismo</h2>': '<h2>Oinez</h2>',

    'alt="Amanecer entre nubes junto al moj&oacute;n de la cumbre de Urko, km 7,9 de la ruta"':
        'alt="Egunsentia hodeien artean, Urkoko gailurreko mugarriaren ondoan, ibilbideko 7,9 km"',
    'alt="Foto ampliada del recorrido de Urko, Kalamua, San Migel y Mendibil"':
        'alt="Urko, Kalamua, San Migel eta Mendibilgo ibilbidearen argazki handitua"',
    'alt="Torreta de la cumbre de Kalamua bajo un cielo despejado, km 12,4"':
        'alt="Kalamuako gailurreko dorretxoa zeru garbi baten azpian, 12,4 km"',
    'alt="Vistas hacia las monta&ntilde;as desde la cumbre de Kalamua, km 12,4"':
        'alt="Mendietarako ikuspegiak Kalamuako gailurretik, 12,4 km"',
    'alt="Caser&iacute;o y antena vistos desde lo alto, entre San Migel y Markina, km 20,3"':
        'alt="Baserria eta antena goitik ikusita, San Migel eta Markinaren artean, 20,3 km"',
    'alt="Amanecer sobre un mar de nubes, cerca de Mendibil, km 32,7"':
        'alt="Egunsentia hodei-itsaso baten gainean, Mendibiletik gertu, 32,7 km"',
    'alt="Torreta de una cumbre entre colinas verdes, en un d&iacute;a despejado"':
        'alt="Gailur bateko dorretxoa muino berdeen artean, egun garbi batean"',
    'alt="Caser&iacute;o blanco y ovejas entre prados verdes, con los montes al fondo"':
        'alt="Baserri zuria eta ardiak larre berdeen artean, mendiak atzealdean"',
    'alt="Moj&oacute;n en la cima con vistas a un pueblo en el valle al fondo"':
        'alt="Mugarria gailurrean, haraneko herri baten ikuspegiarekin atzealdean"',

    'Subimos desde Trabakua hasta <b>Urko</b> (km 7,9 &middot; 791 m) por el mismo camino que la ruta de '
    '<a href="urko.html">Trabakua, Asuntza y Urko</a>. Desde ah&iacute; bajamos hacia Ixua para cruzar la '
    'carretera general junto a un restaurante, y empezamos a subir hacia <b>Kalamua</b>: una subida muy '
    'bonita, con varias fuentes por el camino donde abastecerse de agua &mdash;la &uacute;ltima hasta '
    'Markina.':
        'Trabakuatik <b>Urkora</b> igotzen gara (7,9 km &middot; 791 m), '
        '<a href="urko.html">Trabakua, Asuntza eta Urko</a>ko bide beretik. Handik Ixurantz jaisten gara '
        'errepide nagusia jatetxe baten parean gurutzatzeko, eta <b>Kalamua</b>rako igoerari ekiten diogu: '
        'igoera oso polita da, bidean ur hornidura egiteko hainbat iturrirekin &mdash;azkena Markinarako '
        'bidean.',

    'En la cumbre de <b>Kalamua</b> (km 12,4 &middot; 768 m) hay una torreta y muy buenas vistas hacia el '
    'resto de las monta&ntilde;as. Bajamos hasta llegar a la altura de <b>Urkarregi</b>, donde se cruza la '
    'carretera de <b>San Migel</b> (km 13,7 &middot; 526 m).':
        '<b>Kalamua</b>ko tontorrean (12,4 km &middot; 768 m) torreta bat dago eta oso ikuspegi onak '
        'gainerako mendietara. <b>Urkarregi</b> pareraino jaisten gara, <b>San Migel</b>ko errepidea '
        'gurutzatzeko (13,7 km &middot; 526 m).',

    'Tras cruzar la carretera empieza un tramo largo: primero un camino de cemento y, al dejarlo, '
    'giramos a la izquierda para pasar junto a un caser&iacute;o y encarar una subida en '
    'condici&oacute;n. A veces coincidimos aqu&iacute; con peregrinos que hacen el Camino de Santiago '
    'rumbo a Markina, y compartimos un rato de camino con ellos. Poco a poco el paisaje se abre en lo '
    'alto, ya sobre pista de tierra, hasta que empieza la bajada hacia Markina.':
        'Errepidea gurutzatu eta gero tarte luzea hasiko da: lehenengo zementuzko bidea eta, hura '
        'utzitakoan, ezkerrera biratzen dugu baserri baten paretik pasa eta benetako igoera bati '
        'ekiteko. Batzuetan hemen Done Jakue bidea Markinarantz egiten duten erromesekin topo egiten '
        'dugu, eta bidearen zati bat haiekin partekatzen dugu. Pixkanaka paisaia zabaldu egiten da '
        'goian, lurrezko pistaren gainean jada, Markinarako jaitsiera hasi arte.',

    'Bajamos hasta <b>Markina</b> (km 24,3 &middot; 79 m), donde nos abastecemos de agua. Seguimos '
    'subiendo por el mismo corredor que la ruta de <a href="urregarai.html">Iturreta, Markina y '
    'Urregarai</a>, pero en sentido contrario, pasando de nuevo por la zona de <b>Iturreta</b> (km 28,4 '
    '&middot; 415 m) camino de la &uacute;ltima subida importante del d&iacute;a.':
        '<b>Markinaraino</b> jaisten gara (24,3 km &middot; 79 m), eta bertan urez hornitzen gara. '
        '<a href="urregarai.html">Iturreta, Markina eta Urregarai</a> ibilbidearen korridore beretik '
        'gora jarraitzen dugu, baina alderantziz, <b>Iturreta</b>ko gunetik berriro pasatuz (28,4 km '
        '&middot; 415 m) eguneko azken igoera garrantzitsuaren bidean.',

    'Esa &uacute;ltima subida lleva hasta <b>Mendibil</b> (km 32,8 &middot; 612 m). Desde ah&iacute; ya '
    'solo queda bajar de vuelta hacia Trabakua para cerrar el circuito.':
        'Azken igoera horrek <b>Mendibilera</b> eramaten gaitu (32,8 km &middot; 612 m). Hortik aurrera '
        'Trabakuara itzultzeko jaitsiera besterik ez da geratzen zirkuitua ixteko.',

    '36,0 km y +1.500 m de desnivel en un solo circuito, con tres subidas importantes (Urko, Kalamua y '
    'Mendibil) y tramos de pista, asfalto y cemento. Hay varias fuentes en la subida a Kalamua para '
    'abastecerse de agua; a partir de ah&iacute; escasea hasta Markina.':
        '36,0 km eta +1.500 m-ko desnibela zirkuitu bakar batean, hiru igoera garrantzitsurekin (Urko, '
        'Kalamua eta Mendibil) eta pista, asfalto eta zementuzko tarteekin. Kalamuarako igoeran hainbat '
        'iturri daude urez hornitzeko; hortik aurrera ur eskasia egon daiteke Markinaraino.',

    '&mdash; <b>Distancia</b>, calculada a partir del track GPX real. <b>Desnivel</b>, el que marc&oacute; '
    'el dispositivo. <b>Dificultad</b>, estimada a partir de ambos. <b>Superficie</b> y <b>Tipo</b>, observados sobre el terreno.':
        '&mdash; <b>Distantzia</b>, benetako GPX trackaren arabera kalkulatua. <b>Desnibela</b>, gailuak '
        'markatutakoa. <b>Zailtasuna</b>, bien arabera zenbatetsia. <b>Azalera</b> eta <b>Mota</b>, lurrean bertan behatuak.',
}

MUNDIOKOKOBA = {
    '<h2>Senderismo</h2>': '<h2>Oinez</h2>',
    '<title>Collado de Asuntza': '<title>Asuntzako lepoa',
    '<span class="num">1</span>Collado de Asuntza': '<span class="num">1</span>Asuntzako lepoa',
    '<span>Pista, tierra y cueva</span><span class="sep">/</span><span>Asuntza y Mundioko Koba</span><span class="sep">/</span><span>Circuito</span>':
        '<span>Pista, lur eta koba</span><span class="sep">/</span><span>Asuntza eta Mundioko Koba</span><span class="sep">/</span><span>Zirkuitua</span>',
    '<p class="full-name">Circuito desde Trabakua hasta la cueva de Mundioko Koba, pasando por el Collado de Asuntza</p>':
        '<p class="full-name">Zirkuitua Trabakuatik Mundioko Kobaraino, Asuntzako lepotik igarota</p>',
    'alt="Entrada de la cueva de Mundioko Koba, escondida entre helechos y rocas en el bosque"':
        'alt="Mundioko Kobaren sarrera, basoan iratzeen eta harkaitzen artean ezkutatuta"',
    'alt="Foto ampliada del recorrido de Mundioko Koba"':
        'alt="Mundioko Kobaren ibilbidearen argazkia handituta"',
    'alt="Un murci&eacute;lago colgado del techo de la cueva, junto a formaciones de piedra"':
        'alt="Saguzar bat kobaren sabaitik zintzilik, harrizko formazioen ondoan"',
    'alt="Vista hacia el pozo interior de la cueva, con una cuerda preparada para el descenso"':
        'alt="Kobaren barruko putzurantz begira, jaisteko soka bat prest"',
    'alt="Nudo en la cuerda usada para bajar al segundo tramo de la cueva"':
        'alt="Kobaren bigarren zatira jaisteko erabilitako sokaren korapiloa"',
    'alt="Galer&iacute;a interior de la cueva, con paredes de roca estratificada"':
        'alt="Kobaren barruko galeria, harrizko horma geruzatuekin"',
    'Se sale desde el Alto de Trabakua. Los primeros metros bajan &mdash;poco m&aacute;s de un '
    'kil&oacute;metro&mdash; hasta un cruce a la izquierda donde se deja el asfalto atr&aacute;s: '
    'desde ah&iacute;, todo es pista en solitario, alternando cemento y tramos de piedra. El primer '
    'repecho es el m&aacute;s duro de toda la ruta &mdash;se sube de un tir&oacute;n&mdash;, pero '
    'enga&ntilde;a: no llega a los 300 m de distancia. La pista sigue hasta el <b>Collado de '
    'Asuntza</b> (km 5 &middot; 494 m) &mdash;el mismo cruce de la ruta de <a href="urko.html">'
    'Trabakua, Asuntza y Urko</a>&mdash;, con una casita a un lado, visible tanto de subida como de '
    'bajada.':
        'Trabakuko altotik abiatzen da ibilbidea. Lehen metroak beherantz dira &mdash;kilometro '
        'pasatxo&mdash;, ezkerretara datorren bidegurutze batera iritsi arte. Han uzten da asfaltoa, '
        'eta hortik aurrera pista bakartia da nagusi, hormigoizko eta harrizko tarteak '
        'txandakatuz.</p>\n'
        '    <p>Lehen aldapa da ibilbide osoko gogorrena: kolpean igotzen da, baina tranpa egiten '
        'du: ez da 300 metroko luzerara iristen. Pistak <b>Asuntzako Lepo</b>raino '
        'jarraitzen du (5. km &middot; 494 m), <a href="urko.html">Trabakua, Asuntza eta '
        'Urko</a> ibilbideko bidegurutze ezagunera. Lepoan bada etxe txiki bat, igoeran zein '
        'jaitsieran beti ikusgai geratzen dena.',
    'En el collado se deja a un lado el camino que sigue hacia Urko y se gira a la derecha, bajando '
    'un poco junto a unos huertos, hasta coger una pista de tierra que se adentra en la parte alta '
    'del barrio de Berano Txiki, entre un pinar cerrado y poco frecuentado. Conviene ir atentos al '
    'GPS, porque incluso con el track cargado cuesta encontrar la boca de <b>Mundioko Koba</b> '
    '(km 6,3 &middot; 492 m), bien escondida entre los pinos. Un peque&ntilde;o riachuelo con poca '
    'agua, ya cerca de la cueva, es la mejor se&ntilde;al de que se est&aacute; en el sitio correcto.':
        'Lepotik, Urkurantz jarraitzen duen bidea alde batera utzi eta eskuinera egingo dugu, baratz '
        'batzuen ondotik apur bat jaitsiz, Berano Txiki auzoaren goialdean sartzen den lurrezko '
        'bidea hartu arte; bide hori pinu-sail itxi eta jende gutxik zapaltzen duen leku batetik '
        'igarotzen da. Arreta GPSan jartzea '
        'komeni da: track-a kargatuta egon arren, kostatu egiten da pinu artean oso ondo ezkutatuta '
        'dagoen <b>Mundioko Koba</b>ren ahoa aurkitzea (6,3 km &middot; 492 m). Ur gutxiko errekatxo '
        'txiki bat, kobazulotik gertu, leku egokian gaudenaren seinalerik onena da.',
    'La entrada es peque&ntilde;a &mdash;hay que agacharse para pasar&mdash;, pero el interior se '
    'abre enseguida: tiene altura y algo de profundidad, y sorprende con solo asomarse. A partir de '
    'ah&iacute;, mucho cuidado: no conviene adentrarse m&aacute;s sin cuerda, porque hay un '
    'peque&ntilde;o descenso que sin ella no se puede bajar &mdash;extremar la precauci&oacute;n si '
    'se va con ni&ntilde;os. Con cuerda se baja unos pocos metros y se avanza un poco m&aacute;s, '
    'hasta toparse arriba, en la roca, con un agujero medio oculto por el que hay que colarse como '
    'se puede: da paso a una segunda b&oacute;veda, tan bonita como la primera. M&aacute;s '
    'all&aacute; la cosa se complica para seguir, pero lo poco que se alcanza a ver ya es precioso.':
        'Sarrera txikia da &mdash;makurtu egin behar da pasatzeko&mdash;, baina barrualdea berehala '
        'zabaltzen da: altuera eta sakonera pixka bat ditu, eta begiratu hutsarekin harritzen du. '
        'Hemendik aurrera, kontu handiz ibili behar da: ez da komeni barrura sartzea sokarik gabe, '
        'jaitsiera txiki bat baitago eta ezin baita bertatik jaitsi sokarik gabe &mdash;haurrekin '
        'bagoaz, are kontu handiagoz.</p>\n'
        '    <p>Soka batekin metro batzuk jaitsi eta pixka bat aurrerago egin daiteke, harkaitzean '
        'goian erdi ezkutatuta dagoen zulo batekin topo egin arte. Zulo horretatik ahal den moduan '
        'pasatuta, bigarren ganbera agertzen da, lehenengoaren adinako edertasunarekin. Handik '
        'aurrera bidea zailtzen da, baina ikusten den apurra ere ederra da.',
    'Despu&eacute;s de la cueva se vuelve a pasar por el <b>Collado de Asuntza</b>, esta vez en el '
    'km 7. Desde ah&iacute; se sigue por el mismo camino de ida durante un kil&oacute;metro, hasta '
    'girar a la izquierda hacia bosque y pistas poco transitadas: un desv&iacute;o que hace la '
    'vuelta m&aacute;s entretenida que repetir todo el trayecto, y de paso se descubren zonas '
    'nuevas de la ruta.':
        'Koba ikusi ondoren, berriro igarotzen da <b>Asuntzako Lepo</b>a, oraingoan 7. kilometroan. '
        'Handik aurrera, joaneko bide beretik jarraituko dugu kilometro batez. Ezkerrera '
        'desbideratuko gara basorantz, jende gutxik ibiltzen duen pista polit batera. Itzulera '
        'askoz ere atseginagoa egiten du, joaneko bidea errepikatu beharrean, eta bide batez '
        'ibilbideko txoko berriak ezagutzen dira.',
    'Ese desv&iacute;o enlaza con el tramo final de la ruta de <a href="trabakua.html">Trabakua '
    'bira</a>, aunque bastante m&aacute;s arriba &mdash;sin pasar por Berano Txiki ni la parte alta '
    'de Berano&mdash;, antes de remontar de nuevo hacia Trabakua, para cerrar el c&iacute;rculo.':
        'Desbideratze horrek <a href="trabakua.html">Trabakua bira</a>ren azken zatiarekin egiten '
        'du bat, baina askoz gorago &mdash;Berano Txikitik zein Beranoko goialdetik pasa '
        'gabe&mdash;, berriro Trabakurantz igo baino lehen, zirkulua ixteko.',
    '13,0 km y +404 m de desnivel en un circuito corto pero con un desv&iacute;o especial: la '
    'entrada a la cueva de Mundioko Koba. Dentro hay un peque&ntilde;o descenso que sin cuerda no '
    'se puede bajar &mdash;no llevar ni&ntilde;os m&aacute;s all&aacute; de la entrada sin la '
    'preparaci&oacute;n adecuada.':
        '13,0 km eta +404 m desnibela, zirkuitu labur batean baina desbideratze berezi batekin: '
        'Mundioko Kobaren sarrera. Barruan jaitsiera txiki bat dago, eta sokarik gabe ez da '
        'jaisteko modukoa &mdash;haurrak ez eramatea gomendatzen da, sarreratik harago ez bada.',
}

IRUZUBIETA = {
    '<span>Mixta</span><span class="sep">/</span><span>Iturreta, Iruzubieta, Arta y Gerea</span>':
        '<span>Nahasia</span><span class="sep">/</span><span>Iturreta, Iruzubieta, Arta eta Gerea</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    '<b>Distancia</b> y <b>Desnivel</b>, calculados a partir del track GPX real. '
    '<b>Dificultad</b>, estimada a partir de ambos. '
    '<b>Superficie</b> y <b>Tipo</b>, orientativos.':
        '<b>Distantzia</b> eta <b>Desnibela</b>, benetako GPX trackatik kalkulatuak. '
        '<b>Zailtasuna</b>, bien arabera zenbatetsia. '
        '<b>Azalera</b> eta <b>Mota</b>, orientagarriak.',
    '<h1>Trabakua, Iturreta<br><em>e Iruzubieta</em></h1>':
        '<h1>Trabakua, Iturreta<br><em>eta Iruzubieta</em></h1>',
    'Circuito desde Trabakua por Iturreta, Iruzubieta, Arta y Gerea':
        'Zirkuitua Trabakuatik, Iturreta, Iruzubieta, Arta eta Gereatik igarota',
    'alt="Atardecer sobre una pista rural cercada, con montes iluminados de naranja al fondo"':
        'alt="Ilunabarra landa-pista itxi batean, mendiak laranja kolorez atzealdean"',
    'alt="Foto ampliada del recorrido de Trabakua, Iturreta e Iruzubieta"':
        'alt="Trabakua, Iturreta eta Iruzubietako ibilbidearen argazki handitua"',
    'alt="Nubes iluminadas por el sol al atardecer sobre los montes del recorrido"':
        'alt="Eguzkiak ilunabarrean argiztatutako hodeiak ibilbideko mendien gainean"',
    'alt="Montones de hierba seca junto a un seto, durante el recorrido"':
        'alt="Belar lehorrezko pilak hesi baten ondoan, ibilbidean zehar"',
    'alt="Ovejas pastando en una ladera, con caseríos y bosque en el valle al fondo"':
        'alt="Ardiak hegalean bazkan, baserriak eta basoa haranean atzealdean"',
    'alt="Una cancela de madera junto a un prado con ganado, con niebla entre los montes '
    'al fondo"':
        'alt="Zurezko atetxo bat larre baten ondoan abereekin, lainoa mendien artean '
        'atzealdean"',
    'alt="Camino hundido entre helechos y árboles, cubierto de hojas secas"':
        'alt="Bide hondoratua iratzeen eta zuhaitzen artean, hosto lehorrez estalia"',
    'download="Trabakua, Iturreta e Iruzubieta.gpx"':
        'download="Trabakua, Iturreta eta Iruzubieta.gpx"',
    '<title>Collado, señal Markina': '<title>Lepoa, Markina seinalea',
    '<span class="num">1</span>Collado, señal Markina</span>':
        '<span class="num">1</span>Lepoa, Markina seinalea</span>',
    '<title>Desvío a Iturreta': '<title>Iturretarako desbideraketa',
    '<span class="num">2</span>Desvío a Iturreta</span>':
        '<span class="num">2</span>Iturretarako desbideraketa</span>',
    '19,22 km y +769 m de desnivel en un solo circuito, apto tanto para andar como para '
    'bicicleta. Los únicos puntos de agua son el bar de arriba de Trabakua, en la misma salida, y '
    'el bar del barrio de Iruzubieta.':
        '19,22 km eta +769 m desnibel zirkuitu bakar batean, oinez zein bizikletaz egiteko '
        'modukoa. Uraren bi puntu bakarrak dira '
        'Trabakuako goiko taberna, irteera puntuan bertan, eta Iruzubietako auzoko taberna.',
    'Sale del Alto de Trabakua bajando un kilómetro por la carretera general rumbo a Ermua, '
    'hasta dejar el asfalto para enfilar la misma pista que sube hacia Asuntza y Urko, de la '
    'ruta de <a href="urko.html">Trabakua, Asuntza y Urko</a>. El camino pasa junto a un puñado '
    'de chalés —con una puerta corredera de acceso—, y después de la siguiente curva el '
    'terreno se pone serio: una cuesta pronunciada que muere justo donde se acaba el cemento. '
    'Ahí, en ese cruce, la ruta se despega del camino de Urko y Asuntza —que sigue de frente— '
    'para tirar a la izquierda.':
        'Trabakuatik ateratzen da, errepide nagusitik kilometro bat Ermuarantz jaitsita, eta '
        'ezkerrera jotzen du Asuntza eta Urkorako igoera hartzeko —txalet batzuen ondotik, '
        'sarrerako ate irristakor batekin— <a href="urko.html">Trabakua, Asuntza eta Urko</a> '
        'ibilbideko tarte beretik. Hurrengo bihurgunearen ondoren aldapa nahiko pikoa hasten '
        'da, zementuzko bidea amaitzen den lekuan hiltzen dena: han dago bidegurutzea, non '
        'aurrera jarraituz Urko eta Asuntzarako bidea den, eta hemen ezkerrekoa hartzen den.',
    'La pista gana altura sin descanso hasta un <b>collado</b> marcado por un cartel hacia '
    'Markina, con las marcas blancas y amarillas del PR-BI 140 (km 3,9 &middot; 529 m): el '
    'techo de todo el circuito. Desde ahí el camino se desploma por un tramo de tierra con '
    'buena pendiente, hasta enlazar con una pista de piedra junto a un caserío. Ahí se gira '
    'hacia la <b>Ermita de Iturreta</b> (361 m) —aunque, a un kilómetro escaso de llegar, el '
    'trazado vuelve a girar, esta vez al norte, para acortar camino.':
        'Pistak aurrera jarraitzen du <b>lepo</b> batera iritsi arte, Markina aldera seinale bat '
        'duena, PR-BI 140 bidearen marka zuri-horiekin (3,9 km &middot; 529 m), zirkuitu osoko '
        'punturik gorena. Handik lurrezko tarte bat jaisten da aldapa onarekin, baserri baten '
        'ondoko harrizko pista batekin bat egin arte, eta han ezkerrera jotzen da <b>Iturretako '
        'ermita</b>rantz (361 m) —nahiz eta, iritsi baino kilometro bat lehenago, bideak berriro '
        'bira egiten duen, oraingoan iparralderantz, tarte bat mozteko.',
    'Sube después junto a un puñado de casitas de fin de semana, antes de dejarse caer de '
    'nuevo hacia <b>Iruzubieta</b>, entre caseríos, pastos y ganado. Es aquí donde el paisaje '
    'se abre: Bolibar asoma lejos, al suroeste, y más arriba se recorta el Oiz, con sus '
    'aerogeneradores y las antenas de la cima. Ya en el fondo, se cruza la carretera y se '
    'entra en el barrio, con un bar junto al camino.':
        'Orduan gora egiten du asteburuko etxetxoen ondotik, berriz ere '
        '<b>Iruzubieta</b>rantz jaisteko, baserri, larre eta abereen artean —Bolibar aldea '
        'urrunean agertzen dela hego-mendebalderantz eta, gorago, Oiz eolikoekin eta gailurreko '
        'antenekin. Behean, errepidea zeharkatu eta auzoan sartzen da, bidearen ondoan taberna '
        'bat dagoela.',
    'Desde Iruzubieta el camino se funde, durante un buen tramo, con el que siguen los '
    'peregrinos del Camino de Santiago del Norte hacia Bolibar —cuna de los antepasados de '
    'Simón Bolívar, con museo propio, camino ya de Ziortza y el Monasterio de Zenarruza, fuera '
    'de esta ruta. El descenso atraviesa una zona vistosa entre prados, con bastante ganado '
    'suelto y alguna cancela que conviene dejar cerrada, tal y como se encontró. Sin llegar a '
    'pisar Bolibar, se abandona ese camino para tirar a la izquierda, cuesta arriba, hacia el '
    'barrio de <b>Arta</b>. Desde allí, una pista forestal en ascenso constante conduce hasta '
    '<b>Gerea</b>, último tramo antes de cerrar el círculo de vuelta en Trabakua.':
        'Iruzubietatik aurrera bideak tarte batean bat egiten du Iparraldeko Donejakue Bideko '
        'erromesek Bolibar aldera jarraitzen dutenarekin —Simon Bolivarren arbasoen jaioterria, '
        'harentzako museo batekin, jada Ziortza eta Zenarruzako Monasteriorako bidean, ibilbide '
        'honetatik kanpo. Larre artean jaisten da lehenik, eremu polit batetik, abere ugarirekin '
        'eta bidean itxi behar den atetxoren batekin. Bolibarrera iritsi gabe, bide hori uzten '
        'da ezkerretara <b>Arta</b> auzorantz igotzen denari heltzeko. Handik, basoan barrena '
        'doan pista batek, gora eginez, <b>Gerea</b> auzoraino garamatza, Trabakuara itzuli eta '
        'zirkulua itxi aurretik.',
}

MENDIBIL = {
    'download="Trabakua Mendibil.gpx"': 'download="Trabakua Mendibil.gpx"',
    'alt="Foto ampliada del recorrido de Trabakua Mendibil"':
        'alt="Trabakua Mendibilgo ibilbidearen argazki handitua"',
    'alt="Moj&oacute;n en la cima del Mendibil, con el parque e&oacute;lico y el pueblo al fondo"':
        'alt="Mendibilgo gailurreko mugarria, parke eolikoa eta herria atzealdean"',
    'alt="Otra vista del moj&oacute;n de la cima, con los aerogeneradores del parque e&oacute;lico al fondo"':
        'alt="Gailurreko mugarriaren beste ikuspegi bat, parke eolikoaren aerosorgailuak atzealdean"',
    'alt="Vista de un caser&iacute;o en el valle, rodeado de prados y bosque"':
        'alt="Haraneko baserri baten ikuspegia, larreen eta basoen artean"',
    'alt="Vacas pastando junto al moj&oacute;n de la cima del Mendibil"':
        'alt="Behiak bazkan Mendibilgo gailurreko mugarriaren ondoan"',
    'alt="Un adulto y un ni&ntilde;o posando con una bota de vino en la cima del Mendibil, con '
    'las monta&ntilde;as del entorno al fondo"':
        'alt="Heldu bat eta haur bat ardo-zahato batekin posatzen Mendibilgo gailurrean, '
        'inguruko mendiak atzealdean"',
    'alt="Niebla entre los montes del entorno, con el parque e&oacute;lico del Oiz '
    'asomando entre las nubes"':
        'alt="Lainoa inguruko mendien artean, Oizeko parke eolikoa hodeien artetik '
        'ageri dela"',
    '<span>Sendero</span><span class="sep">/</span><span>Mendibil</span>':
        '<span>Bidezidorra</span><span class="sep">/</span><span>Mendibil</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    '<h1>Trabakua<br><em>Mendibil</em></h1>': '<h1>Trabakua<br><em>Mendibil</em></h1>',
    'Circuito desde Trabakua hasta la cima del Mendibil':
        'Zirkuitua Trabakuatik Mendibilgo gailurreraino',
    'Sale del Alto de Trabakua. Los primeros metros bajan &mdash;poco m&aacute;s de un '
    'kil&oacute;metro&mdash; hasta un cruce a la izquierda donde se deja el asfalto atr&aacute;s '
    'y arranca una cuesta que por un momento se pone intensa, pero corta. Arriba, en un cruce a '
    'los 2,5 km, aparecen las primeras indicaciones hacia el monte Mendibil: es la misma pista '
    'principal, de piedra, que sigue de frente hacia Asuntza y Urko &mdash;con la que se puede '
    'montar tambi&eacute;n la circular de <a href="urko.html">Trabakua, Asuntza y Urko</a>'
    '&mdash;, mientras que a la derecha se baja hacia Berano, Berano Txiki y, m&aacute;s lejos, '
    'Ermua.':
        'Trabakuko Goitik ateratzen da. Lehen metroek behera egiten dute &mdash;kilometro bat '
        'baino gehixeago&mdash; ezkerreko bidegurutze batera arte, non asfaltoa atzean utzi eta '
        'aldapa bati ekiten zaion, tarte batez gogorra baina laburra. Goian, 2,5 kilometrotan '
        'dagoen bidegurutzean, Mendibil menditarako lehen seinaleak agertzen dira: harrizko '
        'pista nagusi bera da, aurrera jarraitzen duena Asuntza eta Urkorantz &mdash;horrekin '
        '<a href="urko.html">Trabakua, Asuntza eta Urko</a> zirkuitua ere egin daiteke&mdash;, '
        'eskuinera berriz Berano, Berano Txiki eta, urrutixeago, Ermuarantz jaisten da.',
    'Se sigue esa pista principal unos metros hacia la izquierda hasta un roble gigante, con '
    'marcas blancas y amarillas en el tronco: ah&iacute;, justo detr&aacute;s del &aacute;rbol, '
    'se deja la pista de piedra para coger un camino de tierra. Sin abandonarlo en '
    'ning&uacute;n momento, ese camino lleva hasta la parte m&aacute;s alta, entre un grupo de '
    'eucaliptos.':
        'Pista nagusi horri jarraitzen zaio metro batzuk ezkerrera, haritz erraldoi batera '
        'arte, enborrean marka zuri-horiak dituena: han, zuhaitzaren atzean bertan, harrizko '
        'pista utzi eta lur-bide bati heltzen zaio. Bidea inoiz utzi gabe, lur-bide horrek '
        'gorenera eramaten gaitu, eukalipto talde baten artetik.',
    'En medio del eucaliptal se toma un sendero a la izquierda que baja ligeramente, con el '
    '<b>Mendibil</b> ya de frente, asomando como una peque&ntilde;a cumbre entre los pastos. '
    'M&aacute;s adelante se cruza una puerta de hierro, y apenas cinco minutos despu&eacute;s '
    'se corona la cima (km 2,98 &middot; 616 m).':
        'Eukaliptodian, ezkerreko bidezidor bati heltzen zaio, apur bat behera egiten duena, '
        '<b>Mendibil</b> aurrez aurre dugularik, larreen artean altxatzen den tontor txiki '
        'gisa. Aurrerago, burdinazko ate bat zeharkatzen da, eta bost minutu eskasera gailurra '
        'hartzen da (2,98 km &middot; 616 m).',
    'Desde arriba hay vistas al Oiz y a los montes del Duranguesado, hasta el Urko, y hacia la '
    'zona de Markina y la costa &mdash;con buen tiempo llega a verse el mar. La vuelta se hace '
    'por el mismo camino, aunque desde la cima tambi&eacute;n hay otras dos opciones: hacia el '
    'sureste, bajando hacia Arteta y su fuente, de la ruta de <a href="arteta.html">Trabakua, '
    'Mendibil, Olamendi y Arteta</a>, o hacia el noreste, bordeando la monta&ntilde;a por la '
    'misma pista que une Trabakua con Iturreta, de la ruta de <a href="iruzubieta.html">Trabakua, '
    'Iturreta e Iruzubieta</a>, pero en sentido contrario.':
        'Goitik Oizerako eta Durangaldeko mendietarako ikuspegiak daude, Urkoraino, eta Markina '
        'aldera eta kostaldera ere bai &mdash;eguraldi onarekin itsasoa ere ikusten da. '
        'Itzulera bide beretik egiten da, nahiz eta gailurretik beste bi aukera ere dauden: '
        'hego-ekialdera, Arteta eta bere iturrira jaisten dena, <a href="arteta.html">Trabakua, '
        'Mendibil, Olamendi eta Arteta</a> ibilbidekoa, edo ipar-ekialdera, mendia inguratuz, '
        'Trabakua eta Iturreta lotzen dituen pista beretik, <a href="iruzubieta.html">Trabakua, '
        'Iturreta eta Iruzubieta</a> ibilbidekoa, baina alderantziz.',
    '<h2>Senderismo</h2>': '<h2>Oinez</h2>',
    '6,08 km y +432 m de desnivel en un circuito corto hasta la cima del Mendibil, ideal '
    'para ir con ni&ntilde;os, coincidiendo el primer tramo con la ruta de <a '
    'href="urko.html">Trabakua, Asuntza y Urko</a>. No hay fuentes en la ruta, as&iacute; que conviene llevar agua '
    '&mdash;hay una en el bar de arriba de Trabakua, junto a los columpios.':
        '6,08 km eta +432 m-ko desnibela zirkuitu labur batean, Mendibilgo gailurreraino, '
        'haurrekin joateko aproposa, lehen tartea <a href="urko.html">Trabakua, Asuntza eta '
        'Urko</a> ibilbidearekin bat eginez. Ez dago iturririk ibilbidean, beraz ura eramatea komeni da &mdash;bat dago '
        'Trabakuako goiko tabernan, kulunken ondoan.',
}

ARTETA = {
    'download="Trabakua, Mendibil, Olamendi y Arteta.gpx"':
        'download="Trabakua, Mendibil, Olamendi eta Arteta.gpx"',
    'alt="Foto ampliada del recorrido de Trabakua, Mendibil, Olamendi y Arteta"':
        'alt="Trabakua, Mendibil, Olamendi eta Artetako ibilbidearen argazki handitua"',
    'alt="Vista de los montes del entorno con los aerogeneradores del Oiz al fondo, y el '
    'valle con caser&iacute;os en primer plano, entre pinos j&oacute;venes"':
        'alt="Inguruko mendien ikuspegia, Oizeko eolikoak atzealdean eta harana '
        'baserriekin aurrealdean, pinu gazteen artean"',
    'alt="Nubes iluminadas al atardecer sobre las monta&ntilde;as del entorno"':
        'alt="Ilunabarrean argiztatutako hodeiak inguruko mendien gainean"',
    'alt="V&eacute;rtice geod&eacute;sico en la cima de Olamendi, con el parque '
    'e&oacute;lico del Oiz al fondo entre nubes"':
        'alt="Gailur geodesikoa Olamendiko tontorrean, Oizeko parke eolikoa '
        'atzealdean hodeien artean"',
    'alt="Un caser&iacute;o en lo alto de una loma, rodeado de prados y bosque, con '
    'montes al fondo"':
        'alt="Baserri bat muino baten gainean, larre eta basoz inguratuta, mendiak '
        'atzealdean"',
    '<span>Mixta</span><span class="sep">/</span><span>Mendibil, Olamendi y Arteta</span>':
        '<span>Nahasia</span><span class="sep">/</span><span>Mendibil, Olamendi eta Arteta</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    '<h1>Trabakua, Mendibil,<br><em>Olamendi y Arteta</em></h1>':
        '<h1>Trabakua, Mendibil,<br><em>Olamendi eta Arteta</em></h1>',
    'Circuito desde Trabakua por Mendibil, Olamendi y Arteta':
        'Zirkuitua Trabakuatik, Mendibil, Olamendi eta Artetatik igarota',
    'Sale del Alto de Trabakua y sigue, hasta la cima del <b>Mendibil</b> (km 3,45 &middot; '
    '612 m), el mismo trazado que la ruta de <a href="mendibil.html">Trabakua '
    'Mendibil</a>. Desde la cima hay dos formas de bajar de vuelta a Trabakua '
    '&mdash;hacia el sureste, por Arteta y su fuente, o hacia el noreste, bordeando la '
    'monta&ntilde;a por la misma pista que la ruta de <a href="iruzubieta.html">Trabakua, '
    'Iturreta e Iruzubieta</a>, en sentido contrario&mdash;, y esta ruta las enlaza las dos.':
        'Trabakuko Goitik ateratzen da, eta <b>Mendibil</b>go gailurreraino (3,45 km '
        '&middot; 612 m) <a href="mendibil.html">Trabakua Mendibil</a> ibilbidearen '
        'trazadu bera jarraitzen du. Gailurretik Trabakuara jaisteko bi bide daude '
        '&mdash;hego-ekialdera, Arteta eta bere iturritik, edo ipar-ekialdera, mendia '
        'inguratuz, <a href="iruzubieta.html">Trabakua, Iturreta eta Iruzubieta</a> '
        'ibilbidearen pista beretik, alderantziz&mdash;, eta ibilbide honek biak lotzen '
        'ditu.',
    'Baja hacia el sureste hasta <b>Olamendi</b> (km 3,88 &middot; 596 m), dejando '
    'atr&aacute;s las pistas m&aacute;s conocidas de la zona para meterse por caminos '
    'y sendas menos transitados.':
        'Hego-ekialdera jaisten da <b>Olamendi</b>raino (3,88 km &middot; 596 m), '
        'inguruko pista ezagunenak atzean utzita, gutxiago ibilitako bide eta '
        'bidezidorretan sartzeko.',
    'De camino se pasa junto a la <b>Fuente de Arteta</b> (km 5,1 &middot; 458 m), antes '
    'de llegar a la propia zona de <b>Arteta</b> (km 5,7 &middot; 505 m), donde una '
    'ermita en ruinas queda escondida entre el bosque que la ha ido cubriendo. Desde '
    'ah&iacute; se vuelve a subir hasta la cima del Mendibil, y esta vez se baja por el '
    'otro lado, por la misma pista que la ruta de <a href="iruzubieta.html">Trabakua, '
    'Iturreta e Iruzubieta</a>, pero en sentido contrario, hasta cerrar el '
    'c&iacute;rculo de vuelta a Trabakua.':
        'Bidean, <b>Artetako iturri</b>aren ondotik pasatzen da (5,1 km &middot; 458 m), '
        '<b>Arteta</b>ko eremura bertara iritsi aurretik (5,7 km &middot; 505 m), non '
        'ermita hondatu bat basoak estalita ezkutatzen den. Hortik berriro igotzen da '
        'Mendibilgo gailurreraino, eta oraingoan beste aldetik jaisten da, '
        '<a href="iruzubieta.html">Trabakua, Iturreta eta Iruzubieta</a> ibilbidearen '
        'pista beretik, alderantziz, Trabakuara bueltan zirkulua itxi arte.',
    '<title>Fuente de Arteta': '<title>Artetako iturria',
    '<span class="num">3</span>Fuente de Arteta': '<span class="num">3</span>Artetako iturria',
    '<h2>Senderismo</h2>': '<h2>Oinez</h2>',
    '11,38 km y +565 m de desnivel en un circuito largo, pensado para quien quiera '
    'conocer rincones escondidos y pistas o caminos distintos de los habituales por la '
    'zona de Mendibil y Arteta. La Fuente de Arteta sirve de punto de agua a mitad de '
    'recorrido.':
        '11,38 km eta +565 m-ko desnibela zirkuitu luze batean, ohikoak ez diren txoko '
        'ezkutuak eta pista edo bide ezberdinak ezagutu nahi dituenarentzat, Mendibil '
        'eta Arteta inguruan. Artetako iturriak ur-puntu gisa balio du ibilbidearen '
        'erdialdean.',
}

GOITA = {
    '<title>Polígono de Anbre · 2,39 km · 229 m</title>':
        '<title>Anbre industrialdea · 2,39 km · 229 m</title>',
    '<span class="num">1</span>Polígono de Anbre':
        '<span class="num">1</span>Anbre industrialdea',
    '<span>Carretera y pista</span><span class="sep">/</span><span>Goita</span>':
        '<span>Errepidea eta pista</span><span class="sep">/</span><span>Goita</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    '<h1>Trabakua<br><em>paseo por el barrio Goita</em></h1>':
        '<h1>Trabakua<br><em>Goita auzoko paseoa</em></h1>',
    'Paseo circular por el barrio Goita desde Trabakua':
        'Ibilbide zirkularra Goita auzotik, Trabakuatik',
    'alt="Vistas al atardecer sobre los valles y montes del entorno, con un mont&oacute;n de '
    'piedras en primer plano"':
        'alt="Ilunabarreko ikuspegiak inguruko haran eta mendietara, aurrean harri-pila '
        'batekin"',
    'alt="Foto ampliada del recorrido de Trabakua, paseo por el barrio Goita"':
        'alt="Trabakua, Goita auzoko paseo ibilbidearen argazki handitua"',
    'alt="Pista de cemento entre &aacute;rboles, en un tramo con sombra"':
        'alt="Porlanezko pista zuhaitzen artean, itzalpeko tarte batean"',
    'alt="Ermita de piedra con espada&ntilde;a y tejado de teja, junto a la carretera"':
        'alt="Harrizko ermita espadaina eta teilatu gorriarekin, errepidearen ondoan"',
    'alt="Camino junto a una valla, con un caser&iacute;o al fondo entre &aacute;rboles"':
        'alt="Bidea hesi baten ondoan, atzealdean baserri bat zuhaitzen artean"',
    'alt="Vista del barrio de Goita, con caser&iacute;os y prados entre el bosque"':
        'alt="Goita auzoaren ikuspegia, baserri eta belardiekin basoaren artean"',
    'alt="Una vaca junto a una valla de alambre de espino, con monta&ntilde;as al fondo"':
        'alt="Behi bat arantzazko hesi baten ondoan, mendiak atzealdean dituela"',
    'alt="Ermita de San Mart&iacute;n de Apoita, con su peque&ntilde;a espada&ntilde;a de piedra, y '
    'los aerogeneradores del Oiz al fondo"':
        'alt="Apoitako San Martin ermita, harrizko espadaina txikiarekin, eta Oizeko '
        'aerosorgailuak atzealdean"',
    'alt="Vistas amplias sobre los valles del entorno, con una monta&ntilde;a de doble pico al '
    'fondo y nubes alargadas en el cielo"':
        'alt="Inguruko haranen ikuspegi zabalak, bi tontorreko mendi bat atzealdean eta '
        'hodei luzatuak zeruan"',
    'alt="Casas del valle entre prados y bosque, con nubes de tormenta acerc&aacute;ndose"':
        'alt="Haraneko etxeak belardi eta basoen artean, ekaitz-hodeiak hurbiltzen"',
    'download="Trabakua paseo barrio Goita.gpx"':
        'download="Trabakua, Goita auzoko paseoa.gpx"',
    '<span class="v">Carretera y pista</span>': '<span class="v">Errepidea eta pista</span>',
    'Salimos del bar de Trabakua y cruzamos el puente de madera que pasa sobre la autovía. Nada más cruzarlo, comenzamos a bajar por la carretera asfaltada en dirección al barrio de <b>Goita</b>, donde empiezan a aparecer las primeras vistas de la ruta.':
        'Trabakuko tabernatik abiatuko gara eta autobidearen gainetik igarotzen den egurrezko zubia zeharkatuko dugu. Zubia igaro bezain laster, asfaltatutako errepidetik jaisten hasiko gara <b>Goita</b> auzorantz. Bertan hasiko gara ibilbideko lehen bistak ikusten.',
    'A nuestra derecha podemos ver la zona de <b>Osma</b>, con sus barrios y caseríos. De frente empezamos a distinguir la ermita de <b>San Juan de Goita</b>, hacia la que nos dirigimos. Junto a ella se conservan restos de una antigua necrópolis medieval, documentada en el siglo XI. La ermita ha estado siempre muy ligada a los vecinos del barrio, que tradicionalmente se han organizado en auzolan para cuidarla y mantener también sus alrededores.':
        'Gure eskuinean <b>Osma</b> ingurua ikusiko dugu, bertako auzo eta baserriekin. Aurrez aurre <b>Goitako San Juan</b> ermita agertzen da, guk jarraitzen dugun norabide berean. Ermitaren inguruan Erdi Aroko nekropoli baten aztarnak daude, XI. mendean dokumentatuak. Betidanik egon da ermita auzoko bizilagunei lotuta, eta tradizioz auzolanean aritu izan dira ermita eta ingurua zaintzen eta mantentzen.',
    'A nuestra izquierda tenemos la zona de Arteta, con sus caseríos y prados. Continuamos bajando por la carretera, disfrutando tranquilamente del paisaje.':
        'Ezkerrean, berriz, Arteta ingurua izango dugu, bertako baserri eta belardiekin. Errepidean behera jarraituko dugu, paisaiaz lasai gozatzen.',
    'Tras aproximadamente 2,5 kilómetros, llegamos a la parte más baja del recorrido, junto al polígono de <b>Anbre</b>. Aquí debemos estar atentos: giramos a la derecha y continuamos por el polígono durante unos 300 metros.':
        'Gutxi gorabehera 2,5 kilometro egin ondoren, ibilbideko punturik baxuenera iritsiko gara, <b>Anbre</b> industrialdearen ondoan. Hemen adi egon behar dugu: eskuinera biratu eta industrialdetik jarraituko dugu 300 metro inguru.',
    'En plena curva encontraremos, también a nuestra derecha, una carretera de barrio más estrecha. El cruce está señalizado con indicaciones hacia varios caseríos, entre ellos <b>Amesti</b> y <b>Boliña</b>. Tomamos esta carretera y avanzamos unos 200 metros.':
        'Bihurgune betean, gure eskuinean, auzoko errepide estuago bat aurkituko dugu. Bidegurutzea hainbat baserritara joateko seinaleekin markatuta dago, besteak beste <b>Amesti</b> eta <b>Boliña</b>. Errepide hori hartu eta 200 metro inguru egingo ditugu.',
    'Llegamos a un nuevo cruce, donde tomamos el camino de la izquierda. El asfalto deja paso a una pista de gravilla que nos lleva hasta el caserío Amesti. Pasamos junto a él y continuamos hacia arriba hasta encontrarnos de nuevo con una carretera de barrio.':
        'Beste bidegurutze batera iristean, ezkerreko bidea hartuko dugu. Asfaltoa amaitu eta hartxintxarrezko pista batean sartuko gara. Pista horrek Amesti baserrira eramango gaitu. Baserriaren ondotik igaro eta gorantz jarraituko dugu, berriro auzoko errepide batekin topo egin arte.',
    'Cuando llevamos unos 3,2 kilómetros, llegamos a una carretera de barrio que viene de Mallabia y sube hacia Trabakua. Giramos a la derecha y continuamos por esta carretera de cemento en dirección a Trabakua.':
        'Gutxi gorabehera 3,2 kilometro daramatzagunean, Mallabitik datorren eta Trabakurantz igotzen den auzoko errepide batera iritsiko gara. Eskuinerantz biratu eta porlanezko errepide horretatik jarraituko dugu, Trabaku norabidean.',
    'Mientras subimos, a nuestra derecha volvemos a tener vistas hacia el barrio de Goita, por donde hemos bajado anteriormente hacia el polígono. Ahora lo vemos desde otra perspectiva, con sus caseríos, sus prados y todo el paisaje que los rodea.':
        'Igotzen goazen bitartean, eskuinean Goita auzoa ikusiko dugu berriro, lehenago industrialderantz jaisteko zeharkatu dugun ingurua. Oraingoan beste ikuspegi batetik ikusiko dugu, bertako baserri, belardi eta inguruko paisaiarekin.',
    'Continuamos subiendo por la zona de <b>Apoita</b>, pasando junto a la ermita de <b>San Martín de Apoita</b>, situada en una pequeña loma junto al caserío San Martín. Una pequeña ermita con siglos de historia, en la que antiguamente también se celebraban romerías.':
        '<b>Apoita</b> ingurutik gora jarraituko dugu, <b>Apoitako San Martin</b> ermitaren ondotik igaroz. Muino txiki batean dago ermita, San Martin baserriaren ondoan. Mendeetako historia duen ermita txiki bat da, eta garai batean erromeriak ere egiten ziren bertan.',
    'Seguimos ascendiendo hasta salir finalmente a la carretera general, ya cerca de Trabakua.':
        'Gorantz jarraituko dugu, azkenean errepide nagusira atera arte, Trabakutik nahiko gertu.',
    'Al llegar a la carretera general, giramos a la derecha y continuamos por el arcén, con mucha precaución, durante aproximadamente un kilómetro y poco hasta regresar a Trabakua.':
        'Errepide nagusira iristean, eskuinera biratu eta bazterbidetik jarraituko dugu, kontu handiz, kilometro bat pasatxo eginez Trabakura itzuli arte.',
    'Este último tramo nos permite echar la vista atrás y ver, a nuestra derecha, buena parte de todo lo que hemos recorrido. Se abren ante nosotros los dos valles y, al fondo, montañas como Aizkorri, <a href="egoarbitza.html">Egoarbitza</a> y <a href="urko.html">Urko</a>, que completan unas bonitas vistas antes de terminar.':
        'Azken zati honetan atzera begiratu eta gure eskuinean egin dugun ibilbidearen zati handi bat ikusteko aukera izango dugu. Bi haranak ikusiko ditugu eta, urrunean, Aizkorri, <a href="egoarbitza.html">Egoarbitza</a> eta <a href="urko.html">Urko</a> bezalako mendiak, ibilbidea amaitu aurretik ikuspegi ederra eskainiz.',
    'Es una ruta corta y sencilla, apta para prácticamente todo el mundo: ideal para dar un paseo, disfrutar del paisaje y conocer un poco mejor la zona. Se puede hacer tanto andando como en bici (incluida e-bike), pero mejor a pie, para disfrutar de las vistas con calma. Buena excusa, además, para terminar donde se empieza: en el bar de Trabakua, con un buen pintxo.':
        'Ibilbide laburra, erraza eta ia edonork egiteko modukoa da, paseotxo bat eman, paisaiaz gozatu eta ingurua pixka bat hobeto ezagutzeko aproposa. Oinez zein bizikletaz egin daiteke (e-bikez barne), baina hobe oinez, ikuspegiez lasaiago gozatzeko. Eta, bide batez, gosea egiteko eta amaieran hasierako lekura itzultzeko aitzakia ezin hobea: Trabakuko tabernan pintxo eder bat jatera.',
}

HIRUTXIKIAK = {
    # eyebrow / h1 / full-name
    '<span>Sendero y pista</span><span class="sep">/</span><span>Urko, Oiz y Egoarbitza</span>':
        '<span>Bidezidorra eta pista</span><span class="sep">/</span><span>Urko, Oiz eta Egoarbitza</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    '<h2>Senderismo &middot; Trail running</h2>': '<h2>Oinez &middot; Trail running</h2>',
    '<h1>Hiru Txikiak<br><em>Urko, Oiz y Egoarbitza</em></h1>':
        '<h1>Hiru Txikiak<br><em>Urko, Oiz eta Egoarbitza</em></h1>',
    '<p class="full-name">Urko, Oiz y Egoarbitza desde Ermua</p>':
        '<p class="full-name">Urko, Oiz eta Egoarbitza Ermuatik</p>',

    # elev markers / legend (place names are shared elsewhere; only the
    # Spanish words need translating here)
    'Collado de Asuntza': 'Asuntzako lepoa',
    'Presa de Aixola': 'Aixolako presa',
    '<title>Trabakua (1&#170; avituallamiento) &middot; 10,69 km &middot; 411 m</title>':
        '<title>Trabakua (1. hornidura-postua) &middot; 10,69 km &middot; 411 m</title>',

    # hero + gallery photos
    'alt="Cruz de hierro y v&eacute;rtice geod&eacute;sico en una cima, con aerogeneradores cerca y un banco de nubes al fondo"':
        'alt="Burdinazko gurutzea eta bertize geodesikoa gailur batean, aerosorgailuak gertu eta hodei-banku bat atzealdean"',
    'alt="Se&ntilde;al de la cima de Urko (791 m), con aves volando y las monta&ntilde;as al fondo entre la calima"':
        'alt="Urko gailurreko seinalea (791 m), hegaztiak hegan eta mendiak atzealdean, lausotasunaren artean"',
    'alt="Corredor con dorsal de carrera en una cresta herbosa, con el cielo nuboso al fondo"':
        'alt="Lasterketako dortsala daraman korrikalaria kresta belartsu batean, zeru hodeitsua atzealdean"',
    'alt="V&eacute;rtice geod&eacute;sico en una cima, con bastones de trekking apoyados en las rocas y monta&ntilde;as al fondo"':
        'alt="Bertize geodesikoa gailur batean, trekking bastoiak harkaitzen kontra bermatuta eta mendiak atzealdean"',
    'alt="Vistas a las monta&ntilde;as calizas del Duranguesado, con un pueblo en el valle al fondo"':
        'alt="Durangaldeko mendi kararrien ikuspegia, herri bat haranean atzealdean"',
    'alt="Cresta verde con los aerogeneradores del parque e&oacute;lico del Oiz al fondo"':
        'alt="Kresta berdea, Oizeko parke eolikoaren aerosorgailuekin atzealdean"',
    'alt="Llegada a meta por la alfombra roja entre confeti, de la mano de un ni&ntilde;o, con el p&uacute;blico animando a los lados"':
        'alt="Helmugara alfonbra gorritik iristen, konfetien artean, haur bat eskutik hartuta, jendea alboetan animatzen"',
    'alt="Baliza verde de sendero entre rocas, con una hilera de aerogeneradores en la cresta y el valle al fondo"':
        'alt="Bidearen baliza berdea harkaitzen artean, kresta-lerroan aerosorgailu ilara batekin eta harana atzealdean"',
    'alt="Foto ampliada del recorrido de Hiru Txikiak"':
        'alt="Hiru Txikiak ibilbidearen argazki handitua"',

    # body copy
    'La <a href="https://hirutxikiak.com/" target="_blank" rel="noopener noreferrer">Hiru Txikiak Trail</a> es una carrera de trail organizada por el club Korrikazaleak, con salida y meta en Ermua, que sube a tres cumbres muy conocidas de la zona: <b><a href="urko.html">Urko</a></b>, <b><a href="oiz.html">Oiz</a></b> y <b><a href="egoarbitza.html">Egoarbitza</a></b>. Es una carrera dura y exigente &mdash;m&aacute;s de 40 km y m&aacute;s de 2.000 m de desnivel positivo&mdash; en la que, desde casi el principio, toca subir.':
        '<a href="https://hirutxikiak.com/" target="_blank" rel="noopener noreferrer">Hiru Txikiak Trail</a> lasterketa gogor eta zorrotza da, Korrikazaleak klubak antolatua, Ermuan hasi eta amaitzen dena, eskualdeko hiru gailur ezagunetara igotzen gaituena: <b><a href="urko.html">Urko</a></b>, <b><a href="oiz.html">Oiz</a></b> eta <b><a href="egoarbitza.html">Egoarbitza</a></b>. 40 km baino gehiagoko eta 2.000 m-tik gorako desnibel positiboa duen lasterketa da, eta ia hasieratik gorantz egin behar da.',
    'Desde Ermua, el primer objetivo es <b>Urko</b> (km 3,38 &middot; 792 m), la primera cima del d&iacute;a. Una vez arriba empieza el descenso, pasando por el <b>Collado de Asuntza</b> (km 6,14 &middot; 497 m), para continuar hacia <b>Trabakua</b> (km 10,69), donde se encuentra el primer avituallamiento.':
        'Ermutik irteten gara, eta eguneko lehen helburua <b>Urko</b> da (km 3,38 &middot; 792 m), lehen gailurra. Behin goian, jaitsierari ekiten diogu <b>Asuntzako Lepo</b>tik igarota (km 6,14 &middot; 497 m), <b>Trabakua</b>rantz jarraitzeko (10,69. km), non baitago lehen hornidura-postua.',
    'Y aqu&iacute; empieza una de las partes serias del recorrido. Desde Trabakua se ataca la subida hacia <b>Zengotitagane</b> (km 12,32 &middot; 809 m), una subida durísima en la que toca encontrar un ritmo y no quemarse, porque queda much&iacute;simo por delante. Superada esta parte, se contin&uacute;a hacia <b>Oiz</b> (km 15,78 &middot; 1.027 m) pasando por Iturzuri.':
        'Eta hemen hasten da ibilbideko zatirik serioenetako bat. Trabakuatik <b>Zengotitagane</b>rako igoerari ekiten diogu (km 12,32 &middot; 809 m); igoera oso gogorra da, erritmoa aurkitu eta gehiegi ez behartzeko modukoa, oraindik bide luzea baitago aurretik. Zati hori gaindituta, <b>Oiz</b>erantz jarraitzen dugu (km 15,78 &middot; 1.027 m), Iturzuritik igaroz.',
    'Llegar a Oiz da una sensaci&oacute;n especial: segunda cima completada, y por un momento parece que la carrera ya est&aacute; dominada. Nada m&aacute;s lejos de la realidad.':
        'Oizera iristeak sentsazio berezia ematen du: bigarren gailurra eginda dago, eta une batez badirudi lasterketa kontrolpean dugula. Baina ezer ez dago errealitatetik urrunago.',
    'Desde Oiz toca bajar de nuevo hacia la zona de <b>Zengotitagane</b> (km 20,04 &middot; 738 m), donde est&aacute; el segundo avituallamiento, para continuar despu&eacute;s en direcci&oacute;n a Areitio y la <b>Presa de Aixola</b> (km 30,30 &middot; 311 m).':
        'Oizetik berriz <b>Zengotitagane</b> aldera jaitsi behar da (km 20,04 &middot; 738 m); han dago bigarren hornidura-postua. Ondoren, Areitio eta <b>Aixolako presa</b>ren norabidean jarraitzen dugu (km 30,30 &middot; 311 m).',
    'Sobre el papel puede parecer un tramo m&aacute;s llevadero, al no tener las grandes subidas anteriores, pero enga&ntilde;a: se hace muy largo. Los kil&oacute;metros empiezan a pesar, y es aqu&iacute; donde se empieza a notar de verdad el estado f&iacute;sico. No hay una subida brutal que pare en seco, pero el terreno va desgastando poco a poco.':
        'Paperean tarte eramangarriagoa dirudi, aurreko igoera handirik ez duelako, baina engainagarria da: oso luzea egiten da. Kilometroak nabaritzen hasten dira, eta hemen hasten da benetan norberaren egoera fisikoa agerian geratzen. Ez dago bat-batean geldiarazten zaituen igoera bortitzik, baina lurrak pixkanaka higatzen zaitu.',
    'En la Presa de Aixola est&aacute; el tercer avituallamiento, y toca afrontar la &uacute;ltima gran subida del d&iacute;a: <b>Egoarbitza</b> (km 33,17 &middot; 731 m).':
        '<b>Aixolako presa</b>n dago hirugarren hornidura-postua, eta eguneko azken igoera handiari aurre egitea tokatzen da: <b>Egoarbitza</b> (km 33,17 &middot; 731 m).',
    'Arriba, mucha alegr&iacute;a: las tres cimas de la Hiru Txikiak est&aacute;n completadas &mdash;Urko, Oiz y Egoarbitza&mdash;. La cabeza empieza a decir que ya est&aacute;, que solo queda bajar hasta Ermua. Pero todav&iacute;a no.':
        'Goian, poza handia: Hiru Txikiak-eko hiru gailurrak osatuta daude &mdash;Urko, Oiz eta Egoarbitza&mdash;. Buruak esaten hasten dizu amaitu dela, Ermura jaistea besterik ez dela geratzen. Baina oraindik ez.',
    'Hay que descender de nuevo hacia la presa y, desde all&iacute;, tirar hacia Ermua con lo que queden de piernas. Despu&eacute;s de tantos kil&oacute;metros y desnivel, cualquier peque&ntilde;o repecho se nota mucho m&aacute;s de lo que deber&iacute;a. Y todav&iacute;a queda una &uacute;ltima sorpresa: pasada la zona del barrio de Eitzaga, aparece una peque&ntilde;a subida final que, a estas alturas, tiene poco de peque&ntilde;a.':
        'Berriro presarantz jaitsi behar da, eta handik Ermurantz abiatu, hanketan geratzen zaigun guztiarekin. Hainbeste kilometro eta desnibel egin ondoren, edozein aldapatxo askoz gehiago nabaritzen da. Eta oraindik azken sorpresa bat geratzen da: Eitzaga auzoaren ingurua igaro ondoren, azken igoera txiki hori agertzen da, eta une horretan txikia baino gutxiago du.',
    'Superada esa &uacute;ltima subida, solo queda apretar los dientes y tirar para abajo hasta la meta, en Ermua.':
        'Gaindituta, orain bai: Ermua usaintzen dugu, helmuga gertu dagoela badakigu, eta hortzak estutu eta daukagun guztiarekin beherantz egitea besterik ez da geratzen.',
    '<b>Urko. Oiz. Egoarbitza.</b> Tres cumbres y un recorrido que no termina hasta que cruzas la meta.':
        '<b>Urko. Oiz. Egoarbitza.</b> Hiru gailur eta helmuga zeharkatu arte amaitzen ez den ibilbidea.',

    # parada
    'Aunque no empieza ni termina en Trabakua, la ruta s&iacute; pasa por all&iacute;; y, sobre todo, es una carrera en la que tambi&eacute;n tomamos parte, as&iacute; que ten&iacute;a que estar aqu&iacute;. 43,91 km y +2.291 m de desnivel en un solo circuito, con tres subidas importantes (Urko, Oiz y Egoarbitza) y salida y llegada en Ermua. Es el recorrido real de la Hiru Txikiak Trail, organizada por el club Korrikazaleak, as&iacute; que tambi&eacute;n sirve como referencia para quien quiera prepararla. Los avituallamientos de Trabakua, Zengotitagane y la presa de Aixola solo existen el d&iacute;a de la carrera; fuera de ese d&iacute;a hay fuente en el Alto de Trabakua, Iturzuri, el barrio de Zengotita, el barrio de Goierri, en la presa de Aixola (con un peque&ntilde;o desv&iacute;o) y en el barrio de Eitzaga.':
        'Nahiz eta Trabakuan hasi ez eta amaitu ere ez, ibilbideak Trabakuatik igarotzen da; eta, batez ere, guk ere parte hartzen dugun lasterketa bat da, beraz hemen egon behar zuen. 43,91 km eta +2.291 m-ko desnibela zirkuitu bakar batean, hiru igoera garrantzitsurekin (Urko, Oiz eta Egoarbitza) eta Ermuan irten eta amaituz. Hiru Txikiak Trail lasterketaren benetako ibilbidea da, Korrikazaleak klubak antolatua, beraz prestatu nahi duenarentzat erreferentzia ere bada. Trabakuako, Zengotitaganeko eta Aixolako presako hornidura-postuak lasterketa egunean bakarrik daude; egun horretatik kanpo, iturria dago Trabakuako Altoan, Iturzurin, Zengotita auzoan, Goierri auzoan, Aixolako presan (desbideratze txiki batekin) eta Eitzaga auzoan.',

    # map + footer
    'data-marker-title="Ermua (salida y llegada)"':
        'data-marker-title="Ermua (irteera eta helmuga)"',
    'Circuito — vuelve al mismo punto': 'Zirkuitua — puntu berera itzultzen da',
}

ZALDIBAR = {
    # hero
    '<span>Carretera, pista y sendero</span><span class="sep">/</span><span>Aixola, Elgeta y Zaldibar</span><span class="sep">/</span><span>Circuito</span>':
        '<span>Errepidea, pista eta bidezidorra</span><span class="sep">/</span><span>Aixola, Elgeta eta Zaldibar</span><span class="sep">/</span><span>Zirkuitua</span>',
    '<h1>Trabakua, Aixola<br><em>y Berriz</em></h1>':
        '<h1>Trabakua, Aixola<br><em>eta Berriz</em></h1>',
    '<p class="full-name">Circuito en e-bike desde Trabakua por Aixola, Elgeta y Zaldibar hasta Berriz</p>':
        '<p class="full-name">Zirkuitua e-bikez Trabakuatik, Aixola, Elgeta eta Zaldibartik igarota Berrizeraino</p>',

    # elevation profile markers + legend (used twice: hero chart and map section)
    '<title>Collado de Asuntza &middot; 5,2 km &middot; 499 m</title>':
        '<title>Asuntzako lepoa &middot; 5,2 km &middot; 499 m</title>',
    '<title>Presa de Aixola &middot; 13,1 km &middot; 308 m</title>':
        '<title>Aixolako presa &middot; 13,1 km &middot; 308 m</title>',
    '<title>Ermita de San Juan &middot; 40,0 km &middot; 412 m</title>':
        '<title>San Juan ermita &middot; 40,0 km &middot; 412 m</title>',
    '<span class="elev-legend-item"><span class="num">1</span>Collado de Asuntza</span> '
    '<span class="elev-legend-item"><span class="num">2</span>Presa de Aixola</span> '
    '<span class="elev-legend-item"><span class="num">3</span>Elgeta</span> '
    '<span class="elev-legend-item"><span class="num">4</span>Berriz</span> '
    '<span class="elev-legend-item"><span class="num">5</span>Ermita de San Juan</span>':
        '<span class="elev-legend-item"><span class="num">1</span>Asuntzako lepoa</span> '
        '<span class="elev-legend-item"><span class="num">2</span>Aixolako presa</span> '
        '<span class="elev-legend-item"><span class="num">3</span>Elgeta</span> '
        '<span class="elev-legend-item"><span class="num">4</span>Berriz</span> '
        '<span class="elev-legend-item"><span class="num">5</span>San Juan ermita</span>',

    # photos
    'alt="La presa de Aixola entre los &aacute;rboles, con la niebla asomando sobre el agua"':
        'alt="Aixolako presa zuhaitzen artean, lainoa uraren gainean agertzen"',
    'alt="Foto ampliada del recorrido de Trabakua, Aixola y Berriz"':
        'alt="Trabakua, Aixola eta Berriz ibilbidearen argazki handitua"',
    'alt="Ovejas pastando en un prado, con un pueblo del valle al fondo, al atardecer"':
        'alt="Ardiak larrean, haranaren erdiko herria atzealdean, ilunabarrean"',
    'alt="Farola encendida junto a una calle de un barrio, ya de noche"':
        'alt="Farol piztua auzoko kale baten ondoan, gauean"',
    'alt="Zona deportiva y parque infantil iluminados de noche, junto a un colegio"':
        'alt="Kirol-gunea eta haurren parkea gauean argiztatuta, ikastetxe baten ondoan"',
    'alt="La presa de Aixola en un d&iacute;a soleado, con la torre de la toma de agua asomando sobre el embalse"':
        'alt="Aixolako presa egun eguzkitsu batean, ur-hartuneko dorrea urtegiaren gainean ageri dela"',

    # wikiloc / gpx
    'download="Trabakua, Aixola y Berriz.gpx"':
        'download="Trabakua, Aixola eta Berriz.gpx"',

    # body copy
    'Salimos de <b>Trabakua</b> y comenzamos bajando, como tantas otras veces, en direcci&oacute;n Urko &ndash; Asuntza &ndash; Iturreta. Este primer tramo coincide con otras rutas de la zona y seguimos el recorrido habitual hasta llegar a <b>Asuntza</b> (5,2 km &middot; 499 m).':
        '<b>Trabakua</b>tik irtengo gara eta, ohiko bidetik, beherantz hasiko gara Urko &ndash; Asuntza &ndash; Iturreta norabidean. Lehen zati hau inguruko beste ibilbide batzuekin bat dator, eta ohiko bideari jarraituko diogu <b>Asuntza</b>ra iritsi arte (5,2 km &middot; 499 m).',
    'Aqu&iacute; dejamos el camino conocido. Junto a los huertos giramos a la derecha y comenzamos a bajar hacia el barrio de <b>Berano Txiki</b>. Al llegar a los caser&iacute;os de Berano, esta vez giramos a la izquierda y continuamos perdiendo altura en direcci&oacute;n a Ermua, pasando por la zona de la cantera.':
        'Hemen utziko dugu ezagutzen dugun bidea. Baratzeen ondoan eskuinera hartu eta <b>Berano Txiki</b> auzorantz jaisten hasiko gara. Beranoko baserrietara iristean, oraingoan ezkerrera egingo dugu eta Ermua aldera jaisten jarraituko dugu, harrobiaren ingurutik igaroz.',
    'Un poco m&aacute;s adelante de la cantera salimos a la carretera general, donde giramos a la izquierda para atravesar pr&aacute;cticamente todo <b>Ermua</b>. Ya a la salida del pueblo, cerca de San Lorenzo, giramos a la derecha y comenzamos a subir en direcci&oacute;n a Eitzaga.':
        'Harrobia pasa eta pixka bat aurrerago errepide nagusira irtengo gara. Han ezkerrera hartu eta ia <b>Ermua</b> osoa zeharkatuko dugu. Herriaren irteeran, San Lorentzo inguruan, eskuinera hartu eta Eitzaga aldera igotzen hasiko gara.',
    'Al llegar a <b>Eitzaga</b> encontramos la primera fuente de la ruta, un buen punto para aprovechar y coger agua antes de continuar hacia la presa de Aixola.':
        '<b>Eitzaga</b>ra iristean ibilbideko lehen iturria aurkituko dugu. Leku aproposa da ura hartzeko, Aixolako urtegirantz jarraitu aurretik.',
    'Un poco m&aacute;s adelante, despu&eacute;s de atravesar el t&uacute;nel, subimos unos metros y tomamos, a mano derecha, una pista de cemento que poco a poco se convierte en un peque&ntilde;o camino de piedra. De esta manera evitamos continuar por la carretera general. Es un camino lateral, utilizado habitualmente por paseantes y ciclistas, que nos lleva directamente hasta la <b>presa de Aixola</b> (13,1 km &middot; 308 m).':
        'Pixka bat aurrerago, tunela zeharkatu ondoren, metro batzuk igo eta eskuinean porlanezko pista bat hartuko dugu. Aurrera egin ahala, pista harrizko bidexka bihurtzen da. Horrela, errepide nagusitik igotzea saihestuko dugu. Oinezkoek eta txirrindulariek sarri erabiltzen duten alboko bidea da, eta zuzenean <b>Aixolako urtegi</b>ra eramango gaitu (13,1 km &middot; 308 m).',
    'Una vez en la presa de Aixola, comenzamos a bordearla dej&aacute;ndola a nuestra derecha. A los pocos metros encontramos otra fuente. Cruzamos la presa y comenzamos la subida hacia Elgeta. Nada m&aacute;s afrontar las primeras rampas, a mano izquierda, encontraremos una nueva fuente que sale directamente de la pared de la monta&ntilde;a, un buen punto para volver a coger agua antes de continuar la subida.':
        'Aixolako urtegira iristean, urtegia gure eskuinean utzita inguratzen hasiko gara. Metro gutxira beste iturri bat aurkituko dugu. Presa zeharkatu eta Elgeta aldera igotzen hasiko gara. Lehen aldapak hartzearekin batera, ezkerrean, mendi-hegaleko hormatik zuzenean ateratzen den beste iturri bat aurkituko dugu. Leku ona da berriro ura hartzeko, igoerarekin jarraitu aurretik.',
    'Seguimos ganando altura en direcci&oacute;n a <b>Elgeta</b>, aunque unos metros antes de alcanzar el pueblo giramos a la izquierda. La intenci&oacute;n es alargar un poco el recorrido y, de paso, disfrutar de uno de los tramos m&aacute;s bonitos de la ruta.':
        '<b>Elgeta</b> aldera altuera irabazten jarraituko dugu, baina herrira iritsi baino metro batzuk lehenago ezkerrera egingo dugu. Helburua ibilbidea pixka bat luzatzea da eta, bide batez, ibilbideko zatirik politenetako batez gozatzea.',
    'Damos la vuelta por la zona de <b>Goiko Mendia</b>, enlazando peque&ntilde;os senderos muy agradables, antes de bajar finalmente hacia Elgeta (20,4 km &middot; 474 m). Atravesamos el pueblo y podemos aprovechar nuevamente para coger agua en la fuente situada junto al polideportivo y el front&oacute;n.':
        '<b>Goiko Mendia</b> ingurutik bira egingo dugu, bidexka politak lotuz, eta ondoren Elgeta aldera jaitsiko gara (20,4 km &middot; 474 m). Herria zeharkatuko dugu, eta berriro ura hartzeko aukera izango dugu kiroldegiaren eta frontoiaren ondoan dagoen iturrian.',
    'Desde Elgeta continuamos por carretera durante aproximadamente 1,5&ndash;2 kil&oacute;metros. Despu&eacute;s de varias curvas llegaremos a una zona m&aacute;s recta, donde giramos a la derecha para tomar una pista de piedra que nos conduce hasta <b>Goierri</b>.':
        'Elgetatik errepidez jarraituko dugu gutxi gorabehera 1,5-2 kilometroz. Hainbat bihurgune igaro ondoren, zuzenagoa den tarte batera iritsiko gara. Han eskuinera egingo dugu eta harrizko pista bat hartuko dugu, <b>Goierri</b>raino eramango gaituena.',
    'Al llegar a Goierri, nuestra ruta gira a la izquierda y comienza a bajar hacia <b>Zaldibar</b> por una tranquila carretera de barrio, evitando la carretera general.':
        'Goierrira iristean, gure ibilbideak ezkerrera egiten du eta <b>Zaldibar</b> aldera jaisten hasten da auzo-errepide lasai batetik, errepide nagusia saihestuz.',
    'En este punto tenemos tambi&eacute;n una alternativa por si no queremos alargar tanto la vuelta ni sumar m&aacute;s desnivel. En lugar de girar a la izquierda, podemos continuar de frente hacia la ermita y enlazar con el GR, que nos llevar&aacute; hacia Zengotita. Es una buena opci&oacute;n para recortar la ruta, evitando la bajada hacia Zaldibar y Berriz y la posterior subida.':
        'Puntu honetan beste aukera bat ere badugu, ibilbidea hainbeste luzatu edo desnibel gehiago pilatu nahi ez badugu. Ezkerrera hartu beharrean, zuzen jarrai dezakegu ermitarantz eta GRarekin bat egin. GRak Zengotita aldera eramango gaitu. Aukera ona da ibilbidea laburtzeko, Zaldibar eta Berriz aldera jaistea eta ondorengo igoera saihestuz.',
    'Siguiendo con el recorrido principal, atravesamos Zaldibar y, junto a la estaci&oacute;n, continuamos en direcci&oacute;n a <b>Berriz</b> (36,3 km &middot; 184 m). Vamos perdiendo altura poco a poco y, ya a la entrada de Berriz, tomamos el bidegorri que discurre por un lateral del pueblo, junto al riachuelo.':
        'Ibilbide nagusiarekin jarraituz, Zaldibar zeharkatu eta, geltokiaren ondoan, <b>Berriz</b> aldera jarraituko dugu (36,3 km &middot; 184 m). Pixkanaka altuera galtzen joango gara eta, Berrizko sarreran bertan, herriaren albo batetik, Erreka bazterretik doan bidegorria hartuko dugu.',
    'El bidegorri nos deja en la parte alta de Berriz, donde salimos nuevamente a la carretera y comenzamos la subida en direcci&oacute;n a Zengotita y, despu&eacute;s, Trabakua. Pero estaremos muy poco tiempo en la carretera principal: a la altura del barrio de <b>San Juan</b> (40,0 km &middot; 412 m), tomamos a mano derecha la antigua carretera que sube hacia Zengotita.':
        'Bidegorriak Berrizko goialdean utziko gaitu; han, berriro errepidera irten eta Zengotita eta, ondoren, Trabakua aldera igotzen hasiko gara. Hala ere, oso denbora gutxian egongo gara errepide nagusian: <b>San Juan</b> auzoaren parean (40,0 km &middot; 412 m), eskuinetara hartuko dugu Zengotita aldera igotzen den antzinako errepidea.',
    'Superada esta &uacute;ltima parte de la subida, ya solo nos queda continuar hacia Trabakua, punto de inicio y final de la ruta.':
        'Igoeraren azken zati hau gaindituta, Trabakua aldera jarraitzea besterik ez zaigu geratuko; ibilbidearen hasiera eta amaiera puntua da.',
    'Una vuelta larga y muy variada, combinando carreteras secundarias, pistas, senderos y bidegorri. El paso por Aixola, Elgeta y Goiko Mendia aporta algunos de los tramos m&aacute;s agradables del recorrido, mientras que la bajada hacia Zaldibar y Berriz nos permite alargar la vuelta antes de afrontar el regreso por Zengotita. Adem&aacute;s, encontramos varias fuentes bien repartidas a lo largo del recorrido, algo especialmente &uacute;til en una ruta de esta longitud.':
        'Ibilbide luzea da, bide desberdinetik, auzo-errepideak, pistak, bidexkak eta bidegorria uztartzen dituena. Aixola, Elgeta eta Goiko Mendia inguruko pasabideek ibilbideko zatirik atseginenetako batzuk eskaintzen dituzte; Zaldibar eta Berriz aldera egindako jaitsierak, berriz, itzulia luzatzeko aukera ematen digu, Zengotitatik Trabakuara itzuli aurretik.'
        '</p>\n    <p>Gainera, ibilbidean zehar hainbat iturri aurkituko ditugu, nahiko ondo banatuta; oso baliagarriak horrelako luzera duen ibilbide batean.',

    # para quién es
    '<h2>Una vuelta larga en e-bike</h2>':
        '<h2>Bira luzea e-bikez</h2>',
}

MAGUNA = {
    # hero
    '<span>Pista y carretera</span><span class="sep">/</span><span>Zengotitagane, Iturzurigana y Maguna</span><span class="sep">/</span><span>Circuito</span>':
        '<span>Pista eta errepidea</span><span class="sep">/</span><span>Zengotitagane, Iturzurigana eta Maguna</span><span class="sep">/</span><span>Zirkuitua</span>',
    '<h1>Trabakua, Zengotitagane<br><em>y Maguna</em></h1>':
        '<h1>Trabakua, Zengotitagane<br><em>eta Maguna</em></h1>',
    '<p class="full-name">Circuito en e-bike desde Trabakua por Zengotitagane, el Dolmen de Iturzurigana y Maguna</p>':
        '<p class="full-name">Zirkuitua e-bikez Trabakuatik, Zengotitagane eta Iturzuriganako Trikuharritik igarota Magunaraino</p>',

    # elevation profile markers + legend (used twice: hero chart and map section)
    '<title>Dolmen de Iturzurigana &middot; 4,6 km &middot; 843 m</title>':
        '<title>Iturzuriganako Trikuharria &middot; 4,6 km &middot; 843 m</title>',
    '<title>Ermita de San Crist&oacute;bal Txiki &middot; 26,8 km &middot; 496 m</title>':
        '<title>San Kristobal Txiki ermita &middot; 26,8 km &middot; 496 m</title>',
    '<title>Ermita de San Juan &middot; 30,8 km &middot; 403 m</title>':
        '<title>San Juan ermita &middot; 30,8 km &middot; 403 m</title>',
    '<span class="elev-legend-item"><span class="num">1</span>Zengotitagane</span> <span class="elev-legend-item"><span class="num">2</span>Dolmen de Iturzurigana</span> <span class="elev-legend-item"><span class="num">3</span>Maguna</span> <span class="elev-legend-item"><span class="num">4</span>Ermita de San Crist&oacute;bal Txiki</span> <span class="elev-legend-item"><span class="num">5</span>Ermita de San Juan</span>':
        '<span class="elev-legend-item"><span class="num">1</span>Zengotitagane</span> <span class="elev-legend-item"><span class="num">2</span>Iturzuriganako Trikuharria</span> <span class="elev-legend-item"><span class="num">3</span>Maguna</span> <span class="elev-legend-item"><span class="num">4</span>San Kristobal Txiki ermita</span> <span class="elev-legend-item"><span class="num">5</span>San Juan ermita</span>',

    # photos
    'alt="Caballo pastando al atardecer en una cresta, con las monta&ntilde;as al fondo"':
        'alt="Zaldia bazkan ilunabarrean gandor batean, mendiak atzealdean dituela"',
    'alt="Foto ampliada del recorrido de Trabakua, Zengotitagane y Maguna"':
        'alt="Trabakua, Zengotitagane eta Maguna ibilbidearen argazki handitua"',
    'alt="Nubes al atardecer sobre la ladera del parque e&oacute;lico, con los aerogeneradores en la cresta"':
        'alt="Ilunabarreko hodeiak parke eolikoaren magalean, aerosorgailuak gandorrean dituela"',
    'alt="Atardecer sobre las monta&ntilde;as, con el sol asom&aacute;ndose entre capas de nubes"':
        'alt="Ilunabarra mendien gainean, eguzkia hodei-geruzen artetik agertzen"',
    'alt="Bosque de repoblaci&oacute;n con los aerogeneradores del Oiz asomando sobre la loma"':
        'alt="Birlandatutako basoa, Oizko aerosorgailuak muinoaren gainetik agertzen direla"',
    'alt="Vista desde el manillar de la e-bike hacia un prado con rocas y las monta&ntilde;as al fondo, bajo un cielo nuboso"':
        'alt="E-bikearen eskulekutik ikusitako larrea, harriekin eta mendiak atzealdean, zeru hodeitsu baten azpian"',
    'alt="Vista del valle con niebla entre las monta&ntilde;as y un pueblo al fondo"':
        'alt="Harana lainoarekin mendien artean eta herri bat atzealdean"',
    'alt="Bicicleta apoyada en un pino, en un pinar"':
        'alt="Bizikleta pinu baten kontra jarrita, pinudi batean"',
    'alt="Vista del valle con niebla y un banco de nubes bajo un cielo cubierto"':
        'alt="Harana lainoarekin eta hodei-banku batekin, zeru estali baten azpian"',
    'alt="Aerogenerador junto a una pista de grava, con el parque e&oacute;lico al fondo bajo un cielo nuboso"':
        'alt="Aerosorgailua legarrezko pista baten ondoan, parke eolikoa atzealdean zeru hodeitsu baten azpian"',

    # wikiloc / gpx
    'download="Trabakua, Zengotitagane y Maguna.gpx"':
        'download="Trabakua, Zengotitagane eta Maguna.gpx"',

    # body copy
    'Salimos de <b>Trabakua</b> en direcci&oacute;n a Osma por carretera. Algo m&aacute;s de 2 km despu&eacute;s giramos a la derecha para coger la pista que sube hasta <b>Zengotitagane</b> (km 3,6 &middot; 788 m), entre los aerogeneradores del parque e&oacute;lico. Las rampas son muy duras, casi imposibles de subir con una bici normal.':
        '<b>Trabakua</b>tik Osma aldera ateratzen gara errepidez. 2 km pasatxo egin ondoren, eskuinera biratu eta <b>Zengotitagane</b>ra (3,6 km &middot; 788 m) igotzen den pista hartzen dugu, parke eolikoko aerosorgailuen artean. Maldak oso gogorrak dira, eta ia ezinezkoa da bizikleta arrunt batekin igotzeko.',
    'Tras Zengotitagane seguimos por la cresta hasta el <b>Dolmen de Iturzurigana</b> (km 4,6 &middot; 843 m), con buenas vistas hacia los dos lados. Quien necesite coger agua puede desviarse unos metros a la derecha.':
        'Zengotitagane igaro ondoren, gailurretik jarraitzen dugu <b>Iturzurigana</b> trikuharrira (4,6 km &middot; 843 m), bi aldeetara ikuspegi ederrak ditugula. Ura hartu behar duenak eskuinera metro batzuk desbidera daiteke.',
    'Continuamos por la parte alta del <b>Oiz</b>, avanzando en paralelo a los aerogeneradores, hasta salir a la pista de cemento que sube desde <b>Garai</b> y San Crist&oacute;bal. Subimos por ella unos 300 metros y enseguida nos desviamos a la izquierda por una pista de tierra.':
        '<b>Oiz</b>en goialdetik jarraitzen dugu, aerosorgailuen azpitik eta norabide berean, <b>Garai</b> eta San Kristobaletik igotzen den porlanezko pistara irten arte. Handik 300 metro inguru igotzen gara, eta berehala ezkerrera desbideratzen gara lurrezko pista batetik.',
    'Al principio avanzamos pr&aacute;cticamente en transversal, pero poco a poco el terreno empieza a inclinarse y entramos de lleno en la bajada. El camino tiene alg&uacute;n tramo algo abrupto, aunque en general se circula bien. M&aacute;s abajo hay que estar atentos para localizar, a mano derecha, un sendero medio escondido entre los eucaliptos.':
        'Hasieran ia zeharka egiten dugu aurrera, baina pixkanaka malda handitzen hasten da eta jaitsieran bete-betean sartzen gara. Bideak tarte malkartsuren bat badu ere, oro har ondo ibiltzen da. Beherago adi egon behar dugu, eskuinaldean eukaliptoen artean erdi ezkutatuta dagoen bidezidor bat aurkitzeko.',
    'Aqu&iacute; empieza uno de los tramos m&aacute;s entretenidos de la ruta: un sendero algo roto, juguet&oacute;n y con pendiente, donde conviene bajar con cuidado. Seguimos perdiendo altura hasta desembocar en una pista. En el primer cruce no seguimos de frente: giramos a la derecha y continuamos bajando.':
        'Hemen hasten da ibilbideko tarterik entretenigarrienetako bat: bidezidor apur bat hautsia, jostaria eta aldapatsua, kontuz jaistea komeni den horietakoa. Garaiera galtzen jarraitzen dugu pista batera iritsi arte. Lehen bidegurutzean ez dugu zuzen jarraitzen: eskuinera biratu eta jaisten jarraitzen dugu.',
    'Es posible encontrarse alguna alambrada en este tramo, pero hay visibilidad suficiente para verla con tiempo. A partir de aqu&iacute; la sensaci&oacute;n puede ser la de andar un poco perdidos, sobre todo la primera vez que se pasa por la zona, pero precisamente ah&iacute; est&aacute; parte del encanto. Es un entorno solitario y merece la pena meterse por estos caminos.':
        'Baliteke tarte honetan alanbradaren bat aurkitzea, baina nahikoa ikuspen dago garaiz ikusteko. Hemendik aurrera, apur bat galduta gabiltzala senti dezakegu, batez ere ingurutik lehen aldiz igarotzen bagara; baina horixe da, hain zuzen, tarte honen xarmaren zati bat. Ingurua bakartia da, eta merezi du bide hauetan barrena ibiltzea.',
    'Seguimos con una buena bajada en direcci&oacute;n a <b>Maguna</b> (km 15 &middot; 413 m) hasta terminar saliendo junto a un caser&iacute;o a la carretera. Giramos a la izquierda y nos queda aproximadamente 1 km por asfalto hasta llegar al pueblo.':
        'Jaitsiera ederrarekin jarraitzen dugu <b>Maguna</b> (15 km &middot; 413 m) aldera, eta azkenean baserri baten ondoan errepidera irteten gara. Ezkerrera biratu, eta asfaltoan kilometro bat inguru geratzen zaigu herrira iritsi arte.',
    'Maguna merece una peque&ntilde;a menci&oacute;n. Es uno de esos sitios que, si no conoces la zona, cuesta incluso situar en el mapa. Quien no haya estado nunca seguramente se sorprenda: peque&ntilde;o, tranquilo, en un entorno realmente bonito y con una fuente de agua, un buen punto para reponer antes de continuar.':
        'Magunak aipamen txiki bat merezi du. Ingurua ezagutzen ez baduzu, mapan kokatzea ere kostatzen den leku horietako bat da. Inoiz egon ez dena ziurrenik harrituko da: txikia, lasaia eta benetan ingurune ederrean kokatua. Gainera, ur-iturri bat dago, aurrera jarraitu aurretik ura hartzeko leku aproposa.',
    'Atravesamos Maguna y continuamos por carretera hasta encontrarnos con una curva cerrada, donde abandonamos el asfalto por una pista que sale a mano izquierda. Aqu&iacute; comienza otra subida larga, que nos llevar&aacute; de nuevo hacia la zona de la carretera que asciende desde Garai hacia Oiz y Zengotitagane, aunque bastante m&aacute;s abajo que por donde hemos pasado anteriormente.':
        'Maguna zeharkatu eta errepidez jarraitzen dugu bihurgune itxi batera iritsi arte. Han asfaltoa utzi eta ezkerretik ateratzen den pista hartzen dugu. Hemen beste igoera luze bat hasten da, Garaitik Oiz eta Zengotitaganera igotzen den errepidearen ingurura berriro eramango gaituena, nahiz eta aurretik igaro garen lekutik dezente beherago egon.',
    'Vamos ganando altura poco a poco por una bonita pista de piedra, muy agradecida para pedalear. Durante la subida tenemos la posibilidad de atajar por un sendero de tierra. Es una alternativa m&aacute;s directa, pero no es obligatoria: quien prefiera puede continuar sin problema por la pista de piedra hasta alcanzar la pista de cemento.':
        'Pixkanaka garaiera irabazten dugu harrizko pista polit batetik, pedalei eragiteko oso atsegina. Igoeran zehar lurrezko bidezidor batetik lasterbidea hartzeko aukera dugu. Alternatiba zuzenagoa da, baina ez da derrigorrezkoa: nahiago duenak arazorik gabe jarrai dezake harrizko pistatik, porlanezko pistara iritsi arte.',
    'Al llegar a ella giramos a la izquierda y continuamos ascendiendo. Subimos hasta estar ya muy cerca del cruce donde se separan los caminos: de frente contin&uacute;a la subida hacia Oiz y por la derecha se llega desde Zengotitagane. No llegamos hasta el cruce: unos pocos metros antes giramos a la derecha y cogemos una pista de piedra que sale en direcci&oacute;n sur y comienza a bajar.':
        'Hara iristean, ezkerrera biratu eta igotzen jarraitzen dugu. Bideak banatzen diren bidegurutzetik oso gertu egon arte igotzen gara: aurrez aurre Oizerako igoerak jarraitzen du, eta eskuinetik Zengotitaganetik datorren bidea iristen da. Gu ez gara bidegurutzeraino iristen: metro batzuk lehenago eskuinera biratu eta hegoalderantz jaisten hasten den harrizko pista hartzen dugu.',
    'A partir de aqu&iacute; nos espera una bonita y larga bajada, m&aacute;s propia de bicicletas y veh&iacute;culos 4x4 que de coches normales. Durante el descenso iremos viendo, en algunos puntos junto a la pista, tramos de antiguos canales de agua.':
        'Hemendik aurrera jaitsiera eder eta luze bat dugu zain, ohiko autoentzat baino gehiago bizikleta eta 4x4 ibilgailuentzat egokia. Jaitsieran zehar, pistaren ondoan zenbait puntutan, ur-kanal zaharren tarteak ikusiko ditugu.',
    'Despu&eacute;s de perder bastante altura salimos a la carretera que comunica la zona de <b>Sarria</b> con Garai. Giramos unos metros a la izquierda y enseguida volvemos a girar con fuerza hacia la izquierda para afrontar otra subida.':
        'Garaiera dezente galdu ondoren, <b>Sarria</b>tik Garaira doan errepidera irteten gara. Metro batzuk ezkerrera egin, eta berehala berriro ezkerrera gogor biratu eta beste igoera bati ekiten diogu.',
    'Nos dirigimos ahora hacia la <b>Ermita de San Crist&oacute;bal Txiki</b> (km 26,8 &middot; 496 m). Alcanzado el punto m&aacute;s alto, encontraremos una fuente a mano izquierda, un buen lugar para rellenar agua antes de comenzar nuevamente el descenso.':
        'Orain <b>San Kristobal Txiki ermita</b>ra (26,8 km &middot; 496 m) goaz. Punturik gorenera iritsitakoan, ezkerrean iturri bat aurkituko dugu, berriro jaitsiera hasi aurretik ura betetzeko leku aproposa.',
    'Desde aqu&iacute; bajamos hacia San Crist&oacute;bal Txiki y enlazamos con una bajada larga, r&aacute;pida y muy disfrutona que nos lleva hasta el barrio de <b>San Juan</b> (km 30,8 &middot; 403 m). Continuamos descendiendo hasta encontrarnos con la carretera general que une Trabakua con Berriz.':
        'Hemendik San Kristobal Txikirantz jaisten gara, eta jaitsiera luze, azkar eta oso gozagarri batekin jarraitzen dugu <b>San Juan</b> auzoraino (30,8 km &middot; 403 m). Jaisten jarraitzen dugu Trabakua eta Berriz lotzen dituen errepide nagusia aurkitu arte.',
    'La cruzamos all&iacute; mismo, con mucho cuidado, y cogemos enfrente la antigua carretera que sube hacia Zengotita. El ascenso es ya mucho m&aacute;s suave y, a estas alturas, se agradece.':
        'Han bertan zeharkatzen dugu, kontu handiz, eta aurrean Zengotitara igotzen den errepide zaharra hartzen dugu. Igoera askoz leunagoa da jada, eta une honetan eskertzen da.',
    'La ruta est&aacute; pr&aacute;cticamente hecha. Desde aqu&iacute; apenas nos separan un par de kil&oacute;metros de Trabakua. Despu&eacute;s de todas las subidas, senderos, pistas y bajadas del recorrido, esos &uacute;ltimos kil&oacute;metros ya los tenemos chupados.':
        'Ibilbidea ia amaituta dago. Hemendik Trabakuara iristeko pare bat kilometro besterik ez zaizkigu geratzen. Ibilbideko igoera, bidezidor, pista eta jaitsiera guztiak gainditu ondoren, azken kilometro horiek dagoeneko ia eginda ditugu.',

    # para quién es
    '<h2>Un circuito largo en e-bike</h2>':
        '<h2>E-bikearekin egiteko ibilbide luzea</h2>',
    '33,44 km y +1.215 m de desnivel en un solo circuito, con la subida m&aacute;s dura nada m&aacute;s salir hacia Zengotitagane y un recorrido bastante m&aacute;s largo que el resto de rutas de la zona del Oiz. Hay agua cerca de Iturzurigana (km 4,6), en Maguna (km 15) y en una fuente junto a la Ermita de San Crist&oacute;bal Txiki (km 26,8).':
        '33,44 km eta +1.215 m-ko desnibela, zirkuitu bakarrean. Igoerarik gogorrena hasieran bertan dator, Trabakuatik Zengotitaganera bidean, eta ibilbidea Oiz inguruko gainerako ibilbideak baino dezente luzeagoa da. Ura hartzeko aukera dago Iturzuriganatik gertu (4,6 km), Magunan (15 km) eta San Kristobal Txiki ermitaren inguruko iturrian (26,8 km).',
}

PAGO7 = {
    # hero
    '<span>Mixta</span><span class="sep">/</span><span>Oiz</span><span class="sep">/</span><span>Circuito</span>':
        '<span>Nahasia</span><span class="sep">/</span><span>Oiz</span><span class="sep">/</span><span>Zirkuitua</span>',
    '<p class="full-name">El trazado real de la 7 Pago Mendi Lasterketa, con paso por la cima del Oiz</p>':
        '<p class="full-name">7 Pago Mendi Lasterketaren benetako ibilbidea, Oizko gailurretik igarota</p>',

    # elev markers / legend (used twice: hero chart and map section)
    '<title>Dolmen de Iturzurigana &middot; 16,5 km &middot; 855 m</title>':
        '<title>Iturzuriganako Trikuharria &middot; 16,5 km &middot; 855 m</title>',
    '<span class="elev-legend-item"><span class="num">1</span>Zengotita</span> '
    '<span class="elev-legend-item"><span class="num">2</span>Ur Jauziak</span> '
    '<span class="elev-legend-item"><span class="num">3</span>Oiz</span> '
    '<span class="elev-legend-item"><span class="num">4</span>Dolmen de Iturzurigana</span> '
    '<span class="elev-legend-item"><span class="num">5</span>Osmagain</span> '
    '<span class="elev-legend-item"><span class="num">6</span>Arietzu</span>':
        '<span class="elev-legend-item"><span class="num">1</span>Zengotita</span> '
        '<span class="elev-legend-item"><span class="num">2</span>Ur Jauziak</span> '
        '<span class="elev-legend-item"><span class="num">3</span>Oiz</span> '
        '<span class="elev-legend-item"><span class="num">4</span>Iturzuriganako Trikuharria</span> '
        '<span class="elev-legend-item"><span class="num">5</span>Osmagain</span> '
        '<span class="elev-legend-item"><span class="num">6</span>Arietzu</span>',

    # photos
    'alt="Corredores subiendo una cresta con los aerogeneradores del Oiz al fondo, dorsal 63 en primer plano"':
        'alt="Korrikalariak kresta batean gora, Oizeko aerosorgailuak atzealdean, 63 dortsala aurrealdean"',
    'alt="Foto ampliada del recorrido de la 7 Pago Mendi Lasterketa"':
        'alt="7 Pago Mendi Lasterketaren ibilbidearen argazki handitua"',
    'alt="Corredores en un tramo de bosque, junto a una bandera oficial de la 7 Pago Mendi Lasterketa, dorsales 27 y 28"':
        'alt="Korrikalariak baso-zati batean, 7 Pago Mendi Lasterketaren bandera ofizial baten ondoan, 27 eta 28 dortsalak"',
    'alt="V&eacute;rtice geod&eacute;sico en una cima, entre niebla"':
        'alt="Bertize geodesikoa gailur batean, lainoaren artean"',
    'alt="Cascada de Ur Jauziak, con el agua cayendo entre las rocas del bosque"':
        'alt="Ur Jauziak ur-jauzia, ura basoko harrien artetik erortzen"',
    'alt="Pista forestal entre niebla, con troncos apilados a un lado"':
        'alt="Baso-pista lainoaren artean, enborrak alde batean pilatuta"',
    'alt="Hayas junto al camino, en un tramo de bosque"':
        'alt="Pagoak bidearen ondoan, baso-zati batean"',
    'alt="Sendero entre &aacute;rboles cubiertos de musgo"':
        'alt="Bidezidorra goroldioz estalitako zuhaitzen artean"',
    'alt="Camino de grava que se bifurca en una loma, con aerogeneradores y monta&ntilde;as al fondo"':
        'alt="Grabazko bidea bitan banatzen den loma batean, aerosorgailuak eta mendiak atzealdean"',
    'alt="Fila de aerogeneradores en una loma, con un prado y una valla en primer plano"':
        'alt="Aerosorgailu ilara loma batean, larre bat eta hesi bat aurrealdean"',
    'alt="&Aacute;rbol solitario en una ladera de hierba, con niebla y un camino junto a &eacute;l"':
        'alt="Zuhaitz bakartia belar-hegal batean, lainoarekin eta bide bat ondoan"',
    'alt="Caballos pastando en un claro del bosque, con aerogeneradores al fondo en una loma"':
        'alt="Zaldiak basoko soilgune batean bazkan, aerosorgailuak atzealdean loma batean"',

    # facts note (custom wording: Desnivel is the race's official figure, not raw GPX)
    '&mdash; <b>Distancia</b>, calculada a partir del track GPX real. <b>Desnivel</b>, dato oficial de la organizaci&oacute;n de la carrera. <b>Dificultad</b>, estimada a partir de ambos. <b>Superficie</b> y <b>Tipo</b>, observados sobre el terreno.':
        '&mdash; <b>Distantzia</b>, benetako GPX trackatik kalkulatua. <b>Desnibela</b>, lasterketaren antolakuntzaren datu ofiziala. <b>Zailtasuna</b>, bien arabera zenbatetsia. <b>Azalera</b> eta <b>Mota</b>, bertatik bertara ikusiak.',

    # body copy
    'El trazado real de la 7 Pago Mendi Lasterketa, con paso por la cima del <b>Oiz</b>. Carrera de monta&ntilde;a que se celebra cada mayo en Mallabia.':
        '7 Pago Mendi Lasterketaren benetako ibilbidea, <b>Oiz</b>ko gailurretik igarota. Maiatzero Mallabian jokatzen den mendi lasterketa da.',
    'La 25K de la 7 Pago Mendi Lasterketa enga&ntilde;a un poco sobre el papel. Son 25 kil&oacute;metros, pero sus cerca de 1.400 metros de desnivel y un recorrido con pocos tramos para relajarse hacen que se terminen notando.':
        '7 Pago Mendi Lasterketako 25K ibilbideak paperean dirudiena baino gehiago dauka. 25 kilometro dira, baina ia 1.400 metroko desnibel positiboarekin eta atseden hartzeko tarte gutxirekin, kilometroak nabaritzen joaten dira.',
    'Tambi&eacute;n se puede acceder al circuito desde <b>Trabakua</b> en apenas 15 minutos. Al tratarse de una ruta de Mallabia y teniendo en cuenta que muchas de las rutas que salen de Trabakua discurren por tramos de carrera, este recorrido tiene aqu&iacute; su sitio.':
        '<b>Trabaku</b>tik ere 15 minutu eskasean iritsi daiteke zirkuitura. Mallabiko ibilbidea izanik, eta Trabakutik abiatzen diren beste ibilbide batzuekin inguru bera partekatzen duenez, ibilbide honek ere badu hemen bere lekua.',
    'Salimos de la plaza de <b>Mallabia</b> y enseguida dejamos atr&aacute;s el pueblo para meternos entre barrios, caser&iacute;os y caminos de monte. Los primeros kil&oacute;metros van ganando altura poco a poco, pasando por la <b>Ermita de San Juan</b>, en el barrio de <b>Zengotita</b>, antes de subir hacia <b>Zengotitagane</b>.':
        '<b>Mallabi</b>ko plazatik ateratzen gara eta berehala uzten dugu herria atzean, auzo, baserri eta mendi-bideetan sartzeko. Lehen kilometroetan pixkanaka irabazten dugu altuera, <b>San Juan ermita</b>tik igaro, <b>Zengotita</b> auzoan, <b>Zengotitagane</b>ra igo aurretik.',
    'Despu&eacute;s de Zengotitagane toca bajar, y bastante. Al principio se puede correr bien, pero seg&uacute;n vamos perdiendo altura la bajada se vuelve m&aacute;s t&eacute;cnica y hay que estar atentos. Abajo cambia de nuevo el terreno y comenzamos a subir de forma m&aacute;s suave hacia <a href="gerea.html">Ur Jauziak</a>.':
        'Zengotitagane pasatu ondoren jaitsiera gogorra dator, eta ez da motza. Hasieran ondo korrika egin daiteke, baina behera egin ahala gero eta teknikoagoa bihurtzen da eta adi ibili behar da. Behean, lurra berriro aldatzen da eta igoera lasaiago bati ekiten diogu <a href="gerea.html">Ur Jauziak</a> aldera.',
    'A partir de ah&iacute; ponemos rumbo a <b>Oiz</b>.':
        'Handik aurrera, <b>Oiz</b> dugu jomugan.',
    'La subida se va haciendo notar y, seg&uacute;n ganamos altura, dejamos atr&aacute;s el bosque y el paisaje empieza a abrirse. Oiz, con sus m&aacute;s de 1.000 metros, es el punto m&aacute;s alto de la carrera y uno de los lugares que m&aacute;s marca el recorrido. Si el d&iacute;a est&aacute; despejado, merece la pena levantar un momento la cabeza y mirar alrededor. Si aparece viento, niebla o lluvia, la historia puede ser bastante diferente.':
        'Igoera pixkanaka nabaritzen hasten da eta, altuera irabazi ahala, basoa atzean utzi eta paisaia zabaltzen hasten da. Oiz, 1.000 metrotik gorako garaierarekin, lasterketako punturik altuena da eta ibilbidea gehien markatzen duen lekuetako bat. Eguna garbi badago, merezi du une batez burua altxatu eta ingurura begiratzea. Haizea, lainoa edo euria agertzen badira, ordea, kontua dezente alda daiteke.',
    'Llegar arriba da alegr&iacute;a. Tambi&eacute;n puede dar una falsa sensaci&oacute;n de que lo peor ya ha pasado.':
        'Gora iristeak poza ematen du. Baita zailena eginda dagoela pentsatzeko sentsazioa ere.',
    'Todav&iacute;a queda carrera.':
        'Baina oraindik lasterketa geratzen da.',
    'Desde Oiz comenzamos a bajar hacia <b>Iturzurigana</b>, pero el regreso a Mallabia no es simplemente dejarse caer. Hay cambios de terreno, alg&uacute;n repecho y kil&oacute;metros en los que las piernas empiezan a recordar todo lo que llevan acumulado.':
        'Oiztik <b>Iturzurigana</b> aldera jaisten hasten gara, baina Mallabirako itzulera ez da beherantz joatea besterik. Lur aldaketak, aldapatxoren bat eta ordurako pilatutako guztia hanketan nabaritzen hasten diren kilometroak datoz.',
    'Seguimos hacia <b>Osmagain</b> y <b>Arietzu</b>. A estas alturas ya pasamos de los veinte kil&oacute;metros y cualquier peque&ntilde;a subida parece bastante m&aacute;s grande que al principio.':
        '<b>Osmagain</b> eta <b>Arietzu</b> aldera jarraitzen dugu. Puntu honetan hogei kilometro baino gehiago daramatzagu eta hasieran ia konturatu gabe igaroko genukeen aldapa txiki batek ere bestelako itxura hartzen du.',
    'Desde Arietzu s&iacute; empezamos a mirar definitivamente hacia Mallabia. Si quedan piernas, es una zona donde todav&iacute;a se puede correr y disfrutar de los &uacute;ltimos kil&oacute;metros.':
        'Arietzutik aurrera bai, Mallabira begira jartzen gara. Hanketan oraindik indarra badago, korrika egiteko eta azken kilometroez gozatzeko aukera ematen duen zatia da.',
    'Poco a poco vuelve a aparecer el pueblo y terminamos entrando de nuevo en la plaza, justo donde empez&oacute; todo.':
        'Pixkanaka herria berriro agertzen da eta azkenean Mallabiko plazara itzultzen gara, dena hasi den leku berera.',
    'Son 25 km y alrededor de +1.400 m, con pistas, senderos, bosque, alguna bajada t&eacute;cnica y Oiz esperando aproximadamente a mitad de camino.':
        'Guztira, 25 km inguru eta +1.400 m, pistak, bidezidorrak, basoa, jaitsiera tekniko batzuk eta Oiz, gutxi gorabehera ibilbidearen erdialdean zain.',
    'No hace falta complicarlo mucho m&aacute;s.':
        'Ez dago askoz gehiago konplikatu beharrik.',
    'Hay que salir con cabeza, guardar algo para Oiz y no pensar que al llegar arriba est&aacute; todo hecho.':
        'Buruz atera, Oizerako zerbait gorde eta, batez ere, gora iristean dena eginda dagoela ez pentsatu.',
    'Porque todav&iacute;a hay que volver a Mallabia.':
        'Oraindik Mallabira itzuli behar da eta.',
    'Este es el trazado oficial de la <a href="https://7pago.com" target="_blank" rel="noopener noreferrer">7 Pago Mendi Lasterketa</a>, que se corre cada mayo en Mallabia. Buen track para reconocer el recorrido antes de la pr&oacute;xima edici&oacute;n.':
        'Hau da <a href="https://7pago.com" target="_blank" rel="noopener noreferrer">7 Pago Mendi Lasterketa</a>ren ibilbide ofiziala, maiatzero Mallabian jokatzen dena. Track ona hurrengo edizioa baino lehen ibilbidea ezagutzeko.',

    # parada
    'A&ntilde;ado esta ruta por ser de Mallabia y porque buena parte de su recorrido coincide con tramos de otras rutas que salen de Trabakua y alrededores: sube al mismo <a href="oiz.html">Oiz</a> y pasa por los mismos altos de <a href="arietzu.html">Osmagain y Arietzu</a>, con tramos de bosque, la cascada de Ur Jauziak y buenas vistas desde el cordal.':
        'Ibilbide hau gehitzen dut Mallabiakoa delako, eta bere ibilbidearen zati handi bat Trabakuatik eta inguruetatik ateratzen diren beste ibilbide batzuen zatiekin bat datorrelako: <a href="oiz.html">Oiz</a> mendi bera igotzen du eta <a href="arietzu.html">Osmagain eta Arietzu</a>ko goi berberetatik igarotzen da, baso-zatiekin, Ur Jauziak ur-jauziarekin eta gailurreko ikuspegi ederrekin.',

    # map + footer
    'data-marker-title="Mallabia (salida y llegada)"':
        'data-marker-title="Mallabia (irteera eta helmuga)"',
    'Circuito &mdash; vuelve al mismo punto': 'Zirkuitua &mdash; puntu berera itzultzen da',
}

PAGO16 = {
    # hero
    '<span>Mixta</span><span class="sep">/</span><span>Iturzurigana</span><span class="sep">/</span><span>Circuito</span>':
        '<span>Nahasia</span><span class="sep">/</span><span>Iturzurigana</span><span class="sep">/</span><span>Zirkuitua</span>',
    '<p class="full-name">El trazado real de la 7 Pago Mendi Lasterketa 16K, la versi&oacute;n corta de la carrera</p>':
        '<p class="full-name">7 Pago Mendi Lasterketako 16K-ko benetako ibilbidea, lasterketaren bertsio laburra</p>',

    # photos
    'alt="Corredor con dorsal de la 7 Pago dando el pulgar hacia arriba en un tramo de bosque, con otro corredor detr&aacute;s y las monta&ntilde;as al fondo, dorsal 37"':
        'alt="Korrikalari bat 7 Pagoko dortsalarekin hatz lodia gora eginez baso-zati batean, beste korrikalari bat atzean eta mendiak atzealdean, 37 dortsala"',
    'alt="Foto ampliada del recorrido de la 7 Pago Mendi Lasterketa 16K"':
        'alt="7 Pago Mendi Lasterketa 16K ibilbidearen argazki handitua"',
    'alt="Aerogenerador visto desde abajo, con helechos y monta&ntilde;as al fondo"':
        'alt="Aerosorgailua behetik ikusita, garoak eta mendiak atzealdean"',
    'alt="Vista panor&aacute;mica de un valle con caser&iacute;os, monta&ntilde;as y el mar al fondo"':
        'alt="Harana ikuspegi panoramikoan, baserriak, mendiak eta itsasoa atzealdean"',
    'alt="Amanecer desde una cima, con un v&eacute;rtice geod&eacute;sico en primer plano y valles entre niebla"':
        'alt="Egunsentia gailur batetik, bertize geodesikoa aurrealdean eta haranak lainoaren artean"',
    'alt="Sendero entre &aacute;rboles y musgo, en un tramo de bosque"':
        'alt="Bidezidorra zuhaitz eta goroldioaren artean, baso-zati batean"',
    'alt="Hayedo con hojas nuevas brotando, en un d&iacute;a de niebla"':
        'alt="Pagadia hosto berriekin, laino-egun batean"',
    'alt="Cruz de piedra sobre un pedestal, con aerogeneradores al fondo"':
        'alt="Harrizko gurutzea oinarri baten gainean, aerosorgailuak atzealdean"',
    'alt="Corredoras y corredores junto a un muro de piedra antiguo, con dorsales de la carrera"':
        'alt="Korrikalariak harrizko horma zahar baten ondoan, lasterketako dortsalekin"',

    # facts note (custom wording: Desnivel is the race's official figure, not raw GPX)
    '&mdash; <b>Distancia</b>, calculada a partir del track GPX real. <b>Desnivel</b>, dato oficial de la organizaci&oacute;n de la carrera. <b>Dificultad</b>, estimada a partir de ambos. <b>Superficie</b> y <b>Tipo</b>, observados sobre el terreno.':
        '&mdash; <b>Distantzia</b>, benetako GPX trackatik kalkulatua. <b>Desnibela</b>, lasterketaren antolakuntzaren datu ofiziala. <b>Zailtasuna</b>, bien arabera zenbatetsia. <b>Azalera</b> eta <b>Mota</b>, bertatik bertara ikusiak.',

    # body copy
    'El trazado real de la 7 Pago Mendi Lasterketa 16K, por los montes y barrios de Mallabia.':
        '7 Pago Mendi Lasterketako 16K-ko benetako ibilbidea, Mallabiko mendi eta auzoetan barrena.',
    'Son 16 kil&oacute;metros y alrededor de 750 metros de desnivel positivo. Sobre el papel puede parecer un recorrido relativamente corto, pero es una carrera r&aacute;pida, con bastante terreno para correr y pocos tramos donde relajarse. Y precisamente por eso tambi&eacute;n termina siendo exigente.':
        '16 kilometro eta 750 metro inguruko desnibel positiboa ditu. Paperean ez dirudi ibilbide oso luzea, baina lasterketa azkarra da, korrika egiteko tarte askokoa eta lasaitzeko aukera gutxikoa. Eta, hain zuzen ere, horrek egiten du uste baino gogorragoa.',
    'Aunque la carrera sale y termina en Mallabia, desde <b>Trabakua</b> tambi&eacute;n tenemos un acceso bastante c&oacute;modo al recorrido. En unos 40 minutos podemos llegar hasta <a href="zengotitagane.html">Zengotitagane</a> y enlazar directamente con el trazado de esta 16K.':
        'Lasterketa Mallabian hasi eta amaitzen den arren, <b>Trabaku</b>tik ere nahiko erraz sar gaitezke ibilbidean. 40 minutu inguruan <a href="zengotitagane.html">Zengotitagane</a>ra iritsi eta 16K-ko trazatuarekin zuzenean bat egin dezakegu.',
    'Adem&aacute;s, desde Trabakua tenemos todav&iacute;a m&aacute;s cerca el recorrido de la <a href="7pago.html">7 Pago Mendi Lasterketa 25K</a>. En apenas 15 minutos podemos enlazar con la subida que utiliza la carrera larga en direcci&oacute;n a las cascadas de <a href="gerea.html">Gerea</a>. A partir de ah&iacute; podemos seguir parte de su recorrido o utilizarlo para conectar con otras rutas de la zona.':
        'Gainera, Trabakutik are gertuago daukagu <a href="7pago.html">7 Pago Mendi Lasterketa</a>ko 25K-ko ibilbidea. 15 minutu inguruan lasterketa luzeko trazatuarekin bat egin dezakegu, <a href="gerea.html">Gerea</a> ur-jauzietara doan igoeratik. Handik aurrera, lasterketako ibilbidearen zati bat jarrai dezakegu edo inguruko beste ibilbide batzuekin lotzeko erabili.',
    'Al tratarse de una ruta de Mallabia y teniendo en cuenta que muchas de las rutas que parten de Trabakua coinciden en alg&uacute;n momento con los recorridos de la 16K y la 25K de la 7 Pago, este trazado tambi&eacute;n ten&iacute;a que tener aqu&iacute; su sitio.':
        'Mallabiko ibilbidea izanik, eta Trabakutik ateratzen diren hainbat ibilbidek 7 Pagoko 16K eta 25K-ko trazatuetako zatiak erabiltzen dituztela kontuan hartuta, ibilbide honek ere hemen bere lekua izan behar zuen.',
    'Salimos de la plaza de <b>Mallabia</b> y enseguida dejamos atr&aacute;s el pueblo para meternos entre barrios, caser&iacute;os y caminos de monte. Los primeros kil&oacute;metros van ganando altura poco a poco, pasando por la <b>Ermita de San Juan</b>, en el barrio de <b>Zengotita</b>, antes de afrontar la subida hacia <b>Zengotitagane</b>.':
        '<b>Mallabi</b>ko plazatik abiatuko gara, eta berehala utziko dugu herrigunea atzean, auzo, baserri eta mendi-bideetan sartzeko. Lehen kilometroetan pixkanaka irabaziko dugu altuera, <b>Zengotita</b> auzoko <b>San Juan ermita</b>tik igaroz, <b>Zengotitagane</b>rako igoerari ekin aurretik.',
    'Despu&eacute;s de Zengotitagane continuamos por la parte alta, cresteando y con buenas vistas a ambos lados. A nuestra derecha se abre el valle de Gerea, mientras que a la izquierda tenemos las monta&ntilde;as del Duranguesado.':
        'Zengotitagane atzean utzita, goiko aldetik jarraituko dugu, bizkarretik aurrera eginez eta bi aldeetara ikuspegi ederrak izanez. Eskuinean Gerea harana zabaltzen da, eta ezkerrean Durangaldeko mendiak izango ditugu.',
    'Seguimos hacia <b>Iturzurigana</b>. Entramos durante un peque&ntilde;o tramo entre &aacute;rboles, en un hayedo, y poco despu&eacute;s, giramos a la izquierda para afrontar la subida que nos lleva hasta la zona de los d&oacute;lmenes. Continuamos unos metros m&aacute;s hasta alcanzar Iturzurigana, el punto m&aacute;s alto de la carrera.':
        '<b>Iturzurigana</b> aldera jarraituko dugu. Zuhaitz artean tarte labur batean sartu eta, pagadi batean, handik gutxira ezkerrera egingo dugu, trikuharrien ingurura eramango gaituen igoerari ekiteko. Metro batzuk gehiago egin ondoren Iturzuriganera iritsiko gara, lasterketako punturik altuenera.',
    'A partir de aqu&iacute; comienza el regreso. M&aacute;s adelante giramos a la izquierda y, junto a una cruz de piedra, cogemos un sendero que nos hace perder altura en direcci&oacute;n al caser&iacute;o <b>Betzuen</b>. Es una bajada r&aacute;pida y entretenida en la que se pierde bastante altura en poco tiempo.':
        'Hemendik aurrera itzulerako bidea hasten da. Aurrerago ezkerrera egingo dugu eta, harrizko gurutze baten ondoan, <b>Betzuen</b> baserriaren norabidean jaisten den bidezidorra hartuko dugu. Jaitsiera azkar eta entretenigarria da, eta denbora gutxian altuera dezente galtzen da.',
    'Antes de llegar abajo del todo giramos de nuevo a la izquierda y cogemos un camino bastante menos conocido que nos lleva de vuelta hacia el barrio de Zengotita.':
        'Beheraino iritsi baino lehen, berriro ezkerrera egingo dugu eta hain ezaguna ez den bide bat hartuko dugu, Zengotita auzora bueltan eramango gaituena.',
    'Tras pasar de nuevo por la parte baja del barrio de Zengotita, cerca de la ermita de San Juan, todav&iacute;a quedan las dos &uacute;ltimas subidas de la carrera. Primero afrontamos la subida a <a href="arietzu.html">Osmagain</a>, coronada por una cruz, y despu&eacute;s continuamos hacia <a href="arietzu.html">Arietzu</a>, donde encontramos otra cruz en la cima.':
        'Zengotita auzoko beheko aldetik berriro igaro ondoren, San Juan ermitaren ingurutik, lasterketako azken bi igoerak geratzen zaizkigu oraindik. Lehenengo <a href="arietzu.html">Osmagain</a>era igoko gara, tontorreko gurutzeraino, eta ondoren <a href="arietzu.html">Arietzu</a> aldera jarraituko dugu, han ere tontorrean beste gurutze bat aurkituko dugularik.',
    'Superado Arietzu, ya s&iacute; comienza el descenso definitivo hacia Mallabia. Bajamos hasta alcanzar la zona del r&iacute;o y, desde all&iacute;, el terreno se suaviza. Continuamos junto al agua, pr&aacute;cticamente llaneando y con alg&uacute;n peque&ntilde;o repecho, hasta regresar al pueblo y completar los 16 kil&oacute;metros.':
        'Arietzu gaindituta, orain bai, Mallabiarako azken jaitsiera hasiko dugu. Erreka ingurura jaitsi eta, handik aurrera, ibilbidea nabarmen leuntzen da. Uraren ondotik eta ia lauan jarraituko dugu, tarteka aldapatxo txikiren batekin, Mallabiara itzuli eta 16 kilometroko ibilbidea osatu arte.',
    'No es una carrera especialmente t&eacute;cnica ni tiene desniveles exagerados, pero tampoco conviene confiarse. Es una carrera r&aacute;pida, y ser r&aacute;pida no significa que sea f&aacute;cil. Se puede correr durante buena parte del recorrido, las subidas se hacen a buen ritmo y apenas hay momentos para recuperar del todo. Si se aprieta demasiado al principio, Osmagain, Arietzu y los &uacute;ltimos kil&oacute;metros de regreso a Mallabia pueden terminar haci&eacute;ndose bastante largos.':
        'Ez da bereziki lasterketa teknikoa, eta desnibelak ere ez dira ikaragarriak, baina ez da komeni gehiegi fidatzea. Lasterketa azkarra da, eta azkarra izateak ez du esan nahi erraza denik. Ibilbidearen zati handi batean korrika egin daiteke, igoerak erritmo onean egiten dira eta atseden hartzeko aukera gutxi dago. Hasieran gehiegi estutuz gero, Osmagain, Arietzu eta Mallabiarako azken kilometroak espero baino luzeagoak egin daitezke.',
    'Este es el trazado oficial de la <a href="https://7pago.com" target="_blank" rel="noopener noreferrer">7 Pago Mendi Lasterketa 16K</a>, que se corre cada mayo en Mallabia. Buen track para reconocer el recorrido antes de la pr&oacute;xima edici&oacute;n.':
        'Hau da <a href="https://7pago.com" target="_blank" rel="noopener noreferrer">7 Pago Mendi Lasterketa 16K</a>ren ibilbide ofiziala, maiatzero Mallabian jokatzen dena. Track ona hurrengo edizioa baino lehen ibilbidea ezagutzeko.',

    # map + footer
    'data-marker-title="Mallabia (salida y llegada)"':
        'data-marker-title="Mallabia (irteera eta helmuga)"',
    'Circuito &mdash; vuelve al mismo punto': 'Zirkuitua &mdash; puntu berera itzultzen da',
}

HISTORIAS = {
    # dock + progress + hint + buttons (shared across every card)
    'Anterior': 'Aurrekoa',
    'Sorpréndeme': 'Harritu nazazu',
    'Siguiente': 'Hurrengoa',
    'Volver a rutas': 'Itzuli ibilbideetara',
    'La forma del recorrido es la portada. Desliza para descubrir otra.': 'Ibilbidearen forma bera da azala. Irristatu beste bat ezagutzeko.',
    'Entrar en esta ruta': 'Sartu ibilbide honetan',
    'Abrir ruta completa': 'Ireki ibilbide osoa',

    # per-card eyebrow ("Ruta 01")
    'Ruta': 'Ibilbidea',

    # per-card activity/type/surface tag
    'BTT/e-bike · Circuito · Pista': 'BTT/e-bike · Zirkuitua · Pista',
    'Senderismo · Circuito · Sendero': 'Oinez · Zirkuitua · Bidezidorra',
    'Senderismo · Circuito · Mixta': 'Oinez · Zirkuitua · Nahasia',
    'BTT/e-bike · Circuito · Mixta': 'BTT/e-bike · Zirkuitua · Nahasia',
    'Senderismo · Ida y vuelta · Sendero': 'Oinez · Joan-etorria · Bidezidorra',
    'Senderismo · Trail running · Circuito · Mixta': 'Oinez · Trail running · Zirkuitua · Nahasia',
    'BTT/e-bike · Circuito · Carretera y pista': 'BTT/e-bike · Zirkuitua · Errepidea eta pista',
    'BTT/e-bike · Circuito · Carretera, pista y sendero': 'BTT/e-bike · Zirkuitua · Errepidea, pista eta bidezidorra',
    'BTT/e-bike · Circuito · Pista y carretera': 'BTT/e-bike · Zirkuitua · Pista eta errepidea',

    # per-card surface badge (Pista is identical in both languages)
    'Sendero': 'Bidezidorra',
    'Mixta': 'Nahasia',
    'Carretera y pista': 'Errepidea eta pista',
    'Carretera, pista y sendero': 'Errepidea, pista eta bidezidorra',
    'Pista y carretera': 'Pista eta errepidea',

    # route names
    'Trabakua, Zengotitagane y Maguna': 'Trabakua, Zengotitagane eta Maguna',
    'Trabakua, Aixola y Berriz': 'Trabakua, Aixola eta Berriz',
    'Iturzuri, Zengotitagane subida por la cascada de Gerea': 'Iturzuri, Zengotitagane Gereako ur-jauzitik gora',
    'Zenarruza, San Kristobal y Zengotitagane': 'Zenarruza, San Kristobal eta Zengotitagane',
    'Trabakua, Elgeta y Argi&ntilde;eta': 'Trabakua, Elgeta eta Argi&ntilde;eta',
    'Zengotitagane, Iturzurigana y San Crist&oacute;bal Txiki': 'Zengotitagane, Iturzurigana eta San Kristobal Txiki',
    'Zengotitagane, Askako y San Crist&oacute;bal': 'Zengotitagane, Askako eta San Kristobal',
    'Zengotitagane, Axmakur y Oiz': 'Zengotitagane, Axmakur eta Oiz',
    'Osmagain y Arietzu': 'Osmagain eta Arietzu',
    'Trabakua, Asuntza y Urko': 'Trabakua, Asuntza eta Urko',
    'Trabakua, Barinaga y Iturreta': 'Trabakua, Barinaga eta Iturreta',
    'Urko, Egoarbitza y Zengotitagane': 'Urko, Egoarbitza eta Zengotitagane',
    'Iturreta, Markina y Urregarai': 'Iturreta, Markina eta Urregarai',
    'Urko, Kalamua, San Migel y Mendibil': 'Urko, Kalamua, San Migel eta Mendibil',
    'Trabakua, Iturreta e Iruzubieta': 'Trabakua, Iturreta eta Iruzubieta',
    'Trabakua, Mendibil, Olamendi y Arteta': 'Trabakua, Mendibil, Olamendi eta Arteta',
    'Trabakua paseo por el barrio Goita': 'Trabakua Goita auzoko paseoa',
    'Hiru Txikiak Urko, Oiz y Egoarbitza': 'Hiru Txikiak Urko, Oiz eta Egoarbitza',

    # route descriptions
    'Pista entre cemento, piedra y tierra, con un repecho duro al principio —no llega a 300 m—, un desvío técnico opcional a Aginaga y vistas al Duranguesado desde Berano.': 'Pista zementu, harri eta lur artean; hasieran 300 metro baino gutxiagoko aldapa gogorra du, Aginagara desbideratze tekniko aukerakoa, eta Durangaldeko ikuspegi zabalak eskaintzen ditu Beranotik.',
    'Sendero hasta el punto más alto de Mallabia: cascadas, un dolmen prehistórico y un cresterio con vistas a ambos lados antes de rodear Zengotitagane por el este.': 'Bidezidorra Mallabiako punturik altueneraino: ur-jauziak, historiaurreko trikuharri bat eta gailurrerdi bat bi aldeetara bistak dituena, Zengotitagane ekialdetik inguratu aurretik.',
    'Circuito largo desde Trabakua: la colegiata cisterciense de Zenarruza, una ermita de pastores en la ladera del Oiz y el dolmen de Iturzurigana, con dos subidas largas seguidas.': 'Zirkuitu luzea Trabakuatik: Zenarruzako kolegiata zisterziarra, artzainen ermita bat Oizen hegalean eta Iturzuriganako trikuharria, bi igoera luze jarraian.',
    'Circuito desde Trabakua por ermitas y caser&iacute;os del Duranguesado hasta la Necr&oacute;polis de Argi&ntilde;eta, veinte sarc&oacute;fagos medievales en Elorrio.': 'Zirkuitua Trabakuatik, Durangaldeko ermita eta baserrien artean, Argi&ntilde;etako Nekropoliraino, hogei bat Erdi Aroko hilobi Elorrion.',
    'Sendero corto y familiar hasta la cascada de Gerea.': 'Bidezidor laburra eta familiarra Gereako ur-jauziraino.',
    'Circuito largo en e-bike desde Trabakua a Zengotitagane e Iturzurigana, con dos ermitas de camino.': 'Zirkuitu luzea e-bikez Trabakuatik Zengotitagane eta Iturzuriganaraino, bidean bi ermitarekin.',
    'Circuito largo en e-bike desde Trabakua a Zengotitagane y Askako, con las ermitas de San Crist&oacute;bal Txiki y San Juan de camino.': 'Zirkuitu luzea e-bikez Trabakuatik Zengotitagane eta Askakoraino, San Kristobal Txiki eta San Juan ermitak bidean.',
    'Ida y vuelta desde Trabakua hasta el Oiz, con dos altos de camino y vistas a la costa cant&aacute;brica desde la cumbre.': 'Joan-etorria Trabakuatik Oizeraino, bidean bi goirekin eta kostalde kantauriarrerako ikuspegiekin gailurretik.',
    'Circuito corto desde la Ermita de San Juan, con dos altos de camino y una cruz de piedra en cada uno.': 'Zirkuitu laburra San Juan ermitatik, bidean bi goirekin eta bakoitzean harrizko gurutze batekin.',
    'Circuito desde Trabakua por Arandomendi, Urko y el Collado de Asuntza.': 'Zirkuitua Trabakuatik, Arandomendi, Urko eta Asuntzako lepotik.',
    'Circuito en e-bike desde Trabakua por Barinaga hasta Iturreta y Mendibil.': 'Zirkuitua e-bikez Trabakuatik, Barinaga, Iturreta eta Mendibiletik igarota.',
    'Circuito en e-bike desde Trabakua por Urko, Egoarbitza y Santamañesar hasta Zengotitagane.': 'Zirkuitua e-bikez Trabakuatik, Urko, Egoarbitza eta Santamañesarretik igarota Zengotitaganeraino.',
    'Circuito en e-bike desde Trabakua por Iturreta, Markina y Urregarai hasta Bolibar.': 'Zirkuitua e-bikez Trabakuatik, Iturreta, Markina eta Urregaraitik igarota Bolibarreraino.',
    'Circuito en e-bike desde Trabakua por Urko, Kalamua, San Migel, Markina, Iturreta y Mendibil.': 'Zirkuitua e-bikez Trabakuatik, Urko, Kalamua, San Migel, Markina, Iturreta eta Mendibiletik igarota.',
    'Circuito desde Trabakua hasta la cueva de Mundioko Koba, pasando por el Collado de Asuntza.': 'Zirkuitua Trabakuatik Mundioko Kobaraino, Asuntzako lepotik igarota.',
    'Circuito desde Trabakua por Iturreta, Iruzubieta, Arta y Gerea.': 'Zirkuitua Trabakuatik, Iturreta, Iruzubieta, Arta eta Gereatik igarota.',
    'Circuito desde Trabakua hasta la cima del Mendibil.': 'Zirkuitua Trabakuatik Mendibilgo gailurreraino.',
    'Circuito desde Trabakua por Mendibil, Olamendi y Arteta.': 'Zirkuitua Trabakuatik, Mendibil, Olamendi eta Artetatik igarota.',
    'Paseo corto y llano por el barrio Goita, con vistas y dos ermitas de camino.': 'Ibilbide laburra eta laua Goita auzotik, ikuspegiekin eta bi ermitarekin bidean.',
    'El recorrido real de la carrera Hiru Txikiak Trail, con salida y meta en Ermua.': 'Hiru Txikiak Trail lasterketaren benetako ibilbidea, Ermuan irten eta amaituz.',
    'Circuito muy largo en e-bike desde Trabakua, con paso por Aixola, Elgeta y Zaldibar antes de volver por Berriz.': 'Zirkuitu oso luzea e-bikez Trabakuatik, Aixola, Elgeta eta Zaldibartik igarota, Berriztik itzuli aurretik.',
    'Circuito muy largo en e-bike desde Trabakua, con paso por Zengotitagane, el Dolmen de Iturzurigana y Maguna.': 'Zirkuitu oso luzea e-bikez Trabakuatik, Zengotitagane, Iturzuriganako Trikuharria eta Magunatik igarota.',
    'El trazado real de la 7 Pago Mendi Lasterketa, con paso por la cima del Oiz.': '7 Pago Mendi Lasterketaren benetako ibilbidea, Oizko gailurretik igarota.',
    'El trazado real de la 7 Pago Mendi Lasterketa 16K, por los montes y barrios de Mallabia.': '7 Pago Mendi Lasterketako 16K-ko benetako ibilbidea, Mallabiko mendi eta auzoetan barrena.',
}

# <meta name="description"> per page (head files)
DESCRIPTIONS = {
    'mallabia': 'Mallabia inguruko auzoak, mendiak eta herriak zeharkatzen dituzten ibilbideak. '
        'Bertatik bertara dokumentatuak, benetako datuekin, ez liburuxka batekoak.',
    'trabakua': 'Trabakua, Asuntzako lepoa eta San Juan Artetako ermita Trabakuatik',
    'iturrizuri': 'Iturzuri, Probazelaiburu II.a tumulua eta Zengotitagane Trabakuatik',
    'zenarruza': 'Zenarruzako monasterioa, San Kristobal ermita eta Zengotitagane Trabakuatik',
    'osma': 'Zirkuitua Trabakuatik, Osma eta Argi&ntilde;etako Nekropolitik',
    'gerea': 'Zirkuitua Trabakuatik Gereako ur-jauzira',
    'zengotitagane': 'Zirkuitua Trabakuatik, San Kristobal Txiki eta San Juan ermitekin',
    'oiz': 'Joan-etorria Trabakuatik Oizeraino',
    'arietzu': 'Zirkuitua San Juan ermitatik',
    'urko': 'Zirkuitua Trabakuatik, Arandomendi, Urko eta Asuntzako lepotik',
    'sancristobal': 'Zirkuitua Trabakuatik, Zengotitagane eta Askakotik, San '
        'Kristobal Txiki eta San Juan ermitekin',
    'iturreta': 'Zirkuitua e-bikez Trabakuatik, Barinaga, Iturreta eta Mendibiletik igarota',
    'egoarbitza': 'Zirkuitua e-bikez Trabakuatik, Urko, Egoarbitza eta Santamañesarretik '
        'igarota Zengotitaganeraino',
    'urregarai': 'Zirkuitua e-bikez Trabakuatik, Iturreta, Markina eta Urregaraitik '
        'igarota Bolibarreraino',
    'kalamua': 'Zirkuitua e-bikez Trabakuatik, Urko, Kalamua, San Migel, Markina, '
        'Iturreta eta Mendibiletik igarota',
    'mundiokokoba': 'Zirkuitua Trabakuatik Mundioko Kobaraino, Asuntzako lepotik igarota',
    'iruzubieta': 'Zirkuitua Trabakuatik, Iturreta, Iruzubieta, Arta eta Gereatik igarota',
    'mendibil': 'Zirkuitua Trabakuatik Mendibilgo gailurreraino',
    'arteta': 'Zirkuitua Trabakuatik, Mendibil, Olamendi eta Artetatik igarota',
    'goita': 'Ibilbide zirkularra Goita auzotik, Trabakuatik',
    'hirutxikiak': 'Urko, Oiz eta Egoarbitza Ermuatik',
    'zaldibar': 'Zirkuitua e-bikez Trabakuatik, Aixola, Elgeta eta Zaldibartik igarota Berrizeraino',
    'maguna': 'Zirkuitua e-bikez Trabakuatik, Zengotitagane eta Iturzuriganako '
        'Trikuharritik igarota Magunaraino',
    '7pago': '7 Pago Mendi Lasterketaren benetako ibilbidea, Oizko gailurretik igarota',
    '7pago16': '7 Pago Mendi Lasterketako 16K-ko benetako ibilbidea, Mallabiko mendi eta auzoetan barrena',
    'historias': 'Mallabiako 24 ibilbideak, banan-banan: track bakoitzaren benetako '
        'forma da bere azala. Irristatu, konparatu eta sartu ibilbide bakoitzaren mapan.',
}

# <title> per page (head files)
TITLES = {
    'mallabia': 'Trabakutik · Herriko ibilbideak · Oinez eta bizikletaz Bizkaian',
    'trabakua': 'Asuntza bira · Bizikleta ibilbidea — Herriko ibilbideak',
    'iturrizuri': 'Iturzuri eta Zengotitagane · Oinezko ibilbidea — Herriko ibilbideak',
    'zenarruza': 'Zenarruza eta San Kristobal · Bizikleta ibilbidea — Herriko ibilbideak',
    'osma': 'Trabakua, Elgeta eta Argiñeta · Bizikleta ibilbidea — Herriko ibilbideak',
    'gerea': 'Ur Jauziak, Gerea · Oinezko ibilbidea — Herriko ibilbideak',
    'zengotitagane': 'Zengotitagane · Bizikleta ibilbidea — Herriko ibilbideak',
    'oiz': 'Oiz, Trabakuatik · Oinezko ibilbidea — Herriko ibilbideak',
    'arietzu': 'Osmagain eta Arietzu · Oinezko ibilbidea — Herriko ibilbideak',
    'urko': 'Trabakua, Asuntza eta Urko · Oinezko ibilbidea — Herriko ibilbideak',
    'sancristobal': 'Zengotitagane, Askako eta San Kristobal · Bizikleta '
        'ibilbidea — Herriko ibilbideak',
    'iturreta': 'Trabakua, Barinaga eta Iturreta · Bizikleta ibilbidea — Herriko ibilbideak',
    'egoarbitza': 'Urko, Egoarbitza eta Zengotitagane · Bizikleta ibilbidea — Herriko ibilbideak',
    'urregarai': 'Iturreta, Markina eta Urregarai · Bizikleta ibilbidea — Herriko ibilbideak',
    'kalamua': 'Urko, Kalamua, San Migel eta Mendibil · Bizikleta ibilbidea — Herriko ibilbideak',
    'mundiokokoba': 'Mundioko Koba · Oinezko ibilbidea — Herriko ibilbideak',
    'iruzubieta': 'Trabakua, Iturreta eta Iruzubieta · Bizikleta ibilbidea — Herriko ibilbideak',
    'mendibil': 'Trabakua Mendibil · Oinezko ibilbidea — Herriko ibilbideak',
    'arteta': 'Trabakua, Mendibil, Olamendi eta Arteta · Oinezko ibilbidea — Herriko ibilbideak',
    'goita': 'Trabakua, Goita auzoko paseoa · Oinezko ibilbidea — Herriko ibilbideak',
    'hirutxikiak': 'Hiru Txikiak · Trail ibilbidea — Herriko ibilbideak',
    'zaldibar': 'Trabakua, Aixola eta Berriz · Bizikleta ibilbidea — Herriko ibilbideak',
    'maguna': 'Trabakua, Zengotitagane eta Maguna · Bizikleta ibilbidea — Herriko ibilbideak',
    '7pago': '7 Pago Mendi Lasterketa · Ibilbide ofiziala 25K — Herriko ibilbideak',
    '7pago16': '7 Pago Mendi Lasterketa 16K · Ibilbide ofiziala — Herriko ibilbideak',
    'historias': 'Ibilbideak istorio gisa · Herriko ibilbideak',
}

PAGE_STRINGS = {
    'mallabia': HOME,
    'trabakua': TRABAKUA,
    'iturrizuri': ITURZURI,
    'zenarruza': ZENARRUZA,
    'osma': OSMA,
    'gerea': GEREA,
    'zengotitagane': ZENGOTITAGANE,
    'oiz': OIZ,
    'arietzu': ARIETZU,
    'urko': URKO,
    'sancristobal': SANCRISTOBAL,
    'iturreta': ITURRETA,
    'egoarbitza': EGOARBITZA,
    'urregarai': URREGARAI,
    'kalamua': KALAMUA,
    'mundiokokoba': MUNDIOKOKOBA,
    'iruzubieta': IRUZUBIETA,
    'mendibil': MENDIBIL,
    'arteta': ARTETA,
    'goita': GOITA,
    'hirutxikiak': HIRUTXIKIAK,
    'zaldibar': ZALDIBAR,
    'maguna': MAGUNA,
    '7pago': PAGO7,
    '7pago16': PAGO16,
    'historias': HISTORIAS,
}
