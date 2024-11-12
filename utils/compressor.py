import cv2
import pywt
import numpy as np
def compress_video(input_video, output_video):
    def compress_frame(frame):
        coeffs_R = pywt.dwt2(frame[:, :, 0], 'haar')
        coeffs_G = pywt.dwt2(frame[:, :, 1], 'haar')
        coeffs_B = pywt.dwt2(frame[:, :, 2], 'haar')
        LL_R, (LH_R, HL_R, HH_R) = coeffs_R
        LL_G, (LH_G, HL_G, HH_G) = coeffs_G
        LL_B, (LH_B, HL_B, HH_B) = coeffs_B
        coeffs = (LL_R, LL_G, LL_B), (
            np.zeros_like(LH_R), np.zeros_like(HL_R), np.zeros_like(HH_R)
        )
        compressed_frame_R = pywt.idwt2(coeffs_R, 'haar')
        compressed_frame_G = pywt.idwt2(coeffs_G, 'haar')
        compressed_frame_B = pywt.idwt2(coeffs_B, 'haar')
        compressed_frame = np.stack(
            [compressed_frame_R, compressed_frame_G, compressed_frame_B], axis=-1
        )
        compressed_frame = np.uint8(compressed_frame)
        return compressed_frame
    vid = cv2.VideoCapture(input_video)
    fps = vid.get(cv2.CAP_PROP_FPS)
    frame_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_vid = cv2.VideoWriter(output_video, fourcc, fps,
                              (frame_width, frame_height), isColor=True)
    while vid.isOpened():
        ret, frame = vid.read()
        if ret == True:
            compressed_frame = compress_frame(frame)
            out_vid.write(compressed_frame)
        else:
            break
    vid.release()
    out_vid.release()
