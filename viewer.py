from OpenGL.GLU import *
from OpenGL.GL import *
import window
import glfw
import controls

flashLightPos = [ 0.0, 0.0, 0.0]
flashLightDir = [ 0.0, 0.0, -1.0 ]
flashLightColor = [ 0.02, 0.02, 0.02 ]

redLightColor = [ 0.1, 0.1, 0.12 ]
redLightPos = [ 10.0, 0.0, 5.0, 1.0 ]

greenLightColor = [ 0.6, 0.6, 0.6 ]
greenLightPos = [ 10.0, 0.0, 10.0, 1.0 ]

def _staticLighting():
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)              ### test
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, flashLightPos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, flashLightColor)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, flashLightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, flashLightColor)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, flashLightDir)
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 12.0)
    # set up static red light
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, redLightColor)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, redLightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, redLightColor)
    # set up moving green light
    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, greenLightColor)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, greenLightColor)
    glLightfv(GL_LIGHT2, GL_SPECULAR, greenLightColor)


class _3DViewHandler(window._GLFWWindow):
    """
    Realtime 3D Display FrontEnd
    """
    def __init__(self,backdrop_handler,head_extrinsic,spatial_pipeline):
        super(_3DViewHandler, self).__init__()
        self._spatial_pipeline = spatial_pipeline
        self._controller = controls._ViewController()
        self._head_extrinsic   = head_extrinsic
        self._backdrop_handler = backdrop_handler
        self._cursor = None
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glClearColor(0,0,0,1)
        glEnable(GL_DEPTH_TEST)
        _staticLighting()

    def _on_key_press(self, event):
        action = self._KEYMAP.get(str(event.text()))
        if action:action()

    def __call__(self):
        glfw.poll_events()
        ct = glfw.get_time()
        self._controller()
        glLoadIdentity()
        gluPerspective(45, (self._screen_size[0] / self._screen_size[1]), 1, 500.0)
        glTranslatef(0.0, 0.0, -10)

        glRotatef(1, 5, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT |
                GL_DEPTH_BUFFER_BIT |
                GL_ACCUM_BUFFER_BIT)

        # position the red light
        glLightfv(GL_LIGHT1, GL_POSITION, redLightPos)

        # draw the red light
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glTranslatef(redLightPos[0], redLightPos[1], redLightPos[2])
        glColor3fv(redLightColor)
        glEnable(GL_LIGHTING)
        glPopMatrix()

        # position and draw the green light
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glLightfv(GL_LIGHT2, GL_POSITION, greenLightPos)
        glTranslatef(greenLightPos[0], greenLightPos[1], greenLightPos[2])
        glColor3fv(greenLightColor)
        glEnable(GL_LIGHTING)
        glEnable(GL_MULTISAMPLE)
        glPopMatrix()

        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)

        self._backdrop_handler._glDraw(self._controller._control_bind)
        self._head_extrinsic.  _glDraw(self._controller._control_bind)
        self._spatial_pipeline._glDraw(self._controller._control_bind)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)
        return super(_3DViewHandler, self).__call__(_poll_events=False)


if __name__ == '__main__':
    viewer = _3DViewHandler()
    while viewer():
        frame = viewer.window()
        ...
    viewer.terminate()
