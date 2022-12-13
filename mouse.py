import ctypes

def move_mouse(x, y):
  # Get the screen size.
  screen_width = ctypes.windll.user32.GetSystemMetrics(0)
  screen_height = ctypes.windll.user32.GetSystemMetrics(1)

  # Scale the coordinates to the screen size.
  x_scaled = x * screen_width
  y_scaled = y * screen_height

  # Move the mouse to the scaled coordinates.
  ctypes.windll.user32.SetCursorPos(x_scaled, y_scaled)

def click_mouse():
  # Simulate a left mouse button click.
  ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
  ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
