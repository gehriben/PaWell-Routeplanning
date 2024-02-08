Installation
=============================

Es wird Python in der aktuellen Version benötigt (3.8.3 Stand 19.06.2020). <br />
Nachfolgend sind die erforderlichen Bibliotheken für die Installation dokumentiert.

===============

Zu Beginn sollte ein Virtuelles Environment im Root Ordner des Projekts eingerichtet werden. Dies ist folgendermassen möglich:
    
    python -m flask run

Anschliessen kann dieses mit folgendem Befehl aktiviert werden:
    
    ./env/Scripts/activate.ps1

**Python Dependencies:**

    pip packages: flask, flask_restful, flask_cors, geojson, shapely, pyproj, geopy
    
    - pip install flask
    - pip install flask_restful
    - pip install flask_cors
    - pip install geojson
    - pip install shapely
    - pip install pyproj
    - pip install geopy
    

Applikation starten:
=============================

Das Backend kann nun mit folgendem Befehl gestartet werden:
    
    python -m flask run
    
Der Flask Server ist nun in Betrieb und auf die Applikation kann mit einem Browser unter folgender Adresse zugegriffen werden:

    http://localhost:5000/
  

