# Copyright 2020 The MediaPipe Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""MediaPipe solution drawing utils."""

import dataclasses
import math
from typing import List, Mapping, Optional, Tuple, Union

import cv2
import matplotlib.pyplot as plt
import numpy as np

from mediapipe.framework.formats import detection_pb2
from mediapipe.framework.formats import landmark_pb2
from mediapipe.framework.formats import location_data_pb2



import cv2
import mediapipe as mp
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from google.cloud import vision
import tensorflow.lite as tflite


import os

_PRESENCE_THRESHOLD = 0.5
_VISIBILITY_THRESHOLD = 0.5
_BGR_CHANNELS = 3

WHITE_COLOR = (224, 224, 224)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 128, 0)
BLUE_COLOR = (255, 0, 0)


@dataclasses.dataclass
class DrawingSpec:
  # Color for drawing the annotation. Default to the white color.
  color: Tuple[int, int, int] = WHITE_COLOR
  # Thickness for drawing the annotation. Default to 2 pixels.
  thickness: int = 2
  # Circle radius. Default to 2 pixels.
  circle_radius: int = 2


def _normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int,
    image_height: int) -> Union[None, Tuple[int, int]]:
  """Converts normalized value pair to pixel coordinates."""

  # Checks if the float value is between 0 and 1.
  def is_valid_normalized_value(value: float) -> bool:
    return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                      math.isclose(1, value))

  if not (is_valid_normalized_value(normalized_x) and
          is_valid_normalized_value(normalized_y)):
    # TODO: Draw coordinates even if it's outside of the image bounds.
    return None
  x_px = min(math.floor(normalized_x * image_width), image_width - 1)
  y_px = min(math.floor(normalized_y * image_height), image_height - 1)
  return x_px, y_px


def draw_detection(
    image: np.ndarray,
    detection: detection_pb2.Detection,
    keypoint_drawing_spec: DrawingSpec = DrawingSpec(color=RED_COLOR),
    bbox_drawing_spec: DrawingSpec = DrawingSpec()):
  """Draws the detction bounding box and keypoints on the image.

  Args:
    image: A three channel BGR image represented as numpy ndarray.
    detection: A detection proto message to be annotated on the image.
    keypoint_drawing_spec: A DrawingSpec object that specifies the keypoints'
      drawing settings such as color, line thickness, and circle radius.
    bbox_drawing_spec: A DrawingSpec object that specifies the bounding box's
      drawing settings such as color and line thickness.

  Raises:
    ValueError: If one of the followings:
      a) If the input image is not three channel BGR.
      b) If the location data is not relative data.
  """
  if not detection.location_data:
    return
  if image.shape[2] != _BGR_CHANNELS:
    raise ValueError('Input image must contain three channel bgr data.')
  image_rows, image_cols, _ = image.shape

  location = detection.location_data
  if location.format != location_data_pb2.LocationData.RELATIVE_BOUNDING_BOX:
    raise ValueError(
        'LocationData must be relative for this drawing funtion to work.')
  # Draws keypoints.
  for keypoint in location.relative_keypoints:
    keypoint_px = _normalized_to_pixel_coordinates(keypoint.x, keypoint.y,
                                                   image_cols, image_rows)
    cv2.circle(image, keypoint_px, keypoint_drawing_spec.circle_radius,
               keypoint_drawing_spec.color, keypoint_drawing_spec.thickness)
  # Draws bounding box if exists.
  if not location.HasField('relative_bounding_box'):
    return
  relative_bounding_box = location.relative_bounding_box
  rect_start_point = _normalized_to_pixel_coordinates(
      relative_bounding_box.xmin, relative_bounding_box.ymin, image_cols,
      image_rows)
  rect_end_point = _normalized_to_pixel_coordinates(
      relative_bounding_box.xmin + relative_bounding_box.width,
      relative_bounding_box.ymin + relative_bounding_box.height, image_cols,
      image_rows)
  cv2.rectangle(image, rect_start_point, rect_end_point,
                bbox_drawing_spec.color, bbox_drawing_spec.thickness)


