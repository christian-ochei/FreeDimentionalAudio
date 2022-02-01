import threading

import keyboard
import multiprocessing
import interface
import sys
import run

if __name__ == '__main__':
    window = interface.IntroVideo()
    window.show()
    window._begin()
    intro_thread = threading.Thread(target=interface.App.exec,args=())
    intro_thread.start()


    while True:
        if keyboard.is_pressed('backspace'):
            interface.App.closeAllWindows()
            break
        ...

    run.run()