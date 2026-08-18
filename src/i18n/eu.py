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
    '<span class="k">Superficie</span>': '<span class="k">Zorua</span>',
    '<span class="k">Tipo</span>': '<span class="k">Mota</span>',
    '<span class="k">Actividad</span>': '<span class="k">Jarduera</span>',
    '<span class="k">Salida</span>': '<span class="k">Irteera</span>',

    # facts values
    '<span class="v">Circuito</span>': '<span class="v">Zirkuitua</span>',
    '<span class="v">Pista</span>': '<span class="v">Pista</span>',
    '<span class="v">Sendero</span>': '<span class="v">Bidezidorra</span>',
    '<span class="v">Mixta</span>': '<span class="v">Nahasia</span>',
    '<span class="v">Bici</span>': '<span class="v">Bizikleta</span>',
    '<span class="v">Senderismo</span>': '<span class="v">Oinez</span>',
}

# Shared by the three route pages.
ROUTE = {
    '&larr; Mallabia': '&larr; Mallabia',
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
    '<b>Superficie</b> y <b>Tipo</b>, observados sobre el terreno.':
        '<b>Distantzia</b> eta <b>Desnibela</b>, benetako GPX trackatik kalkulatuak. '
        '<b>Zorua</b> eta <b>Mota</b>, bertatik bertara ikusiak.',
    '<span class="k">Para quién es</span>': '<span class="k">Norentzat</span>',
    '<span class="k">Para qui&eacute;n es</span>': '<span class="k">Norentzat</span>',
    '<p class="eyebrow">Mapa de la ruta</p>': '<p class="eyebrow">Ibilbidearen mapa</p>',
    'Track GPX real sobre': 'Benetako GPX tracka',
    '&middot; tambi&eacute;n en': 'gainean &middot; Wikilocen ere bai:',
    '&larr; Volver a inicio': '&larr; Itzuli hasierara',
    '<b>· Puerto de Trabakua</b>': '<b>· Trabakuko mendatea</b>',
    '<b>&middot; Puerto de Trabakua</b>': '<b>&middot; Trabakuko mendatea</b>',
    'Circuito — vuelve casi al mismo punto': 'Zirkuitua — ia puntu berera itzultzen da',
    'Circuito &mdash; vuelve casi al mismo punto': 'Zirkuitua &mdash; ia puntu berera itzultzen da',
    'data-marker-title="Trabakua (salida y llegada)"':
        'data-marker-title="Trabakua (irteera eta helmuga)"',
}

