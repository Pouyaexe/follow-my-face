use opencv::core::*;
use opencv::highgui::*;
use opencv::objdetect::*;
use opencv::prelude::*;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    // Create a cascade classifier object
    let mut face_cascade = CascadeClassifier::new()?;
    face_cascade.load("haarcascade_frontalface_default.xml")?;

    // Open the default camera
    let mut cap = VideoCapture::new(0, CAP_ANY)?;

    // Loop until the user hits the 'Esc' key
    while true {
        // Read the next frame from the camera
        let mut frame = Mat::default()?;
        cap.read(&mut frame)?;

        // Convert the frame to grayscale
        let mut gray = Mat::default()?;
        cvt_color(&frame, &mut gray, COLOR_BGR2GRAY, 0)?;

        // Detect faces in the frame
        let mut faces = VectorOfRect::new();
        face_cascade.detect_multi_scale(&gray, &mut faces, 1.1, 3, 0, Size::new(30, 30), Size::new(0, 0))?;

        // Draw a rectangle around each face
        for face in faces {
            rectangle(&mut frame, face, Scalar::new(0., 0., 0., 0.), 2, 8, 0)?;
        }

        // Show the frame
        imshow("Face Detection", &frame)?;

        // Check if the user hit the 'Esc' key
        let c = wait_key(1)?;
        if c == 27 {
            break;
        }
    }

    // Release the camera
    cap.release()?;

    Ok(())
}