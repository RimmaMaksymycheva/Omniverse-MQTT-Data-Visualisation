import paho.mqtt.client as mqtt
from collections import deque
import matplotlib.pyplot as plt
import omni.ui as ui
import time

class MqttDataManager:
    def __init__(self, broker, port, topic, max_values=10):
        self.data_buffer = deque(maxlen=max_values)
        self.client = mqtt.Client()
        self.client.on_connect = lambda c, u, f, r: (print(f"Verbunden mit {broker}"), c.subscribe(topic))
        self.client.on_message = lambda c, u, msg: self._process_message(msg)
        self.client.connect(broker, port)
        self.client.loop_start()

    def _process_message(self, msg):
        try:
            self.data_buffer.append(float(msg.payload.decode()))
            print(f"Empfangen: {self.data_buffer[-1]}")
        except ValueError:
            print("Fehler bei der Verarbeitung:", msg.payload)

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

    def get_data(self):
        return list(self.data_buffer)

def plot_data(data_manager):
    if (data := data_manager.get_data()):
        plt.figure(figsize=(10, 5))
        plt.plot(data, marker='o', linestyle='-', color='b')
        plt.title("Energieverbrauch Verlauf")
        plt.xlabel("Zeit (in Sekunden)")
        plt.ylabel("Energieverbrauch")
        plt.grid(True)
        plt.show()
    else:
        print("Keine Daten verfügbar.")

class MyWidgetOverlayExtension:
    def __init__(self):
        self.data_manager = MqttDataManager("test.mosquitto.org", 1883, "sometopic/data")
        self.window = ui.Window("Maschinenstatus Plot", width=400, height=300)
        with self.window.frame:
            with ui.VStack():
                ui.Label("Energieverbrauch Verlauf")
                self.series = ui.PlotLineSeries(ui.Plot(width=380, height=250), label="Verlauf", color=0xFF00FF00)
        omni.kit.app.get_app().get_idle_callback_stream().add_callback(self.update_plot)

    def update_plot(self, dt):
        if (data := self.data_manager.get_data()):
            self.series.set_y_data(data)

    def on_shutdown(self):
        if self.window: self.window.destroy()
        self.data_manager.stop()

if __name__ == "__main__":
    data_manager = MqttDataManager("test.mosquitto.org", 1883, "sometopic/data")
    time.sleep(5)  # Zeit zum Empfangen von Daten
    print("Aktuelle Daten:", data_manager.get_data())
    plot_data(data_manager)
    data_manager.stop()
