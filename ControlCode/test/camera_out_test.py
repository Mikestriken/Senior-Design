import cv2, os

# Initializing webcam
cap = cv2.VideoCapture(2)

if not cap.isOpened():
            is_working = False
            print("Port is not working.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('Webcam', frame)

    # Check for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()