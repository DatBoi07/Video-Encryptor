import cv2
import pywt
import numpy as np
def decompress_video(input_video, output_video):
    def decompress_frame(frame):
        compressed_frame_R = frame[:, :, 0]
        compressed_frame_G = frame[:, :, 1]
        compressed_frame_B = frame[:, :, 2]
        coeffs_R = pywt.dwt2(compressed_frame_R, 'haar')
        coeffs_G = pywt.dwt2(compressed_frame_G, 'haar')
        coeffs_B = pywt.dwt2(compressed_frame_B, 'haar')
        LL_R, _ = coeffs_R
        LL_G, _ = coeffs_G
        LL_B, _ = coeffs_B
        decompressed_frame_R = pywt.idwt2((LL_R, (np.zeros_like(LL_R), np.zeros_like(LL_R), np.zeros_like(LL_R))), 'haar')
        decompressed_frame_G = pywt.idwt2((LL_G, (np.zeros_like(LL_G), np.zeros_like(LL_G), np.zeros_like(LL_G))), 'haar')
        decompressed_frame_B = pywt.idwt2((LL_B, (np.zeros_like(LL_B), np.zeros_like(LL_B), np.zeros_like(LL_B))), 'haar')
        decompressed_frame = np.stack([decompressed_frame_R, decompressed_frame_G,decompressed_frame_B], axis=-1)
        decompressed_frame = np.uint8(decompressed_frame)
        return decompressed_frame
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
            decompressed_frame = decompress_frame(frame)
            out_vid.write(decompressed_frame)
        else:
            break
    vid.release()
    out_vid.release()