def draw_landmarks(
    image: np.ndarray,
    landmark_list: landmark_pb2.NormalizedLandmarkList,
    connections: Optional[List[Tuple[int, int]]] = None,
    landmark_drawing_spec: Optional[
        Union[DrawingSpec, Mapping[int, DrawingSpec]]
    ] = DrawingSpec(color=RED_COLOR),
    connection_drawing_spec: Union[
        DrawingSpec, Mapping[Tuple[int, int], DrawingSpec]
    ] = DrawingSpec(),
    is_drawing_landmarks: bool = True,
):
  """Draws the landmarks and the connections on the image.

  Args:
    image: A three channel BGR image represented as numpy ndarray.
    landmark_list: A normalized landmark list proto message to be annotated on
      the image.
    connections: A list of landmark index tuples that specifies how landmarks to
      be connected in the drawing.
    landmark_drawing_spec: Either a DrawingSpec object or a mapping from hand
      landmarks to the DrawingSpecs that specifies the landmarks' drawing
      settings such as color, line thickness, and circle radius. If this
      argument is explicitly set to None, no landmarks will be drawn.
    connection_drawing_spec: Either a DrawingSpec object or a mapping from hand
      connections to the DrawingSpecs that specifies the connections' drawing
      settings such as color and line thickness. If this argument is explicitly
      set to None, no landmark connections will be drawn.
    is_drawing_landmarks: Whether to draw landmarks. If set false, skip drawing
      landmarks, only contours will be drawed.

  Raises:
    ValueError: If one of the followings:
      a) If the input image is not three channel BGR.
      b) If any connetions contain invalid landmark index.
  """
  if not landmark_list:
    return
  if image.shape[2] != _BGR_CHANNELS:
    raise ValueError('Input image must contain three channel bgr data.')
  image_rows, image_cols, _ = image.shape
  idx_to_coordinates = {}
  for idx, landmark in enumerate(landmark_list.landmark):
    if ((landmark.HasField('visibility') and
         landmark.visibility < _VISIBILITY_THRESHOLD) or
        (landmark.HasField('presence') and
         landmark.presence < _PRESENCE_THRESHOLD)):
      continue
    landmark_px = _normalized_to_pixel_coordinates(landmark.x, landmark.y,
                                                   image_cols, image_rows)
    if landmark_px:
      idx_to_coordinates[idx] = landmark_px
  if connections:
    num_landmarks = len(landmark_list.landmark)
    # Draws the connections if the start and end landmarks are both visible.
    for connection in connections:
      start_idx = connection[0]
      end_idx = connection[1]
      if not (0 <= start_idx < num_landmarks and 0 <= end_idx < num_landmarks):
        raise ValueError(f'Landmark index is out of range. Invalid connection '
                         f'from landmark #{start_idx} to landmark #{end_idx}.')
      if start_idx in idx_to_coordinates and end_idx in idx_to_coordinates:
        drawing_spec = connection_drawing_spec[connection] if isinstance(
            connection_drawing_spec, Mapping) else connection_drawing_spec
        cv2.line(image, idx_to_coordinates[start_idx],
                 idx_to_coordinates[end_idx], drawing_spec.color,
                 drawing_spec.thickness)
  # Draws landmark points after finishing the connection lines, which is
  # aesthetically better.
  if is_drawing_landmarks and landmark_drawing_spec:
    for idx, landmark_px in idx_to_coordinates.items():
      drawing_spec = landmark_drawing_spec[idx] if isinstance(
          landmark_drawing_spec, Mapping) else landmark_drawing_spec
      # White circle border
      circle_border_radius = max(drawing_spec.circle_radius + 1,
                                 int(drawing_spec.circle_radius * 1.2))
      cv2.circle(image, landmark_px, circle_border_radius, WHITE_COLOR,
                 drawing_spec.thickness)
      # Fill color into the circle
      cv2.circle(image, landmark_px, drawing_spec.circle_radius,
                 drawing_spec.color, drawing_spec.thickness)


