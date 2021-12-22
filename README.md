# FrightKnight
Bachelorprojekt THU WS2021/22

Das Projekt steuert eine Puppe, namens Fright Knight, die sich vor Menschen erschreckt.
Sobald eine Person den Raum betritt, erschrickt der Fright Knight. Beim Erschrecken
dreht er seinen Fuß nach innen, wodurch er den Oberkörper nach hinten lehnt. Außerdem
öffnet er seinen Mund und beobachtet die Person im Raum, indem er ihr mit seinem Blick 
folgt. Die Software läuft auf einem Raspberry Pi 3 und die Körperteile werden über 
Servomotoren gesteuert.

Die beiden Setup-Dateien installieren alles Nötige auf dem Pi. Das Gesamtprogramm steht in
der Python Datei "gesamt_programm.py".

Die Gesichtserkennung ist mithilfe von imutils realisiert. Im Ordner Testprogramme findet
man den Code unter "imutils_face_detection.py". Für diese Gesichtserkennung benötigt man 
die "deploy.prototxt.txt"-Datei und die "res10_300x300_ssd_iter_140000.caffemodel"-Datei. 
Am Anfang sollte das Programm über die Python Library face_recognition implementiert werden.
Dies ist allerdings etwas langsam auf dem Pi. Den Code findet man ebenfalls im Ordner 
Testprogramme unter dem Namen "face_recognition.py".

Die Motoren werden über ein Servoboard angesteuert und es wird die Library Adafruit Servokit
verwendet. Die Programme der einzelnen Motoransteuerungen śind ebenfalls im Ornder Testprogramme
zu finden.
