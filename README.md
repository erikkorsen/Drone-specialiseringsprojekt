Local set up (kan skilja sig något beroende på OS)

Kolla så du har pyhton installerat:
python3 --version

Installera Pythonpaket:
pip3 install flask flask-cors requests redis flask-socketio geopy

Installera redis (tror man skriver annorlunda om det inte är på macOS):
brew install redis

Starta och testa redis:
redis-server
redis-cli
ping (kolla så du får PONG)


Starta projektet

Kör följande kommandon i separata terminalfönster/flikar

1. redis-server
2. python3 database.py
3. python3 drone_manager.py
4. python3 route_planner.py
5. python3 build.py

Öppna i webbläsaren
http://127.0.0.1:5002


Om du får SSL-error från geopy, typ SSL: CERTIFICATE_VERIFY_FAILED,
kan man behöva installera/uppdatera certifi via typ: pip install certifi (eller nåt sånt)
 

