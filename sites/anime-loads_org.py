# -*- coding: utf-8 -*-
import json
import time
from resources.lib import logger
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

# Basis-Einträge für xStream
SITE_IDENTIFIER = 'anime-loads_org'
SITE_NAME = 'Anime-Loads'
SITE_ICON = 'anime-loads.png'

# Links definieren
URL_MAIN = 'http://www.anime-loads.org/'
URL_SEARCH_ANIME = URL_MAIN + 'search?q=%s&type=anime'
URL_MOVIES = URL_MAIN + 'anime-movies/'
URL_MOVIES_ASC = URL_MOVIES + '?sort=title&order=asc'
URL_SERIES = URL_MAIN + 'anime-series/'
URL_SERIES_ASC = URL_SERIES + '?sort=title&order=asc'

SITE_KEY = '6LdSHggTAAAAAEdkVArXG7E27hyEc2Ij-UxpPveG'

def load():
    # Logger-Eintrag
    logger.info("Load %s" % SITE_NAME)

    # Gui-Elemet erzeugen
    oGui = cGui()

    # Menü erzeugen
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMovieMenu'))
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showSeriesMenu'))
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))

    # Debug (zum prüfen des Capatcha)
    #oParams = ParameterHandler()
    #oParams.addParams({'sUrl':  URL_SEARCH_ANIME % 'silver spoon 2'})
    #oGui.addFolder(cGuiElement('***Capatcha-Test***', SITE_IDENTIFIER, 'showEntries'), oParams)

    # Debug (zum testen von mehreren Releases)
    #oParams = ParameterHandler()
    #oParams.addParams({'sUrl': URL_SEARCH_ANIME % 'garden of words'})
    #oGui.addFolder(cGuiElement('***Mutli-Release-Test***', SITE_IDENTIFIER, 'showEntries'), oParams)

    # Liste abschließen
    oGui.setEndOfDirectory()

