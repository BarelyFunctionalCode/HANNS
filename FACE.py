import time
import threading

from .display.display import Display

class FACE:
  def __init__(self):
    self.text = ""
    self.expression = ""

    self.display = Display()

    self.new_thread = threading.Thread(target=self.worker)
    self.new_thread.start()

  def worker(self):
    while True:
      if self.display.root == None: break

      if self.text != "":
        self.display.enqueue_update_text(self.text + "\n\n")
        self.text = ""

      if self.expression != "":
        self.display.set_face_expression(self.expression)
        self.expression = ""

      time.sleep(0.1)

  def start(self):
    self.display.start()
    self.new_thread.join()

  def speak(self, text):
    self.text = text

  def update_expression(self, expression):
    self.expression = expression


if __name__ == "__main__":
  face = FACE()
  
  face.speak("Death to all humans")
  face.update_expression("slow_scan")

  face.start()