HOME = {
    '<span>Rutas del pueblo</span>': '<span>Herriko ibilbideak</span>',

    # hero
    'alt="Bicicleta de montaña junto a un poste de señales en el monte, al atardecer, con Mallabia iluminada al fondo"':
        'alt="Mendiko bizikleta seinale-zutoin baten ondoan mendian, ilunabarrean, Mallabia argiztatuta atzealdean"',
    '<span>Salida desde Mallabia</span>': '<span>Mallabiatik irtenda</span>',
    '<span>Barrios, montes y pueblos del entorno</span>':
        '<span>Inguruko auzoak, mendiak eta herriak</span>',
    '<h1>Mallabia<br><em>a pie y en bici</em></h1>':
        '<h1>Mallabia<br><em>oinez eta bizikletaz</em></h1>',
    'Rutas que salen de Mallabia y recorren los barrios, montes y pueblos de alrededor. '
    'Documentadas sobre el terreno, con datos de verdad, no de folleto.':
        'Mallabiatik irten eta inguruko auzoak, mendiak eta herriak zeharkatzen dituzten ibilbideak. '
        'Bertatik bertara dokumentatuak, benetako datuekin, ez liburuxka batekoak.',

    # readout
    '<span class="k">Recorrido documentado</span>': '<span class="k">Dokumentatutako ibilbidea</span>',
    '<span class="k">Desnivel acumulado</span>': '<span class="k">Metatutako desnibela</span>',
    '<span class="k">Track GPX real</span>': '<span class="k">Benetako GPX tracka</span>',
    '<span class="k">Rutas documentadas</span>': '<span class="k">Dokumentatutako ibilbideak</span>',

    # mini gallery
    '<p class="eyebrow">Sobre el terreno</p>': '<p class="eyebrow">Bertatik bertara</p>',
    'alt="Vista desde un alto sobre los montes de alrededor de Mallabia, con una cruz de madera en primer plano"':
        'alt="Mallabia inguruko mendien gaineko bista goi batetik, egurrezko gurutze bat aurrealdean"',
    'alt="Grupo caminando por un sendero de piedra junto a un arroyo, entre bosque"':
        'alt="Taldea harrizko bidezidorretik oinez, erreka baten ondoan, basoan barrena"',
    'alt="Bicicleta de montaña apoyada en un mojón de piedra, con niebla"':
        'alt="Mendiko bizikleta harrizko mugarri baten kontra, lainoarekin"',

    # filters
    '<p class="eyebrow">Rutas documentadas</p>': '<p class="eyebrow">Dokumentatutako ibilbideak</p>',
    'aria-label="Filtrar por actividad"': 'aria-label="Iragazi jardueraren arabera"',
    '>Bici</button>': '>Bizikleta</button>',
    '>Senderismo</button>': '>Oinez</button>',
    'data-no-limit="(sin l&iacute;mite)" data-approx="aprox."':
        'data-no-limit="(mugarik gabe)" data-approx="inguru"',
    'Distancia hasta': 'Distantzia gehienez',
    'Desnivel hasta': 'Desnibela gehienez',
    'No hay rutas de este tipo todav&iacute;a.': 'Oraindik ez dago mota honetako ibilbiderik.',
    'Según vayamos documentando más rutas, se añaden aquí.':
        'Ibilbide gehiago dokumentatu ahala, hemen gehituko dira.',

    # route cards
    'alt="Pista de cemento y piedra en la ruta de Trabakua"':
        'alt="Zementuzko eta harrizko pista Trabakuako ibilbidean"',
    '<h2>Trabakua<br><em>bira</em></h2>': '<h2>Trabakua<br><em>bira</em></h2>',
    'Pista entre cemento, piedra y tierra, con un repecho duro al principio —no llega a 300 m—, '
    'un desvío técnico opcional a Aginaga y vistas al Duranguesado desde Berano. '
    'Grabada sobre el terreno, no propuesta desde un mapa.':
        'Pista zementu, harri eta lur artean; hasieran 300 metro baino gutxiagoko aldapa gogorra du, '
        'Aginagara desbideratze tekniko aukerakoa, eta Durangaldeko ikuspegi zabalak eskaintzen ditu '
        'Beranotik. Ibilbidea terrenoan bertan grabatua dago, ez mapa baten gainean proposatua.',
    'alt="Vista panorámica desde la ruta de Iturzuri, con el valle cubierto de niebla"':
        'alt="Bista panoramikoa Iturzuriko ibilbidetik, harana lainoz estalita"',
    '<h2>Iturzuri, Zengotitagane<br><em>subida por la cascada</em></h2>':
        '<h2>Iturzuri, Zengotitagane<br><em>ur-jauzitik gora</em></h2>',
    'Sendero hasta el punto más alto de Mallabia: cascadas, un dolmen prehistórico y un cresterio '
    'con vistas a ambos lados antes de rodear Zengotitagane por el este. '
    'Grabada sobre el terreno, no propuesta desde un mapa.':
        'Bidezidorra Mallabiako punturik altueneraino: ur-jauziak, historiaurreko trikuharri bat '
        'eta gailurrerdi bat bi aldeetara bistak dituena, Zengotitagane ekialdetik inguratu aurretik. '
        'Bertatik bertara grabatua, ez mapa batetik proposatua.',
    'alt="Arroyo entre el bosque durante la subida hacia San Kristobal, ruta de Zenarruza"':
        'alt="Erreka basoan barrena San Kristobalerako igoeran, Zenarruzako ibilbidea"',
    '<h2>Zenarruza, San Kristobal<br><em>y Zengotitagane</em></h2>':
        '<h2>Zenarruza, San Kristobal<br><em>eta Zengotitagane</em></h2>',
    'Circuito largo desde Trabakua: la colegiata cisterciense de Zenarruza, una ermita de pastores '
    'en la ladera del Oiz y el dolmen de Iturzurigana, con dos subidas largas seguidas. '
    'Grabada sobre el terreno, no propuesta desde un mapa.':
        'Zirkuitu luzea Trabakuatik: Zenarruzako kolegiata zisterziarra, artzainen ermita bat '
        'Oizen hegalean eta Iturzuriganako trikuharria, bi igoera luze jarraian. '
        'Bertatik bertara grabatua, ez mapa batetik proposatua.',
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
    'Bici &middot; Trabakua, Zenarruza y Osma': 'Bizikleta &middot; Trabakua, Zenarruza eta Osma',
    'Senderismo &middot; Iturzuri': 'Oinez &middot; Iturzuri',

    # osma card
    'alt="Presa de Aixola, junto a Larrosako Iturri, en la ruta de Osma"':
        'alt="Aixolako presa, Larrosako Iturritik gertu, Osmako ibilbidean"',
    '<h2>Osma, Argi&ntilde;eta<br><em>y Trabakua</em></h2>':
        '<h2>Osma, Argi&ntilde;eta<br><em>eta Trabakua</em></h2>',
    'Circuito desde Trabakua por ermitas y caser&iacute;os del Duranguesado hasta la Necr&oacute;polis '
    'de Argi&ntilde;eta, veinte sarc&oacute;fagos medievales en Elorrio. Grabada sobre el terreno, no '
    'propuesta desde un mapa.':
        'Zirkuitua Trabakuatik, Durangaldeko ermita eta baserrien artean, Argi&ntilde;etako '
        'Nekropoliraino, hogei bat Erdi Aroko hilobi Elorrion. Bertatik bertara grabatua, ez mapa '
        'batetik proposatua.',
}

