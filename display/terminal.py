from queue import Queue
import tkinter as tk


class TkinterTerminal:
  def __init__(self, root, talking_queue):
    self.root = root
    self.talking_queue = talking_queue
    self.is_active = False
    self.is_enabled = True

    # Terminal Parameters
    self.terminal_text_output = ""
    self.terminal_text_output_index = 0
    self.update_queue = Queue()

    # Terminal for text output
    self.frame = tk.Frame(self.root, bg="black")
    self.frame.pack(fill=tk.X, padx=5, pady=5, side=tk.BOTTOM)

    self.terminal_text = tk.Text(self.frame, height=10, state='disabled', bg="black", fg="green", font=("Courier", 20), borderwidth=0, highlightthickness=0, insertbackground="green")
    self.terminal_text.pack()

    # Add blinking cursor
    self.terminal_text.config(state='normal')
    self.terminal_text.insert(tk.END, "_")
    self.terminal_text.tag_add("cursor", "1.0")
    self.terminal_text.config(state='disabled')

    self.update()
    self.blink_cursor()

  # Used to set the active state of the terminal
  def set_enabled(self, is_enabled):
    self.is_enabled = is_enabled

  def update(self):
    # Update text output from queue
    while not self.update_queue.empty():
      self.terminal_text_output += self.update_queue.get()

    new_line = False
    
    if self.terminal_text_output_index < len(self.terminal_text_output):
      self.is_active = True
      if self.is_enabled:
        # Add new character to text object
        char = self.terminal_text_output[self.terminal_text_output_index]
        self.terminal_text.config(state='normal')
        self.terminal_text.insert("end-2c", char)
        self.terminal_text.config(state='disabled')
        if char == "\n":
          new_line = True
        self.terminal_text_output_index += 1
        self.terminal_text.see(tk.END)

        # Update talking queue to move the mouth when text is outputting
        if char == " " or char == "\n" or char == "\t":
          self.talking_queue.put(0.0)
        else:
          self.talking_queue.put(0.7)
    else:
      self.is_active = False
      self.talking_queue.put(0.0)
  
    # Longer delay after new line
    if new_line:
      self.root.after(1000, self.update)
    else:
      self.root.after(50, self.update)

  # Blinking cursor following text output
  def blink_cursor(self):
    if "cursor" in self.terminal_text.tag_names():
      self.terminal_text.config(state='normal')
      self.terminal_text.tag_config(
        "cursor",
        foreground="black" if self.terminal_text.tag_cget("cursor", "foreground") == "green" else "green"
      )
      self.terminal_text.config(state='disabled')
    self.root.after(500, self.blink_cursor)