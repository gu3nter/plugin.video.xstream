# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.util import cUtil
import re, json

SITE_IDENTIFIER = 'hdfilme_tv'
SITE_NAME = 'HDfilme.tV'
SITE_ICON = 'hdfilme.png'

URL_MAIN = 'http://hdfilme.tv/'
URL_MOVIES = URL_MAIN + 'movie-movies'
URL_CINEMA_MOVIES = URL_MAIN + 'movie-cinemas'
URL_SHOWS = URL_MAIN + 'movie-series'
URL_SEARCH = URL_MAIN + 'movie/search?key='

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('sUrl', URL_MOVIES)
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_CINEMA_MOVIES)
    oGui.addFolder(cGuiElement('Kinofilme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_SHOWS)
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    iPage = int(params.getValue('page'))
    logger.info(iPage)
    if iPage > 0:
        oRequest = cRequestHandler(entryUrl + '?per_page=' + str(iPage * 50))
    else:
        oRequest = cRequestHandler(entryUrl)

    sHtmlContent = oRequest.request()
    oGui.setView('movie')

    # Filter out the main section
    pattern = '<ul class="products row">(.*?)</ul>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0] or not aResult[1][0]: return
    sMainContent = aResult[1][0]

    # Grab the link
    pattern = '<div[^>]*class="box-product clearfix"[^>]*>\s*'
    pattern += '<a[^>]*href="([^"]*)"[^>]*>.*?'
    # Grab the thumbnail
    pattern += '<img[^>]*src="([^"]*)"[^>]*>.*?'
    # Grab the name
    pattern += '<div[^>]*class="popover-title"[^>]*>.*?'
    pattern += '<span[^>]*class="name"[^>]*>([^<>]*)</span>.*?'
    # Grab the description
    pattern += '<div[^>]*class="popover-content"[^>]*>\s*<p[^>]*>([^<>]*)</p>'

    aResult = cParser().parse(sMainContent, pattern)
    if not aResult[0]:
        return
    for sUrl, sThumbnail, sName, sDesc in aResult[1]:
        # Grab the year (for movies)
        aYear = re.compile("(.*?)\((\d*)\)").findall(sName)
        iYear = False
        for name, year in aYear:
            sName = name
            iYear = year
            break;
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        if iYear:
            oGuiElement.setYear(iYear)
        oGuiElement.setMediaType('movie')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(cUtil().unescape(sDesc.decode('utf-8')).encode('utf-8'))
        params.setParam('entryUrl', sUrl)
        oGui.addFolder(oGuiElement, params)

    pattern = '<ul[^>]*class="pagination[^>]*>.*?'
    pattern += '<li[^>]*class="active"[^>]*><a>(\d*)</a>.*?</ul>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if aResult[0] and aResult[1][0]:
        params.setParam('page', int(aResult[1][0]))
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    params = ParameterHandler()
    oRequest = cRequestHandler(params.getValue('entryUrl').replace("-info","-stream"))
    sHtmlContent = oRequest.request()
    pattern = 'var newlink = (.*?);'
    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0] or not aResult[1][0]: return

    hosters = []
    for aEntry in json.loads(aResult[1][0]):
        if 'file' not in aEntry or 'label' not in aEntry: continue
        oGuiElement = cGuiElement(aEntry['label'], SITE_IDENTIFIER, 'play')
        params.setParam('url', aEntry['file'])
        oGui.addFolder(oGuiElement, params, False)
    oGui.setEndOfDirectory()

def play(sUrl = False):
    oParams = ParameterHandler()
    if not sUrl: sUrl = oParams.getValue('url')
    results = []
    result = {}
    logger.info(sUrl)
    result['streamUrl'] = sUrl
    result['resolved'] = True
    results.append(result)
    return results

# Show the search dialog, return/abort on empty input
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(oGui, sSearchText)

# Search using the requested string sSearchText
def _search(oGui, sSearchText):
    if not sSearchText: return
    showEntries(URL_SEARCH + sSearchText, oGui)
    oGui.setEndOfDirectory()