TRABAKUA = {
    '<span>Pista</span><span class="sep">/</span><span>Cemento, piedra y tierra</span>':
        '<span>Pista</span><span class="sep">/</span><span>Zementua, harria eta lurra</span>',
    '<span>Circuito</span></p>': '<span>Zirkuitua</span></p>',
    '<h1>Trabakua<br><em>bira</em></h1>': '<h1>Trabakua<br><em>bira</em></h1>',
    'Trabakua, Collado de Asuntza y Ermita de San Juan de Arteta desde Trabakua':
        'Trabakua, Asuntzako lepoa eta San Juan Artetako ermita Trabakuatik',
    'alt="Vistas desde el recorrido de Trabakua, con los montes del Duranguesado al fondo"':
        'alt="Bistak Trabakuako ibilbidetik, Durangaldeko mendiak atzealdean"',
    'alt="Foto ampliada del recorrido de Trabakua"':
        'alt="Trabakuako ibilbidearen argazki handitua"',
    'alt="La pista junto al muro de piedra, con tramos de tierra"':
        'alt="Pista harrizko hormaren ondoan, lurrezko tarteekin"',
    'alt="Vistas al Duranguesado desde la subida, con los aerogeneradores al fondo"':
        'alt="Durangaldeko bistak igoeratik, aerosorgailuak atzealdean"',
    'alt="Manillar de la bici en marcha por la pista de Trabakua"':
        'alt="Bizikletaren manillarra Trabakuako pistan martxan"',
    # The first Spanish paragraph becomes two in Basque -- the natural break
    # falls after the descent, so the </p><p> is part of the replacement.
    'Se sale desde el Alto de Trabakua. Los primeros metros bajan —poco más de un kilómetro— '
    'hasta un cruce a la izquierda donde se deja el asfalto atrás: desde ahí, todo es pista en '
    'solitario, alternando cemento y tramos de piedra. El primer repecho es el más duro de toda '
    'la ruta —se sube de un tirón y se nota en las piernas—, pero no engaña: no llega a los 300 m. '
    'Lo que viene después se lleva mejor.':
        'Ibilbidea Trabakuako mendatean hasten da. Lehen zatia beherantz doa — kilometro bat inguru — '
        'ezkerrerako bidegurutze batera iritsi arte; puntu horretan uzten da asfaltua, eta hemendik '
        'aurrera pista hutsa da, zementu eta harrizko tarteak txandakatuz.</p>\n'
        '    <p>Lehen aldapa da ibilbideko gogorrena: etenik gabe igotzen da eta hanketan nabaritzen '
        'da, baina laburra da — 300 metrora ere ez da iristen. Ondorengoa askoz eramangarriagoa da.',
    'Justo después de esas primeras cuestas hay una buena bajada algo técnica —sin riesgo para '
    'quien tenga algo de soltura— hasta hacernos con el camino de subida, en la zona del barrio '
    'Aginaga, sin perder mucha altura. Se sube de vuelta por esa misma pista de tierra hasta '
    'enlazar de nuevo con la pista principal. Es un tramo opcional: se puede evitar siguiendo '
    'recto, sin desviarse hacia él.':
        'Aldapa horien ostean, beheraldi tekniko samarra dator — trebetasun pixka bat duenarentzat '
        'erraza —, eta hortik berriz hartzen da igoerako bidea Aginaga auzoaren inguruan, altuera '
        'handirik galdu gabe. Tarte hori aukerakoa da: nahi izanez gero, zuzen jarraituta saihestu '
        'daiteke.',
    'La pista rueda bien de principio a fin, sin sendero estrecho de por medio, y en las bajadas '
    'hay pendientes suficientes para coger algo de velocidad y disfrutarlas. El camino cruza Berano '
    'Txiki y la parte alta de Berano, con vistas hacia el barrio de Goita y las montañas del '
    'Duranguesado, antes de remontar de nuevo hacia Trabakua — una vuelta rápida y con paisaje.':
        'Pistak oso ondo rodatu egiten du hasieratik amaierara, bidezidor esturik gabe, eta '
        'beheraldietan nahikoa malda dago abiadura hartzeko eta gozatzeko. Bidea Berano Txiki eta '
        'Beranoko goiko partea zeharkatzen du, Goita eta Durangaldeko mendietarako ikuspegiekin, '
        'Trabakuarantz berriro igotzen hasi aurretik — buelta azkarra eta paisaiaz betea.',
    '<h2>BTT y e-bike</h2>': '<h2>BTT eta e-bike</h2>',
    'Terreno de pista (cemento y piedra, con un tramo opcional de tierra), sin sendero estrecho — '
    'apta para bici de montaña convencional, no solo para eléctrica. El track de esta ficha se '
    'grabó con e-bike (1h 15min), así que el tiempo no sirve de referencia si vas sin asistencia.':
        'Pista-terrenoa (zementua eta harria, eta lurrezko tarte aukerakoa), bidezidor esturik gabe — '
        'mendiko bizikleta arrunterako egokia, ez soilik elektrikorako. Fitxa honetako tracka e-bike '
        'batekin grabatu zen (1h 15 min), beraz, denbora ez da erreferentzia egokia laguntzarik gabe '
        'zoazenerako.',
}

