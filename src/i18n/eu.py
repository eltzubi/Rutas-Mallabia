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

    # facts values
    '<span class="v">Circuito</span>': '<span class="v">Zirkuitua</span>',
    '<span class="v">Ida y vuelta</span>': '<span class="v">Joan-etorria</span>',
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
        '<b>Azalera</b> eta <b>Mota</b>, bertatik bertara ikusiak.',
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
    'aria-label="Ampliar mapa"': 'aria-label="Handitu mapa"',
    'data-label-expand="Ampliar mapa"': 'data-label-expand="Handitu mapa"',
    'data-label-collapse="Reducir mapa"': 'data-label-collapse="Txikitu mapa"',
}

HOME = {
    '<span class="brand-name">Rutas en torno al <em>pueblo</em></span>':
        '<span class="brand-name">Herri inguruko <em>ibilbideak</em></span>',

    # hero
    'alt="Bicicleta de montaña junto a un poste de señales en el monte, al atardecer, con Mallabia iluminada al fondo"':
        'alt="Mendiko bizikleta seinale-zutoin baten ondoan mendian, ilunabarrean, Mallabia argiztatuta atzealdean"',
    'alt="Bicicleta de montaña con el foco encendido junto a un poste de señales, al '
    'anochecer, con un refugio de montaña y el valle iluminado al fondo"':
        'alt="Mendiko bizikleta fokua piztuta seinale-zutoin baten ondoan, ilunabarrean, '
        'mendiko aterpe batekin eta harana argiztatuta atzealdean"',
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
    'aria-label="Antes de salir y d&oacute;nde aparcar"':
        'aria-label="Irten aurretik eta non aparkatu"',
    'Ver como historias &rarr;': 'Ikusi istorio gisa &rarr;',
    '<span class="k">Antes de salir</span>': '<span class="k">Irten aurretik</span>',
    '<h2>GPS obligatorio</h2>': '<h2>GPSa nahitaezkoa</h2>',
    'aria-label="Rutas desde Trabakua"': 'aria-label="Trabakuatik abiatzen diren ibilbideak"',
    '<span class="signpost-name">Iturzuri, Zengotitagane subida por la cascada de Gerea</span>':
        '<span class="signpost-name">Iturzuri, Zengotitagane Gereako ur-jauzitik gora</span>',
    '<span class="signpost-name">Zenarruza, San Kristobal y Zengotitagane</span>':
        '<span class="signpost-name">Zenarruza, San Kristobal eta Zengotitagane</span>',
    '<span class="signpost-name">Ur Jauziak Gerea</span>':
        '<span class="signpost-name">Ur Jauziak Gerea</span>',
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
    'Las rutas est&aacute;n documentadas sobre el terreno, no dise&ntilde;adas desde un mapa, pero la '
    'informaci&oacute;n es b&aacute;sica: no est&aacute;n se&ntilde;alizadas, as&iacute; que llevar GPS '
    'es casi obligatorio. Se apunta lo m&aacute;s relevante para orientarte por el camino &mdash;'
    'vistas, fuentes de agua, alg&uacute;n cruce&mdash;, pero no sustituye al track cargado en el '
    'dispositivo.':
        'Ibilbideak bertan bertatik dokumentatuta daude, ez mapa batetik dise&ntilde;atuta, baina '
        'informazioa oinarrizkoa da: ez daude seinalizatuta, beraz GPSa eramatea ia derrigorrezkoa '
        'da. Bidean orientatzeko garrantzitsuena jasotzen da &mdash;ikuspegiak, ur-iturriak, noizbehinka '
        'gurutze bat&mdash;, baina ez du ordezten gailuan kargatutako trackak.',
    'aria-label="Filtrar por actividad"': 'aria-label="Iragazi jardueraren arabera"',
    '>Bici</button>': '>Bizikleta</button>',
    '>Senderismo</button>': '>Oinez</button>',
    'data-no-limit="(sin l&iacute;mite)" data-approx="aprox."':
        'data-no-limit="(mugarik gabe)" data-approx="inguru"',
    'aria-label="Distancia m&iacute;nima"': 'aria-label="Gutxieneko distantzia"',
    'aria-label="Distancia m&aacute;xima"': 'aria-label="Gehieneko distantzia"',
    'aria-label="Desnivel m&iacute;nimo"': 'aria-label="Gutxieneko desnibela"',
    'aria-label="Desnivel m&aacute;ximo"': 'aria-label="Gehieneko desnibela"',
    '<label>Distancia <b': '<label>Distantzia <b',
    '<label>Desnivel <b': '<label>Desnibela <b',
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
    'Bici &middot; Trabakua, Zenarruza, Osma, Zengotitagane, San Crist&oacute;bal y Urregarai':
        'Bizikleta &middot; Trabakua, Zenarruza, Osma, Zengotitagane, San Kristobal eta Urregarai',
    'Senderismo &middot; Iturzuri, Gerea, Oiz, Arietzu, Urko, Egoarbitza y Urregarai':
        'Oinez &middot; Iturzuri, Gerea, Oiz, Arietzu, Urko, Egoarbitza eta Urregarai',
    'Toca una ruta en el mapa para ver su informaci&oacute;n.':
        'Sakatu ibilbide bat mapan, bere informazioa ikusteko.',

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
        'alt="Pista aerosorgailuen ondoan, lainoak gailurra estaltzen duela"',
    '<h2>Zengotitagane, Askako<br><em>y San Crist&oacute;bal</em></h2>':
        '<h2>Zengotitagane, Askako<br><em>eta San Kristobal</em></h2>',
    'Circuito largo en e-bike desde Trabakua a Zengotitagane y Askako, con las '
    'ermitas de San Crist&oacute;bal Txiki y San Juan de camino.':
        'Zirkuitu luzea e-bikez Trabakuatik Zengotitagane eta Askakoraino, San '
        'Kristobal Txiki eta San Juan ermitak bidean.',

    # oiz card
    'alt="Aerogeneradores del Oiz reflejados en un charco de la cumbre, con las antenas al '
    'fondo"':
        'alt="Oizeko aerosorgailuak gailurreko putzu batean islatuta, antenak atzealdean"',
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
        'alt="Bizikleta elektrikoaren eskulekua sasi arteko bidezidor batean, Oizeko aerosorgailuak atzealdean"',
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
    'Circuito de trail desde Trabakua por Urko, Egoarbitza y Santamañesar hasta Zengotitagane.':
        'Zirkuitua trailez Trabakuatik, Urko, Egoarbitza eta Santamañesarretik igarota Zengotitaganeraino.',

    # urregarai card
    '<span class="signpost-name">Iturreta, Markina y Urregarai</span>':
        '<span class="signpost-name">Iturreta, Markina eta Urregarai</span>',
    '<span class="v">Senderismo y bici</span>':
        '<span class="v">Oinez eta bizikleta</span>',
    'alt="Amanecer con luz anaranjada sobre las monta&ntilde;as, al salir de Trabakua"':
        'alt="Egunsentia argi laranjaz mendien gainean, Trabakuatik irtetean"',
    '<h2>Iturreta, Markina<br><em>y Urregarai</em></h2>':
        '<h2>Iturreta, Markina<br><em>eta Urregarai</em></h2>',
    'Circuito de trail desde Trabakua por Iturreta, Markina y Urregarai hasta Bolibar.':
        'Zirkuitua trailez Trabakuatik, Iturreta, Markina eta Urregaraitik igarota Bolibarreraino.',
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
        'alt="Durangaldeko bistak igoeratik, aerosorgailuak atzealdean"',
    'alt="Manillar de la bici en marcha por la pista de Trabakua"':
        'alt="Bizikletaren manillarra Trabakuako pistan martxan"',
    'alt="Vistas al Duranguesado desde Berano, con caseríos y prados en el valle"':
        'alt="Durangaldeko bistak Beranotik, baserriak eta larreak haranean"',
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
    'Aginaga, sin perder mucha altura. Desde Aginaga se sube por un tramo de pista de cemento '
    'hasta enlazar con el camino de tierra, de vuelta a la pista principal, justo al collado de '
    'Asuntza. Es un tramo opcional: '
    'se puede evitar siguiendo recto, sin desviarse hacia él.':
        'Aldapa horien ostean, beheraldi tekniko samarra dator — trebetasun pixka bat duenarentzat '
        'erraza —, eta hortik berriz hartzen da igoerako bidea Aginaga auzoaren inguruan, altuera '
        'handirik galdu gabe. Aginagatik zementuzko pista-tarte batetik igotzen da lurrezko '
        'bidearekin lotu arte, pista nagusira itzultzeko, Asuntzako lepoan bertan. Tarte hori '
        'aukerakoa da: nahi izanez '
        'gero, zuzen jarraituta saihestu daiteke.',
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
    'grabó con e-bike —una Orbea Rise— (1h 15min), así que el tiempo no sirve de referencia si vas '
    'sin asistencia.':
        'Pista-terrenoa (zementua eta harria, eta lurrezko tarte aukerakoa), bidezidor esturik gabe — '
        'mendiko bizikleta arrunterako egokia, ez soilik elektrikorako. Fitxa honetako tracka e-bike '
        'batekin grabatu zen —Orbea Rise bat— (1h 15 min), beraz, denbora ez da erreferentzia egokia '
        'laguntzarik gabe zoazenerako.',
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
    'Sale de Trabakua hacia el norte y, subiendo y bajando por los altos entre Mallabia y '
    'Ziortza-Bolibar, pierde altura de golpe en el &uacute;ltimo tramo hasta el <b>Monasterio de '
    'Zenarruza</b> (km 9,4 &middot; 287 m) &mdash;colegiata cisterciense fundada en el siglo XI, la '
    '&uacute;nica colegiata de Bizkaia y parada hist&oacute;rica del Camino de Santiago del Norte.':
        'Trabakuatik iparralderantz ateratzen da eta, Mallabia eta Ziortza-Bolibar arteko goietan '
        'gora eta behera, altuera bat-batean galtzen du azken tartean <b>Zenarruzako monasterioraino</b> '
        '(9,4 km &middot; 287 m) &mdash;XI. mendean sortutako kolegiata zisterziarra, Bizkaiko kolegiata '
        'bakarra eta Iparraldeko Donejakue Bidearen geldialdi historikoa.',
    'Desde el monasterio el camino gira hacia el oeste-suroeste y sube por la ladera del Oiz durante '
    'casi 9 km, ganando m&aacute;s de 500 m de desnivel &mdash;con un buen tramo llano a media subida '
    'para recuperarse, cruzando un arroyo escondido entre el bosque (km 15,4 &middot; 553 m)&mdash; '
    'hasta la '
    '<b>Ermita San Kristobal</b> (km 18,6 &middot; 797 m), antigua ermita-refugio de pastores con '
    'romer&iacute;a el domingo siguiente al 10 de julio.':
        'Monasteriotik bideak mendebalde-hego-mendebalderantz egiten du eta Oizen hegaletik igotzen da '
        'ia 9 km-tan zehar, 500 m baino gehiagoko desnibela irabaziz &mdash;igoeraren erdian tarte '
        'lau on bat du, indarrak berreskuratzeko, basoan ezkutatutako erreka bat zeharkatuz (15,4 km '
        '&middot; 553 m)&mdash; <b>San Kristobal '
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
    'e-bike &mdash;una Orbea Rise&mdash; (2h 06min), as&iacute; que el tiempo no sirve de referencia '
    'si vas sin asistencia. Sube '
    'casi sin descanso hasta San Kristobal y vuelve a subir despu&eacute;s del collado hasta el '
    'dolmen: dos tirones largos seguidos.':
        '31,7 km eta +1.161 m-ko desnibela zirkuitu bakarrean. Fitxa honetako tracka e-bikearekin '
        'grabatu zen &mdash;Orbea Rise batekin&mdash; (2h 06min), beraz denbora ez da erreferentzia '
        'laguntzarik gabe bazoaz. Ia '
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

    'Esta ruta sale de Trabakua hacia el suroeste, hasta el barrio de Zengotita (km 1,3 &middot; 412 '
    'm), donde se coge la pista forestal que llega desde Areitio y enlaza con el GR &mdash;que va casi '
    'en llano, en paralelo al monte Arietzu&mdash;, camino del barrio de Goierri (km 5,2 &middot; 319 '
    'm), escondido entre robles. Se sigue ganando altura por esa pista hacia el sureste hasta '
    'dejarla, poco antes de la presa de Aixola, para bajar por un tramo de tierra juget&oacute;n hasta '
    'la propia presa &mdash;quien prefiera no perder desnivel puede seguir por la pista principal, '
    'que llega al mismo punto sin bajar. Despu&eacute;s de la presa, ya al empezar a subir hacia '
    'Elgeta, est&aacute; <b>Larrosako Iturri</b> (km 11,9 &middot; 355 m), punto de agua a mitad de '
    'ruta.':
        'Ibilbide honek Trabakuatik hego-mendebalderantz egiten du, Zengotita auzoraino (1,3 km '
        '&middot; 412 m), hemen hartzen baita Areitiotik datorren eta GRarekin lotzen '
        'den baso-pista &mdash;ia laua, Arietzu mendiaren paraleloan&mdash;, '
        'Goierri auzorantz bidean (5,2 km &middot; 319 m), '
        'haritzen artean ezkutatuta. Pista horretatik jarraitzen da altuera irabaziz hego-ekialderantz, '
        'Aixolako presa baino pixka bat lehenago utzi arte, lurrezko tarte jolasti batetik presaraino '
        'jaisteko &mdash;desnibela galdu nahi ez duenak pista nagusitik jarrai dezake, puntu berera '
        'iristen dena jaitsi gabe. Presaren ondoren, Elgetarantz igotzen hasita, '
        '<b>Larrosako Iturri</b> dago (11,9 km &middot; 355 m), ur-puntua ibilbidearen erdian.',
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
        'Handik Elgetaraino igotzen jarraitzen du, jada Durangaldean, eta bihurguneen artean '
        'jarraitzen du '
        'asfaltozko tarte batetik '
        'Elorriorantz jaisteko bidegurutzeraino, Aldape auzotik, bat-batean jaitsi aurretik (18,8 km '
        '&middot; 286 m). Kilometro eta '
        'erdi geroago ipar-mendebalderantz biratzen du <b>Argi&ntilde;etako Nekropoliraino</b> (20,1 km '
        '&middot; 247 m): hogei bat harrizko hilobi eta bost estela '
        'Oizeko harrian landuak, VII. eta IX. mendeen artekoak &mdash;Bizkaian aurkitutako kristau '
        'epigrafia zaharrenetakoa, Kultura Ondasun izendatua 1931tik. Hilobiak, jatorriz Elorrioko '
        'hainbat auzotan sakabanatuta, XIX. mendean bildu ziren hemen Retolaza apaizaren aginduz. '
        'Iturri bat ere badago nekropoliaren ondoan, kantinplorak betetzeko.',
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
        'Handik gora jarraitzen du Mendraca auzorantz, non paisaia ikuspegi zabal batean irekitzen '
        'den, Elorriorantz eta Udalaitza bezalako gailurretara begira, eta bideak asfaltoa utzi eta '
        'bidezidor eta lurrezko pista bihurtzen den (22,4 km &middot; 312 m). <b>Murgoitioko San Juan '
        'Bataiatzailetik</b> pasatzen da (24,3 km &middot; 277 '
        'm) &mdash;XVII. mendeko erregistroak ditu inoiz induskatu gabeko hilobi bikoitzei buruz, '
        'Argi&ntilde;etakoen antzekoak&mdash; eta Olakueta auzotik (25,8 km &middot; 160 m), non '
        'altuera bat-batean galtzen den. Gero ekialderantz biratzen du, Zaldibar herrira sartu gabe '
        'bordeatuz, <b>Okangoko San Migel ermitaraino</b> igotzeko (28,4 km &middot; 227 m), auzoaren '
        'zaindaria eta irailaren 29an jaiak dituena, bolo-jokoz eta odolkiz, eta berriro jaisten da '
        '<b>Berrizeraino</b> (30,7 km &middot; 187 m), Ibaizabal haranean, Oizen oinean.',
    'Ya de vuelta, pasa por el barrio de San Lorenzo (Mend&iacute;bil-Sallobente) (km 32,1 &middot; '
    '264 m), cerca de la Casa Madre de las Mercedarias '
    'Misioneras de B&eacute;rriz, antes de subir sin parar los &uacute;ltimos 4,7 km y 143 m de '
    'desnivel de vuelta hasta Trabakua, para cerrar el c&iacute;rculo.':
        'Itzuli bidean, San Lorentzo auzotik pasatzen da (Mend&iacute;bil-Sallobente) (32,1 km '
        '&middot; 264 m), '
        'B&eacute;rrizko Mertzedarien Misiolarien Ama '
        'Etxetik gertu, azken 4,7 km-ak eta 143 m-ko desnibela etenik gabe igo aurretik Trabakuara, '
        'zirkulua ixteko.',

    '<h2>BTT y e-bike</h2>': '<h2>BTT eta e-bike</h2>',
    '<p>36,8 km y +1.002 m de desnivel en un solo circuito, entre ermitas y caser&iacute;os del '
    'Duranguesado. El track de esta ficha se grab&oacute; con e-bike &mdash;una Orbea Rise&mdash; '
    '(2h 50min), as&iacute; que el '
    'tiempo no sirve de referencia si vas sin asistencia. Hay agua en Larrosako Iturri (km 11,9) y '
    'junto a la Necr&oacute;polis de Argi&ntilde;eta (km 20,1).</p>':
        '<p>36,8 km eta +1.002 m-ko desnibela zirkuitu bakarrean, Durangaldeko ermita eta baserrien '
        'artean. Fitxa honetako tracka e-bikearekin grabatu zen &mdash;Orbea Rise batekin&mdash; '
        '(2h 50min), beraz denbora ez da '
        'erreferentzia laguntzarik gabe bazoaz. Ura dago Larrosako Iturrin (11,9 km) eta Argi&ntilde;etako '
        'Nekropolitik gertu (20,1 km).</p>',
}

