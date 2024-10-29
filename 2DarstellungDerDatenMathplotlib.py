#Initial Data Plotting: Develop an initial data visualization using matplotlib to plot values.
import matplotlib.pyplot as plt
import time

# MQTT-Datenmanager importieren oder definieren
# from mqtt_data_manager import MqttDataManager (Falls bereits in einer separaten Datei)

# Beispiel MQTT-Details
broker = "test.mosquitto.org"
port = 1883
topic = "sometopic/data"

# Datenmanager erstellen und starten                #x=10
data_manager = MqttDataManager(broker, port, topic, max_values=10)
data_manager.start()

# Warte kurz, um Daten zu sammeln
time.sleep(5)  # Warte, um MQTT-Daten zu empfangen

# Plot-Funktion
def plot_data(data_manager):
    # Daten vom MqttDataManager abrufen
    data = data_manager.get_data()
    if not data:
        print("Keine Daten verfügbar.")
        return
    
    # Plot erstellen
    plt.figure(figsize=(10, 5))
    plt.plot(data, marker='o', linestyle='-', color='b', label="Energieverbrauch")
    plt.title("Verlauf der letzten Werte")
    plt.xlabel("Zeit (in Sekunden)")
    plt.ylabel("Energieverbrauch")
    plt.legend()
    plt.grid(True)
    
    # Plot anzeigen
    plt.show()

# Daten plotten
plot_data(data_manager)

# Stoppen des Clients nach dem Plotten
data_manager.stop()
