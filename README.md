Home AI Fitness Tracker is a fitness application designed to provide real-time exercise tracking and feedback using advanced computer vision. With a user-friendly interface built using Tkinter and ttkbootstrap, the app supports eight exercises, offering live feedback on form and repetitions. Powered by Mediapipe, the app tracks your movements in real time, calculates angles between key body points, and provides instant feedback on your form and performance.  It ensures accurate pose estimation and responsiveness tracking, helping users achieve their fitness goals from the comfort of their homes. 


When you select an exercise, the app leverages your device’s camera to capture your movements. Mediapipe detects your body’s key points, or "landmarks"—like your shoulders, elbows, and knees. By identifying these points, the app can calculate the angles between them, which is critical for analyzing your form and determining if you're performing the exercise correctly. In each exercise, most important landmarks (landmarks included in calculations) are marked with green to separate them from other landmarks marked with yellow color. 


To calculate the angles between your joints, I was using trigonometry—specifically, the cosine rule and the arccosine function. I defined three points for example landmarks for shoulder, elbow and wrist. Than from these points we calculate two vectors. For example if points are A, B and C then vectors BA and BC are: 

BA = (Ax - Bx, Ay - By) and BC = (Cx - Bx, Cy - By). 

Then I calculated dot product between vectors using formula:
dot_product = BA[0] * BC[0] + BA[1] * BC[1]. 

Then the magnitude (length) of each vector is determined using the Pythagorean theorem:

magnitude_BA = sqrt(BA[0]**2 + BA[1]**2)
magnitude_BC = sqrt(BC[0]**2 + BC[1]**2)

Using the formula for the cosine of the angle we calculate cosine.

cos_theta = dot_product / (magnitude_BA * magnitude_BC)

Than we finally calculate the angle in degrees using the arccosine function. 

angle = degrees(acos(cos_theta))


To exit from particulary exercise (turn of your laptop or external webcam) and return to app GUI press "q" button. To exit aplication press close on the app. 

