# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'hdfilme_tv'
SITE_NAME = 'HDfilme.tV'
SITE_ICON = 'hdfilme.png'

URL_MAIN = 'http://hdfilme.tv/'
URL_MOVIES = URL_MAIN + 'movie-movies'
URL_CINEMA_MOVIES = URL_MAIN + 'movie-cinemas'
URL_SHOWS = URL_MAIN + 'movie-series'

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
    oRequest = cRequestHandler(entryUrl)
    oGui.setView('movie')
    sHtmlContent = oRequest.request()
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

    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0]:
        return
    for sUrl, sThumbnail, sName, sDesc in aResult[1]:
        aYear = re.compile("(.*?)\((\d*)\)").findall(sName)
        iYear = 0
        for name, year in aYear:
            sName = name
            iYear = year
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        if iYear:
            logger.info(iYear)
            oGuiElement.setYear(iYear)
        oGuiElement.setMediaType('movie')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(cUtil().unescape(sDesc.decode('utf-8')).encode('utf-8'))
        params.setParam('entryUrl', sUrl)
        oGui.addFolder(oGuiElement, params, bIsFolder = False)
    oGui.setEndOfDirectory()
