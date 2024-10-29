#Widget Overlays
#Nachdem omni.ui und omni.kit.ui importiert wurden
import omni.ui as ui

class MyWidgetOverlayExtension:
    def __init__(self):
        # Fenster und Widgets erstellen
        self.window = ui.Window("Widget Info Overlay", width=300, height=200)
        with self.window.frame:
            with ui.VStack():
                ui.Label("Maschinenstatus")
                ui.ProgressBar(value=0.6)  # Beispiel für Energieverbrauchsanzeige
                ui.Label("Weitere Maschineninformationen hier")

    def on_shutdown(self):
        # Widget und Fenster entfernen
        if self.window:
            self.window.destroy()
