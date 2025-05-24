import time
import ctypes
import pygetwindow as gw
from pynput import keyboard
import pyperclip

# Виртуальные коды клавиш для WinAPI
VK_CONTROL = 0x11
VK_V = 0x56
KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002

# JavaScript code to auto-click the "Confirm" button
JS_SCRIPT = """
(function autoClickConfirm() {
  const selector = 'button[data-testid="confirm-footer-button"]';
  const existing = document.querySelector(selector);
  if (existing) {
    existing.click();
    console.log('✅ Кнопка найдена и нажата сразу');
    return;
  }
  function onInsert(e) {
    const node = e.target;
    if (node.matches && node.matches(selector) || node.querySelector?.(selector)) {
      const btn = node.matches(selector) ? node : node.querySelector(selector);
      btn.click();
      console.log('✅ Кнопка нажата при вставке в DOM');
      document.body.removeEventListener('DOMNodeInserted', onInsert, false);
    }
  }
  document.body.addEventListener('DOMNodeInserted', onInsert, false);
})();
"""

def find_metamask_window():
    """Find and return the MetaMask window."""
    windows = [w for w in gw.getAllWindows() if "MetaMask" in w.title]
    if not windows:
        raise Exception("MetaMask window not found.")
    print(f"Found MetaMask window: {windows[0].title}")
    return windows[0]


def activate_window(window):
    """Activate the given window."""
    window.activate()
    time.sleep(1)  # Wait for the window to activate
    print("MetaMask window activated.")


def key_event(vk, flags):
    """Send a keyboard event via WinAPI."""
    ctypes.windll.user32.keybd_event(vk, 0, flags, 0)


def paste_via_winapi(text):
    """Copy text to clipboard and paste using WinAPI events."""
    pyperclip.copy(text)
    time.sleep(1)

    # Нажать Ctrl
    key_event(VK_CONTROL, KEYEVENTF_KEYDOWN)
    # Нажать V
    key_event(VK_V, KEYEVENTF_KEYDOWN)
    # Отпустить V
    key_event(VK_V, KEYEVENTF_KEYUP)
    # Отпустить Ctrl
    key_event(VK_CONTROL, KEYEVENTF_KEYUP)

    time.sleep(1)
    print("JavaScript script pasted via WinAPI.")


def execute_script():
    """Open console with F12 and paste the JavaScript script using WinAPI."""
    controller = keyboard.Controller()

    # Press F12 to open the developer console
    controller.press(keyboard.Key.f12)
    controller.release(keyboard.Key.f12)
    print("Developer console opened.")
    time.sleep(2)  # Wait for console to open

    # Paste the script via WinAPI
    paste_via_winapi(JS_SCRIPT)

    # Press Enter to execute the script
    controller.press(keyboard.Key.enter)
    controller.release(keyboard.Key.enter)
    print("Script executed.")
    time.sleep(1)  # Wait for execution

    # Press F12 to close the console
    controller.press(keyboard.Key.f12)
    controller.release(keyboard.Key.f12)
    print("Developer console closed.")


def main():
    """Main function to automate MetaMask confirmation."""
    print("Starting MetaMask automation...")
    try:
        metamask_window = find_metamask_window()
        activate_window(metamask_window)
        execute_script()
        print("Automation completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    time.sleep(3)  # Give time to switch to the correct screen
    main()
