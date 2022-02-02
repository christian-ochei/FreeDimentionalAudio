import threading
import time
from visualizer import viewer
from head import headextrinsic, facetracking
from propagation import spatial, stage


class FreeDimensionalAudio:
    """
    """
    def __init__(self):
        ...
        self._face_tracker     = facetracking._FaceTracker()
        self._head_extrinsic = headextrinsic._HeadExtrinsic(
            self._face_tracker
        )
        self._backdrop_handler = stage._StageHandler()
        self._spatial_pipeline = spatial._SpatialPipeline(room=self._backdrop_handler,
                                                          head_extrinsic=self._head_extrinsic)
        self._space_viewer   = viewer._3DViewHandler(
            self._backdrop_handler,self._head_extrinsic,self._spatial_pipeline
        )

    def begin(self):
        tracking_pipe_thread = threading.Thread(
            target=self._face_tracker._tracking_pipeline,args=()
        )
        tracking_pipe_thread.start()

        spatial_pipe_thread = threading.Thread(
            target=self._spatial_pipeline._pipeline,args=()
        )
        spatial_pipe_thread.start()

        head_extrinsic_pipe = threading.Thread(
            target=self._head_extrinsic._pipeline,args=()
        )
        head_extrinsic_pipe.start()

        while self._space_viewer():
            time.sleep(0.009)
            frame = self._space_viewer.window()
            ...
        ...

