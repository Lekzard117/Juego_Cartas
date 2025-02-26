class ConsoleRedirector:
    def __init__(self, label_widget):
        self.label_widget = label_widget

    def write(self, message):
        # Actualizar el texto del Label con el mensaje recibido
        current_text = self.label_widget.cget("text")
        new_text = current_text + "\n" + message.strip()
        self.label_widget.config(text=new_text)

    def flush(self):
        pass  # Necesario para manejar el flujo de salida estándar