import os


import cv2
import numpy as np
from sympy import N
import tensorflow.compat.v1 as tf

from config import config
from models import Inception
from utils import change_channel, gray_normalizer

tf.disable_v2_behavior()


def load_model(session, m_type, m_name):
    # load the weights based on best loss
    best_dir = "best_loss"

    # check model dir
    model_path = "models/" + m_name
    path = os.path.join(model_path, best_dir)
    if not os.path.exists(path):
        raise FileNotFoundError
    model = Inception(m_name, config)

    # load the best saved weights
    ckpt = tf.train.get_checkpoint_state(path)
    if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
        model.restore(session, ckpt.model_checkpoint_path)

    else:
        raise ValueError("There is no best model with given model")

    return model


def rescale(image):
    """
    If the input video is other than network size, it will resize the input video
    :param image: a frame form input video
    :return: scaled down frame
    """
    scale_side = max(image.shape)
    # image width and height are equal to 192
    scale_value = config["input_width"] / scale_side

    # scale down or up the input image
    scaled_image = cv2.resize(image, dsize=None, fx=scale_value, fy=scale_value)

    # convert to numpy array
    scaled_image = np.asarray(scaled_image, dtype=np.uint8)

    # one of pad should be zero
    w_pad = int((config["input_width"] - scaled_image.shape[1]) / 2)
    h_pad = int((config["input_width"] - scaled_image.shape[0]) / 2)

    # create a new image with size of: (config["image_width"], config["image_height"])
    new_image = (
        np.ones((config["input_width"], config["input_height"]), dtype=np.uint8) * 250
    )

    # put the scaled image in the middle of new image
    new_image[
        h_pad : h_pad + scaled_image.shape[0], w_pad : w_pad + scaled_image.shape[1]
    ] = scaled_image

    return new_image


def main(
    m_type,
    m_name,
):
    with tf.Session() as sess:  # start a session

        # load best model
        model = load_model(sess, m_type, m_name)  # load the best model
        cap = cv2.VideoCapture(0)  # load the camera
        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if frame.shape[0] != 192:
                frame = rescale(frame)
            image = gray_normalizer(frame)
            image = change_channel(image, config["input_channel"])
            [p] = model.predict(sess, [image])
            print(p)
            cv2.circle(frame, (int(p[0]), int(p[1])), int(p[2]), (0, 0, 255), 2)
            cv2.circle(frame, (int(p[0]), int(p[1])), 1, (0, 0, 255), -1)
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    model_name = "3A4Bh-Ref25"
    model_type = "INC"
    video_path = 0

    # initial a logger

    main(model_type, model_name)
