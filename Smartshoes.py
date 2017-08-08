import numpy as np
import sys
import csv
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import time
import tkinter
from PIL import Image, ImageTk, ImageSequence


class Smartshoes:

    # File that contains the training data
    # Contains values for the five sensors and the class the data belongs to
    # In-Shoe Pressure Sensor values are in range (0,3) 0- Lowest 3- Highest
    # Classes: Sensor data is classified into 5 classes depending on pressure
    training_data_path ="./Ndata.csv"

    # Method to display the gif
    def gif(self,parent,gifpath):
        self.parent = parent
        self.canvas = tkinter.Canvas(parent, width= 600, height=600)
        self.canvas.pack()
        self.sequence = [ImageTk.PhotoImage(img)
                            for img in ImageSequence.Iterator(
                                Image.open(gifpath))]
        self.image  = self.canvas.create_image(250,245,image=self.sequence[0])
        self.animate(1)

    # Method to find the number of images in gif and animate
    def animate(self, counter):
        self.canvas.itemconfig(self.image,image=self.sequence[counter])
        self.parent.after(50,lambda:self.animate((counter+1) % len(self.sequence)))

    # Method to train the machine
    # Classifier used is Decision Tree Classifier
    def train(self):
        training_data = pd.read_csv(self.training_data_path)
        print("Loading data from file...\n")

        features_cols = training_data[['s1', 's2', 's3', 's4', 's5']]
        X = features_cols
        y = training_data.cls

        Dtrees = DecisionTreeClassifier()
        print("Training machine...\n")

        t1 = time.time()
        Dtrees.fit(X, y)
        t2 = time.time()

        t = t2 - t1
        print("Time taken for training: " + str(t) + " seconds\n")
        return(Dtrees)

    # Method to predict which class the new set of data belongs to and if finds if the walking pattern is normal or abnormal
    # Accepts the classifier and the 5 sensor values as parameters
    def predict(self,classifier,arr):
        result = classifier.predict(arr)
        if result == 1:
            print("\nVibrator 1 and Vibrator 2 vibrate\n")
            print("Sensor image\n")
            root = tkinter.Tk()
            self.gif(root, './gifclass/class1.gif')
            root.mainloop()
            return ('ab', '1')
        elif result == 2:
            print("\nVibrator 3 and Vibrator 4 vibrate\n")
            print("Sensor image\n")
            root = tkinter.Tk()
            self.gif(root, './gifclass/class2.gif')
            root.mainloop()
            return ('ab', '2')
        elif result == 3:
            print("\nVibrator 1 and Vibrator 3 vibrate\n")
            print("Sensor image\n")
            root = tkinter.Tk()
            self.gif(root, './gifclass/class3.gif')
            root.mainloop()
            return ('ab', '3')
        elif result == 4:
            print("\nVibrator 2 and Vibrator 4 vibrate\n")
            print("Sensor image\n")
            root = tkinter.Tk()
            self.gif(root, './gifclass/class4.gif')
            root.mainloop()
            return ('ab', '4')
        else:
            print("\nNormal Walking detected\n")
            print("Sensor image\n")
            root = tkinter.Tk()
            self.gif(root, './gifclass/class5.gif')
            root.mainloop()
            return ('nor', '5')

    # Method that updates the machine in real-time with the new data, making the machine learn continuously
    def feedbk(self,arr, cla):
        new_data_line = str(arr[0]) + "," + str(arr[1]) + "," + str(arr[2]) + "," + str(arr[3]) + "," + str(
            arr[4]) + "," + str(cla)
        try:
            with open(self.training_data_path, 'a', newline='') as csvfile:
                linewriter = csv.writer(csvfile, delimiter=' ')
                linewriter.writerow(new_data_line)
        except:
            print("Error while writing new steps into file:",sys.exc_info()[0])


    # Method that corrects the steps of the user if any abnormality is identified over time until it is corrected
    def correction(self,status, step):
        if status == 'ab':
            print("Users next step with improvement\n")
            corr = step
            a = step
            for i in range(len(a)):
                if a[i] == 3:
                    b = a[i]
                    b = b - 1
                    corr[i] = b
                elif a[i] == 0:
                    b = a[i]
                    b = b + 1
                    corr[i] = b
                elif a[i] == 1:
                    b = a[i]
                    b = b + 1
                    corr[i] = b
                else:
                    corr[i] = a[i]
            print(corr)
            status, cla = self.predict(classifier,corr)
            self.correction(status, corr)

    # Method to display the menu
    def menu(self,classifier):
        while(True):
            try:
                ch = input(
                    "Press 1 - Enter the sensor readings for the next step in the order s1 to s5 \nPress 2 - Exit \n")

                if ch == '1':
                    arr = []
                    for i in range(5):
                        sd = int(input("S" + str(i + 1) + " value:"))
                        if (sd in range(-1 and 4)):
                            arr.append(sd)
                        else:
                            print("\nInvalid Entry")
                            break
                    status, cla = self.predict(classifier, arr)
                    self.feedbk(arr, cla)
                    self.correction(status, arr)

                elif ch == '2':
                    exit()

                else:
                    print("\nInvalid entry try again!!!\n")

            except:
                print(sys.exc_info()[0])
                exit()

ss = Smartshoes()
classifier = ss.train()
ss.menu(classifier)






























