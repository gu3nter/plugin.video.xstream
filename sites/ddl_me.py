# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib import logger
from resources.lib.config import cConfig
import json

SITE_IDENTIFIER = 'ddl_me'
SITE_NAME = 'DirectDownLoad'
SITE_ICON = 'ddl.png'
SITE_SETTINGS = '<setting default="de.ddl.me" enable="!eq(-1,false)" id="ddl_me-domain" label="' + SITE_NAME + ' domain" type="labelenum" values="de.ddl.me|en.ddl.me" />'

oConfig = cConfig()
DOMAIN = oConfig.getSetting('ddl_me-domain')

URL_MAIN = 'http://' + DOMAIN
URL_SEARCH = URL_MAIN + '/search_99/?q='
URL_MOVIES = URL_MAIN + '/moviez'
URL_SHOWS = URL_MAIN + '/episodez'
URL_TOP100 = URL_MAIN + '/top100/cover/'

PARMS_GENRE_ALL = "_00"

PARMS_SORT_LAST_UPDATE = "_0"
PARMS_SORT_BLOCKBUSTER = "_1"
PARMS_SORT_IMDB_RATING = "_2"
PARMS_SORT_YEAR = "_3"

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()

    params.setParam('sUrl', URL_MOVIES)
    params.setParam('sTop100Type', 'movies')
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showContentMenu'), params)
    params.setParam('sUrl', URL_SHOWS)
    params.setParam('sTop100Type', 'tv')
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showContentMenu'), params)
    params.setParam('sUrl', URL_TOP100 + 'total/all/')
    oGui.addFolder(cGuiElement('Hall of Fame', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showContentMenu():
    oGui = cGui()
    params = ParameterHandler()
    baseURL = params.getValue('sUrl')

    oGui.addFolder(cGuiElement('Top 100',SITE_IDENTIFIER,'showTop100Menu'), params) 
    params.setParam('sUrl', baseURL + PARMS_GENRE_ALL + PARMS_SORT_LAST_UPDATE)
    oGui.addFolder(cGuiElement('Letztes Update', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + PARMS_GENRE_ALL + PARMS_SORT_BLOCKBUSTER)
    oGui.addFolder(cGuiElement('Blockbuster', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + PARMS_GENRE_ALL + PARMS_SORT_IMDB_RATING)
    oGui.addFolder(cGuiElement('IMDB Rating', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + PARMS_GENRE_ALL + PARMS_SORT_YEAR)
    oGui.addFolder(cGuiElement('Jahr', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + PARMS_GENRE_ALL + PARMS_SORT_LAST_UPDATE)
    oGui.addFolder(cGuiElement('Genre',SITE_IDENTIFIER,'showGenreList'), params)
    oGui.setEndOfDirectory()

def showTop100Menu():
    oGui = cGui()
    params = ParameterHandler()

    params.setParam('sUrl',URL_TOP100 + 'today/' + params.getValue('sTop100Type'))
    oGui.addFolder(cGuiElement('Heute', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl',URL_TOP100 + 'month/' + params.getValue('sTop100Type'))
    oGui.addFolder(cGuiElement('Monat', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()

def showGenreList():
    oGui = cGui()
    params = ParameterHandler()

    sHtmlContent = cRequestHandler(params.getValue('sUrl')).request()
    pattern = '<a[^>]*href="([^"]*)".*?' # url
    pattern += '<i[^>]*class="fa fa-dot-circle-o".*?i>(.*?)</a>.*?' # title
    aResult = cParser().parse(sHtmlContent, pattern)

    if not aResult[0]:
        return

    total = len (aResult[1])
    for sUrl, sTitle in aResult[1]:
        params.setParam('sUrl',URL_MAIN + sUrl)
        oGui.addFolder(cGuiElement(sTitle.strip(), SITE_IDENTIFIER, 'showEntries'), params, iTotal = total)
    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()

    if not sGui: oGui.setView('tvshows' if URL_SHOWS in entryUrl else 'movies')
    if not entryUrl: entryUrl = params.getValue('sUrl')

    sHtmlContent = cRequestHandler(entryUrl).request()
    pattern = "<div[^>]*class='iwrap type_(\d*)'[^>]*>\s*?" # smType
    pattern += "<a[^>]*title='([^']*)'*[^>]*href='([^']*)'*>.*?" # title / url
    pattern += "<img[^>]*src='([^']*)'[^>]*>.*?" # thumbnail
    pattern += "<span[^>]*class='bottomtxt'[^>]*>\s*?<i>(\d*)<span" # year
    aResult = cParser().parse(sHtmlContent, pattern)

    if not aResult[0] or not aResult[1][0]: 
        pattern = "<title>(.*?)[(](\d*)[)].*?" # name
        pattern += "<img[^>]*class='detailCover'[^>]*src='([^']*)'[^>]*>.*?" # thumbnail
        pattern += "var[ ]mtype[ ]=[ ](\d*);" # mediatyp
        aOneResult = cParser().parse(sHtmlContent, pattern)

        if not aOneResult[0] or not aOneResult[1][0]: 
            if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
            return

        for sName, sYear, sThumbnail, smType in aOneResult[1]:
            sName = _stripTitle(sName)
            oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
            if sYear: oGuiElement.setYear(sYear)
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setMediaType('tvshow' if smType == "1" else 'movie')
            params.setParam('entryUrl', entryUrl)
            params.setParam('sName', sName)
            params.setParam('sThumbnail', sThumbnail)
            if smType == "1": # show season-list for tvshows
                oGuiElement.setFunction("showAllSeasons")
                oGui.addFolder(oGuiElement, params)
            else:
                oGui.addFolder(oGuiElement, params, bIsFolder = False)
        if not sGui: oGui.setEndOfDirectory()
        return

    if not aResult[0] or not aResult[1][0]: 
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    for smType, sName, sUrl, sThumbnail,sYear in aResult[1]:
        sName = _stripTitle(sName)
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        if sYear: oGuiElement.setYear(sYear)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setMediaType('tvshow' if smType == "1" else 'movie')
        params.setParam('entryUrl', URL_MAIN + sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        if smType == "1":  # show season-list for tvshows
            oGuiElement.setFunction("showAllSeasons")
            oGui.addFolder(oGuiElement, params)
        else:
            oGui.addFolder(oGuiElement, params, bIsFolder = False)

    pattern = "<div[^>]*class='paging'[^>]*>(.*?)</div>"
    aResult = cParser().parse(sHtmlContent, pattern)
    if aResult[0]:
        aResult = cParser().parse(aResult[1][0], "<a[^>]href='([^']*)'[^>]*>(\d)<[^>]*>")
        if aResult[0]:
            currentPage = int(params.getValue('mediaTypePageId'))
            for sUrl, sPage in aResult[1]:
                page = int(sPage)
                if page <= currentPage: continue
                params.setParam('sUrl', URL_MAIN + sUrl)
                params.setParam('mediaTypePageId', page)
                oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
                break

    if not sGui:
        oGui.setEndOfDirectory()

def showAllSeasons():
    oGui = cGui()
    params = ParameterHandler()

    sUrl = params.getValue('entryUrl')
   
    sHtmlContent = cRequestHandler(sUrl).request()
    aResult = cParser().parse(sHtmlContent, "var[ ]subcats[ ]=[ ](.*?);") #json for hoster

    if not aResult[0] or not aResult[1][0]: 
        oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    data = json.loads(aResult[1][0])
    seasons = []
    for key, value in data.items():
        SeasonsNr = int(value['info']['staffel'])
        if SeasonsNr not in seasons:
            seasons.append(SeasonsNr)

    sThumbnail = params.getValue('sThumbnail')
    sName = params.getValue('sName')

    seasons = sorted(seasons)
    total = len(seasons)
    for iSeason in seasons:
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showAllEpisodes')
        oGuiElement.setTitle("Staffel " + str(iSeason))
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setSeason(iSeason)
        oGuiElement.setMediaType('season')
        oGuiElement.setThumbnail(sThumbnail)
        oOutParms = ParameterHandler()
        oOutParms.setParam('entryUrl', sUrl)
        oOutParms.setParam('sName', sName)
        oOutParms.setParam('sThumbnail', sThumbnail)
        oOutParms.setParam('iSeason', iSeason)
        oOutParms.setParam('sJson', aResult[1][0])
        oGui.addFolder(oGuiElement, oOutParms, iTotal = total)
    oGui.setView('seasons')
    oGui.setEndOfDirectory()

def showAllEpisodes():
    oGui = cGui()

    params = ParameterHandler()
    iSeason = int(params.getValue('iSeason'))
    sThumbnail = params.getValue('sThumbnail')
    sName = params.getValue('sName')
    sJson = params.getValue('sJson')

    episodes = {}
    data = json.loads(sJson)
    for key, value in data.items():
        SeasonsNr = int(value['info']['staffel'])
        if SeasonsNr != iSeason:
            continue
        episodeNr = int(value['info']['nr'])
        if episodeNr not in episodes.keys():
            episodes.update({episodeNr : key})

    for iEpisodesNr, sEpisodesID in episodes.items():
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showHosters')
        epiName = data[sEpisodesID]['info']['name'].encode('utf-8')
        aResult = cParser().parse(epiName, "(.*?)»") # try to get name
        if aResult[0]: 
            epiName = aResult[1][0]
        oGuiElement.setTitle(str(iEpisodesNr) + " - " + epiName)
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setSeason(iSeason)
        oGuiElement.setEpisode(iEpisodesNr)
        oGuiElement.setMediaType('episode')
        oGuiElement.setThumbnail(sThumbnail)
        oOutParms = ParameterHandler()
        oOutParms.setParam('sJson', sJson)
        oOutParms.setParam('sJsonID', sEpisodesID)
        oGui.addFolder(oGuiElement, oOutParms, bIsFolder = False)

    oGui.setView('episodes')
    oGui.setEndOfDirectory()

def showHosters():
    params = ParameterHandler()
    
    sJson = params.getValue('sJson')
    if not sJson:
        sHtmlContent = cRequestHandler(params.getValue('entryUrl')).request()
        aResult = cParser().parse(sHtmlContent, "var[ ]subcats[ ]=[ ](.*?);")
        if aResult[0]: 
            sJson = aResult[1][0]

    hosters = []
    if sJson:
        data = json.loads(sJson)
        sJsonID = params.getValue('sJsonID')
        if not sJsonID:
            sJsonID = data.keys()[0]
        partCount = 1 # fallback for series (because they get no MultiParts)
        if '1' in data[sJsonID]:
            partCount = int(data[sJsonID]['1'])
        for jHoster in data[sJsonID]['links']:
            for jHosterEntry in data[sJsonID]['links'][jHoster]:
                if jHosterEntry[5] == 'stream':
                    hoster = {}
                    if partCount > 1:
                        hoster['displayedName'] = jHoster + ' - Part ' + jHosterEntry[0]
                    hoster['link'] = jHosterEntry[3]
                    hoster['name'] = jHoster
                    hosters.append(hoster)

    if len(hosters) > 0:
        hosters.append('getHosterUrl')
    return hosters
  
def getHosterUrl(sUrl = False):
    if not sUrl: sUrl = ParameterHandler().getValue('url')
    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = False
    results.append(result)
    return results

def _stripTitle(sName):
    sName = sName.replace("- Serie","")
    sName = sName.replace("(English)","")
    sName = sName.replace("(Serie)","")
    return sName.strip()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()

def _search(oGui, sSearchText):
    if not sSearchText: return
    showEntries(URL_SEARCH + sSearchText.strip(), oGui)
