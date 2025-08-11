import threading
import time

class Sablier:
    def __init__(self, message="⏳ Réflexion en cours...", intervalle=0.5):
        self._stop_event = threading.Event()
        self.intervalle = intervalle
        self.message = message
        self.icônes = ["⏳", "⌛"]

    def start(self):
        def loop():
            i = 0
            print(f"\n{self.message} ", end="")
            while not self._stop_event.is_set():
                print(self.icônes[i % len(self.icônes)], end="\r")
                time.sleep(self.intervalle)
                i += 1
        self.thread = threading.Thread(target=loop)
        self.thread.start()

    def stop(self):
        self._stop_event.set()
        self.thread.join()
        print(" " * 60, end="\r")
