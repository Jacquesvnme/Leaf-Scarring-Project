import sys
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QWidget, QMessageBox, QFileDialog, QListWidget, QVBoxLayout, QLineEdit,
    QDateEdit, QListWidgetItem, QStackedWidget, QTableWidget, QTableWidgetItem, QScrollArea, QHeaderView,
    QWidget, QGridLayout)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush, QIcon
from PyQt5.QtCore import Qt, QDate, QSize

import psycopg2
from psycopg2 import sql

from database import DBHandler as DBObj

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
        #self.add_data_to_db()
        
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

    def open_image_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg)")
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            for file_path in file_paths:
                self.add_image_thumbnail(file_path)

    def add_image_thumbnail(self, file_path):
        pixmap = QPixmap(file_path)
        thumbnail = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        fileFirstCut = file_path.rfind("/") + 1
        fileSecondCut = file_path.find(".")
        captionName = file_path[fileFirstCut:fileSecondCut]

        item = QListWidgetItem(QIcon(thumbnail), f"{captionName}")
        self.image_preview_area.addItem(item)

        
    """def add_data_to_db(self):
        imagelocation = self.location_input.text()
        imagedate = self.date_input.date().toString("yyyy-mm-dd")        
        
        #data1 = generate_imagedata_id() #function to make a new imagedataID, based on the newest imagedataID + 1#
        data2 = imagelocation
        data3 = imagedate
                
        for image_path in self.get_image_paths():
            data4 = FTObj.image_path
            data5 = FTObj. image_path
            
            data = (
                #data1,
                data2,
                data3,
                data4,
                data5,
                FTObj.labeled_resized_leaf.get('image_label', ''),  # Label if available
                FTObj.leaf_area_cm2.get('lamina_area', 0),
                FTObj.leaf_length_cm.get('lamina_length', 0),
                FTObj.leaf_width_cm.get('lamina_width', 0),
                #count.get('scar_count', 0),
                FTObj.scar_area_cm2.get('scar_area', 0),
                FTObj.damage_percentage.get('damage_percentage', 0),
                #.get('petiole_length', 0)
            )        
            # Insert data into the database
            DBObj.insertCollection(*data)"""
            
    #CREATES POP-UP WITH INSTRUCTIONS WIP
    def show_instructions(self):
        instructions = (
            "Instructions for New Sample Page:\n\n"
            "1. Use the 'Add Images' button to upload image files (.png, .jpg).\n"
            "2. Fill out the location and date fields.\n"
            "3. Click 'Next' to proceed to the next step.\n"
            "4. Use the 'Home' button to navigate back to the main screen"
        )
        QMessageBox.information(self, "Instructions", instructions)