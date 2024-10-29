#MqttDataManager
import paho.mqtt.client as mqtt
from collections import deque # für die Speicherung nur der letzten x Werte

class MqttDataManager:                                                  #x=10
    def __init__(self, broker: str, port: int, topic: str, max_values: int = 10):
        """
        Initialisiert die MqttDataManager-Klasse.
        
        :param broker: Die Adresse des MQTT-Brokers.
        :param port: Der Port des MQTT-Brokers.
        :param topic: Das MQTT-Topic, das abonniert wird.
        :param max_values: Die maximale Anzahl der gespeicherten Werte.
        """
        self.broker = broker
        self.port = port
        self.topic = topic
        self.max_values = max_values
        self.data_buffer = deque(maxlen=max_values)  # speichert nur die letzten x Werte
        self.client = mqtt.Client()

        # Callback-Funktionen setzen
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        """
        Wird aufgerufen, wenn der Client sich erfolgreich mit dem MQTT-Broker verbindet.
        """
        print("Verbunden mit dem Broker:", self.broker)
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        """
        Wird aufgerufen, wenn eine Nachricht empfangen wird.
        Fügt die empfangenen Daten in den Datenpuffer ein.
        """
        try:
            # Nachrichtendaten konvertieren (hier wird angenommen, dass es ein Float ist)
            value = float(msg.payload.decode())
            self.add_value(value)
            print(f"Empfangen: {value}")
        except ValueError:
            print("Fehler bei der Verarbeitung der Nachricht:", msg.payload)

    def add_value(self, value):
        """
        Fügt einen neuen Wert zum Datenpuffer hinzu.
        
        :param value: Der neue Wert, der hinzugefügt werden soll.
        """
        self.data_buffer.append(value)

    def start(self):
        """
        Startet den MQTT-Client und verbindet sich mit dem Broker.
        """
        self.client.connect(self.broker, self.port)
        self.client.loop_start()  # startet eine Hintergrundschleife, um Nachrichten zu empfangen

    def stop(self):
        """
        Stoppt den MQTT-Client und trennt die Verbindung.
        """
        self.client.loop_stop()  # beendet die Hintergrundschleife
        self.client.disconnect()

    def get_data(self):
        """
        Gibt die aktuellen Werte im Datenpuffer zurück.
        
        :return: Liste der letzten x Werte.
        """
        return list(self.data_buffer)

# Beispiel für die Nutzung der Klasse
if __name__ == "__main__":
    # MQTT-Broker und Topic-Details
    broker = "test.mosquitto.org"   #Als Beispiel, ein öffentlicher MQTT-Broker
    port = 1883                     #unverschlüsselt
    topic = "sometopic/data"

    # MqttDataManager erstellen und starten                     #x=10
    data_manager = MqttDataManager(broker, port, topic, max_values=10)
    data_manager.start()

    # Zeit geben, um einige Daten zu empfangen
    import time
    time.sleep(5)  # Zeit zum Empfangen von Daten

    # Aktuelle Daten abrufen und anzeigen
    print("Aktuelle Daten:", data_manager.get_data())

    # MQTT-Client stoppen
    data_manager.stop()
