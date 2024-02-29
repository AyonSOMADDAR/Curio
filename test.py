import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import cv2

# Define a video processor class to capture frames
class ImageProcessor(VideoProcessorBase):
    def __init__(self):
        super().__init__()
        self.latest_frame = None

    def recv(self, frame):
        self.latest_frame = frame.to_ndarray(format="bgr24")

def main():
    st.title("Streamlit Camera App")

    # Display the live camera feed
    webrtc_ctx = webrtc_streamer(
        key="example",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=ImageProcessor,
        async_processing=True,
    )

    # Display captured image when the button is clicked
    if webrtc_ctx.video_processor:
        if st.button("Capture Image"):
            captured_image = webrtc_ctx.video_processor.latest_frame
            if captured_image is not None:
                st.image(captured_image, channels="BGR", caption="Captured Image")

if __name__ == "__main__":
    main()