ITURZURI = {
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
    '<h1>Iturzuri, Zengotitagane<br><em>subida por la cascada</em></h1>':
        '<h1>Iturzuri, Zengotitagane<br><em>ur-jauzitik gora</em></h1>',
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
        'alt="Bidezidorra gailurrerditik, aerosorgailuak atzealdean"',
    'alt="Restos junto a un aerogenerador cerca de Zengotitagane"':
        'alt="Hondarrak aerosorgailu baten ondoan Zengotitagane inguruan"',
    'Sale de Trabakua hacia el noreste y, tras cuarenta minutos de subida, llega a la primera '
    'parada: la <b>cascada de Gerena</b>. Sigue subiendo hasta la segunda cascada, la de arriba: '
    'ahí, y solo ahí, se cruza el agua para engancharse a un sendero que sube hacia <b>7 Pago</b>, '
    'escondido entre la vegetación y fácil de perder si no se mira bien por dónde sigue. Ya en la '
    'zona de las siete hayas milenarias que dan nombre a la carrera de montaña de Mallabia, el '
    'camino vuelve a abrirse antes de llegar a la <b>fuente de Iturzuri</b> (km 4,3 · 831 m) —con '
    'agua para llenar cantimploras. Después de la fuente, ya en terreno abierto, aparecen los '
    '<b>túmulos de Iturzuri</b>: el camino gira con fuerza hacia el sureste y gana los últimos '
    'metros hasta el punto más alto de la ruta, el <b>túmulo de Probazelaiburu II</b> (854 m) —un '
    'dolmen prehistórico donde el horizonte se abre entero, con las crestas del Duranguesado '
    'extendiéndose hasta perderse de vista.':
        'Trabakuatik ipar-ekialderantz ateratzen da eta, berrogei minutuko igoeraren ondoren, lehen '
        'geldialdira iristen da: <b>Gerenako ur-jauzia</b>. Bigarren ur-jauziraino igotzen jarraitzen '
        'du, goikoraino: han, eta han bakarrik, ura zeharkatzen da <b>7 Pago</b> alderantz igotzen den '
        'bidezidor bati heltzeko, landaretzaren artean ezkutatuta eta erraz galtzekoa non jarraitzen '
        'duen ondo begiratzen ez bada. Mallabiako mendi-lasterketari izena ematen dioten zazpi pago '
        'milaurtekoen inguruan, bidea berriro zabaltzen da <b>Iturzuriko iturrira</b> (4,3 km · 831 m) '
        '—ura dago kantinplorak betetzeko. Iturriaren ondoren, jada eremu irekian, <b>Iturzuriko '
        'tumuluak</b> agertzen dira: bideak indarrez egiten du hego-ekialderantz eta azken metroak '
        'irabazten ditu ibilbideko punturik altueneraino, <b>Probazelaiburu II.a tumulua</b> (854 m) '
        '—historiaurreko trikuharri bat, non zerumuga osorik zabaltzen den, Durangaldeko gailurrak '
        'begi-bistatik galdu arte hedatzen direla.',
    'Desde el túmulo, el camino sigue el <b>cresterio</b> hacia el este, con vistas abiertas a '
    'ambos lados de la loma, hasta la cima de <b>Zengotitagane</b> (km 5,6 · 801 m). Desde aquí se '
    'puede bajar directo a Trabakua y acortar bastante el día —pero esta vez decidimos seguir: '
    'rodear la montaña por el lado este y alargar la vuelta un poco más.':
        'Tumulutik, bideak <b>gailurrerdiari</b> jarraitzen dio ekialderantz, bistak zabalik '
        'bizkarraren bi aldeetara, <b>Zengotitagane</b> gailurreraino (5,6 km · 801 m). Hemendik '
        'zuzenean jaits daiteke Trabakuara eta eguna nabarmen laburtu —baina oraingoan jarraitzea '
        'erabaki genuen: mendia ekialdetik inguratu eta bira pixka bat gehiago luzatu.',
    'El descenso empieza hacia el sur, por un tramo escondido entre la vegetación que apenas conoce '
    'nadie, hasta una <b>borda abandonada</b> (km 6,1 · 768 m). Ahí el camino gira hacia el este '
    'para rodear la montaña, bajando hasta un <b>refugio de montaña</b> (km 6,6 · 675 m). Desde el '
    'refugio se sigue perdiendo altura hasta casi tocar la carretera general, ya en el barrio de '
    'Osma —pero justo antes de llegar, el camino gira bruscamente y volvemos en dirección norte '
    'hasta enlazar con el camino de ida, ya muy cerca de Trabakua, para cerrar el círculo.':
        'Jaitsiera hegoalderantz hasten da, ia inork ezagutzen ez duen landaretzaren arteko tarte '
        'ezkutu batetik, <b>borda abandonatu</b> bateraino (6,1 km · 768 m). Han bideak ekialderantz '
        'egiten du mendia inguratzeko, <b>mendiko aterpe</b> bateraino jaitsiz (6,6 km · 675 m). '
        'Aterpetik altuera galtzen jarraitzen du errepide nagusia ia ukitu arte, jada Osma auzoan '
        '—baina iritsi baino justu lehenago, bideak bat-batean egiten du eta iparralderantz itzultzen '
        'gara joaneko bidearekin lotu arte, jada Trabakuatik oso gertu, zirkulua ixteko.',
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
    'Sale de Trabakua hacia el norte y, subiendo y bajando por los altos entre Mallabia y '
    'Ziortza-Bolibar, pierde altura de golpe en el &uacute;ltimo tramo hasta el <b>Monasterio de '
    'Zenarruza</b> (km 9,4 &middot; 287 m) &mdash;colegiata cisterciense fundada en el siglo XI, la '
    '&uacute;nica colegiata de Bizkaia y parada hist&oacute;rica del Camino de Santiago del Norte.':
        'Trabakuatik iparralderantz ateratzen da eta, Mallabia eta Ziortza-Bolibar arteko goietan '
        'gora eta behera, altuera bat-batean galtzen du azken tartean <b>Zenarruzako monasterioraino</b> '
        '(9,4 km &middot; 287 m) &mdash;XI. mendean sortutako kolegiata zisterziarra, Bizkaiko kolegiata '
        'bakarra eta Iparraldeko Donejakue Bidearen geldialdi historikoa.',
    'Desde el monasterio el camino gira hacia el oeste-suroeste y no deja de subir en casi 9 km '
    'seguidos, ganando m&aacute;s de 500 m de desnivel por la ladera del Oiz &mdash;cruzando un '
    'arroyo escondido entre el bosque a media subida (km 15,4 &middot; 553 m)&mdash; hasta la '
    '<b>Ermita San Kristobal</b> (km 18,6 &middot; 797 m), antigua ermita-refugio de pastores con '
    'romer&iacute;a el domingo siguiente al 10 de julio.':
        'Monasteriotik bideak mendebalde-hego-mendebalderantz egiten du eta ia 9 km jarraian igotzeari '
        'utzi gabe, 500 m baino gehiagoko desnibela irabaziz Oizen hegaletik &mdash;basoan ezkutatutako '
        'erreka bat zeharkatuz igoeraren erdian (15,4 km &middot; 553 m)&mdash; <b>San Kristobal '
        'ermitaraino</b> (18,6 km &middot; 797 m), artzainen ermita-aterpe zaharra, uztailaren 10aren '
        'hurrengo igandean erromeria egiten duena.',
    'Tras la ermita el camino baja hacia el sur hasta un collado a 605 m (km 22,1) para remontar '
    'despu&eacute;s hacia el este, ganando otra vez altura hasta el punto m&aacute;s alto de toda la '
    'ruta: el <b>Dolmen Iturzurigana</b> (km 26,6 &middot; 863 m). Un kil&oacute;metro m&aacute;s al '
    'este, ya dentro del parque e&oacute;lico del Oiz, se corona <b>Zengotitagane</b> (km 27,7 &middot; 822 m).':
        'Ermitaren ondoren bidea hegoalderantz jaisten da 605 m-ko lepo bateraino (22,1 km) gero '
        'ekialderantz igotzeko, berriro altuera irabaziz ibilbide osoko punturik altueneraino: '
        '<b>Iturzuriganako trikuharria</b> (26,6 km &middot; 863 m). Kilometro bat ekialderago, jada '
        'Oizeko parke eolikoaren barruan, <b>Zengotitagane</b> koroatzen da (27,7 km &middot; 822 m).',
    'Desde Zengotitagane el descenso final va hacia el este-sureste, perdiendo los &uacute;ltimos '
    '400 m de desnivel en poco m&aacute;s de 4 km hasta cerrar el c&iacute;rculo de vuelta en '
    'Trabakua. Una ruta larga, para pedalear hasta saciarse.':
        'Zengotitagatik azken jaitsiera ekialde-hego-ekialderantz doa, azken 400 m-ko desnibela '
        'galduz 4 km pasatxotan, Trabakuan zirkulua itxi arte. Ibilbide luzea, aseraino pedalkatzeko.',
    '<h2>BTT y e-bike</h2>': '<h2>BTT eta e-bike</h2>',
    '31,7 km y +1.161 m de desnivel en un solo circuito. El track de esta ficha se grab&oacute; con '
    'e-bike (2h 06min), as&iacute; que el tiempo no sirve de referencia si vas sin asistencia. Sube '
    'casi sin descanso hasta San Kristobal y vuelve a subir despu&eacute;s del collado hasta el '
    'dolmen: dos tirones largos seguidos.':
        '31,7 km eta +1.161 m-ko desnibela zirkuitu bakarrean. Fitxa honetako tracka e-bikearekin '
        'grabatu zen (2h 06min), beraz denbora ez da erreferentzia laguntzarik gabe bazoaz. Ia '
        'atsedenik gabe igotzen da San Kristobaleraino eta lepoaren ondoren berriro igotzen da '
        'trikuharriraino: bi tirada luze jarraian.',
}

