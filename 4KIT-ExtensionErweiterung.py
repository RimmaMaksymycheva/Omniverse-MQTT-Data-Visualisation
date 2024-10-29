#Erweitere die KIT-Extension zur Darstellung der Daten aus 1.) mit der Plot UI Komponente
#https://docs.omniverse.nvidia.com/kit/docs/omni.ui/latest/omni.ui/omni.ui.Plot.html

import omni.ui as ui
import time
from .mqtt_data_manager import MqttDataManager  # Falls die Klasse importierbar ist

class MyWidgetOverlayExtension:
    def __init__(self):
        # MQTT Datenmanager initialisieren
        self.data_manager = MqttDataManager(broker="test.mosquitto.org", port=1883, topic="sometopic/data", max_values=10)
        self.data_manager.start()
        
        # Fenster und Plot erstellen
        self.window = ui.Window("Maschinenstatus Plot", width=400, height=300)
        
        # Plot einrichten
        with self.window.frame:
            with ui.VStack():
                ui.Label("Energieverbrauch Verlauf")
                self.plot = ui.Plot(width=380, height=250)
                self.series = ui.PlotLineSeries(self.plot, label="Verlauf", color=0xFF00FF00) #color - grün
                self.plot.add_line_series(self.series)
                
        # Timer für die Aktualisierung des Plots
        self._update_timer = omni.kit.app.get_app().get_idle_callback_stream().add_callback(self.update_plot)

    def update_plot(self, dt):
        """
        Aktualisiert den Plot mit den neuesten Daten aus dem MqttDataManager.
        """
        data = self.data_manager.get_data()
        if data:
            # Aktualisiere den Plot mit neuen Werten
            self.series.set_y_data(data)

    def on_shutdown(self):
        # Fenster schließen und MQTT-Client stoppen
        if self.window:
            self.window.destroy()
        self.data_manager.stop()
        omni.kit.app.get_app().get_idle_callback_stream().remove_callback(self._update_timer)