GEREA = {
    '<title>Vistas a Gerea': '<title>Gereako ikuspegiak',
    '<span class="num">2</span>Vistas a Gerea':
        '<span class="num">2</span>Gereako ikuspegiak',
    '<span>Sendero</span><span class="sep">/</span><span>Cascada, aerogeneradores y borda</span>':
        '<span>Bidezidorra</span><span class="sep">/</span><span>Ur-jauzia, aerosorgailuak eta borda</span>',
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
        'alt="Bidezidorra borda abandonatu baten ondoan, teilatu gorriarekin, aerosorgailuak '
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
        'aerosorgailuak lagun ia bide osoan. Ez dago ofizialki seinalizatuta pintura berde eta '
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
        'da, aerosorgailuen ondoan dagoen beste San Kristobal ermitatik bereizteko.',
    'Continuamos a toda velocidad cuesta abajo hasta el barrio de San Jos&eacute;. Cruzamos la '
    'carretera general entre Trabakua y Berriz y subimos por la carretera vieja hacia el '
    'barrio de Zengotita, donde est&aacute; la <b>Ermita de San Juan</b> (km 19,6, 400 m), ya '
    'cerca de cerrar el c&iacute;rculo, antes de bajar de vuelta a Trabakua.':
        'Abiadura betean jarraitzen dugu behera San Jos&eacute; auzoraino. Trabakua eta Berriz '
        'arteko errepide nagusia gurutzatzen dugu eta errepide zaharretik gora egiten dugu '
        'Zengotita auzorantz, non dagoen <b>San Juan ermita</b> (19,6 km, 400 m), zirkulua '
        'ixteko zorian, Trabakura jaitsi aurretik.',
    '<h2>BTT y e-bike</h2>': '<h2>BTT eta e-bike</h2>',
    '22,4 km y +1.029 m de desnivel en un solo circuito, con rampas muy duras nada m&aacute;s '
    'salir hacia Zengotitagane &mdash;casi imposibles de subir con una bici normal en este '
    'sentido. El track de esta ficha se grab&oacute; con e-bike &mdash;una Orbea Rise&mdash; '
    '(1h 32min), as&iacute; que el tiempo no sirve de referencia si vas sin asistencia. Hay '
    'agua cerca de Iturzurigana (km 4,8) y en la zona de Garai, antes de la Ermita de San '
    'Crist&oacute;bal Txiki.':
        '22,4 km eta +1.029 m-ko desnibela zirkuitu bakarrean, malda oso gogorrekin '
        'Zengotitaganerako irteeran bertan &mdash;ia ezinezkoak bizikleta arrunt batekin '
        'igotzeko norabide honetan. Fitxa honetako tracka e-bikearekin grabatu zen &mdash;Orbea '
        'Rise batekin&mdash; (1 ordu 32 min), beraz denbora ez da erreferentzia egokia '
        'laguntzarik gabe bazoaz. Ura badago Iturzuriganatik gertu (4,8 km) eta Garaiko aldean, '
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
        'alt="Oizeko aerosorgailuak gailurreko putzu batean islatuta, antenak atzealdean"',
    'alt="Vistas panor&aacute;micas desde el Oiz, con los aerogeneradores y el sol de frente"':
        'alt="Oizetiko ikuspegi panoramikoak, aerosorgailuekin eta eguzkia aurrez aurre"',
    'alt="V&eacute;rtice geod&eacute;sico en el Oiz de noche, con las luces rojas de los '
    'aerogeneradores al fondo"':
        'alt="Vertize geodesikoa Oizen gauez, aerosorgailuen argi gorriak atzealdean"',
    'alt="Atardecer en el Oiz, con la silueta de los aerogeneradores en la cresta"':
        'alt="Ilunabarra Oizen, aerosorgailuen silueta gailur-gerrikoan"',
    'alt="Un reba&ntilde;o de camino al Oiz de noche, con las luces de un pueblo al fondo"':
        'alt="Artalde bat Oizerako bidean gauez, herri baten argiak atzealdean"',
    'alt="Un aerogenerador del Oiz recortado contra la luna, al anochecer"':
        'alt="Oizeko aerosorgailu bat ilargiaren kontra, ilunabarrean"',
    'alt="Atardecer rojizo desde el Oiz"':
        'alt="Ilunabar gorrixka Oiztik"',
    'Salimos de Trabakua y subimos hasta <b>Zengotitagane</b> (km 2,1, 810 m) &mdash;una '
    'subida muy fuerte, aunque corta, casi recta, que sale arriba entre el segundo y el '
    'tercer aerogenerador. A partir de ah&iacute;, hacia el Oiz, la pendiente se '
    'suaviza mucho y se hace muy llevadero.':
        'Trabakuatik irten eta <b>Zengotitagane</b>raino igotzen gara (2,1 km, 810 m) '
        '&mdash;igoera oso gogorra, laburra izan arren, ia zuzena, bigarren eta hirugarren '
        'aerosorgailuen artean ateratzen dena goian. Handik aurrera, Oizerantz, malda '
        'asko leuntzen da eta oso eramangarria bihurtzen da.',
    'Continuamos por la cresta, con unas vistas preciosas a ambos lados, hasta meternos en '
    'el hayedo que nos lleva a la fuente de Iturzuri; tras cruzarlo, se ve un refugio a un '
    'lado, aunque no pasamos por &eacute;l.':
        'Gailur-bizkarretik jarraitzen dugu, bi aldeetara ikuspegi ederrekin, pagadira sartu '
        'arte, Iturzuriko iturrira eramaten gaituena; hura zeharkatu ondoren, aterpe bat '
        'ikusten da alboan, nahiz eta ez garen bertatik pasatzen.',
    '<b>Axmakur</b> (km 4, 888 m) viene justo despu&eacute;s de la fuente, un repecho de la '
    'cresta conectado con el propio Oiz, con vistas hacia el Duranguesado, Urdaibai y Bilbao.':
        '<b>Axmakur</b> (4 km, 888 m) iturriaren ondoren dator, Oiz bertarekin lotutako '
        'gailur-bizkarreko malda bat, Durangaldera, Urdaibaira eta Bilbora ikuspegiekin.',
    'La cresta cumbrera del <b>Oiz</b> (km 5,69, 1.025 m) est&aacute; ocupada por antenas y '
    'uno de los parques e&oacute;licos m&aacute;s extensos de Bizkaia &mdash;el primero que '
    'se instal&oacute; en el territorio. Desde ah&iacute; hay vistas a la costa '
    'cant&aacute;brica y, en d&iacute;as claros, hasta los Pirineos. Es uno de los montes '
    '&laquo;bocineros&raquo; de Bizkaia, usados antiguamente para convocar reuniones con el '
    'sonido de una bocina que cruzaba los valles.':
        '<b>Oiz</b>eko gailur-gerrikoa antenaz eta Bizkaiko parke eoliko zabalenetako batez '
        'okupatuta dago &mdash;lurraldean instalatutako lehena. Handik kostalde '
        'kantauriarrerako ikuspegiak daude, eta egun argietan Pirinioetaraino ere bai. '
        'Bizkaiko mendi &laquo;bozinari&raquo; bat da, garai batean bilerak deitzeko '
        'erabiltzen zena, haranetan zehar zabaltzen zen bozina baten soinuarekin.',
    'La vuelta es por el mismo camino, de vuelta a Trabakua.':
        'Itzulera bide beretik da, Trabakura bueltan.',
    '<h2>Senderismo</h2>': '<h2>Oinez</h2>',
    '11,1 km y +752 m de desnivel en una ruta de ida y vuelta, con dos altos de camino '
    '(Zengotitagane y Axmakur) antes de coronar el Oiz (1.025 m). El track de esta ficha se '
    'grab&oacute; corriendo (1h 35min), as&iacute; que el tiempo no sirve de referencia si '
    'vas andando.':
        '11,1 km eta +752 m-ko desnibela joan-etorriko ibilbide batean, bidean bi goirekin '
        '(Zengotitagane eta Axmakur) Oiz gailurreratu aurretik (1.025 m). Fitxa honetako '
        'tracka lasterka grabatu zen (1 ordu 35 min), beraz denbora ez da erreferentzia '
        'egokia oinez bazoaz.',
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
    'de camino (Osmagain y Arietzu). El track de esta ficha se grab&oacute; corriendo '
    '(34 min), as&iacute; que el tiempo no sirve de referencia si vas andando.':
        '4,3 km eta +235 m-ko desnibela zirkuitu laburrean, haurrentzat egokia, bidean bi '
        'goirekin (Osmagain eta Arietzu). Fitxa honetako tracka lasterka grabatu zen '
        '(34 min), beraz denbora '
        'ez da erreferentzia egokia oinez bazoaz.',
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
    'Se sale desde el Alto de Trabakua. Los primeros metros bajan &mdash;poco m&aacute;s de '
    'un kil&oacute;metro&mdash; hasta un cruce a la izquierda donde se deja el asfalto '
    'atr&aacute;s y empieza una cuesta que por un momento se pone intensa, pero corta; '
    'una vez arriba vemos las indicaciones para el monte Mendibil, entre otras. Desde '
    'ah&iacute;, todo es pista en solitario, alternando cemento y tramos de piedra. Lo '
    'que viene despu&eacute;s se lleva mejor, y el camino ondula entre subidas y bajadas '
    'suaves, hasta llegar a Asuntza.':
        'Trabakuako mendatetik ateratzen gara. Lehen zatia beherantz doa &mdash;kilometro '
        'bat inguru&mdash; ezkerrerako bidegurutze batera iritsi arte, non asfaltua '
        'uzten den eta aldapa bat hasten den, uneren batean bizi baina laburra; goian, '
        'Mendibil mendirako seinaleak ikusten ditugu, besteak beste. Hortik aurrera, '
        'pista hutsa da, zementu eta harrizko tarteak txandakatuz. Ondorengoa '
        'eramangarriagoa da, eta bidea igoera eta jaitsiera leunen artean uhinka doa, '
        'Asuntzara iritsi arte.',
    'Por el camino coronamos <b>Arandomendi</b> (km 6,4 &middot; 686 m), donde la '
    'pendiente da un respiro durante el siguiente kil&oacute;metro, antes de atacar la '
    'cuesta final hacia la cumbre del Urko.':
        'Bidean <b>Arandomendi</b> gailurra egiten dugu (6,4 km &middot; 686 m), non '
        'maldak arnasa hartzeko tartea ematen duen hurrengo kilometroan zehar, Urkoko '
        'gailurrerako azken aldapari heldu aurretik.',
    'Poco despu&eacute;s llegamos al punto m&aacute;s alto de la ruta, <b>Urko</b> (km 8, '
    '785 m), con su v&eacute;rtice geod&eacute;sico y vistas a las monta&ntilde;as del '
    'entorno. Es el punto m&aacute;s alto de los municipios de Ermua y Eibar, y su cumbre '
    'marca la frontera entre Bizkaia y Gipuzkoa.':
        'Handik gutxira ibilbideko punturik altuenera iristen gara, <b>Urko</b>ra (8 km, '
        '785 m), bere bertize geodesikoarekin eta inguruko mendietarako ikuspegiekin. '
        'Ermua eta Eibar udalerrien punturik altuena da, eta bere gailurrak Bizkaia eta '
        'Gipuzkoaren arteko muga markatzen du.',
    'Bajamos por un bonito tramo de cresta hasta el <b>Collado de Asuntza</b> (km 10,8 '
    '&middot; 490 m), que separa el Urko del monte Mendibil (613 m), y cogemos la misma '
    'pista de la Asuntza, antes de remontar de nuevo hacia Trabakua.':
        'Gailurrerdi eder batetik jaisten gara <b>Asuntzako lepora</b> (10,8 km &middot; '
        '490 m), Urko eta Mendibil mendia (613 m) bereizten dituena, eta Asuntzako pista '
        'bera hartzen dugu, Trabakuarantz berriro igotzen hasi aurretik.',
    '<h2>Senderismo</h2>': '<h2>Oinez</h2>',
    '15,3 km y +873 m de desnivel en un circuito con dos altos de camino (Arandomendi y '
    'el Collado de Asuntza) antes y despu&eacute;s de coronar el Urko (785 m). El track de '
    'esta ficha se grab&oacute; corriendo, una ma&ntilde;ana de noviembre (2h 25min), '
    'as&iacute; que el tiempo no sirve de referencia si vas andando. No hay fuentes en la '
    'ruta, as&iacute; que conviene llevar agua &mdash;hay una en el bar de arriba de '
    'Trabakua, junto a los columpios.':
        '15,3 km eta +873 m-ko desnibela zirkuitu batean, bidean bi goirekin (Arandomendi '
        'eta Asuntzako lepoa) Urko gailurra (785 m) egin aurretik eta ondoren. Fitxa '
        'honetako tracka lasterka grabatu zen, azaroko goiz batean (2h 25min), beraz '
        'denbora ez da erreferentzia egokia oinez bazoaz. Ez dago iturririk ibilbidean, '
        'beraz komeni da ura eramatea &mdash;bat dago Trabakuko goiko tabernan, '
        'kulunkaren ondoan.',
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
        'alt="Pista aerosorgailuen ondoan, lainoak gailurra estaltzen duela"',
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
    'Salimos de Trabakua en direcci&oacute;n Osma por carretera. Algo m&aacute;s de 2 km '
    'despu&eacute;s giramos a la derecha para coger la pista que sube hasta <b>Zengotitagane</b> '
    '(km 3,7, 810 m), entre los aerogeneradores del parque e&oacute;lico. Las rampas son muy '
    'duras, casi imposibles de subir con una bici normal &mdash;aunque en sentido contrario, '
    'con esta subida convertida en bajada, s&iacute; se puede hacer la ruta con una bici '
    'normal.':
        'Trabakuatik irten eta Osma norabidean egiten dugu errepidez. 2 km pasatxo geroago '
        'eskuinera jotzen dugu, <b>Zengotitagane</b>raino (3,7 km, 810 m) igotzen duen pista '
        'hartzeko, parke eolikoaren aerosorgailuen artean. Maldak oso gogorrak dira, ia '
        'ezinezkoak bizikleta arrunt batekin igotzeko &mdash;alderantzizko norabidean, ordea, '
        'igoera hori jaitsiera bihurtuta, bai egin daiteke ibilbidea bizikleta arrunt batekin.',
    'Tras Zengotitagane seguimos por la cresta hasta <b>Iturzurigana</b> (km 4,8, 858 m), con '
    'vistas a los dos lados. Quien quiera coger agua puede desviarse unos metros a la derecha. '
    'Un poco m&aacute;s adelante, tras cruzar en paralelo a los aerogeneradores la parte alta '
    'del Oiz, bajamos a una pista de cemento en busca de la subida a la zona de la cumbre de '
    '<b>Askako</b> (km 5,7, 681 m), que cruzamos por un precioso sendero semioculto bajo la '
    'vegetaci&oacute;n: parte del trazado cl&aacute;sico del AstoTrail, la exigente carrera de '
    'monta&ntilde;a que organiza el municipio de Garai.':
        'Zengotitagane igaro ondoren gailurraren bidetik jarraitzen dugu <b>Iturzurigana</b>'
        'raino (4,8 km, 858 m), bi aldeetara ikuspegiekin. Ura hartu nahi duenak eskuinera '
        'desbideratu ditzake metro batzuk. Handik pixka batera, aerosorgailuen paraleloan '
        'Oizeko goialdea zeharkatu ondoren, zementuzko pista batera jaisten gara, Askako '
        'gailur-eremurako igoeraren bila (5,7 km, 681 m). Handik, landaretzak ia ezkutatzen '
        'duen bidezidor eder batetik gurutzatzen dugu <b>Askako</b>, Garaiko udalak '
        'antolatzen duen AstoTrail lasterketa gogorraren ibilbide klasikoaren zati denetik.',
    'Bajamos entonces hacia Garai por un hayedo precioso, una de las bajadas que m&aacute;s '
    'se disfrutan de toda la ruta. Nada m&aacute;s salir de Garai hay una fuente a mano '
    'izquierda, con agua durante todo el a&ntilde;o.':
        'Orduan Garairantz jaisten gara pagadi eder batetik, ibilbide osoko jaitsiera '
        'gozagarrienetako bat. Garaitik irten bezain laster iturri bat dago ezkerraldean, '
        'urtean zehar beti urarekin.',
    'La subida de Garai hasta la <b>Ermita de San Crist&oacute;bal Txiki</b> (km 20,3, 493 m) '
    'la hacemos por una pista de piedra &mdash;as&iacute; se conoce esta ermita, para '
    'distinguirla de la otra Ermita de San Crist&oacute;bal, la de arriba, junto a los '
    'aerogeneradores.':
        'Garaitik <b>San Kristobal Txiki ermita</b>raino (20,3 km, 493 m) igotzeko harrizko '
        'pista hartzen dugu &mdash;horrela ezagutzen da ermita hau, aerosorgailuen ondoan '
        'dagoen beste San Kristobal ermitatik bereizteko.',
    'Continuamos a toda velocidad cuesta abajo hasta el barrio de San Jos&eacute;. Cruzamos la '
    'carretera general entre Trabakua y Berriz y subimos por la carretera vieja hacia el '
    'barrio de Zengotita, donde est&aacute; la <b>Ermita de San Juan</b> (km 24,5, 404 m), ya '
    'cerca de cerrar el c&iacute;rculo, antes de bajar de vuelta a Trabakua.':
        'Abiadura betean jarraitzen dugu behera San Jos&eacute; auzoraino. Trabakua eta Berriz '
        'arteko errepide nagusia gurutzatzen dugu eta errepide zaharretik gora egiten dugu '
        'Zengotita auzorantz, non dagoen <b>San Juan ermita</b> (24,5 km, 404 m), zirkulua '
        'ixteko zorian, Trabakura jaitsi aurretik.',
    '<h2>BTT y e-bike</h2>': '<h2>BTT eta e-bike</h2>',
    '26,9 km y +1.248 m de desnivel en un solo circuito, con rampas muy duras nada m&aacute;s '
    'salir hacia Zengotitagane &mdash;casi imposibles de subir con una bici normal en este '
    'sentido. El track de esta ficha se grab&oacute; con e-bike &mdash;una Orbea Rise&mdash; '
    '(2h 02min), as&iacute; que el tiempo no sirve de referencia si vas sin asistencia. Hay '
    'agua cerca de Iturzurigana (km 4,8) y en una fuente a la salida de Garai, con agua todo '
    'el a&ntilde;o, antes de la Ermita de San Crist&oacute;bal Txiki.':
        '26,9 km eta +1.248 m-ko desnibela zirkuitu bakarrean, malda oso gogorrekin '
        'Zengotitaganerako irteeran bertan &mdash;ia ezinezkoak bizikleta arrunt batekin '
        'igotzeko norabide honetan. Fitxa honetako tracka e-bikearekin grabatu zen &mdash;Orbea '
        'Rise batekin&mdash; (2 ordu 02 min), beraz denbora ez da erreferentzia egokia '
        'laguntzarik gabe bazoaz. Ura badago Iturzuriganatik gertu (4,8 km) eta Garaiko '
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
        'alt="Bizikleta elektrikoaren eskulekua sasi arteko bidezidor batean, Oizeko aerosorgailuak atzealdean"',
    'alt="Foto ampliada del recorrido de Trabakua, Barinaga y Iturreta"':
        'alt="Trabakua, Barinaga eta Iturretako ibilbidearen argazki handitua"',
    'alt="Vista del valle desde la ruta, con caseríos y bordas entre prados y bosque"':
        'alt="Haranaren ikuspegia ibilbidetik, baserriak eta bordak larre eta basoen artean"',
    'alt="Pista de cemento en la ladera, con los aerogeneradores del Oiz al fondo"':
        'alt="Zementuzko pista hegalean, Oizeko aerosorgailuak atzealdean"',
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

    '<h2>BTT y e-bike</h2>':
        '<h2>BTT eta e-bike</h2>',

    '19,65 km y +975 m de desnivel en un solo circuito, con una rampa corta pero intensa después de Iturreta —difícil de subir con una bici normal en ese tramo. El track de esta ficha se grabó con bicicleta eléctrica (1h 35min), así que el tiempo no sirve de referencia si vas sin asistencia. No hay fuentes de agua en el recorrido: en caso de necesidad, habría que desviarse hasta el pueblo de Barinaga.':
        '19,65 km eta +975 m-ko desnibela zirkuitu bakarrean, Iturreta ondoren malda labur baina bizi batekin —zaila bizikleta arrunt batekin igotzeko tarte horretan. Fitxa honetako tracka bizikleta elektrikoarekin grabatu zen (1h 35min), beraz denbora ez da erreferentzia laguntzarik gabe bazoaz. Ez dago ur-iturririk ibilbidean: beharrezkoa balitz, Barinaga herrira desbideratu beharko litzateke.',

    'Se sale desde el Alto de Trabakua. Los primeros metros bajan hasta un cruce donde se deja el asfalto, y todo pasa a ser pista en solitario. El primer repecho —duro, poco más de 300 m— es el que más se nota. Después hay una bajada algo técnica hasta la zona de <b>Aginaga</b> (km 5).':
        'Ibilbidea Trabakuako mendatean hasten da. Lehen metroek behera egiten dute asfaltoa uzten den bidegurutze batera iritsi arte, eta hortik aurrera dena da pista bakarrik. Lehen malda —gogorra, 300 metrotik gutxixeago— da gehien nabaritzen dena. Ondoren jaitsiera teknikoxka bat dago <b>Aginagako</b> eremuraino (5 km).',

    'En Aginaga se coge la pista de la izquierda, bajando entre caseríos y prados con ganado hasta <b>el río</b> (km 9,2), en el fondo del valle. Ahí se gira a la izquierda y empieza la subida por cemento hacia <b>Iturreta</b> (km 12,5). Una vez arriba, coge otra pista de piedra —varios kilómetros para recuperar piernas— antes de la siguiente subida: corta pero intensa, por pista de tierra, difícil de subir con una bici normal —ahí se le pide a la eléctrica todo lo que da. La subida sigue hasta divisar <b>Mendibil</b> a la izquierda (km 14,5), señal de que se ha llegado a la parte más alta de la ruta.':
        'Aginagan ezkerreko pista hartzen da, baserri eta abere-larreen artean behera eginez <b>ibaira</b> iritsi arte (9,2 km), haranaren hondoan. Han ezkerrera biratzen da eta zementuzko igoera hasten da <b>Iturretarantz</b> (12,5 km). Gainean, beste pista bat hartzen da, harrizkoa —kilometro batzuk hankak berreskuratzeko— hurrengo igoeraren aurretik: laburra baina bizia, lurrezko pistatik, zaila bizikleta arrunt batekin igotzeko —hor eskatzen zaio elektrikoari eman dezakeen guztia. Igoerak jarraitzen du <b>Mendibil</b> ezkerrera ikusi arte (14,5 km), ibilbideko puntu altuenera iritsi garenaren seinale.',

    'Baja entonces una pista de tierra para estirar unos cuantos kilómetros más, seguida de un buen tramo de piedra donde se puede dar bastante tralla. Ya abajo del todo, la última subida vuelve hacia Trabakua, con los aerogeneradores del Oiz y el barrio de Gerea como paisaje de fondo, antes de llegar de vuelta a Trabakua, punto de salida y llegada.':
        'Orduan lurrezko pista batean behera egiten da kilometro batzuk gehiago luzatzeko, eta ondoren harrizko tarte on bat dator, non tralla franko eman daitekeen. Erabat behean, azken igoerak Trabakuarantz egiten du, Oizeko aerosorgailuak eta Gereako auzoa atzealde gisa dituela, Trabakuara itzuli arte, irteera eta helmuga puntura.',
}

