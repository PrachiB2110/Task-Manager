import cv2
import face_recognition
import pickle
import os
import time
def capture_and_store_face(user_name):
    video_capture = cv2.VideoCapture(0)

    print(f"Capturing face for {user_name}...")

    start_time = time.time()   
    face_captured = False  

    while True:
        ret, frame = video_capture.read()
        
        if not ret:
            print("Failed to capture image")
            break
        
        # Find face locations in the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # If we detect a face
        if face_locations:
            # Capture the first face found
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Save the captured face image
                cv2.imwrite(f"faces/{user_name}.jpg", frame[top:bottom, left:right])

                # Save the face encoding in the encoding file
                if not os.path.exists("face_encodings"):
                    os.makedirs("face_encodings")

                encodings_file = "face_encodings/encodings.pkl"
                if os.path.exists(encodings_file):
                    with open(encodings_file, "rb") as f:
                        face_encodings_dict = pickle.load(f)
                else:
                    face_encodings_dict = {}

                # Add the new user's face encoding to the dictionary
                face_encodings_dict[user_name] = face_encoding

                # Save the updated face encodings to the pickle file
                with open(encodings_file, "wb") as f:
                    pickle.dump(face_encodings_dict, f)

                # Mark that the face has been captured
                face_captured = True

                # Break the loop since the face has been successfully captured
                break

        # Check if we've successfully captured a face for 3 seconds
        if face_captured and time.time() - start_time > 3:
            break

    # Release the video capture and close any OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()

    if face_captured:
        print(f"Face for {user_name} captured and stored successfully.")
    else:
        print(f"No face detected for {user_name}. Please try again.")


def authenticate_face(user_name):
    encodings_file = "face_encodings/encodings.pkl"
    
    # Check if the encodings file exists
    if os.path.exists(encodings_file):
        with open(encodings_file, "rb") as f:
            face_encodings_dict = pickle.load(f)
    else:
        print("No face encodings found. Please capture a face first.")
        return False

    
    if user_name not in face_encodings_dict:
        print(f"No face found for {user_name}. Please capture a face first.")
        return False

     
    stored_encoding = face_encodings_dict[user_name]
    res = False
   
    # Start video capture
    video_capture = cv2.VideoCapture(0)

    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    start_time = time.time()
    while True:
        
        ret, frame = video_capture.read()
        
        if not ret:
            print("Failed to capture image")
            break
        
      
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
 
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
      
            

 
            matches = face_recognition.compare_faces([stored_encoding], face_encoding)

            if matches[0]:
             
                res = True
                 
                print("Authentication successful!")
                
            
                break
            else:
            
                cv2.putText(frame, "Authentication Failed", (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                print("Authentication failed.")
                 
 
        
        if  time.time() - start_time > 2:
             
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

  
    video_capture.release()
    
    print(res)
    
    return res


def main():
  
    print("Choose an option:")
    print("1: Capture face")
    print("2: Authenticate face")

    choice = input()

    if choice == "1":
        user_name = input("Enter your name: ")
        capture_and_store_face(user_name)
    elif choice == "2":
        user_name = input("Enter your name: ")
        authenticate_face(user_name)
    else:
        print("Invalid option")

if __name__ == "__main__":
    main()
