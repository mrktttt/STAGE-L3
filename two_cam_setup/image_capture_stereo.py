import cv2 as cv
import numpy as np
import os 
import sys

def capture_image_stereo(file_path1, file_path2, id_cam1, id_cam2):

    """
    FR: 
    Capture en simultané d'une image à partir des deux caméras pour la calibration stéréo.
    Ces images sont enregistrées dans des dossiers séparés pour chaque caméra.

    EN: 
    Simultaneous capture of an image from both cameras for stereo calibration.
    These images are saved in separate folders for each camera.

    Parameters: 
        file_path1: The path to the folder of images for the first cam.
        file_path2: The path to the folder of images for the second cam.
        id_cam1: The ID of the first camera.
        id_cam2: The ID of the second camera.
    Returns:
        None
    """
    # Initialisation des caméras
    # Initializing the cameras
    cap1 = cv.VideoCapture(id_cam1)
    cap2 = cv.VideoCapture(id_cam2)

    # Tuple des caméras pour permettre d'appliquer des paramètres communs facilement.
    # Tuple of cameras to allow easy application of common parameters.
    caps = [cap1, cap2]

    # Changement de la résolution à celle que nous allons utiliser ensuite.
    # Changing the resolution to the one we will be using next. 
    frame_shape = [720, 1280]

    # Définir la résolution des caméras
    # Set the resolution of the cameras
    for cap in caps:
        cap.set(3, frame_shape[1])
        cap.set(4, frame_shape[0])

    # Créer les dossiers pour stocker les images de calibration
    # Create folders to store calibration images
    if not os.path.exists(file_path1):
        os.makedirs(file_path1)
    if not os.path.exists(file_path2):
        os.makedirs(file_path2)

    img_counter = 0

    print("Appuyez sur ESPACE pour capturer une image, 'q' pour quitter")
    print("Capturez au moins 10-20 images de l'échiquier sous différents angles")

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        # Dans le cas où les caméras ne sont pas accessibles.
        # In case the cameras are not accessible.
        if not ret1 or not ret2:
            break

        # Redimensionner les images en 720x720.
        # Crop to 720x720.
        if frame1.shape[1] != 720:
            frame1 = frame1[:, frame_shape[1] // 2 - frame_shape[0] // 2: frame_shape[1] // 2 + frame_shape[0] // 2]
        
        if frame2.shape[1] != 720:
            frame2 = frame2[:, frame_shape[1] // 2 - frame_shape[0] // 2: frame_shape[1] // 2 + frame_shape[0] // 2]

        # Ajouter des labels sur chaque frame
        # Add labels on each frame
        cv.putText(frame1, "Camera 0", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv.putText(frame2, "Camera 1", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Affichage côte à côte des deux caméras
        # Display side by side of the two cameras
        combined_frame = np.hstack((frame1, frame2))

        cv.imshow('Capture - Appuyez sur ESPACE pour capturer', combined_frame)

        key = cv.waitKey(1) & 0xFF

        # Si la touche espace est pressée, sauvegarder les images
        # If the space key is pressed, save the images
        if key == ord(' '):
            img_name1 = f"{file_path1}/img_{img_counter:02d}.png"
            img_name2 = f"{file_path2}/img_{img_counter:02d}.png"
            cv.imwrite(img_name1, frame1)
            cv.imwrite(img_name2, frame2)
            print(f"Images sauvegardées: {img_name1} et {img_name2}")
            img_counter += 1

        # Si la touche 'q' est pressée, quitter la boucle
        # If the 'q' key is pressed, exit the loop
        elif key == ord('q'): 
            break

    cv.destroyAllWindows()
    for cap in caps:
        cap.release()

    print(f"Capture terminée. {img_counter} images sauvegardées dans {file_path1} et {file_path2}.")

if __name__ == "__main__":

    if len(sys.argv) == 5:
        file_path1 = sys.argv[1]
        file_path2 = sys.argv[2]
        id_cam1 = int(sys.argv[3])
        id_cam2 = int(sys.argv[4])

        capture_image_stereo(file_path1, file_path2, id_cam1, id_cam2)
    
    else:
        print("Erreur dans l'utilisation des arguments.")
        print("Utilisation: python3 image_capture_stereo.py <chemin_dossier_cam1> <chemin_dossier_cam2> <id_cam1> <id_cam2>")