EGOARBITZA = {
    '<span>Pista, sendero y cresta</span><span class="sep">/</span><span>Urko, Egoarbitza y Zengotitagane</span>':
        '<span>Pista, bidezidorra eta gailurra</span><span class="sep">/</span><span>Urko, Egoarbitza eta Zengotitagane</span>',

    '<span>Circuito</span></p>':
        '<span>Zirkuitua</span></p>',

    '<h1>Urko, Egoarbitza<br><em>y Zengotitagane</em></h1>':
        '<h1>Urko, Egoarbitza<br><em>eta Zengotitagane</em></h1>',

    'Circuito de trail desde Trabakua por Urko, Egoarbitza y Santama&ntilde;esar hasta Zengotitagane':
        'Zirkuitua trailez Trabakuatik, Urko, Egoarbitza eta Santama&ntilde;esarretik igarota Zengotitaganeraino',

    'download="Urko, Egoarbitza y Zengotitagane.gpx"':
        'download="Urko, Egoarbitza eta Zengotitagane.gpx"',

    '<title>Presa de Aixola &middot; 19,0 km &middot; 312 m</title>':
        '<title>Aixolako presa &middot; 19,0 km &middot; 312 m</title>',
    '<span class="num">4</span>Presa de Aixola</span>':
        '<span class="num">4</span>Aixolako presa</span>',

    '<h2>Trail de monta&ntilde;a</h2>':
        '<h2>Mendiko trail-a</h2>',

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

    'La subida hasta <b>Urko</b> (km 8 &middot; 785 m) es la misma que sube desde Trabakua en la ficha de '
    '<a href="urko.html">Asuntza y Urko</a>: pista de cemento y piedra. Desde la cima empieza la '
    'bajada, coincidiendo con el &uacute;ltimo tramo del acceso que sube desde Ermua: primero sendero, '
    'luego un trozo de carretera y despu&eacute;s un cruce escondido que cuesta encontrar la primera vez, '
    'hasta bajar al barrio de <b>Ama&ntilde;a</b> (km 12 &middot; 171 m), en Eibar.':
        'Trabakuatik <b>Urkorako</b> igoera (8 km &middot; 785 m) <a href="urko.html">Asuntza eta Urko</a> '
        'fitxako berbera da: zementuzko eta harrizko pista. Gailurretik jaitsiera hasten da, '
        'Ermuatik igotzeko sarbidearen azken zatiarekin bat eginez: bidezidorra lehenengo, gero '
        'errepide zati bat eta ondoren aurkitzen zaila den bidegurutze ezkutu bat, <b>Ama&ntilde;a</b> '
        'auzoraino jaitsi arte (12 km &middot; 171 m), Eibarren.',

    'Cruzado Ama&ntilde;a se sube hacia el pol&iacute;gono industrial, y de ah&iacute; arranca el sendero '
    'hasta <b>Egoarbitza</b> (km 16,2 &middot; 722 m): pista al principio, despu&eacute;s media cresta, '
    'empinada y dura, con un tramo final rocoso donde conviene ir con cuidado.':
        'Ama&ntilde;a zeharkatu ondoren, industria-poligonorantz igotzen da, eta handik abiatzen da '
        '<b>Egoarbitzarako</b> bidezidorra (16,2 km &middot; 722 m): hasieran pista, gero gailurraren '
        'erdiko zatia, malda handikoa eta gogorra, amaierako tarte harritsu batekin non kontuz ibili '
        'behar den.',

    'La bajada hacia la <b>presa de Aixola</b> (km 19) es muy buena: primero sendero, despu&eacute;s '
    'pista. Justo al llegar al camino de la presa merece la pena desviarse a la izquierda unos metros '
    'hasta una fuente con agua todo el a&ntilde;o. Se cruza el frente de la presa y se sube '
    'hacia <b>Santama&ntilde;esar</b> (km 22,6 &middot; 663 m), toda por pista, sin ning&uacute;n misterio.':
        '<b>Aixolako presarako</b> jaitsiera (19 km) oso ona da: lehenengo bidezidorra, gero pista. '
        'Presaren bidera iritsi bezain laster, merezi du ezkerrera metro batzuetako desbideratzea urte '
        'osoan urez betetako iturri batera. Presaren aurrealdea zeharkatzen da eta '
        '<b>Santama&ntilde;esarrerantz</b> igotzen da (22,6 km &middot; 663 m), erabat pistan, '
        'inolako misteriorik gabe.',

    'Luego bajamos hacia <b>Santa Marina</b>, donde hay una ermita y se puede volver a abastecer de '
    'agua. En la ermita se coge la GR, que sube poco a poco hacia '
    '<b>Arietxu</b> (km 28,8 &middot; 483 m), el mismo pico de la ruta de <a href="arietzu.html">Osmagain '
    'y Arietzu</a>, pero llegando por el lado contrario.':
        'Gero <b>Santa Marinarantz</b> jaisten gara, non ermita bat dagoen eta berriro ur hornitu '
        'daitekeen. Ermitan GRa hartzen da, pixkanaka '
        '<b>Arietxurantz</b> igotzen duena (28,8 km &middot; 483 m), <a href="arietzu.html">Osmagain eta '
        'Arietzu</a> ibilbideko gailur bera, baina kontrako aldetik iritsita.',

    'Desde Arietxu seguimos por el cresterio hasta m&aacute;s o menos la mitad, y luego bajamos hacia el '
    'barrio de Zengotita, donde hay una fuente con agua '
    'todo el a&ntilde;o. Despu&eacute;s de la fuente empieza la subida hacia <b>Zengotitagane</b> '
    '(km 32,5 &middot; 811 m): todo en pista, subir y subir sin apenas tregua, pero bastante llevadera. '
    'Y de ah&iacute;, casi en vertical hacia Trabakua: la &uacute;ltima bajada tiene buena pendiente, unos 400 m de '
    'desnivel en poco m&aacute;s de 2 km, y se cierra el circuito.':
        'Arietxutik gailurretik jarraitzen dugu erdi bidera gutxi gorabehera, eta gero Zengotita '
        'auzorantz jaisten gara, non urte osoan urez betetako '
        'iturri bat dagoen. Iturriaren ondoren, <b>Zengotitaganerako</b> igoera hasten da (32,5 km '
        '&middot; 811 m): dena pistan, igo eta igo atsedenik gabe, baina nahiko eramangarria. Eta '
        'handik, ia bertikalean Trabakuarantz: azken jaitsierak malda ona du, 2 km baino zertxobait '
        'gehiagotan 400 m-ko desnibela, eta zirkuitua ixten da.',

    '34,1 km y +2.564 m de desnivel en un solo circuito, con cuatro subidas importantes (Urko, '
    'Egoarbitza, Arietxu y Zengotitagane) y tramos de media cresta exigentes. El track de esta ficha se '
    'grab&oacute; corriendo (5h 06min), as&iacute; que el tiempo no sirve de referencia si vas andando. '
    'Hay varios puntos para abastecerse de agua en el recorrido: una fuente todo el a&ntilde;o junto a '
    'la presa de Aixola, otro en Santa Marina, y una fuente todo el a&ntilde;o en el barrio de '
    'Zengotita.':
        '34,1 km eta +2.564 m-ko desnibela zirkuitu bakarrean, lau igoera garrantzitsurekin (Urko, '
        'Egoarbitza, Arietxu eta Zengotitagane) eta gailurreko tarte eskatzaileekin. Fitxa honetako '
        'tracka korrika grabatu zen (5h 06min), beraz denbora ez da erreferentzia oinez bazoaz. Hainbat '
        'puntutan har daiteke ura ibilbidean: urte osoko iturri bat Aixolako presaren ondoan, beste bat '
        'Santa Marinan, eta urte osoko iturri bat Zengotita auzoan.',
}

