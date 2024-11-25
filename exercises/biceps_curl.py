import cv2
import mediapipe as mp
import math

# Initialize MediaPipe pose
mp_pose = mp.solutions.pose

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])
    dot_product = ba[0] * bc[0] + ba[1] * bc[1]
    magnitude_ba = math.sqrt(ba[0]**2 + ba[1]**2)
    magnitude_bc = math.sqrt(bc[0]**2 + bc[1]**2)
    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0
    cos_theta = dot_product / (magnitude_ba * magnitude_bc)
    cos_theta = max(min(cos_theta, 1), -1)
    angle_radians = math.acos(cos_theta)
    return math.degrees(angle_radians)

# Function to calculate responsiveness based on elbow angle
def calculate_responsiveness(angle, min_angle=20, max_angle=150):
    if angle > max_angle:
        return 0
    elif angle < min_angle:
        return 1
    else:
        return (max_angle - angle) / (max_angle - min_angle)

# Function to draw glowing pose connections
def draw_glow_connections(image, landmarks, connections, color=(0, 0, 255), glow_strength=8):
    h, w, _ = image.shape
    overlay = image.copy()
    for connection in connections:
        start_idx, end_idx = connection
        start = landmarks[start_idx]
        end = landmarks[end_idx]
        start_point = (int(start.x * w), int(start.y * h))
        end_point = (int(end.x * w), int(end.y * h))
        for i in range(glow_strength, 0, -1):
            alpha = i / glow_strength
            thickness = i * 2
            glow_color = tuple(int(c * alpha) for c in color)
            cv2.line(overlay, start_point, end_point, glow_color, thickness)
    cv2.addWeighted(overlay, 0.5, image, 0.5, 0, image)

# Function to draw glowing circular counter
def draw_glowing_counter(image, counter, center=(60, 60), radius=30, color=(128, 128, 128), glow_color=(255, 255, 255), glow_strength=8):
    overlay = image.copy()
    for i in range(glow_strength, 0, -1):
        alpha = i / glow_strength
        thickness = radius + (glow_strength - i) * 4
        glow = tuple(int(c * alpha) for c in glow_color)
        cv2.circle(overlay, center, thickness, glow, -1)
    cv2.circle(overlay, center, radius, color, -1)
    cv2.addWeighted(overlay, 0.5, image, 0.5, 0, image)
    cv2.putText(image, str(int(counter)), (center[0] - 15, center[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

# Main function for biceps curl logic
def run_biceps_curl():
    cap = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        counter = 0
        direction = 0  # Tracks whether movement is "up" or "down"
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame. Exiting...")
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                # Draw glowing pose connections
                draw_glow_connections(frame, landmarks, mp_pose.POSE_CONNECTIONS, color=(0, 0, 255), glow_strength=8)

                h, w, _ = frame.shape
                left_shoulder = (int(landmarks[11].x * w), int(landmarks[11].y * h))
                left_elbow = (int(landmarks[13].x * w), int(landmarks[13].y * h))
                left_wrist = (int(landmarks[15].x * w), int(landmarks[15].y * h))
                left_hip = (int(landmarks[23].x * w), int(landmarks[23].y * h))

                right_shoulder = (int(landmarks[12].x * w), int(landmarks[12].y * h))
                right_elbow = (int(landmarks[14].x * w), int(landmarks[14].y * h))
                right_wrist = (int(landmarks[16].x * w), int(landmarks[16].y * h))
                right_hip = (int(landmarks[24].x * w), int(landmarks[24].y * h))

                # Calculate angles
                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                left_shoulder_angle = calculate_angle(left_hip, left_shoulder, left_elbow)
                right_shoulder_angle = calculate_angle(right_hip, right_shoulder, right_elbow)

                # Full extension condition
                if (left_elbow_angle > 150 and right_elbow_angle > 150 and 
                    left_shoulder_angle < 50 and right_shoulder_angle < 50):
                    if direction == 0:  # Transitioning to "down"
                        counter += 0.5
                        direction = 1

                # Full contraction condition
                if (left_elbow_angle < 20 and right_elbow_angle < 20 and 
                    left_shoulder_angle < 50 and right_shoulder_angle < 50):
                    if direction == 1:  # Transitioning to "up"
                        counter += 0.5
                        direction = 0

                # Draw rectangles for responsiveness
                left_responsiveness = calculate_responsiveness(right_elbow_angle)
                right_responsiveness = calculate_responsiveness(left_elbow_angle)

                left_rect_top = 200
                left_rect_bottom = 400
                left_fill_height = int(left_rect_top + (left_rect_bottom - left_rect_top) * (1 - left_responsiveness))
                cv2.rectangle(frame, (8, left_rect_top), (50, left_rect_bottom), (0, 255, 0), 5)
                cv2.rectangle(frame, (8, left_fill_height), (50, left_rect_bottom), (255, 0, 0), -1)
                cv2.putText(frame, 'L', (24, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 5)

                right_rect_top = 200
                right_rect_bottom = 400
                right_fill_height = int(right_rect_top + (right_rect_bottom - right_rect_top) * (1 - right_responsiveness))
                cv2.rectangle(frame, (582, right_rect_top), (632, right_rect_bottom), (0, 255, 0), 5)
                cv2.rectangle(frame, (582, right_fill_height), (632, right_rect_bottom), (255, 0, 0), -1)
                cv2.putText(frame, 'R', (604, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 5)

                # Draw all landmarks, highlighting specific landmarks with a green glow
                for idx, landmark in enumerate(landmarks):
                    center = (int(landmark.x * w), int(landmark.y * h))
                    # Highlight landmarks 11, 12, 13, and 14 with a green glow
                    if idx in [11, 12, 13, 14]:  # Left shoulder, right shoulder, left elbow, right elbow
                        for i in range(8, 0, -1):  # Glow effect
                            alpha = i / 8
                            thickness = i * 2
                            glow_color = (0, int(255 * alpha), 0)  # Green glow
                            cv2.circle(frame, center, thickness, glow_color, -1)
                        cv2.circle(frame, center, 5, (0, 255, 0), -1)  # Solid green for core point
                    else:
                        cv2.circle(frame, center, 5, (0, 255, 255), -1)  # Yellow for other landmarks


            # Draw the glowing counter
            draw_glowing_counter(frame, counter, center=(60, 60), radius=30, color=(128, 128, 128), glow_color=(255, 255, 255), glow_strength=10)

            cv2.imshow("Biceps Curl Exercise", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()