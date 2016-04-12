# xStream für Kodi - README & FAQ

![xStream logo](https://github.com/StoneOffStones/plugin.video.xstream/blob/wiki/graphics/website/logo/logo_512.png?raw=true)


- [1. Allgemeines zum Addon](#1-allgemeines-zum-addon)
    - [1.1 Verfügbare Webseiten](#11-verfügbare-webseiten)
    - [1.2 Rechtliche Konsequenzen bei Nutzung](#12-rechtliche-konsequenzen-bei-nutzung)
   
   
- [2. Installation und Konfiguration](#2-installation-und-konfiguration)
    - [2.1 Bezugsquellen zur Installation](#21-bezugsquellen-zur-installation)
    - [2.2 Allgemeine Einstellungen](#22-allgemeine-einstellungen)
    - [2.3 Webseiten Aktivieren und Deaktivieren](#23-webseiten-aktivieren-und-deaktivieren)
    - [2.4 Manuelle und automatische Hosterwahl](#24-manuelle-und-automatische-hosterwahl)
 
 
- [3. Bekannte Probleme](#3-bekannte-probleme)
    - [3.1 Fehler bei der Installation](#31-fehler-bei-der-installation)
    - [3.2 Fehler bei Verwendung der Globalen Suche](#32-fehler-bei-verwendung-der-globalen-suche)
    - [3.3 Fehler bei Verwendung einzelner Webseiten](#33-fehler-bei-verwendung-einzelner-webseiten)
    - [3.4 Fehler bei Verwendung einiger Hoster](#34-fehler-bei-verwendung-einiger-hoster)
    - [3.5 Fehlermeldungen im Betrieb](#35-fehlermeldungen-im-betrieb)
  
- [4. Fehlerbericht über Log-Datei](#4-fehlerbericht-über-log-datei)
    - [4.1 Allgemeines zur Log-Datei](#41-allgemeines-zur-log-datei)
    - [4.2 Speicherort der Log Datei](#42-speicherort-der-log-datei)
    - [4.3 Erstellen und Hochladen der Log-Datei](#43-erstellen-und-hochladen-der-log-datei)

    
- [5. Phyton Dateien](#5-phyton-dateien)
    - [5.1 Allgemeines zur .py-Datei](#51-allgemeines-zur-py-datei)
    - [5.2 Bearbeiten einer .py-Datei](#52-bearbeiten-einer-py-datei)
    - [5.3 Speicherort der einzelnen Webseiten](#53-speicherort-der-einzelnen-webseiten)



## 1. Allgemeines zum Addon

xStream ist ein Video Addon für die Media-Center-Software Kodi. Mit xStream ist es möglich über eine simple Benutzeroberfläche mehrere Streaming-Seiten zu benutzen, mit denen man Filme und Serien anschauen kann.


### 1.1 Verfügbare Webseiten

| Name           | Domain            | Verfügbarkeit          | Stand      |
|:-------------- |:----------------- | :--------------------- | :--------- |
| AnimeLoads     | anime-loads.org   | funktioniert           | 09.04.2016 |
| BurningSeries  | bs.to             | funktioniert           | 09.04.2016 |
| DirectDownLoad | ddl.me            | funktioniert           | 09.04.2016 |
| FilmPalast     | filmpalast.to     | funktioniert           | 09.04.2016 |
| Gute Filme     | gute-filme.to     | funktioniert           | 09.04.2016 |
| HDfilme        | hdfilme.tv        | funktioniert           | 09.04.2016 |
| KinoLeak       | kinoleak.tv       | funktioniert teilweise | 09.04.2016 |
| KinoX          | kinox.to          | funktioniert           | 09.04.2016 |
| KinoKiste      | kkiste.to         | funktioniert teilweise | 09.04.2016 |
| Movie4k        | movie4k.to        | funktioniert           | 09.04.2016 |
| MoviesEver     | moviesever.com    | funktioniert teilweise | 09.04.2016 |
| SeriesEver     | seriesever.net    | funktioniert           | 09.04.2016 |
| SzeneStreams   | szene-streams.com | funktioniert           | 09.04.2016 |


Empfehlungen und Vorschläge für neue Seiten können über das [Forum](http://xstream-addon.square7.ch) unter dem Bereich [Wünsche und Anregungen](http://xstream-addon.square7.ch/forumdisplay.php?fid=9) angefragt bzw. eingestellt werden. Die Intergration der eingereichten Seiten ist nicht selbsverständlich und folgt daraufhin nicht automatisch. Sowohl das Potenzial der vorgeschlagenen Seite als auch der erforderliche Mehrwert wird geprüft und entscheidet über die Entwicklung eines neuen Site-Plugins.
Grundsätzlich ist jedoch zu erwähnen, dass stätig an der weiterentwicklung von xStream und deren Site-Plugins gearbeitet wird.


### 1.2 Rechtliche Konsequenzen bei Nutzung

Nein, das Addon ermöglicht nur die Nutzung der Streaming-Seiten. Das bloße Streamen hat in Deutschland (momentan) keine rechtlichen Konsequenzen. Die meisten Streaming-Seiten speichern keine Zugriffsdaten. Hier ist ein Video von Rechtsanwalt Christian Solmecke, der über das Thema rechtlich aufklärt:

[![Nutzerfragen: Legalität von Streaming, Arbeitszeiten und Bild.de | Rechtsanwalt Christian Solmecke](http://img.youtube.com/vi/cDmvhJrLkmM/0.jpg)](http://www.youtube.com/watch?v=cDmvhJrLkmM)



## 2. Installation und Konfiguration


### 2.1 Bezugsquellen zur Installation

Das Plugin kann direkt herunterladen werden (wobei die Update-Funktionalität nicht gegeben ist), oder über die xStream Repository installiert werden (empfohlen). Diese ist momentan hier verfügbar:

- [Master-Branch bei GitHub](https://github.com/Lynx187/xStreamRepo/archive/master.zip)

Alternativer Download der Repository:

- [xStream Repository](https://superrepo.org/kodi/addon/repository.xstream/)

Zusätzlich kann man auch die neuste Version von xStream benutzen, indem man die Nightly bzw. Beta Version herunterlädt.

- [Beta-Branch bei GitHub](https://github.com/StoneOffStones/plugin.video.xstream/tree/beta)
- [Nightly-Branch bei GitHub](https://github.com/StoneOffStones/plugin.video.xstream/tree/nightly)

Um die aktuelle Beta von Version 2.1.16 zu installieren, ist es _vorher_ notwendig das Script für Kodi namens Cryptopy zu installieren:

- [Crypropy Script](https://www.github.com/StoneOffStones/script.modul.cryptopy/archive/xstream.zip)

**ACHTUNG!** *Die Beta und Nightly Versionen gelten als Experimentell und werden nicht offiziell unterstützt.*


### 2.2 Allgemeine Einstellungen

Am besten die bevorzugte Sprache auf Deutsch, wenn denn so gewünscht. Sonst am besten alles so wie es ist, die Views leer lassen, sowie die Downloads.

Wenn gesehene Filme auf einmal weg sind, liegt das an den Einstellungen im Seitenmenü. Hier die Markierung „gesehene Filme“ deaktivieren!


### 2.3 Webseiten Aktivieren und Deaktivieren

In den Einstellungen, unter dem Menüpunkt *Site-Plugins*, besteht die Möglichkeit bestimmte Seiten an bzw. auszuschalten. Dies kann von Nutzen sein, wenn kein Interesse an bestimmten Medien besteht. Diese werden dann auch nicht in der globalen Suche angezeigt.


### 2.4 Manuelle und automatische Hosterwahl

Wenn man nicht fitt im Bereich der Hosterauswahl ist, verwendet die Automatische Hosterwahl, in dieser werden auch nicht funktionierende Hoster rausgefiltert. Wenn nicht, dann ist die Hosterwahl auch nicht schwer, sondern sehr übersichtlich. Es ist ähnlich wie bei den Seiten Movie4K und Kinox.



## 3. Bekannte Probleme


### 3.1 Fehler bei der Installation

Fehler können verschiedene Ursachen haben. Bei Hilfe bitte immer folgendes bekannt geben:
Log, Kodi Version, Betriebssystem, xStream Version, genaue Fehlerbeschreibung!
Wird die aktuelle 2.1.16 Beta installiert, ist es vorher notwendig das script.modul Cryptopy  zu installieren:

- https://www.github.com/StoneOffStones/script.modul.cryptopy/archive/xstream.zip

Bitte, schauen, ob der Fehler in einem früheren Post schon beantwortet wurde!
Es kann auch eine fehlerhafte Datei vorliegen, oder die .zip ist falsch aufbereitet.


### 3.2 Fehler bei Verwendung der Globalen Suche

Falls bei der Globalen Suche eine Fehlermeldung bekommen, dass eine Seite nicht erreichbar war bzw. die Suche durch eine Meldung unterbrochen wurde, liegt dies meist an der Seite. Meistens sind die Seiten in diesem Moment nicht erreichbar, dagegen können wir auch nichts tun. Einfach abwarten!
Es kann auch vorkommen, dass bei der Globalen Suche keine Treffer angezeigt werden, dann bitte in der gewünschten Seite die Suche nutzen (manchmal stören die Seiten, die Globale Suche)

*Bei den Seiten Kinox.to und Movie4K.to haben sie in den Einstellungen die Chance die Domain in z.B. Kinox.tv oder .se zu verwenden. Nutzen sie diese Alternativen, die Seiten zu erreichen!*


### 3.3 Fehler bei Verwendung einzelner Webseiten

Das kann verschiedene Ursachen haben. Meistens liegt es jedoch an der eigentlichen Webseite.
Denn wenn dort auch nur eine Kleinigkeit geändert wird, kann es schon sein, dass  das Site-Plugin nicht mehr geht.
Die Entwickler wissen es meist und arbeiten an einer Lösung. Bitte Sachlich bleiben und nicht jammern!
Die Seite im Browser aufrufen und auf Funktion überprüfen.
Im Anschluss das Problem schildern.


### 3.4 Fehler bei Verwendung einiger Hoster

Sollte dies der Fall sein, bitte den aktuellen URL Resolver installieren:

- https://offshoregit.com/tvaresolvers/tva-common-repository/raw/master/zips/script.module.urlresolver/

Bitte den gewünschten Film auf der Homepage auf Funktion kontrollieren.


### 3.5 Fehlermeldungen im Betrieb

- **ImportError:** Bad magic number in bs_finalizer.pyo

	- Status: Problem behoben (Master)

	- Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=505)

- **TypeError:** string indices must be integers

	- Status: Problem behoben (Master)

	- Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=608)

- **AttributeError:** "...Resolver" object has no attribute "priority"

	- Status: Problem behoben (Master)

	- Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=604)

- **KeyError:**'TVShowTitle'

	- Status: Problem behoben (Master)

- **Movie4k funktioniert nicht**

	- Status: Problem behoben (Beta)

	- Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=610)

- **Metahandler funktioniert nicht**

	- Status: Problem bekannt, ist in Arbeit

Angaben in (...) = Aktueller "Ort"

- Master  =>  Ist im aktuellen Master Branch, fix kommt in der nächsten Version

- Beta    =>  Ist im Beta Branch  [(siehe: xStream Beta/Nightly)](http://xstream-addon.square7.ch/showthread.php?tid=584)
- Nightly =>  Ist im Nightly Branch [(siehe: xStream Beta/Nightly)](http://xstream-addon.square7.ch/showthread.php?tid=584)

- **Beim Starten von Xstream kommt folgende Fehlermeldung**

	- "IOError: [Errno socket error] [SSL:
CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)
File "/Users/Shared/jenkins/workspace/TVOS/tools/depends/xbmc line 579, in __init__

	- Status: in den xStream-Settings die Suche nach Updates ausschalten, dann läuft es wieder
Updates von Git muss man dann manuell einspielen oder auf Updates über das offizielle xStreamRepo warten


## 4. Fehlerbericht über Log-Datei


### 4.1. Allgemeines zur Log-Datei

In dem log File werden alle Aktivitäten/Programmabläufe von Kodi protokolliert und gespeichert. Wenn man nun Probleme mit Kodi hat, ist es sehr hilfreich, dieses Log File im Forum zu Posten. Nur so kann eine schnelle und Zielgerichtete Lösung erfolgen.


### 4.2 Speicherort der Log Datei

Den Speicherpfad von Kodi anzeigen lassen – Scroll weiter runter zum Punk Debug_Loggin und folgen den Beschreibungen.

Das ist immer vom Betriebssystem abhängig.
Im Folgenden werden bekannte Ordnerstrukturen der jeweiligen Betriebssysteme aufgelistet. Anstelle von "xbmc" kann in den Ordnern auch "kodi" stehen
(die Ordnerstruktur kann jedoch auch leicht von dieser Anleitung abweichen):

- Windows XP
    - `Documents and Settings\<your_user_name>\Application Data\Kodi`
- Vista/Windows 7
    - `C:\Users\<your_user_name>/%APPDATA%/Roaming/Kodi/Kodi.log`
- Mac OS X
    - `/Users/<username>/Library/Logs/ oder`
    - `/Users/<your_user_name>/Library/Application Support/Kodi/userdata`
- iOS
    - `/private/var/mobile/Library/Preferences`
- Linux, OpenElec, Raspberry Pi 1-3
    - `$HOME/.kodi/temp/`
    - `$HOME/.kodi/userdata/temp/xbmc.log`
    - `$HOME/.kodi/userdata`
- Android
    - `/android/data/org.xbmc.Kodi/files/.kodi/temp`
    - `data/data/org.xbmc.Kodi/cache/temp`

Die Ordner sind meist versteckt und müssen sichtbar gemacht werden, im Windows Explorer oder auf Android mit dem ESDateiexplorer.

Das Log File kann am besten mit Notepad++  unter Windows oder gedit unter Linux betrachtet werden.
Auch der normale Texteditor unter Windows geht, Notepad ist aber übersichtlicher.
Auf Android einen Texteditor verwenden zum Betrachten.
Übrigens die Kodi „log.old“ ist die Logdatei vom letzten Neustart/Crash. Also wenn man keine mehr erstellen kann, dann diese nehmen.


### 4.3. Erstellen und Hochladen der Log-Datei

Kodi hat Standardmäßig die beiden wichtigen Log Addons integriert (eines zum Lesen der Log, das andere zum Hochladen). Damit ist das Erstellen der Log Datei und Posten im Forum sehr viel einfacher.

In Kodi gehe zu:

- Desktop-Optionen
- Einstellungen
- Addons
- Suche

In die Zeile "log" ein und Klicks auf Fertig.

Folgende Addons auswählen und installieren diese:

Log Viewer für Kodi (nur zum Lesen der Log-Datei)
Kodi Log Uploader (zum Auslesen & Uploaden der Log-Datei)

Mit dem LogViewer kann man die Log Datei ansehen, mit dem LogUploaded das Log-File auf http://xbmclogs.com hochladen.

Bei der Installation eine E-Mail Adresse angeben. An diese wird dir dann nach dem LogUpload ein Link zur Log Datei geschickt.
Diesen Link im Forum Posten oder alles in einen Texteditor koperien, Die Datei speicherun und im Forum hochladen.

Debug-Logging (Kodi GUI):

Manchmal ist es gut das Debug Logging in Kodi zu aktivieren um noch mehr Informationen zu erhalten.

Folgendes Ausführen:
 Desktop-Optionen
 
- Einstellungen
- System
- Debugging
- "Debug-Logging aktivieren" anklicken

Fertig

Es wird nun am oberen Rand eine Statuszeile eingeblendet mit Infos; **Hier ist auch der Speicherort der Log-Datei zu sehen!**

Starte Kodi neu und öffne das Addon welches einen Fehler verursacht. Erstellen dann sofort eine Log-Datei (dann ist der Fehler leichter herauszulesen).

Das Debug-Logging kann im Anschluss wieder deaktiviert werden.

Unter dem Punkt  Komponentenspezifische Protokollierung kann man bei der Kategorie "Konfiguration der Komponentenspezifischen Protokollierung" noch Einstellen was alles im Debug-Log Protokolliert werden soll.


## 5. Phyton Dateien


### 5.1. Allgemeines zur .py-Datei

Eine .py Datei ist eigentlich eine Textdatei. Die Endung .py verweist auf die Programmiersprache Python, welche in Kodi zur Anwendung kommt.Diese .py Dateien werden in sämtlichen/den meisten Addons verwendet.
 
 
### 5.2 Bearbeiten einer .py-Datei

Manchmal werdet Ihr lesen z.B. Wechsel die .py Datei in dem Ordner „xyz“, oder ändere den Eintrag in Zeile 134.Öffnen könnt Ihr die Datei mit vielen Programmen z.B. Notepad++ (Freeware) oder Texteditor. In Notepad werden Euch die Zeilen-Nummern angezeigt und ist somit übersichtlicher, aber es geht auch mit dem EditorMit Notepad++ könnt Ihr die .py Datei sofort öffnen und wieder speichern.

Bei Verwendung des Text-Editors müsst Ihr die Endung vorher von .py auf .txt ändern. Dann könnt Ihr die Datei öffnen und Änderungen vornehmen. Im Anschluss bitte „Speichern unter“ wählen und bei „Dateityp“ alle wählen, und wieder als .py Datei speichern


### 5.3 Speicherort der einzelnen Webseiten

In den folgenden Ordnern findet Ihr alle Addons von Kodi. Das Addon xStream wird in aller Regel unter plugin.video.xstream istalliert.

- Android 
	- `/Android/data/org.xbmc.kodi/files/.kodi/addons/`
	- `/sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/`  (.kodi ist ein versteckter Ordner)
- iOS
	- `/private/var/mobile/Library/Preferences/Kodi/addons/`
- Linux 
	- `~/.kodi/addons/`
- Mac 
	- `/Users/<your_user_name>/Library/Application Support/Kodi/addons/`
- OpenELEC 
	- `/storage/.kodi/addons/`
- Windows
	- `C:\Users\BENUTZERNAME\AppData\Roaming\Kodi\addons`    (AppData ist ein versteckter Ordner)

Das Addon xStream wird in aller Regel unter plugin.video.xstream istalliert.
Im Verzeichnis `sites/` sind die .py Daten und im Ordner `resources/art/sites/` die jeweiligen Artworks bzw. Site-Icons der einzelnen Webseiten abgelegt.

