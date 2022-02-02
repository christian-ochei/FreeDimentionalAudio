import cv2
import mediapipe as mp
import time
import numpy as np

class _FaceTracker:
    """
    """
    def __init__(self,draw_landmarks=False):
        self._window_open = True
        self._registered_landmarks = None
        self._ih, self._iw, self._ic = (5,5,5)
        self._draw_landmarks = draw_landmarks

        if self._draw_landmarks:
            self._font = cv2.FONT_HERSHEY_SIMPLEX
            self._fontScale = 0.2
            self._color = (0, 255, 0)
            self._thickness = 1

    def _tracking_pipeline(self):
        """
        Facing tracking and display pipeline
        """
        cap = cv2.VideoCapture(0)
        presentTime = 0
        mpDraw = mp.solutions.drawing_utils
        mpFaceMesh = mp.solutions.face_mesh
        faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
        drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

        while self._window_open:
            success, img = cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = faceMesh.process(imgRGB)
            ih,iw, ic = img.shape
            self._ih,self._iw,self._ic = img.shape
            if results.multi_face_landmarks:
                landmarks = np.array([
                    [[lm.y, lm.x, lm.z] for id, lm in enumerate(faceLms.landmark)] for faceLms in results.multi_face_landmarks]
                )
                landmarks *= np.array([ih,iw,-800])
                self._registered_landmarks = landmarks-np.array([ih,iw,0])
                landmarks = landmarks.astype(int)
                img[landmarks[...,0].clip(0,ih-1),landmarks[...,1].clip(0,iw-1)] = 255

                if self._draw_landmarks:
                    for i,landmark in enumerate(landmarks[0]):
                        image = cv2.putText(img, str(i), (landmark[1],landmark[0]), self._font,
                                            self._fontScale, self._color, self._thickness, cv2.LINE_AA)



            currentTime = time.time()
            fps_rate = 1 / (currentTime - presentTime)
            presentTime = currentTime

            cv2.putText(img, f'fps:{int(fps_rate)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            cv2.imshow('Face Mesh Detection', img)
            cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()

def test():
    tracker = _FaceTracker(draw_landmarks=True)
    tracker._tracking_pipeline()

if __name__ == '__main__':
    test()