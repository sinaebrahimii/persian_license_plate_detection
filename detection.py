import cv2
from ultralytics import YOLO
from utils import replace_class_id,make_text
large_char_path="D:\\Code\\YOLO\\plate_char\\runs\\detect\\train\\weights\\best.pt"
nano_char_path='D:\\Code\\YOLO\\plate_char\\best_char_n.pt'
# Load YOLO models
char_model = YOLO(large_char_path)
plate_model = YOLO('D:\\Code\\YOLO\\plate_char\\best_plate.pt')

# Open the video file
video_path = "5.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create VideoWriter object to save the output
output_path = 'd_' + video_path  # Change the output file path and format if needed
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change the codec according to your system
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run plate_model inference on the frame
        plate_results = plate_model.predict(frame,conf=0.5)
        
        # Check if any plates were detected
        if len(plate_results[0].boxes) > 0:
            for box in plate_results[0].boxes:
                # Extract coordinates and convert to integers
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                
                # Draw rectangle around detected plate
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                # cv2.putText(frame, "Plate", (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (90, 255, 200), 1)
                
               

                # Crop the detected plate from the frame
                cropped_plate = frame[y1:y2, x1:x2]
                
                # Run model inference on the cropped plate

                plate_details = char_model.predict(cropped_plate,conf=0.7)
                plate_text=''
                plate_chars=[]
                # Draw rectangles around detected classes within the cropped plate
                if len(plate_details[0].boxes) > 0:
                    for plate_box in plate_details[0].boxes: 
                        px1, py1, px2, py2 = map(int, plate_box.xyxy[0]) 
                        plate_class_id = int(plate_box.cls[0]) 
                        plate_class=replace_class_id(plate_class_id)
                        plate_chars.append({'px1':px1,"class":plate_class})
                        
                        # Sort the plate_characters list based on px1
                        plate_chars.sort(key=lambda char: char["px1"])


                        # Draw red rectangle around detected class 
                        cv2.rectangle(cropped_plate, (px1, py1), (px2, py2), (200, 100, 0), 1) 
                        # Place class number slightly above the rectangle 
                        # cv2.putText(cropped_plate, plate_class, (px1, py1), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,200, 255), 1)
                        
                        #Replace the original plate region with the annotated plate
                        frame[y1:y2, x1:x2] = cropped_plate
                    if len(plate_chars)==8:
                        plate_text=make_text(plate_chars)
                    
                    # Draw rectangle around detected plate
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)


                        (text_width, text_height), baseline = cv2.getTextSize(plate_text, cv2.FONT_HERSHEY_PLAIN, 1.5, 2)
                        cv2.rectangle(frame, (x1, y1 - text_height - baseline - 10), (x1 + text_width, y1), (128, 0, 0), -1)

                        cv2.putText(frame, plate_text, (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 2)

                    # cv2.putText(frame, plate_text, (x1, y1-30), cv2.FONT_HERSHEY_PLAIN, 1.5, (240,100, 0), 2)
                

        # Save the annotated frame to the output video file
        # out.write(frame)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object, VideoWriter, and close the display window
cap.release()
out.release()
cv2.destroyAllWindows()
