#!/usr/bin/env python3

import cgi
from base64 import b64decode
import face_recognition
import os

# Setup CGI environment
print("Content-Type: text/html")
print()

# Get form data
form = cgi.FieldStorage()
email = form.getvalue("email")
image_data = form.getvalue("current_image")

# Check if the form data was submitted
if email and image_data:
    try:
        # Decode the base64 image data
        header, encoded = image_data.split(",", 1)
        data = b64decode(encoded)

        # Save the image
        image_path = "image.png"
        with open(image_path, "wb") as f:
            f.write(data)

        # Load and compare faces
        got_image = face_recognition.load_image_file(image_path)
        existing_image_path = f"students/{email}.jpg"

        if os.path.exists(existing_image_path):
            existing_image = face_recognition.load_image_file(existing_image_path)

            got_image_facialfeatures = face_recognition.face_encodings(got_image)
            existing_image_facialfeatures = face_recognition.face_encodings(existing_image)

            if got_image_facialfeatures and existing_image_facialfeatures:
                results = face_recognition.compare_faces([existing_image_facialfeatures[0]], got_image_facialfeatures[0])
                if results[0]:
                    print("<script>alert('Welcome {}');</script>".format(email))
                else:
                    print("<script>alert('Face not recognized');</script>")
            else:
                print("<script>alert('Face encoding failed');</script>")
        else:
            print("<script>alert('No image found for the provided email');</script>")

    except Exception as e:
        print("<script>alert('An error occurred: {}');</script>".format(str(e)))
else:
    print("<script>alert('Email or image data is missing');</script>")
