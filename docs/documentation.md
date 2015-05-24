---
documentclass: scrartcl
title: Der Webmpd-Client Snøbær
author: Christopher Pahl und Christoph Piechula
toc: yes
date: \today
---

# Vorwort

## Einleitung

Das Ziel der der Studienarbeit ist es eine Software mit einem Python
Webframework umzusetzen. Aus persönlichen Interesse haben wir uns für einen
Music Player Client (kurz MPC) entschieden. 

Der Music Player Daemon (kurz MPD) ist eine unter unixoiden Betriebssystemen
beliebte Software um Musik mittels einer Client/Server--Architektur abzuspielen.
Der Server verwaltet dabei die komplette Datenbank samt Metadaten, der Client
hingegen dient lediglich als ,,Fernbedienung'' und zeigt oft noch Coverart und
weitere Daten an. 

Auf der offiziellen MPD--Seite (TODO: link) gibt es eine Liste aller verfügbaren
MPD--Clients --- es sind mittlerweile über 200. Darunter sind auch einige
Webbasierte Clients, wie ympd, Volumino (Debian basierend) oder RuneOS
(Archlinux basierend). Die beiden letzteren sind sogar vollwertige
HiFi-Audioplayer Linux--Distrubitionen mit den Raspberry Pi als
Hauptzielplattform. Leider sind diese relativ groß und komplex und auch noch in
PHP geschrieben. ympd ist hingegen in C geschrieben und kommuniziert mittels
Websockets mit dem auf Bootstrap basierten Javascript Frontend. 

## Zielsetzung

Das Ziel unseres Projekt ist es nun eine Mischung beider Welten herzustellen.
Zum einen soll der Client in C geschrieben sein, zudem groß und fett. Nein,
Scherzle macht. Das eigentliche Ziel der Arbeit ist es einen MPD-Client zu
schaffen welcher leichtgewichtig wie ympd ist und den Komfort von Volumio/RuneOS
bietet und zusätzlich plattformunabhängig ist.

Da der Audiosetup in unserer Wohngemeinschaft auf einem Raspberry PI basiert,
ist es zudem wünschenswert, dass das Backend relativ ressourcenschonend ist um
den recht begrenzten Arbeitsspeicher des Rechners (256MB) nicht zu überfüllen. 

## Namensgebung und Logo

Da es in letzter Zeit hipp ist, Früchte in technische Produktnamen zu
integrieren (Raspberry Pi, Bananna Pi, ...) springen wir nun auf diesen Zug auf
und bedienen uns diesem Schema. Da es um Musik geht und die Software
auf einem Raspberry Pi laufen soll haben wir uns hier für ,,Knallerbsen'',
hochdeusch Schneebeeren, entschieden. Um parallel den Unicode--Support in der
Welt zu verbessern und nördig zu wirken bedienten wir uns zudem der nordischen
Sprache und übersetzten Schneebeere auf Norwegisch: Snøbær.

# Grundlagen Music Player Daemon

Um einen Musicplayer zu entwickeln eignet sich ein MPC besonders, da man nicht
das Rad neu erfinden muss. Der MPD bringt bereits die meisten Funktionalitäten
und Konzepte aus anderen Musicplayern mit. Er kann bereits alle gebräuchlichen
Formate einlesen und auf viele Audiobackends ausgeben. Zudem ist er sehr robust
und spielt auch zuverlässig bei hoher Systemlast noch Musik ab --- im Gegensatz
zu Amarok wo die Systemlast durch das Abspielen erst generiert wird.

TODO: MPD Architektur Bild.

Die meisten MPD-Konzepte sind bereits aus anderen Musikplayern bekannt, werden
aber hier noch kurz erwähnt:

* Sämtliche Songs werden in der *Database* gespeichert.
* Songs werden zum abspielen in die *Queue* geladen, wo sie der Reihe nach
  abgespielt werden.
* Der Inhalt der *Queue* kann als *Stored Playlist* unter einem Namen
  abgespeichert werden und zu einem späteren Zeitpunkt wieder geladen werden.
* Clients sprechen mit dem MPD über ein definiertes Textprotokoll (TODO: Link) 
* Es sind mehrere Audioausgaben möglich, darunter ALSA, Pulseaudio oder auch ein
  HTTP Stream. Zudem lassen sich die Qualitätseinstellungen detailiert anpassen
  (libsamplerate etc) weswegen er bei audiophilem Publikum sehr beliebt ist.

Da der MPD netzwerkfähig ist können sich mehrere Clients auf ihn schalten und
den ,,Zustand" des Servers ändern (wie beispielsweise das aktuell spielende
Lied). Man hat pro Server einen gemeinsamen Zustand, welcher von den Clients
widergespiegelt wird. Sollten mehrere  Zustände gewünscht sein, so kann man seit
MPD 0.19 zusätzlich Proxy--Server einrichten, die selbst als Clients des
Haupt--,,Servers'' fungieren, aber einen eigenen Zustand besitzen:

TODO: Grafik

Dieses Prinzip wird beispielsweise in unserer Wohngemeinschaft genutzt um die
Metadaten der Musiksammlung durch einen Hauptserver zu verwalten, der selbst
keine Audioausgabe besitzt, dafür aber Zugriff auf die Musikdaten hat. Auf jedem
abspielfähigem Gerät befindet sich dann ein Proxyserver, welcher die Metadaten
des Hauptservers spiegelt und vom Nutzer des Rechners mittels eines MPD--Clients
gesteuert werden kann. 

# Aufbau von Snøbær

* Screenshots
* Fertiges Produkt

# Architektur

* Diagramme mit Onlinetool

## Frontend

* Views
* JS
* Weitestgehend keinen eigenen Zustand/Spiegelt nur Zustand des Servers wieder

## Backend

* Python
* C

## Verwendete Bibiotheken

    * Tornado, Flask, Bootstrap
    * libmoosecat, glyrc

Warum diese Bibiotheken? 

# Entwicklungsumgebung

* Verwendete Tools
* Tests
* Inbetriebnahme (Docker)

# Fazit

* Known Bugs
* Erweiterungen
* Abschliessendes Resume (Aufteilung in 3 Codebasen sinnvoll? Nein doch oh!)