def showMovieMenu():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # Parameter setzen
    params = ParameterHandler()

    # Menü erzeugen
    params.setParam('sUrl', URL_MOVIES)
    oGui.addFolder(cGuiElement('Neuste Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MOVIES_ASC)
    oGui.addFolder(cGuiElement('Alle Filme', SITE_IDENTIFIER, 'showEntries'), params)

    # Liste abschließen
    oGui.setEndOfDirectory()

def showSeriesMenu():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # Parameter setzen
    params = ParameterHandler()

    # Menü erzeugen
    params.setParam('sUrl', URL_SERIES)
    oGui.addFolder(cGuiElement('Neuste Serien', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_SERIES_ASC)
    oGui.addFolder(cGuiElement('Alle Serien', SITE_IDENTIFIER, 'showEntries'), params)

    # Liste abschließen
    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    # GUI-Element erzeugen wenn nötig
    oGui = sGui if sGui else cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # URL ermitteln falls nicht übergeben
    if not entryUrl: entryUrl = params.getValue('sUrl')

    # HTML-Laden
    sHtmlContent = cRequestHandler(entryUrl).request()

    # Thumbnail ermitteln
    pattern = '<img[^>]*src="([^"]*)"[^>]*class="img-responsive[ ]img-rounded"[^>]*>.*?'

    # Links und Title ermitteln
    pattern += '<a[^>]*href="([^"]*)"[^>]*>(.*?)</a[>].*?'

    # Typ, Jahr und Anzahl der Episoden ermitteln
    pattern += '<a[^>]*><i[^>]*></i>(.*?)</a[>].*?'
    pattern += '<a[^>]*><i[^>]*></i>(.*?)</a[>].*?'
    pattern += '<span[^>]*><i[^>]*></i>(.*?)</span[>].*?'

    # Beschreibung ermitteln
    pattern += '<div[^>]*class="mt10"[^>]*>([^<>]*)</div>.*?'

    # Genre (wird aktuell nicht weiter benutzt)
    pattern += '<a[^>]*class="label[ ]label-info"[^>]*>([^<>]*)</a>'

    # Regex parsen
    aResult = cParser().parse(sHtmlContent, pattern)

    # Nichts gefunden? => raus hier
    if not aResult[0]: 
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    # Prüfen ob es sich um einen Film oder um eine Serie handelt
    isTvshow = True if URL_SERIES in entryUrl else False

    # Listengröße ermitteln
    total = len (aResult[1])

    # Ergebnisse durchlaufen
    for sThumbnail, sUrl, sName, sTyp, sYear, sEpisodes, sDesc, sGenre in aResult[1]:
        # Prüfen ob es sich um einen Film oder um eine Serie handelt
        isMovie = True if sTyp.strip() == 'Anime Film' else False

        # Decoding für die Beschreibung um Anzeifehler zu vermeiden
        sDesc = cUtil().unescape(sDesc.decode('utf-8')).encode('utf-8').strip()

        # Eintrag erzeugen
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showReleases')
        oGuiElement.setMediaType('movie' if isMovie else 'tvshow')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc.strip())
        oGuiElement.setYear(sYear)
        params.setParam('entryUrl', sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        oGui.addFolder(oGuiElement, params, True, total)

    # Seiten-Navigation
    pattern = '<li><a[^>]*href="([^"]*)"[^>]*>(\d+)</a[>]</li>.*?'
    aResult = cParser().parse(sHtmlContent, pattern)

    # Wurde eine Navigation gefunden? => "Next-Page -->" einbauen
    if aResult[0]:
        # Aktuelle Seite ermitteln
        currentPage = int(params.getValue('mediaTypePageId'))

        # alle Ergebnisse durchlaufen
        for sUrl, sPage in aResult[1]:
            # Seite vom Ergebniss ermitteln
            page = int(sPage)

            # Falls die Seite kleiner ist => Weiter machen bis das nicht der Fall ist
            if page <= currentPage: continue

            # Eintrag erzeugen und Schleife verlassen
            params.setParam('sUrl', URL_MAIN + sUrl)
            params.setParam('mediaTypePageId', page)
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
            break

    # List abschließen
    if not sGui:
        oGui.setView('tvshows' if isTvshow else 'movies')
        oGui.setEndOfDirectory()

def showReleases():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Variable für Ansicht vorbereiten
    sThumbnail = params.getValue('sThumbnail')
    sName = params.getValue('sName')

    # Seite laden
    sHtmlContent = cRequestHandler(params.getValue('entryUrl')).request()

    # ReleaseId und Name ermitteln
    pattern = "<a[^>]*href=['\"]#stream_(\d+)['\"][^>]*>.*?</i>(.*?)"

    # Sprache ermitteln (Optional)
    pattern += "(?:<i[^>]*class=['\"].*?flag-(\w+)['\"][^>]*>.*?)?"
    
    # Untertiel ermitteln (Optional) und Pattern schließn
    pattern += "(?:[|]\s<i[^>]*class=['\"].*?flag-(\w+)['\"][^>]*>.*?)?</li>"

    # HTML parsen
    aResult = cParser().parse(sHtmlContent, pattern)

    # Funktion verlassen falls keine Daten ermittelt werden konnten
    if not aResult[0] or not aResult[1][0]: 
        oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    # Listengröße ermitteln
    total = len(aResult[1])

    # alle Ergebnisse durchlaufen
    for sReleaseId, sReleaseName, sLang, sSubLang in aResult[1]:
        # Alle Streams des jeweiligen Releases ermitteln
        aStreams = cParser().parse(sHtmlContent, "id=['\"]streams_episodes_%s_\d['\"]" % sReleaseId)

        # Kein Episoden verfügbar? => weiter machen
        if not aResult[0] or not aResult[1][0]: 
            continue

        # unnötige Leerzeichen entfernen (falls vorhanden)
        sReleaseName = sReleaseName.strip()

        # Sprache ergänzen wenn möglich
        if sLang and sSubLang:
            sReleaseName += " (%s | %s)" % (sLang.upper(),sSubLang.upper())
        elif sLang:
            sReleaseName += " (%s)" % (sLang.upper())

        # Eintrag erzeugen
        oGuiElement = cGuiElement(sReleaseName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setThumbnail(sThumbnail)
        params.setParam('iReleaseId', int(sReleaseId))

        # Episoden Streams verfügbar? => Liste anzeigen 
        if len(aStreams[1]) > 1:
            oGuiElement.setFunction("showEpisodes")
            oGui.addFolder(oGuiElement, params, True, total)
        else:
            params.setParam('iEpisodeId', 0)
            oGui.addFolder(oGuiElement, params, False, total)

    #Liste abschließen
    oGui.setEndOfDirectory()

def showEpisodes():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Seite laden (ungecached)
    sHtmlContent = _getRequestHandlerForCapacha(params.getValue('entryUrl')).request()

    # Pattern zum ermitteln der EpisodeId
    pattern = "<a[^>]*href=['\"]#streams_episodes_%d_(\d+)['\"][^>]*>.*?" % int(params.getValue('iReleaseId'))

    # Seriennummer und Name ermitteln
    pattern += "<strong>(\d+)</strong>(.*?)</span>"

    # HTML parsen
    aResult = cParser().parse(sHtmlContent, pattern)

    # Kein Episoden verfügbar? => weiter machen
    if not aResult[0] or not aResult[1][0]: 
        oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    # Variable für Ansicht vorbereiten
    sThumbnail = params.getValue('sThumbnail')
    sName = params.getValue('sName')

    # Listengröße ermitteln
    total = len(aResult[1])

    # alle Ergebnisse durchlaufen
    for sEpisodeId, sNumber, sEpisodName in aResult[1]:
        oGuiElement = cGuiElement(str(int(sNumber)) + " - " + sEpisodName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setMediaType('episode')
        oGuiElement.setEpisode(int(sNumber))
        oGuiElement.setThumbnail(sThumbnail)
        params.setParam('iEpisodeId', int(sEpisodeId))
        oGui.addFolder(oGuiElement, params, False, total)

    # Ansicht auf "Episoden" setze
    oGui.setView('episodes')

    #Liste abschließen
    oGui.setEndOfDirectory()

# Hoster-Dialog anzeigen
def showHosters():
    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Seite laden (ungecached)
    sHtmlContent = _getRequestHandlerForCapacha(params.getValue('entryUrl')).request()

    # UserID ermitteln
    pattern = "'&ud=(.*?)\">"
    aUdResult = cParser().parse(sHtmlContent, pattern)

    # data-enc für den jeweiligen Eintrag ermitteln
    pattern = 'id="streams_episodes_%d_%d"\sdata-enc="(.+?)"' % (int(params.getValue('iReleaseId')),int(params.getValue('iEpisodeId')))
    aResult = cParser().parse(sHtmlContent, pattern)

    # Hosterliste initalisieren
    hosters = []

    # Liegen beide Einträge vor => Link ermitteln
    if aUdResult[0] and aResult[0]:
        hosters = _decryptLink(aResult[1][0], aUdResult[1][0])

    # Hoster Liste zurückgeben
    return hosters

def getHosterUrl(sUrl = False):
    #ParameterHandler erzeugen
    oParams = ParameterHandler()

    # URL ermitteln falls nicht übergeben
    if not sUrl: sUrl = oParams.getValue('url')

    # Array mit einem Eintrag für Hosterliste erzeugen (sprich direkt abspielen)
    results = []
    result = {}
    result['streamUrl'] = _resolveLeaveLink(sUrl)
    result['resolved'] = False

    # Konnte die URL ermittelt werden? => Zur List hinzufügen
    if result['streamUrl']:
        results.append(result)

    # Ergebniss zurückliefern
    return results

# Sucher über UI
def showSearch():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # Tastatur anzeigen und Eingabe ermitteln
    sSearchText = oGui.showKeyBoard()

    # Keine Eingabe? => raus hier
    if not sSearchText: return

    # Suche durchführen
    _search(False, sSearchText)

    #Liste abschließen
    oGui.setEndOfDirectory()

# Such-Funktion (z.b auch für Globale-Suche)
def _search(oGui, sSearchText):
    # Keine Eingabe? => raus hier
    if not sSearchText: return

    # URL-Übergeben und Ergebniss anzeigen
    showEntries(URL_SEARCH_ANIME % sSearchText.strip(), oGui)

'''
Capatcha und Leaver verarbeitung
'''

def _decryptLink(enc, ud):
    # Versuchen JSon direkt zu bekommen
    response = _sendEnc(enc, ud)

    # Kein Folge? => Capatcha lösen lassen
    if 'code' in response and response['code'] == 'error':
        token = _uncaptcha()
        if token:
            response = _sendEnc(enc, ud, token)

    # Hosterliste initialisieren
    hosters = []

    # Alle Hoster und die jeweiligen Links durchlaufen
    for entry in response['content']:
        for item in entry['links']:
            hoster ={}
            hoster['link'] = item['link']
            hoster['name'] = entry['hoster_name']
            hosters.append(hoster)

    # Sind Hoster vorhanden? => Nachfolgefunktion ergänzen
    if len(hosters) > 0:
        hosters.append('getHosterUrl')

    # Rückgabe
    return hosters

def _resolveLeaveLink(link):
    # Leave-Link aufrufen
    sHtmlContent = _getRequestHandlerForCapacha(URL_MAIN + 'leave/' + link).request()

    # Entgültigen-Link ermitteln
    sPattern = "link\s+=\s'(.*?)',"
    aResult = cParser().parse(sHtmlContent, sPattern)

    # Link gefunden? => Link verfolgen und Redirect ermitteln
    if aResult[0]:
        # Fuck this... Sonnst gehts nicht -.-
        time.sleep(15)

        # Link verfolgen und Redirect zurückgeben
        oRequestHandler = _getRequestHandlerForCapacha(aResult[1][0])
        oRequestHandler.request()
        return oRequestHandler.getRealUrl()

def _sendEnc(enc, ud, response = None):
    # Cookies ermitteln
    _getRequestHandlerForCapacha('%sassets/pub/js/userdata?ud=%s' % (URL_MAIN, ud)).request()

    # Cookie anpassen und captcha AJax zum jeweiligen Link ausführen
    oRequestHandler = _getRequestHandlerForCapacha(URL_MAIN + 'ajax/captcha')
    oRequestHandler.addParameters('enc', enc)
    oRequestHandler.addParameters('response', (response if response else 'nocaptcha'))

    # Rückgabe-JSon lesen
    return json.loads(oRequestHandler.request())

def _uncaptcha():
    try:
        # Capatcha vom URLResolver verarbeiten lassen
        from urlresolver.plugins.lib import recaptcha_v2
        token = recaptcha_v2.UnCaptchaReCaptcha().processCaptcha(SITE_KEY, lang='de')
        return token
    except ImportError:
        pass

def _getRequestHandlerForCapacha(sUrl):
    # RequestHandler ohne Caching und mit User-Agent vom Firefox
    oRequest = cRequestHandler(sUrl, caching = False)
    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0')
    return oRequest
