import face_recognition
import os
import cv2
import pandas


KNOWN_FACES_DIR = 'known_faces'
UNKNOWN_FACES_DIR = 'unknown_faces'
TOLERANCE = 0.55  # its defines the tolerance of face matching Lower the tolerance more the accuracy. Range in float from 0 to 1.
FRAME_THICKNESS = 2  #Thickness of frame drawn on face
FONT_THICKNESS = 2   
MODEL = 'hog'  # It is the model selection point. 'hog' is default , 'cnn' can be uses but it works better with CUDA acceleration. 

# Returns (R, G, B) from name
def name_to_color(name):
    # Take 3 first letters, tolower()
    # lowercased character ord() value rage is 97 to 122, substract 97, multiply by 8
    color = [(ord(c.lower())-97)*8 for c in name[:3]]
    return color

# Function to capture image and video.
def pic_capture():
    camera = cv2.VideoCapture(0)
    print("Press q key to validate your identity.")
    while(camera.isOpened()):
        

        return_value, image = camera.read()
        cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #cv2.destroyAllWindows()
            break

    return_value, image = camera.read()
    cv2.imwrite('unknown_faces/opencv.png', image)
    #if i <= 18:
     #   os.remove('unknown_faces/opencv.png')

    del(camera)
    

# It does the work of loading faces in known_faces directort and encoding them.

print('Loading known faces...')
known_faces = []
known_names = []

# We oranize known faces as subfolders of KNOWN_FACES_DIR
# Each subfolder's name becomes our label (name)
for name in os.listdir(KNOWN_FACES_DIR):

    # Next we load every file of faces of known person
    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
        print(filename)

        # Load an image
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')

        # Get 128-dimension face encoding
        # Always returns a list of found faces, for this purpose we take first face only (assuming one face per image as you can't be twice on one image)
        encoding = face_recognition.face_encodings(image)[0]

        # Append encodings and name
        known_faces.append(encoding)
        known_names.append(name)

     

# check if picture is availabe in unknown_faces directory.
def itemava():

    listitems = os.listdir('unknown_faces') # dir is your directory path
    number_files = len(listitems)
    if number_files > 0:
        flag = "Y"
    else:
        flag = "N"
    return flag


# Function to process the caputerd image and recognasing faces.
def processimage():
    print('Processing unknown faces...')
    for filename in os.listdir(UNKNOWN_FACES_DIR):

    # Load image
        print(f'Filename {filename}', end='')
        image = face_recognition.load_image_file(f'{UNKNOWN_FACES_DIR}/{filename}')
        print(filename)
    # This time we first grab face locations - we'll need them to draw boxes
        locations = face_recognition.face_locations(image, model=MODEL)

    # Now since we know loctions, we can pass them to face_encodings as second argument
    # Without that it will search for faces once again slowing down whole process
        encodings = face_recognition.face_encodings(image, locations)

    # We passed our image through face_locations and face_encodings, so we can modify it
    # First we need to convert it from RGB to BGR as we are going to work with cv2
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # But this time we assume that there might be more faces in an image - we can find faces of dirrerent people
        print(f', found {len(encodings)} face(s)')
        for face_encoding, face_location in zip(encodings, locations):

        # We use compare_faces (but might use face_distance as well)
        # Returns array of True/False values in order of passed known_faces
            results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

        # Since order is being preserved, we check if any face was found then grab index
        # then label (name) of first matching known face withing a tolerance
            match = None
            if True in results:  # If at least one is true, get a name of first of found labels
                match = known_names[results.index(True)]
                print(f' - {match} from {results}')

            # Each location contains positions in order: top, right, bottom, left
                top_left = (face_location[3] - 3, face_location[0] - 3)
                bottom_right = (face_location[1] + 3, face_location[2] + 3)

            # Get color by name using our fancy function
                color = name_to_color(match)

            # Paint frame
                cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

            # Now we need smaller, filled grame below for a name
            # This time we use bottom in both corners - to start from bottom and move 50 pixels down
                top_left = (face_location[3] - 10 , face_location[2])
                bottom_right = (face_location[1] + 10, face_location[2] + 22 )

            # Paint frame
                cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)

            # Wite a name
                cv2.putText(image, match, (face_location[3] , face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)

    # Show image
        cv2.imshow('frame', image)
        cv2.waitKey(2000)
        cv2.destroyWindow(filename)
        if len(encodings) == 1:

            return match
        else:
            return None


# Its the main function also read the csv file which have ACCESS GRANT LIST either the preson is granted or not. 
def main():
    
    
    if flagg == "Y":
        match = processimage()
        accesslist = pandas.read_csv("accesslist.csv")
        names = accesslist["Name"].tolist()
        access = accesslist["Acess"].tolist()
        
        if match in names:
            index_loc = names.index(match)
            if access[index_loc] == 'Y':   
                print("Acess Granted.")
            elif access[index_loc] == 'N':
                print("Acess Not Granted.")         
        
    else:
        sett = True
        while sett ==True:

            print("No image found in directory.")
            
            input(" Press enter to try again")
            
            res = itemava()
            if res == "Y":
                processimage()
                sett = False
            else:
                print('Error -')
                    
# use to loop over again and again.        
par = True                
while par==True:
    
    pic_capture()            
    flagg = itemava()
    main()

    



