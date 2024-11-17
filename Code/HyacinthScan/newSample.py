import sys
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QWidget, QMessageBox, QFileDialog, QListWidget, QVBoxLayout, QLineEdit,
    QDateEdit, QListWidgetItem, QStackedWidget, QTableWidget, QTableWidgetItem, QScrollArea, QHeaderView,
    QWidget, QGridLayout, QListView)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush, QIcon
from PyQt5.QtCore import Qt, QDate, QSize

import psycopg2
from psycopg2 import sql

from database import DBHandler as DBObj
from sections import NewData as DataValidation 

counter = 0
labelNames = []
filePath = []

#NEW SAMPLE PAGE
class NewSamplePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Samples Image Preview section
        self.sample_label = QLabel(self)
        self.sample_label.setText("Samples:")
        self.sample_label.setAlignment(Qt.AlignLeft)
        self.sample_label.setGeometry(20, 20, 720, 640)
        self.sample_label.setStyleSheet("""
            QLabel {
                background-color: qlineargradient(spread:pad, x1:0.474459, y1:1, x2:0.476, y2:0, stop:0 rgba(167, 210, 167, 230), stop:0.813312 rgba(255, 255, 255, 200));
                border-radius: 10px;                
                border: 2px solid rgba(255, 255, 255, 0.4);
                padding: 10px;
                color: #000000;
                font-family: 'Inter';
                font-style: italic;
                font-weight: 600;
                font-size: 20px;
                line-height: 36px;
            }
        """)
        self.image_preview_area = QListWidget(self)
        self.image_preview_area.setGeometry(40, 60, 680, 580)
        self.image_preview_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.image_preview_area.setViewMode(QListView.IconMode)         # Set to Icon Mode
        self.image_preview_area.setIconSize(QSize(150, 150))            # Set larger icon size for thumbnails
        self.image_preview_area.setSpacing(10)                          # Add spacing between icons
        self.image_preview_area.setResizeMode(QListWidget.Adjust)       # Adjust layout to fit contents
        self.image_preview_area.setStyleSheet("""
            QListWidget {
                background-color: rgb(250, 250, 250);
                border-radius: 10px;
            }
        """)

        #ADD IMAGE BUTTON
        #ON CLICK OPENS WINDOWS ADD IMAGE POP-UP
        self.add_image_button = QPushButton('Add Images', self)
        self.add_image_button.setFont(QFont('Inter', 20))
        self.add_image_button.setGeometry(20, 680, 720, 60)
        self.add_image_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: #000000;
                }                           
        """)
        self.add_image_button.clicked.connect(self.open_image_dialog)

        #DATA INPUT SECTION
        self.dataInput_label = QLabel(self)
        self.dataInput_label.setGeometry(800, 90, 460, 570)
        self.dataInput_label.setAlignment(Qt.AlignLeft)        
        self.dataInput_label.setText("Please input the relevant data below:")
        self.dataInput_label.setStyleSheet("""
            QLabel {
                background-color: qlineargradient(spread:pad, x1:0.474459, y1:1, x2:0.476, y2:0, stop:0 rgba(167, 210, 167, 230), stop:0.813312 rgba(255, 255, 255, 200));
                border-radius: 10px;                
                border: 2px solid rgba(255, 255, 255, 0.4);
                padding: 10px;
                color: #000000;
                font-family: 'Inter';
                font-style: italic;
                font-weight: 400;
                font-size: 20px;
            }
        """)
        
        #LOCATION
        self.location_label = QLabel(self)
        self.location_label.setGeometry(820, 130, 400, 30)
        self.location_label.setText("Location:")
        self.location_label.setStyleSheet("""
            QLabel {
                font-family: 'Inter';
                font-style: none;
                font-weight: 400;
                font-size: 15px;
            }
        """)
        self.location_input = QLineEdit(self)
        self.location_input.setGeometry(820, 160, 400, 40)
        self.location_input.setPlaceholderText("Enter Location") 
        
        #DATE
        self.date_label = QLabel(self)
        self.date_label.setGeometry(820, 210, 400, 30)
        self.date_label.setText("Date:")
        self.date_label.setStyleSheet("""
            QLabel {
                font-family: 'Inter';
                font-style: none;
                font-weight: 400;
                font-size: 15px;
            }
        """)
        self.date_input = QDateEdit(self)
        self.date_input.setGeometry(820, 240, 400, 40)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        #NEXT BUTTON
        #ON CLICK GOES TO NEXT PAGE AND ADDS DATA TO DB
        self.next_button = QPushButton('Next', self)
        self.next_button.setFont(QFont('Inter', 20))
        self.next_button.setGeometry(800, 680, 460, 60) 
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: #000000;
                }                           
        """)
        self.next_button.clicked.connect(self.add_data_to_db)
        
        #INSTRUCTIONS BUTTON
        self.instructions_button = QPushButton(self)
        self.instructions_button.setGeometry(1210, 20, 50, 50)
        self.instructions_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)
        icon = QIcon("./assets/images/book_icon.png")
        self.instructions_button.setIcon(icon)
        self.instructions_button.setIconSize(QSize(44, 44))
        self.instructions_button.clicked.connect(self.show_instructions)
        
        #HOME BUTTON
        self.home_button = QPushButton(self)
        self.home_button.setGeometry(1150, 20, 50, 50)
        self.home_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)
        icon = QIcon("./assets/images/home_icon.png")
        self.home_button.setIcon(icon)
        self.home_button.setIconSize(QSize(44, 44))

    

    def addCounter(self):
        global counter
        counter += 1

    def addImageLabel(self,data):
        global labelNames
        labelNames.append(data)

    def addImagePath(self,data):
        global filePath
        filePath.append(data)

    def open_image_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg)")
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            for file_path in file_paths:
                self.addCounter()
                
                path_length = len(file_path)
                cut = file_path.find("/assets")
                custom_file_path = f".{file_path[cut:path_length]}"
                self.addImagePath(custom_file_path)
                
                fileFirstCut = file_path.rfind("/") + 1
                fileSecondCut = file_path.find(".")
                captionName = file_path[fileFirstCut:fileSecondCut]
                labelNames.append(captionName)
                
                reply = self.imageName(captionName)
                self.add_image_thumbnail(file_path, reply)

    def add_image_thumbnail(self, file_path, reply):
        pixmap = QPixmap(file_path)
        thumbnail = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        fileFirstCut = file_path.rfind("/") + 1
        fileSecondCut = file_path.find(".")
        captionName = file_path[fileFirstCut:fileSecondCut]
        self.addImageLabel(captionName)
        
        if (reply == 65536):
            end = "back"
        elif (reply == 16384):
            end = "front"

        item = QListWidgetItem(QIcon(thumbnail), f"{captionName}_{end}")
        self.image_preview_area.addItem(item)

    def add_data_to_db(self):
        image_ID = DBObj.selectID()[0][0]
        imagelocation = self.location_input.text()
        imagedate = self.date_input.date().toString("yyyy-MM-dd") 

        
        if counter == 0:
            QMessageBox.information(self, "Error Message", "Image must be imported")
        elif imagelocation == "" or imagelocation == None:
            QMessageBox.information(self, "Error Message", "Location must be entered")
        elif imagedate == "" or imagedate == None:
            QMessageBox.information(self, "Error Message", "Date must be entered")
        else:
            for i in range(counter):
                image_ID += 1
                arr = DataValidation.analyse_image(filePath[i]);
                
                if ( arr["lamina_area"] == "" or arr["lamina_area"] == None or
                    arr["lamina_length"] == "" or arr["lamina_length"] == None or
                    arr["lamina_width"] == "" or arr["lamina_width"] == None or
                    arr["scar_count"] == "" or arr["scar_count"] == None or
                    arr["scar_area"] == "" or arr["scar_area"] == None or
                    arr["damagepercentage"] == "" or arr["damagepercentage"] == None ):
                    QMessageBox.information(self, "Error Message", "Image Processing Failed")
                else:
                    try:
                        DBObj.insertCollection(image_ID,imagelocation,imagedate,image_ID,image_ID,filePath[i],image_ID,image_ID,labelNames[i],arr["lamina_area"],arr["lamina_length"],arr["lamina_width"],arr["scar_count"],arr["scar_area"],arr["damagepercentage"])
                    except:
                        QMessageBox.information(self, "Error Message", "Adding to database failed")

    #CREATES POP-UP WITH INSTRUCTIONS WIP
    def show_instructions(self):
        instructions = (
            "<h3>Instructions for New Sample Page:</h3>"
            "<ol type='1'><li>Use the 'Add Images' button to upload image files (.png, .jpg).</li>"
            "<li>Follow on screen prompts and pop-ups as needed</li>"
            "<li>Fill out the location and date fields.</li>"
            "<li>Click 'Next' to proceed to the next step.</li>"
            "<li>Use the 'Home' button to navigate back to the main screen</li></ol>"
        )
        QMessageBox.information(self, "Instructions", instructions)

    def imageName(self, imageName):
        reply = QMessageBox.question(self, f"{imageName} Front or Back", "Is this the image front or back?\n" + 
                                    "Yes = Front\nNo = Back\nDefault/Exit = Back",
                                    QMessageBox.Yes | QMessageBox.No)
        return reply