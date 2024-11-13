
# DevNet2
This is the second Dev Net Project
Benjamin Haddad, Carter Hickerson, Henry Gates


Our model is stored in a python utilizing the torch extension as a neural network builder
We trained our project on a 
To Run the code you must use a computer on the csu network, in order to access the website, and give controls (chmod 755) to the files in the project folder
Once this is done you can change the images in the uploads folder to match the images you would like to test.

Our Model was trained on 
Our standardizer uses images from Pillow (the python image package) to look a specified image_path using the filePath and gives it three color channels (RGB)
Then we convert the image to an array using Numpy (np.array) in order to be able to standardize the images with numbers only
The clip function done to the array means each individual pixel must be between zero and one to not give any crazy result while being smoothed.
This data is then converted back to type Image (as defined by Pillow) and sent to the model "setup.py" for analyzation

