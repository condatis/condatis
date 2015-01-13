#Makefile for econets project
#D. Wallis 2014

all: econet_rc.py econetui.py sourcesinkui.py calculatingui.py manualui.py exportgisui.py droppingui.py dropfilterui.py openhabitatui.py settingsui.py addcellui.py addingui.py registerui.py aboutui.py

aboutui.py: ui/about.ui
	pyuic4 -x -o aboutui.py ui/about.ui

registerui.py: ui/register.ui
	pyuic4 -x -o registerui.py ui/register.ui

addingui.py: ui/adding.ui
	pyuic4 -x -o addingui.py ui/adding.ui

addcellui.py: ui/addcell.ui
	pyuic4 -x -o addcellui.py ui/addcell.ui

openhabitatui.py: ui/openhabitat.ui
	pyuic4 -x -o openhabitatui.py ui/openhabitat.ui

settingsui.py: ui/settings.ui
	pyuic4 -x -o settingsui.py ui/settings.ui

dropfilterui.py: ui/dropfilter.ui
	pyuic4 -x -o dropfilterui.py ui/dropfilter.ui

sourcesinkui.py: ui/sourcesinkui2.ui
	pyuic4 -x -o sourcesinkui.py ui/sourcesinkui2.ui

manualui.py: ui/manual.ui
	pyuic4 -x -o manualui.py ui/manual.ui

exportgisui.py: ui/exportgis.ui
	pyuic4 -x -o exportgisui.py ui/exportgis.ui

droppingui.py: ui/dropping.ui
	pyuic4 -x -o droppingui.py ui/dropping.ui

calculatingui.py: ui/calculating2.ui
	pyuic4 -x -o calculatingui.py ui/calculating2.ui

#forwardoptui.py: ui/forwardopt.ui
#	pyuic4 -x -o forwardoptui.py ui/forwardopt.ui

econet_rc.py: ui/econet.qrc
	pyrcc4 -o econet_rc.py ui/econet.qrc

econetui.py: ui/econetui.ui
	pyuic4 -x -o econetui.py ui/econetui.ui

exe: econet.py
	pyinstaller  --icon econet.ico econet.py 

clean:
	rm -rf econet_rc.py econetui.py sourcesinkui.py calculatingui.py manualui.py exportgisui.py droppingui.py dropfilterui.py openhabitatui.py settingsui.py addcellui.py addingui.py registerui.py aboutui.py
	rm -rf *.pyc
	rm -rf *.h5
	rm -rf *.py~
	rm -rf Makefile~
	rm project/*.pyc
