import glfw

class _GLFWWindow:
    """
    glfw window Wrapper
    """
    def __init__(self,name="Viewer",size=(1000,650)):
        assert len(size) == 2
        if not glfw.init():
            raise Exception("Cannot be initialized")
        self._screen_size = size
        self._monitor     = glfw.get_primary_monitor()
        self._monitor_pos = glfw.get_monitor_pos(self._monitor)
        self._mode        = glfw.get_video_mode(self._monitor)
        self._window      = self._create_window(name,size)

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Always refresh after context exit
        """
        self.__call__()

    def __call__(self,_poll_events=True):
        if _poll_events: glfw.poll_events()
        glfw.swap_buffers(self._window)
        if glfw.window_should_close(self._window) or (glfw.get_key(self._window, glfw.KEY_ESCAPE) == glfw.PRESS):
            glfw.terminate()
            return False
        return True

    def _center_window(self,window):
        size = glfw.get_window_size(window)
        mode = glfw.get_video_mode(self._monitor)
        glfw.set_window_pos(
            window,
            int(self._monitor_pos[0] + (mode.size.width - size[0]) / 2),
            int(self._monitor_pos[1] + (mode.size.height - size[1]) / 2))

    def _create_window(self,name,size):
        window = glfw.create_window(*size,name,None,None)
        if not window:
            glfw.terminate()
            raise Exception("Window could not be created")
        self._center_window(window)
        glfw.make_context_current(window)
        return window

    def window(self):
        return self._window

    def terminate(self):
        self._window.terminate()


if __name__ == '__main__':
    window = _GLFWWindow()
    while window():
        frame = window.window()
        ...
    window.terminate()
