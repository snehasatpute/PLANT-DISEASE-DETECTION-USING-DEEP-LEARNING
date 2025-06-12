# PLANT-DISEASE-DETECTION-USING-DEEP-LEARNING

1.Model Setup Instructions
  To use this project, you need to download a pre-trained model from the given Google Drive link and place it in the models     directory. Follow the steps below to set it up correctly:

2.Steps to Download and Place the Model
  Download the Model

3.Click here to open the Google Drive link.
  Click the Download button to save the file to your local system.
  Create the Models Folder

4.Navigate to the root directory of this project.
  Create a folder named models if it does not already exist.
  mkdir models
  Place the Model in the Folder

5.Move the downloaded file into the models directory.
  mv /path/to/downloaded/model models/
  Replace /path/to/downloaded/model with the actual path where you downloaded the file.
  Verify the Setup

6.Ensure that the model file is correctly placed in the models directory by listing the folder's contents:
  ls models
  You should see the downloaded model file in the output.
  Usage
  Specify the Model File Location

7.Open the app.py file in a text editor.
  Locate line 8, which contains the following code:
  tf.keras.models.load_model("")
  Update the empty string with the relative path to the model file. For example:
  tf.keras.models.load_model("models/your_model_file.keras")
  Replace your_model_file.keras with the actual name of the model file you downloaded.
  Run the Server

8.Open a terminal and navigate to the root directory of this project.
  Run the following command to start the server:
  python app.py
  Access the Application

9.Once the server is running, follow the instructions displayed in the terminal to access the application in your web browser