def draw_axis(image: np.ndarray,
              rotation: np.ndarray,
              translation: np.ndarray,
              focal_length: Tuple[float, float] = (1.0, 1.0),
              principal_point: Tuple[float, float] = (0.0, 0.0),
              axis_length: float = 0.1,
              axis_drawing_spec: DrawingSpec = DrawingSpec()):
  """Draws the 3D axis on the image.

  Args:
    image: A three channel BGR image represented as numpy ndarray.
    rotation: Rotation matrix from object to camera coordinate frame.
    translation: Translation vector from object to camera coordinate frame.
    focal_length: camera focal length along x and y directions.
    principal_point: camera principal point in x and y.
    axis_length: length of the axis in the drawing.
    axis_drawing_spec: A DrawingSpec object that specifies the xyz axis drawing
      settings such as line thickness.

  Raises:
    ValueError: If one of the followings:
      a) If the input image is not three channel BGR.
  """
  if image.shape[2] != _BGR_CHANNELS:
    raise ValueError('Input image must contain three channel bgr data.')
  image_rows, image_cols, _ = image.shape
  # Create axis points in camera coordinate frame.
  axis_world = np.float32([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
  axis_cam = np.matmul(rotation, axis_length * axis_world.T).T + translation
  x = axis_cam[..., 0]
  y = axis_cam[..., 1]
  z = axis_cam[..., 2]
  # Project 3D points to NDC space.
  fx, fy = focal_length
  px, py = principal_point
  x_ndc = np.clip(-fx * x / (z + 1e-5) + px, -1., 1.)
  y_ndc = np.clip(-fy * y / (z + 1e-5) + py, -1., 1.)
  # Convert from NDC space to image space.
  x_im = np.int32((1 + x_ndc) * 0.5 * image_cols)
  y_im = np.int32((1 - y_ndc) * 0.5 * image_rows)
  # Draw xyz axis on the image.
  origin = (x_im[0], y_im[0])
  x_axis = (x_im[1], y_im[1])
  y_axis = (x_im[2], y_im[2])
  z_axis = (x_im[3], y_im[3])
  cv2.arrowedLine(image, origin, x_axis, RED_COLOR, axis_drawing_spec.thickness)
  cv2.arrowedLine(image, origin, y_axis, GREEN_COLOR,
                  axis_drawing_spec.thickness)
  cv2.arrowedLine(image, origin, z_axis, BLUE_COLOR,
                  axis_drawing_spec.thickness)


def _normalize_color(color):
  return tuple(v / 255. for v in color)


def plot_landmarks(iteration, landmark_list: landmark_pb2.NormalizedLandmarkList,
                   connections: Optional[List[Tuple[int, int]]] = None,
                   landmark_drawing_spec: DrawingSpec = DrawingSpec(
                       color=RED_COLOR, thickness=5),
                   connection_drawing_spec: DrawingSpec = DrawingSpec(
                       color=BLACK_COLOR, thickness=5),
                   elevation: int = 10,
                   azimuth: int = 10):
  """Plot the landmarks and the connections in matplotlib 3d.

  Args:
    landmark_list: A normalized landmark list proto message to be plotted.
    connections: A list of landmark index tuples that specifies how landmarks to
      be connected.
    landmark_drawing_spec: A DrawingSpec object that specifies the landmarks'
      drawing settings such as color and line thickness.
    connection_drawing_spec: A DrawingSpec object that specifies the
      connections' drawing settings such as color and line thickness.
    elevation: The elevation from which to view the plot.
    azimuth: the azimuth angle to rotate the plot.

  Raises:
    ValueError: If any connection contains an invalid landmark index.
  """
  if not landmark_list:
    return
  plt.figure(figsize=(10, 10))
  ax = plt.axes(projection='3d')
  ax.view_init(elev=elevation, azim=azimuth)
  plotted_landmarks = {}
  for idx, landmark in enumerate(landmark_list.landmark):
    if ((landmark.HasField('visibility') and
         landmark.visibility < _VISIBILITY_THRESHOLD) or
        (landmark.HasField('presence') and
         landmark.presence < _PRESENCE_THRESHOLD)):
      continue
    ax.scatter3D(
        xs=[-landmark.z],
        ys=[landmark.x],
        zs=[-landmark.y],
        color=_normalize_color(landmark_drawing_spec.color[::-1]),
        linewidth=landmark_drawing_spec.thickness)
    plotted_landmarks[idx] = (-landmark.z, landmark.x, -landmark.y)
  if connections:
    num_landmarks = len(landmark_list.landmark)
    # Draws the connections if the start and end landmarks are both visible.
    for connection in connections:
      start_idx = connection[0]
      end_idx = connection[1]
      if not (0 <= start_idx < num_landmarks and 0 <= end_idx < num_landmarks):
        raise ValueError(f'Landmark index is out of range. Invalid connection '
                         f'from landmark #{start_idx} to landmark #{end_idx}.')
      if start_idx in plotted_landmarks and end_idx in plotted_landmarks:
        landmark_pair = [
            plotted_landmarks[start_idx], plotted_landmarks[end_idx]
        ]
        ax.plot3D(
            xs=[landmark_pair[0][0], landmark_pair[1][0]],
            ys=[landmark_pair[0][1], landmark_pair[1][1]],
            zs=[landmark_pair[0][2], landmark_pair[1][2]],
            color=_normalize_color(connection_drawing_spec.color[::-1]),
            linewidth=connection_drawing_spec.thickness)
   # Set custom axis limits for a wider view
  ax.set_xlim([-1, 1])  # Adjust the limits as necessary
  ax.set_ylim([-1, 1])  # Adjust the limits as necessary
  ax.set_zlim([-1, 1])  # Adjust the limits as necessary
  plt.savefig(f"plot{iteration}.png")
  plt.close()
  # plt.show()



def calibrate_position(value):
  if value < 1:
    return -1.938 * 1 / value
  else:
    return 0.04238 * 1 / value


def angles(u, v):
  return np.arccos(u.dot(v)/(np.linalg.norm(u)*np.linalg.norm(v)))

def baseball(frame_toplam=250,
            ball_box=False, ball_line=False, ball_slowmotion=False,
            bat_box=False, bat_line=False,
            glove_box=False, glove_line=False,
            pitcher_box=True, pitcher_pose=False,
            catcher_box=False, catcher_pose=False,
            hitter_box=True, hitter_pose=False,
            hitter_3d=False, catcher_3d=False, pitcher_3d=False,
            pitcher_graph=True, hitter_graph=True, catcher_graph=True,
            map_button=False, heatmap=False):

  ball_boundary_box_button = ball_box
  ball_line_draw_button = ball_line
  ball_slowmotion_button = ball_slowmotion
  bat_boundary_box_button = bat_box
  bat_line_draw_button = bat_line
  glove_boundary_box_button = glove_box
  glove_line_draw_button = glove_line
  pitcher_boundary_box_button = pitcher_box
  pitcher_pose_button = pitcher_pose
  catcher_boundary_box_button = catcher_box
  catcher_pose_button = catcher_pose
  hitter_boundary_box_button = hitter_box
  hitter_pose_button = hitter_pose
  hitter_3d_pose_button = hitter_3d
  catcher_3d_pose_button = catcher_3d
  pitcher_3d_pose_button = pitcher_3d
  pitcher_graph_button = pitcher_graph
  hitter_graph_button = hitter_graph
  catcher_graph_button = catcher_graph
  map_button = map_button
  heatmap_button = heatmap

  pct_model = tflite.Interpreter(model_path="llite_model-5486383802206912512_tflite_2025-02-01T21_50_19.528893Z_model.tflite")
  pct_model.allocate_tensors()

  input_details_pct = pct_model.get_input_details()
  output_details_pct = pct_model.get_output_details()

  ball_model = tflite.Interpreter(model_path="ball_model-1464669334965059584_tflite_2025-02-02T00_33_00.486881Z_model.tflite")
  ball_model.allocate_tensors()

  input_details_ball = ball_model.get_input_details()
  output_details_ball = ball_model.get_output_details()

  input_dtype_pct = input_details_pct[0]['dtype']
  input_dtype_ball = input_details_ball[0]['dtype']


  client = vision.ImageAnnotatorClient.from_service_account_file('acquired-subset-449614-n8-8517ee33d620.json')

  cap = cv2.VideoCapture("HomeRun2.mp4")
  frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  fps = int(cap.get(cv2.CAP_PROP_FPS))
  out = cv2.VideoWriter("output_video.mp4", cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
  map_out = cv2.VideoWriter("map_video.mp4", cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
  pose_pitcher_3d_out = cv2.VideoWriter("pose_3d_pitcher_video.mp4", cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
  pose_hitter_3d_out = cv2.VideoWriter("pose_3d_hitter_video.mp4", cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
  pose_catcher_3d_out = cv2.VideoWriter("pose_3d_catcher_video.mp4", cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
  pose_pitcher_graph_out = cv2.VideoWriter("pose_graph_pitcher_video.mp4", cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
  pose_hitter_graph_out = cv2.VideoWriter("pose_graph_hitter_video.mp4", cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
  pose_catcher_graph_out = cv2.VideoWriter("pose_graph_catcher_video.mp4", cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
  heatmap_out = cv2.VideoWriter("heatmap_video.mp4", cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
  image = np.zeros((512, 512, 3), dtype=np.uint8)

  src_pts = np.array([[0, 0], [frame_width, 0], [frame_width, frame_height * 0.75], [0, frame_height * 0.75]])
  dst_pts = np.array([[0, 0], [27.4, 0], [27.4, 27.4], [0, 27.4]])
  H, _ = cv2.findHomography(src_pts, dst_pts)


  current_time = 0.0
  frame_number = 0
  previous_positions_ball = []
  previous_positions_bat = []
  previous_positions_glove = []
  ball_position = []
  pose_worlds_pitcher = []
  connectors_pitcher = []
  pose_worlds_hitter = []
  connectors_hitter = []
  pose_worlds_catcher = []
  connectors_catcher = []

  home_plate = (27.4 / 2, 0)
  first_base = (27.4, -27.4 / 2)
  second_base = (27.4 / 2, -27.4)
  third_base = (0, -27.4 / 2)
  bases = [home_plate, first_base, second_base, third_base, home_plate]

  if pitcher_boundary_box_button or pitcher_pose_button or pitcher_3d_pose_button or pitcher_graph_button:
    mp_pose_pitcher = mp.solutions.pose
    mp_drawing_pitcher = mp.solutions.drawing_utils
    pose_pitcher = mp_pose_pitcher.Pose(static_image_mode=False, model_complexity=1)

  if catcher_boundary_box_button or catcher_pose_button or catcher_3d_pose_button or catcher_graph_button:
    mp_pose_catcher = mp.solutions.pose
    mp_drawing_catcher = mp.solutions.drawing_utils
    pose_catcher = mp_pose_catcher.Pose(static_image_mode=False, model_complexity=1)

  if hitter_boundary_box_button or hitter_pose_button or hitter_3d_pose_button or hitter_graph_button:
    mp_pose_hitter = mp.solutions.pose
    mp_drawing_hitter = mp.solutions.drawing_utils
    pose_hitter = mp_pose_hitter.Pose(static_image_mode=False, model_complexity=1)

  all_positions = []
  player_positions = []
  frame_positions = []

  scap_angles_pitcher = []
  shoulder_angles_pitcher = []
  hip_angles_pitcher = []
  scap_angles_hitter = []
  shoulder_angles_hitter = []
  hip_angles_hitter = []
  scap_angles_catcher = []
  shoulder_angles_catcher = []
  hip_angles_catcher = []

  first_motion = int(fps * 11.05)#seconds
  foot_plant = int(fps * 20.9)#seconds
  release = int(fps * 21.63)#seconds

  conversion = 1/fps  # 1 second / 240 frames
  Motion_Time = (release - first_motion) * conversion # seconds
  Stride_Time = (foot_plant - first_motion) * conversion # seconds
  Plant_To_Release = (release - foot_plant) * conversion # seconds

  while cap.isOpened():
      ret, frame = cap.read()
      if not ret:
          break
      frame_number += 1
      if frame_number >= frame_toplam:
        break
      _, encoded_image = cv2.imencode('.png', frame)
      content = encoded_image.tobytes()
      image = vision.Image(content=content)
      response = client.object_localization(image=image)
      results = response.localized_object_annotations

      if ball_boundary_box_button or ball_line_draw_button or ball_slowmotion_button:
        if input_dtype_ball == np.uint8:
            image_input_ball = np.expand_dims(frame, axis=0).astype(np.uint8)
        else:
            image_input_ball = np.expand_dims(frame, axis=0).astype(np.float32) / 255.0


        input_shape = input_details_ball[0]['shape']

        image_input_ball = cv2.resize(image_input_ball[0], (input_shape[2], input_shape[1]))
        image_input_ball = np.expand_dims(image_input_ball, axis=0)

        ball_model.set_tensor(input_details_ball[0]['index'], image_input_ball)
        ball_model.invoke()

        boxes = ball_model.get_tensor(output_details_ball[0]['index'])[0]
        classes = ball_model.get_tensor(output_details_ball[1]['index'])[0]
        scores = ball_model.get_tensor(output_details_ball[2]['index'])[0]


        for box, classs, score in zip(boxes, classes, scores):
            y_min, x_min, y_max, x_max = box
            x_min, y_min, x_max, y_max = int(x_min * frame_width), int(y_min * frame_height), int(x_max * frame_width), int(y_max * frame_height)

            if ball_line_draw_button:
                for i in range(1, len(previous_positions_ball)):
                  cv2.line(frame, previous_positions_ball[i - 1], previous_positions_ball[i], (0, 255, 0), 2)

            if score > 0.50:
                x_center_ball = int((x_min + x_max) / 2)
                y_center_ball = int((y_min + y_max) / 2)
                ball_position.append((frame_number + 100, y_center_ball))
                previous_positions_ball.append((x_center_ball, y_center_ball))

                if ball_boundary_box_button:

                  label = f"ID: Ball"
                  cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                  cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                if ball_slowmotion_button:
                  label = f"MPH: 100, Angle: 12"
                  cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                  out.write(frame)
                  out.write(frame)



      if heatmap_button or map_button:
        for result in results:
          vertices_human = result.bounding_poly.normalized_vertices
          points_human = [(int(v.x * frame_width), int(v.y * frame_height)) for v in vertices_human]
          x_min, y_min, x_max, y_max = points_human[0][0], points_human[0][1], points_human[2][0], points_human[2][1]
          class_id = result.name
          confidence = float(result.score)

          if confidence > 0.50 and class_id == 'Person':
              label = f"ID: {class_id}"
              cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
              cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

              area = (x_max - x_min) * (y_max - y_min)
              calibration = area / 6600
              y1_calibrated = y_min + calibrate_position(calibration)
              y2_calibrated = y_max + calibrate_position(calibration)

              center_x_calibrated, center_y_calibrated = (x_min + x_max) / 2, (y1_calibrated + y2_calibrated) / 2

              real_world_coords = cv2.perspectiveTransform(
                  np.array([[[center_x_calibrated, center_y_calibrated]]], dtype=np.float32), H
              )
              all_positions.append(real_world_coords[0][0])
              frame_positions.append(real_world_coords[0][0])
        player_positions.append(all_positions)

        if map_button:
          plt.figure(figsize=(8, 8))

          home_plate = (27.4 / 2, 0)
          first_base = (27.4, -27.4 / 2)
          second_base = (27.4 / 2, -27.4)
          third_base = (0, -27.4 / 2)
          bases = [home_plate, first_base, second_base, third_base, home_plate]

          plt.plot([point[0] for point in bases], [point[1] for point in bases], color='green', linestyle='-', linewidth=2, label="Field Lines")
          plt.scatter(
              [pos[0] for pos in frame_positions],
              [-pos[1] for pos in frame_positions],
              color='red', label="Players", s=100, edgecolors='black'
          )
          plt.gca().get_xaxis().set_visible(False)
          plt.gca().get_yaxis().set_visible(False)

          plt.axis("equal")

          temp_image_map_path = f"temp_frame_map{frame_number}.png"
          plt.savefig(temp_image_map_path)
          plt.close()

          graph_map_frame = cv2.imread(temp_image_map_path)
          resized_graph_map = cv2.resize(graph_map_frame, (frame_width, frame_height))
          map_out.write(resized_graph_map)
          os.remove(temp_image_map_path)

        if heatmap_button:
          if player_positions:
            heatmap_data = np.zeros((35, 35))
            for pos in all_positions:
                  x_idx = min(int(pos[0] + 5), 35)
                  y_idx = int(pos[1])
                  if y_idx > 35 / 2:
                    y_idx = int(-pos[1] - 2)
                  else:
                    y_idx = int(-pos[1] - 2)

                  heatmap_data[y_idx, x_idx] += 1

          offset = 5
          home_plate = (25 / 2 + offset, offset)
          first_base = (25 + offset, 25 / 2 + offset)
          second_base = (25 / 2 + offset, 25 + offset)
          third_base = (offset, 25 / 2 + offset)
          bases = [home_plate, first_base, second_base, third_base, home_plate]
          norm = mcolors.PowerNorm(gamma=0.3)
          extent = [0, heatmap_data.shape[1], 0, heatmap_data.shape[0]]
          plt.imshow(heatmap_data, cmap='jet', interpolation='gaussian', origin='lower', aspect='equal', norm=norm, extent=extent)
          plt.plot([point[0] for point in bases], [point[1] for point in bases], color='white', linestyle='-', linewidth=2, label="Field Lines")
          plt.gca().get_xaxis().set_visible(False)
          plt.gca().get_yaxis().set_visible(False)
          plt.axis("equal")

          temp_image_heatmap_path = f"temp_frame_heatmap_{frame_number}.png"
          plt.savefig(temp_image_heatmap_path)
          plt.close()

          graph_heatmap_frame = cv2.imread(temp_image_heatmap_path)
          resized_graph_heatmap = cv2.resize(graph_heatmap_frame, (frame_width, frame_height))
          heatmap_out.write(resized_graph_heatmap)
          os.remove(temp_image_heatmap_path)

      if pitcher_boundary_box_button or pitcher_pose_button or catcher_boundary_box_button or catcher_pose_button or hitter_boundary_box_button or hitter_pose_button or catcher_3d_pose_button or hitter_3d_pose_button or pitcher_3d_pose_button:
        if input_dtype_pct == np.uint8:
            image_input = np.expand_dims(frame, axis=0).astype(np.uint8)
        else:
            image_input = np.expand_dims(frame, axis=0).astype(np.float32) / 255.0

        input_shape = input_details_pct[0]['shape']

        image_input = cv2.resize(image_input[0], (input_shape[2], input_shape[1]))
        image_input = np.expand_dims(image_input, axis=0)

        pct_model.set_tensor(input_details_pct[0]['index'], image_input)
        pct_model.invoke()

        boxes = pct_model.get_tensor(output_details_pct[0]['index'])[0]
        classes = pct_model.get_tensor(output_details_pct[1]['index'])[0]
        scores = pct_model.get_tensor(output_details_pct[2]['index'])[0]


        for box, classs, score in zip(boxes, classes, scores):
            y_min, x_min, y_max, x_max = box
            x_min, y_min, x_max, y_max = int(x_min * frame_width), int(y_min * frame_height), int(x_max * frame_width), int(y_max * frame_height)

            if pitcher_boundary_box_button or pitcher_pose_button or pitcher_3d_pose_button or pitcher_graph_button:
              if  int(classs) == 1 and score > 0.50:
                if pitcher_boundary_box_button:
                  label = f"ID: Pitcher"
                  cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                  cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                if pitcher_pose_button or pitcher_3d_pose_button or pitcher_graph_button:
                  roi = frame[y_min:y_max, x_min:x_max]
                  roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                  results_pose_pitcher = pose_pitcher.process(roi_rgb)
                  landmarks_pitcher = []
                  if results_pose_pitcher.pose_landmarks:
                      mp_drawing_pitcher.draw_landmarks(
                          roi,
                          results_pose_pitcher.pose_landmarks,
                          mp_pose_pitcher.POSE_CONNECTIONS,
                          mp_drawing_pitcher.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                          mp_drawing_pitcher.DrawingSpec(color=(66, 66, 245), thickness=2, circle_radius=2)
                      )

                      if pitcher_3d_pose_button:
                        for landmark in results_pose_pitcher.pose_landmarks.landmark:
                          landmarks_pitcher.append((int(landmark.x * frame_width), int(landmark.y * frame_height),
                                            (landmark.z * frame_width)))

                  if pitcher_graph_button:
                    if results_pose_pitcher.pose_landmarks:
                          for landmark in results_pose_pitcher.pose_landmarks.landmark:
                                  landmarks_pitcher.append((int(landmark.x * frame_width), int(landmark.y * frame_height),
                                                    (landmark.z * frame_width)))

                                  r_s = np.array([results_pose_pitcher.pose_landmarks.landmark[12].x, results_pose_pitcher.pose_landmarks.landmark[12].z])
                                  l_s = np.array([results_pose_pitcher.pose_landmarks.landmark[11].x, results_pose_pitcher.pose_landmarks.landmark[11].z])  # Left Shoulder
                                  r_e = np.array([results_pose_pitcher.pose_landmarks.landmark[14].x, results_pose_pitcher.pose_landmarks.landmark[14].z])  # Right Elbow

                                  u_temp = r_s - l_s # Creating first vector of origin to left shoulder
                                  v = r_e - l_s # Creating second vector of origin to right elbow
                                  u = np.array([-u_temp[1],u_temp[0]]) # Rotating u vector 90 degrees for simpler math

                                  scap_angles_pitcher.append(math.degrees(angles(u,v))-90) # Getting the Angle from a single frame and adjusting for rotation

                                  r_h = np.array([results_pose_pitcher.pose_landmarks.landmark[23].x,results_pose_pitcher.pose_landmarks.landmark[23].z]) # Right Hip
                                  l_h = np.array([results_pose_pitcher.pose_landmarks.landmark[24].x,results_pose_pitcher.pose_landmarks.landmark[24].z]) # Left Hip

                                  u = l_h - r_h # Creating first vector of right hip to left hip
                                  v = np.array([1,0]) # Creating second vector of origin to right elbow

                                  hip_angles_pitcher.append(math.degrees(angles(u,v))-90) # Getting the Angle from a single frame

                                  u = r_s - l_s # Creating first vector of origin to left shoulder
                                  v = np.array([1,0]) # Creating second vector of origin to right elbow

                                  shoulder_angles_pitcher.append(math.degrees(angles(u,v))-90) # Getting the Angle from a single frame

                          try:
                            plt.plot(np.arange(0,len(scap_angles_pitcher)),scap_angles_pitcher, label = "Scap Angle", c = 'r')
                            plt.plot(np.arange(0,len(shoulder_angles_pitcher)),shoulder_angles_pitcher, label = "Shoulder Angle", c = 'blue')
                            plt.plot(np.arange(0,len(hip_angles_pitcher)),hip_angles_pitcher, label = 'Hip Angle', c = 'orange')

                            plt.axvline(first_motion,label = 'Start of Motion', c = 'purple')
                            plt.axvline(foot_plant,label = 'Foot Plant', c = 'green')
                            plt.axvline(release,label = 'Release', c = 'black')

                            plt.xlabel("Frame")
                            plt.ylabel("Respective Degrees")
                            plt.title("Pitch Metric Vizualization")
                            plt.grid()
                            plt.legend()
                          except:
                            pass

                          temp_image_pitcher_path = f"temp_frame_pitcher{frame_number}.png"
                          plt.savefig(temp_image_pitcher_path)
                          plt.close()

                          graph_pitcher_frame = cv2.imread(temp_image_pitcher_path)
                          resized_graph_pitcher = cv2.resize(graph_pitcher_frame, (frame_width, frame_height))  # Videoya uygun boyuta getir
                          pose_pitcher_graph_out.write(resized_graph_pitcher)
                          os.remove(temp_image_pitcher_path)

                  if pitcher_3d_pose_button:
                    plot_landmarks(frame_number, results_pose_pitcher.pose_world_landmarks, mp_pose_pitcher.POSE_CONNECTIONS)
                    temp_image_pitcher_3d_path = f"plot{frame_number}.png"

                    graph_pitcher_3d_frame = cv2.imread(temp_image_pitcher_3d_path)
                    try:
                      resized_graph_pitcher_3d = cv2.resize(graph_pitcher_3d_frame, (frame_width, frame_height))
                    except:
                      break
                    pose_pitcher_3d_out.write(resized_graph_pitcher_3d)
                    os.remove(temp_image_pitcher_3d_path)
                  frame[y_min:y_max, x_min:x_max] = roi


            if catcher_boundary_box_button or catcher_pose_button or catcher_3d_pose_button or catcher_graph_button:
              if  int(classs) == 2 and score > 0.50:
                if catcher_boundary_box_button:
                  label = f"ID: Catcher"
                  cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                  cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                if catcher_pose_button or catcher_3d_pose_button or catcher_graph_button:
                  roi = frame[y_min:y_max, x_min:x_max]
                  roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                  results_pose_catcher = pose_catcher.process(roi_rgb)
                  landmarks_catcher = []

                  if results_pose_catcher.pose_landmarks:
                      mp_drawing_catcher.draw_landmarks(
                          roi,
                          results_pose_catcher.pose_landmarks,
                          mp_pose_catcher.POSE_CONNECTIONS,
                          mp_drawing_catcher.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                          mp_drawing_catcher.DrawingSpec(color=(66, 66, 245), thickness=2, circle_radius=2)
                      )
                      if catcher_3d_pose_button:
                        for landmark in results_pose_catcher.pose_landmarks.landmark:
                          landmarks_catcher.append((int(landmark.x * frame_width), int(landmark.y * frame_height),
                                            (landmark.z * frame_width)))

                  if catcher_graph_button:
                    if results_pose_catcher.pose_landmarks:
                          for landmark in results_pose_catcher.pose_landmarks.landmark:
                                  landmarks_catcher.append((int(landmark.x * frame_width), int(landmark.y * frame_height),
                                                    (landmark.z * frame_width)))

                                  r_s = np.array([results_pose_catcher.pose_landmarks.landmark[12].x, results_pose_catcher.pose_landmarks.landmark[12].z])
                                  l_s = np.array([results_pose_catcher.pose_landmarks.landmark[11].x, results_pose_catcher.pose_landmarks.landmark[11].z])  # Left Shoulder
                                  r_e = np.array([results_pose_catcher.pose_landmarks.landmark[14].x, results_pose_catcher.pose_landmarks.landmark[14].z])  # Right Elbow

                                  u_temp = r_s - l_s # Creating first vector of origin to left shoulder
                                  v = r_e - l_s # Creating second vector of origin to right elbow
                                  u = np.array([-u_temp[1],u_temp[0]]) # Rotating u vector 90 degrees for simpler math

                                  scap_angles_catcher.append(math.degrees(angles(u,v))-90) # Getting the Angle from a single frame and adjusting for rotation

                                  r_h = np.array([results_pose_catcher.pose_landmarks.landmark[23].x,results_pose_catcher.pose_landmarks.landmark[23].z]) # Right Hip
                                  l_h = np.array([results_pose_catcher.pose_landmarks.landmark[24].x,results_pose_catcher.pose_landmarks.landmark[24].z]) # Left Hip

                                  u = l_h - r_h # Creating first vector of right hip to left hip
                                  v = np.array([1,0]) # Creating second vector of origin to right elbow

                                  hip_angles_catcher.append(math.degrees(angles(u,v))-90) # Getting the Angle from a single frame

                                  u = r_s - l_s # Creating first vector of origin to left shoulder
                                  v = np.array([1,0]) # Creating second vector of origin to right elbow

                                  shoulder_angles_catcher.append(math.degrees(angles(u,v))-90) # Getting the Angle from a single frame

                          try:
                            plt.plot(np.arange(0,len(scap_angles_catcher)),scap_angles_catcher, label = "Scap Angle", c = 'r')
                            plt.plot(np.arange(0,len(shoulder_angles_catcher)),shoulder_angles_catcher, label = "Shoulder Angle", c = 'blue')
                            plt.plot(np.arange(0,len(hip_angles_catcher)),hip_angles_catcher, label = 'Hip Angle', c = 'orange')

                            plt.axvline(first_motion,label = 'Start of Motion', c = 'purple')
                            plt.axvline(foot_plant,label = 'Foot Plant', c = 'green')
                            plt.axvline(release,label = 'Release', c = 'black')

                            plt.xlabel("Frame")
                            plt.ylabel("Respective Degrees")
                            plt.title("Catch Metric Vizualization")
                            plt.grid()
                            plt.legend()

                          except:
                            pass

                          temp_image_catcher_path = f"temp_frame_catcher{frame_number}.png"
                          plt.savefig(temp_image_catcher_path)
                          plt.close()

                          graph_catcher_frame = cv2.imread(temp_image_catcher_path)
                          resized_graph_catcher = cv2.resize(graph_catcher_frame, (frame_width, frame_height))  # Videoya uygun boyuta getir
                          pose_catcher_graph_out.write(resized_graph_catcher)
                          os.remove(temp_image_catcher_path)

                  if catcher_3d_pose_button:
                    plot_landmarks(frame_number, results_pose_catcher.pose_world_landmarks, mp_pose_catcher.POSE_CONNECTIONS)
                    temp_image_catcher_3d_path = f"plot{frame_number}.png"

                    graph_catcher_3d_frame = cv2.imread(temp_image_catcher_3d_path)
                    try:
                      resized_graph_catcher_3d = cv2.resize(graph_catcher_3d_frame, (frame_width, frame_height))
                    except:
                      break
                    pose_catcher_3d_out.write(resized_graph_catcher_3d)
                    os.remove(temp_image_catcher_3d_path)
                  frame[y_min:y_max, x_min:x_max] = roi

            if hitter_boundary_box_button or hitter_pose_button or hitter_3d_pose_button or hitter_graph_button:
              if  int(classs) == 0 and score > 0.50:
                if hitter_boundary_box_button:
                  label = f"ID: Hitter"
                  cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                  cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                if hitter_pose_button or hitter_3d_pose_button or hitter_graph_button:
                  roi = frame[y_min:y_max, x_min:x_max]
                  roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                  results_pose_hitter = pose_hitter.process(roi_rgb)
                  landmarks_hitter = []

                  if results_pose_hitter.pose_landmarks:
                      mp_drawing_hitter.draw_landmarks(
                          roi,
                          results_pose_hitter.pose_landmarks,
                          mp_pose_hitter.POSE_CONNECTIONS,
                          mp_drawing_hitter.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                          mp_drawing_hitter.DrawingSpec(color=(66, 66, 245), thickness=2, circle_radius=2)
                      )
                      if hitter_3d_pose_button:
                        for landmark in results_pose_hitter.pose_landmarks.landmark:
                          landmarks_hitter.append((int(landmark.x * frame_width), int(landmark.y * frame_height),
                                            (landmark.z * frame_width)))

                  if hitter_graph_button:
                    if results_pose_hitter.pose_landmarks:
                          for landmark in results_pose_hitter.pose_landmarks.landmark:
                                  landmarks_hitter.append((int(landmark.x * frame_width), int(landmark.y * frame_height),
                                                    (landmark.z * frame_width)))

                                  r_s = np.array([results_pose_hitter.pose_landmarks.landmark[12].x, results_pose_hitter.pose_landmarks.landmark[12].z])
                                  l_s = np.array([results_pose_hitter.pose_landmarks.landmark[11].x, results_pose_hitter.pose_landmarks.landmark[11].z])  # Left Shoulder
                                  r_e = np.array([results_pose_hitter.pose_landmarks.landmark[14].x, results_pose_hitter.pose_landmarks.landmark[14].z])  # Right Elbow

                                  u_temp = r_s - l_s # Creating first vector of origin to left shoulder
                                  v = r_e - l_s # Creating second vector of origin to right elbow
                                  u = np.array([-u_temp[1],u_temp[0]]) # Rotating u vector 90 degrees for simpler math

                                  scap_angles_hitter.append(math.degrees(angles(u,v))-90) # Getting the Angle from a single frame and adjusting for rotation

                                  r_h = np.array([results_pose_hitter.pose_landmarks.landmark[23].x,results_pose_hitter.pose_landmarks.landmark[23].z]) # Right Hip
                                  l_h = np.array([results_pose_hitter.pose_landmarks.landmark[24].x,results_pose_hitter.pose_landmarks.landmark[24].z]) # Left Hip

                                  u = l_h - r_h # Creating first vector of right hip to left hip
                                  v = np.array([1,0]) # Creating second vector of origin to right elbow

                                  hip_angles_hitter.append(math.degrees(angles(u,v))-90) # Getting the Angle from a single frame

                                  u = r_s - l_s # Creating first vector of origin to left shoulder
                                  v = np.array([1,0]) # Creating second vector of origin to right elbow

                                  shoulder_angles_hitter.append(math.degrees(angles(u,v))-90) # Getting the Angle from a single frame

                          try:
                            plt.plot(np.arange(0,len(scap_angles_hitter)),scap_angles_hitter, label = "Scap Angle", c = 'r')
                            plt.plot(np.arange(0,len(shoulder_angles_hitter)),shoulder_angles_hitter, label = "Shoulder Angle", c = 'blue')
                            plt.plot(np.arange(0,len(hip_angles_hitter)),hip_angles_hitter, label = 'Hip Angle', c = 'orange')

                            plt.axvline(first_motion,label = 'Start of Motion', c = 'purple')
                            plt.axvline(foot_plant,label = 'Foot Plant', c = 'green')
                            plt.axvline(release,label = 'Release', c = 'black')

                            plt.xlabel("Frame")
                            plt.ylabel("Respective Degrees")
                            plt.title("Hit Metric Vizualization")
                            plt.grid()
                            plt.legend()
                          except:
                            pass

                          temp_image_hitter_path = f"temp_frame_hitter{frame_number}.png"
                          plt.savefig(temp_image_hitter_path)
                          plt.close()

                          graph_hitter_frame = cv2.imread(temp_image_hitter_path)
                          resized_graph_hitter = cv2.resize(graph_hitter_frame, (frame_width, frame_height))  # Videoya uygun boyuta getir
                          pose_hitter_graph_out.write(resized_graph_hitter)
                          os.remove(temp_image_hitter_path)

                  if hitter_3d_pose_button:
                    plot_landmarks(frame_number, results_pose_hitter.pose_world_landmarks, mp_pose_hitter.POSE_CONNECTIONS)
                    temp_image_hitter_3d_path = f"plot{frame_number}.png"

                    graph_hitter_3d_frame = cv2.imread(temp_image_hitter_3d_path)
                    try:
                      resized_graph_hitter_3d = cv2.resize(graph_hitter_3d_frame, (frame_width, frame_height))
                    except:
                      break
                    pose_hitter_3d_out.write(resized_graph_hitter_3d)
                    os.remove(temp_image_hitter_3d_path)
                  frame[y_min:y_max, x_min:x_max] = roi


      if bat_boundary_box_button or bat_line_draw_button:
        for result in results:
          vertices_bat = result.bounding_poly.normalized_vertices
          points_bat = [(int(v.x * frame_width), int(v.y * frame_height)) for v in vertices_bat]
          x_min, y_min, x_max, y_max = points_bat[0][0], points_bat[0][1], points_bat[2][0], points_bat[2][1]
          class_id = result.name
          confidence = float(result.score)
          if bat_line_draw_button:
            for i in range(1, len(previous_positions_bat)):
              cv2.line(frame, previous_positions_bat[i - 1], previous_positions_bat[i], (0, 255, 0), 2)

          if confidence > 0.5 and class_id == "Baseball bat":
            x_center_bat = int((x_min + x_max) / 2)
            y_center_bat = int((y_min + y_max) / 2)
            ball_position.append((frame_number, y_center_bat))
            previous_positions_bat.append((x_center_bat, y_center_bat))

            if bat_boundary_box_button:
              label = f"ID: Bat"
              cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
              cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

      if glove_boundary_box_button or glove_line_draw_button:
        for result in results:
          vertices_glove = result.bounding_poly.normalized_vertices
          points_glove = [(int(v.x * frame_width), int(v.y * frame_height)) for v in vertices_glove]
          x_min, y_min, x_max, y_max = points_glove[0][0], points_glove[0][1], points_glove[2][0], points_glove[2][1]
          class_id = result.name
          confidence = float(result.score)

          if glove_line_draw_button:
            for i in range(1, len(previous_positions_glove)):
              cv2.line(frame, previous_positions_glove[i - 1], previous_positions_glove[i], (0, 255, 0), 2)

          if confidence > 0.5 and class_id == "Baseball glove":
            x_center_glove = int((x_min + x_max) / 2)
            y_center_glove = int((y_min + y_max) / 2)
            ball_position.append((frame_number, y_center_glove))
            previous_positions_glove.append((x_center_glove, y_center_glove))

            if glove_boundary_box_button:
              label = f"ID: Glove"
              cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
              cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

      current_time += 1 / fps
      out.write(frame)

  cap.release()
  map_out.release()
  out.release()
  pose_pitcher_3d_out.release()
  pose_hitter_3d_out.release()
  pose_catcher_3d_out.release()
  pose_pitcher_graph_out.release()
  pose_catcher_graph_out.release()
  pose_hitter_graph_out.release()
  heatmap_out.release()
  cv2.destroyAllWindows()