URREGARAI = {
    '<span>Pista, asfalto y cemento</span><span class="sep">/</span><span>Iturreta, Markina y Urregarai</span>':
        '<span>Pista, asfaltoa eta zementua</span><span class="sep">/</span><span>Iturreta, Markina eta Urregarai</span>',

    '<span>Circuito</span></p>':
        '<span>Zirkuitua</span></p>',

    '<h1>Iturreta, Markina<br><em>y Urregarai</em></h1>':
        '<h1>Iturreta, Markina<br><em>eta Urregarai</em></h1>',

    'Circuito de trail desde Trabakua por Iturreta, Markina y Urregarai hasta Bolibar':
        'Zirkuitua trailez Trabakuatik, Iturreta, Markina eta Urregaraitik igarota Bolibarreraino',

    'download="Iturreta, Markina y Urregarai.gpx"':
        'download="Iturreta, Markina eta Urregarai.gpx"',

    '<h2>Trail de monta&ntilde;a</h2>':
        '<h2>Mendiko trail-a</h2>',

    '<span class="v">Senderismo y bici</span>':
        '<span class="v">Oinez eta bizikleta</span>',

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
    'unos chal&eacute;s y enseguida aparece una cuesta bastante pronunciada, hasta un cruce donde el '
    'camino de frente va para Urko y Asuntza y nosotros cogemos el de la izquierda. Seguimos sin dejar '
    'esa pista hasta un collado con una se&ntilde;al que marca &laquo;Markina&raquo;, con marcas blancas '
    'y amarillas. Ah&iacute; bajamos por un camino de tierra con la pendiente pronunciada, hasta llegar '
    'al camino de piedra que est&aacute; junto a un caser&iacute;o. Junto al caser&iacute;o '
    'giramos a la izquierda hacia la ermita de '
    '<b>Iturreta</b> (km 6 &middot; 361 m); despu&eacute;s est&aacute; la '
    'fuente. Volvemos a subir un peque&ntilde;o tramo para bajar de nuevo hacia Markina, siguiendo las '
    'mismas marcas, con buenas vistas hacia el pueblo y varios caser&iacute;os de Iturreta.':
        'Trabakuatik irten eta, Ermua norabidean 1 km errepidez jaitsi ondoren, errepide hori utzi eta '
        'ezkerrera jotzen dugu: <a href="urko.html">Asuntzarako edo Urkorako</a> igotzen den bide bera '
        'hartzen dugu. Txalet batzuen '
        'ondotik pasatzen gara eta berehala aldapa nahiko pikoa agertzen da, Urko eta Asuntzarako aurrez '
        'aurreko bidea eta guk hartzen dugun ezkerrekoa banatzen diren bidegurutze batera arte. Pista '
        'hori utzi gabe jarraitzen dugu kolada batera arte, non &laquo;Markina&raquo; markatzen duen '
        'seinale bat aurkituko dugun, marka zuri eta horiekin. Han lur-bide batetik jaisten gara malda '
        'pikoarekin, harrizko bidera iritsi arte, baserri baten ondoan dagoena. '
        'Baserriaren ondoan ezkerrera jotzen '
        'dugu <b>Iturretako ermitarantz</b> (6 km '
        '&middot; 361 m); ondoren iturria dago. Berriro tarte labur batean igotzen gara Markinarantz '
        'berriro jaisteko, marka berei jarraituz, herrirako eta Iturretako hainbat baserritarako '
        'ikuspegi onekin.',

    'Ya en <b>Markina</b> (km 12 &middot; 79 m) volvemos a abastecernos de agua, en una fuente grande '
    'junto a la iglesia del Carmen. Cruzamos el pueblo hacia la salida, pasando junto a unas escuelas, '
    'y cogemos de nuevo un camino de barrio que sube sin descanso hacia <b>Urregarai</b> (km 16 '
    '&middot; 573 m), en los alrededores de Santa Eufemia. El &uacute;ltimo repecho es precioso, junto '
    'a un caser&iacute;o-granja con muchos pastos. Arriba est&aacute; el refugio de Urregarai, con una '
    'fuente y una bolera enfrente.':
        '<b>Markinan</b> (12 km &middot; 79 m) berriro ur hornitzen gara, Carmen elizaren ondoko iturri '
        'handi batean. Herria zeharkatzen dugu irteera aldera, eskola batzuen ondotik pasatuz, eta '
        'berriro auzo-bide bat hartzen dugu, atsedenik gabe <b>Urregairantz</b> igotzen duena (16 km '
        '&middot; 573 m), Santa Eufemia inguruan. Azken errepikea ederra da, larre asko dituen '
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
        'Trabakuarantz jaistea besterik ez zaigu geratzen, Gerena auzotik, zirkuitua isteko.',

    '30,5 km y +1.163 m de desnivel en un solo circuito, con dos subidas importantes (Urregarai y '
    'Muniozguren) y tramos de pista, asfalto y cemento empinado. El track de esta ficha se '
    'grab&oacute; corriendo (3h 44min), as&iacute; que el tiempo no sirve de referencia si vas andando. '
    'Hay varios puntos para abastecerse de agua en el recorrido: una fuente en Iturreta, otra junto a '
    'la iglesia del Carmen en Markina, y una tercera en el refugio de Urregarai.':
        '30,5 km eta +1.163 m-ko desnibela zirkuitu bakarrean, bi igoera garrantzitsurekin (Urregarai '
        'eta Muniozguren) eta pista, asfalto eta zementu pikoko tarteekin. Fitxa honetako tracka '
        'korrika grabatu zen (3h 44min), beraz denbora ez da erreferentzia oinez bazoaz. Hainbat '
        'puntutan har daiteke ura ibilbidean: iturri bat Iturretan, beste bat Markinako Carmen '
        'elizaren ondoan, eta hirugarren bat Urregairako aterpean.',
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
    'Bici · Circuito · Pista': 'Bizikleta · Zirkuitua · Pista',
    'Senderismo · Circuito · Sendero': 'Oinez · Zirkuitua · Bidezidorra',
    'Bici · Circuito · Mixta': 'Bizikleta · Zirkuitua · Nahasia',
    'Senderismo · Ida y vuelta · Sendero': 'Oinez · Joan-etorria · Bidezidorra',
    'Senderismo · Circuito · Mixta': 'Oinez · Zirkuitua · Nahasia',
    'Senderismo y bici · Circuito · Mixta': 'Oinez eta bizikleta · Zirkuitua · Nahasia',

    # per-card surface badge (Pista is identical in both languages)
    'Sendero': 'Bidezidorra',
    'Mixta': 'Nahasia',

    # route names
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
    'Circuito de trail desde Trabakua por Urko, Egoarbitza y Santamañesar hasta Zengotitagane.': 'Zirkuitua trailez Trabakuatik, Urko, Egoarbitza eta Santamañesarretik igarota Zengotitaganeraino.',
    'Circuito de trail desde Trabakua por Iturreta, Markina y Urregarai hasta Bolibar.': 'Zirkuitua trailez Trabakuatik, Iturreta, Markina eta Urregaraitik igarota Bolibarreraino.',
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
    'egoarbitza': 'Zirkuitua trailez Trabakuatik, Urko, Egoarbitza eta Santamañesarretik '
        'igarota Zengotitaganeraino',
    'urregarai': 'Zirkuitua trailez Trabakuatik, Iturreta, Markina eta Urregaraitik '
        'igarota Bolibarreraino',
    'historias': 'Mallabiako 13 ibilbideak, banan-banan: track bakoitzaren benetako '
        'forma da bere azala. Irristatu, konparatu eta sartu ibilbide bakoitzaren mapan.',
}

# <title> per page (head files)
TITLES = {
    'mallabia': 'Herriko ibilbideak · Oinez eta bizikletaz Bizkaian',
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
    'egoarbitza': 'Urko, Egoarbitza eta Zengotitagane · Trail ibilbidea — Herriko ibilbideak',
    'urregarai': 'Iturreta, Markina eta Urregarai · Trail ibilbidea — Herriko ibilbideak',
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
    'historias': HISTORIAS,
}