OSMA = {
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
    '<h1>Osma, Argi&ntilde;eta<br><em>y Trabakua</em></h1>':
        '<h1>Osma, Argi&ntilde;eta<br><em>eta Trabakua</em></h1>',
    'Circuito desde Trabakua por Osma y la Necr&oacute;polis de Argi&ntilde;eta':
        'Zirkuitua Trabakuatik, Osma eta Argi&ntilde;etako Nekropolitik',

    'alt="Sarc&oacute;fagos medievales de la Necr&oacute;polis de Argi&ntilde;eta, km 20,1 de la ruta"':
        'alt="Erdi Aroko hilobiak Argi&ntilde;etako Nekropolian, ibilbideko 20,1 km"',
    'alt="Foto ampliada del recorrido de Osma"': 'alt="Osmako ibilbidearen argazki handitua"',
    'alt="Presa de Aixola, junto a Larrosako Iturri, km 11,9 de la ruta"':
        'alt="Aixolako presa, Larrosako Iturritik gertu, ibilbideko 11,9 km"',
    'alt="Fila de sarc&oacute;fagos bajo los &aacute;rboles, Necr&oacute;polis de Argi&ntilde;eta"':
        'alt="Hilobi ilara zuhaitzen azpian, Argi&ntilde;etako Nekropolian"',

    'Sale de Trabakua hacia el suroeste, pasando por la primera <b>Ermita de San Juan</b> (km 1,3 &middot; '
    '412 m), en el barrio de Zengotita &mdash;donde se coge la pista forestal que enlaza con el GR '
    'hacia Areitio&mdash;, camino de la <b>Ermita de Santa Marina</b> (km 5,2 &middot; 319 m), en el '
    'barrio de Goierri, escondida entre robles. Sigue hacia el sureste ganando altura; poco antes de '
    'la presa de Aixola hay una pista de piedra que sube suave y luego baja jugetona hasta la propia '
    'presa, aunque quien prefiera no perder desnivel puede seguir por la pista principal, que llega '
    'al mismo punto sin bajar. Despu&eacute;s de la presa, ya al empezar a subir hacia Elgeta, '
    'est&aacute; <b>Larrosako Iturri</b> (km 11,9 &middot; 355 m), punto de agua a mitad de ruta.':
        'Trabakuatik hego-mendebalderantz ateratzen da, lehen <b>San Juan ermitatik</b> pasatuz (1,3 km '
        '&middot; 412 m), Zengotita auzoan &mdash;hemen hartzen da Areitiorantz doan GRa, baso-pistatik'
        '&mdash;, <b>Santa Marina ermitarantz</b> bidean (5,2 km &middot; 319 m), Goierri auzoan, '
        'haritzen artean ezkutatuta. Hego-ekialderantz jarraitzen du altuera irabaziz; Aixolako presa '
        'baino pixka bat lehenago harrizko pista bat dago, leun igo eta gero presaraino jolasti behera '
        'egiten duena, desnibela galdu nahi ez duenak pista nagusitik jarrai dezakeen arren, puntu '
        'berera iristen dena jaitsi gabe. Presaren ondoren, Elgetarantz igotzen hasita, '
        '<b>Larrosako Iturri</b> dago (11,9 km &middot; 355 m), ur-puntua ibilbidearen erdian.',
    'Desde ah&iacute; sigue subiendo hasta Elgeta, con un tramo recto de asfalto, antes de bajar de '
    'golpe hacia Elorrio, donde est&aacute; la segunda <b>Ermita de San Juan</b> (km 18,8 &middot; '
    '286 m). Kil&oacute;metro y medio '
    'despu&eacute;s gira hacia el noroeste hasta la <b>Necr&oacute;polis de Argi&ntilde;eta</b> (km '
    '20,1 &middot; 247 m), junto a la Ermita de San Adri&aacute;n: una veintena de sarc&oacute;fagos de '
    'piedra y cinco estelas labradas en piedra del Oiz, de los siglos VII a IX &mdash;entre la '
    'epigraf&iacute;a cristiana m&aacute;s antigua encontrada en Bizkaia, Bien de Inter&eacute;s '
    'Cultural desde 1931. Las tumbas, repartidas originalmente por distintos barrios de Elorrio, se '
    'agruparon aqu&iacute; en el siglo XIX por orden del p&aacute;rroco Retolaza. Hay tambi&eacute;n '
    'una fuente junto a la necr&oacute;polis para llenar cantimploras.':
        'Handik Elgetaraino igotzen jarraitzen du, asfaltozko tarte zuzen batetik, Elorriorantz '
        'bat-batean jaitsi aurretik, non dagoen bigarren <b>San Juan ermita</b> (18,8 km &middot; '
        '286 m). Kilometro eta '
        'erdi geroago ipar-mendebalderantz biratzen du <b>Argi&ntilde;etako Nekropoliraino</b> (20,1 km '
        '&middot; 247 m), San Adri&aacute;n ermitaren ondoan: hogei bat harrizko hilobi eta bost estela '
        'Oizeko harrian landuak, VII. eta IX. mendeen artekoak &mdash;Bizkaian aurkitutako kristau '
        'epigrafia zaharrenetakoa, Kultura Ondasun izendatua 1931tik. Hilobiak, jatorriz Elorrioko '
        'hainbat auzotan sakabanatuta, XIX. mendean bildu ziren hemen Retolaza apaizaren aginduz. '
        'Iturri bat ere badago nekropoliaren ondoan, kantinplorak betetzeko.',
    'El camino sigue hacia el noroeste encadenando varias ermitas: San Lorenzo (km 22,4 &middot; 312 '
    'm), San Juan Bautista de Murgoitio (km 24,3 &middot; 277 m) y San Antonio de Olakueta (km 25,8 '
    '&middot; 160 m), donde se pierde altura de golpe. Gira despu&eacute;s hacia el este para subir '
    'hasta la <b>Ermita de San Miguel de Okango</b> (km 28,4 &middot; 227 m) y baja de nuevo hasta '
    '<b>Berriz</b> (km 30,7 &middot; 187 m), en el valle del Ibaizabal, al pie del Oiz.':
        'Bideak ipar-mendebalderantz jarraitzen du hainbat ermita kateatuz: San Lorentzo (22,4 km '
        '&middot; 312 m), Murgoitioko San Juan Bataiatzailea (24,3 km &middot; 277 m) eta Olakuetako '
        'San Antonio (25,8 km &middot; 160 m), non altuera bat-batean galtzen den. Gero ekialderantz '
        'biratzen du <b>Okangoko San Migel ermitaraino</b> igotzeko (28,4 km &middot; 227 m) eta '
        'berriro jaisten da <b>Berrizeraino</b> (30,7 km &middot; 187 m), Ibaizabal haranean, Oizen '
        'oinean.',
    'Ya de vuelta, pasa por una segunda <b>Ermita de San Lorenzo</b> (km 32,1 &middot; 264 m), en el '
    'barrio de San Lorenzo (Mend&iacute;bil-Sallobente), cerca de la Casa Madre de las Mercedarias '
    'Misioneras de B&eacute;rriz, antes de subir sin parar los &uacute;ltimos 4,7 km y 143 m de '
    'desnivel de vuelta hasta Trabakua, para cerrar el c&iacute;rculo.':
        'Itzuli bidean, bigarren <b>San Lorentzo ermitatik</b> pasatzen da (32,1 km &middot; 264 m), '
        'San Lorentzo auzoan (Mend&iacute;bil-Sallobente), B&eacute;rrizko Mertzedarien Misiolarien Ama '
        'Etxetik gertu, azken 4,7 km-ak eta 143 m-ko desnibela etenik gabe igo aurretik Trabakuara, '
        'zirkulua ixteko.',

    '<h2>BTT y e-bike</h2>': '<h2>BTT eta e-bike</h2>',
    '<p>36,8 km y +1.002 m de desnivel en un solo circuito, entre ermitas y caser&iacute;os del '
    'Duranguesado. El track de esta ficha se grab&oacute; con e-bike (2h 50min), as&iacute; que el '
    'tiempo no sirve de referencia si vas sin asistencia. Hay agua en Larrosako Iturri (km 11,9) y '
    'junto a la Necr&oacute;polis de Argi&ntilde;eta (km 20,1).</p>':
        '<p>36,8 km eta +1.002 m-ko desnibela zirkuitu bakarrean, Durangaldeko ermita eta baserrien '
        'artean. Fitxa honetako tracka e-bikearekin grabatu zen (2h 50min), beraz denbora ez da '
        'erreferentzia laguntzarik gabe bazoaz. Ura dago Larrosako Iturrin (11,9 km) eta Argi&ntilde;etako '
        'Nekropolitik gertu (20,1 km).</p>',
}

# <title> per page (head files)
TITLES = {
    'mallabia': 'Mallabia',
    'trabakua': 'Trabakua',
    'iturrizuri': 'Iturzuri · Zengotitagane',
    'zenarruza': 'Zenarruza · San Kristobal · Zengotitagane',
    'osma': 'Osma · Argiñeta · Trabakua',
}

PAGE_STRINGS = {
    'mallabia': HOME,
    'trabakua': TRABAKUA,
    'iturrizuri': ITURZURI,
    'zenarruza': ZENARRUZA,
    'osma': OSMA,
}
