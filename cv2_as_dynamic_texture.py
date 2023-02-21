import dearpygui.dearpygui as dpg
import cv2 as cv
import numpy as np
from  mediapipe_inference import inference

dpg.create_context()
dpg.configure_app(docking=True, docking_space=True)
dpg.create_viewport(title="Hand Tracking Demo")
dpg.setup_dearpygui()
# default_font = dpg.add_font("NotoSerifCJKjp-Medium.otf", 20)

inference_model = 'None'

def combo_callback(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    inference_model = app_data
    print(f"user_data is: {user_data}")

cap = cv.VideoCapture(0)
ret, frame = cap.read()

width, height = frame.shape[1], frame.shape[0]

with dpg.texture_registry(show=False):
    dpg.add_raw_texture(width, height, default_value=[], tag="frame")

with dpg.window(label='Webcam', tag="mainWindow", no_resize=True, no_move=True, no_collapse=True):
    dpg.add_image("frame")

with dpg.window(label="Model Selector", width=300):
    dpg.add_combo(['None', 'Mediapipe'], default_value='Please pick a model to test...',
                    width=250, tag='model_combo', callback=combo_callback)

dpg.show_viewport()
# dpg.set_primary_window('mainWindow', True)

while dpg.is_dearpygui_running():
    ret, frame = cap.read()
    assert ret
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    if inference_model == 'Mediapipe':
        frame = inference(frame)
    frame = cv.cvtColor(frame, cv.COLOR_RGB2RGBA)
    frame = np.array(frame, dtype=np.float32).ravel()/255
    dpg.set_value("frame", frame)
    dpg.render_dearpygui_frame()



cap.release()
dpg.destroy_context()
