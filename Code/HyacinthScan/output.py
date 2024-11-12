#OUTPUT PAGE
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

class OutputPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("BCASAA")
        self.setGeometry(100, 100, 1280, 720)
        # MainWindow.set_background_image(self)

        #STARTS IMAGE ARRAY
        self.images = []  #IMAGES STORED AS STRINGS/FILE PATHS
        
        # Samples Image Preview section
        self.sample_label = QLabel(self)
        self.sample_label.setText("Samples:")
        self.sample_label.setAlignment(Qt.AlignLeft)
        self.sample_label.setGeometry(20, 20, 500, 640)
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
        self.image_preview_area.setGeometry(40, 60, 460, 580)
        self.image_preview_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.image_preview_area.setSelectionMode(QListWidget.MultiSelection)
        self.image_preview_area.setStyleSheet("""
            QListWidget {
                background-color: rgb(250, 250, 250);
                border-radius: 10px;
            }
        """)
        self.refresh_image_preview()
        
        #REMOVE SELECTED BUTTON
        self.remove_image_button = QPushButton('Remove Selected', self)
        self.remove_image_button.setFont(QFont('Inter', 20))
        self.remove_image_button.setGeometry(20, 680, 500, 60)
        self.remove_image_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)
        self.remove_image_button.clicked.connect(self.remove_selected_images)

        #INDIVIDUAL IMAGE RESULTS AREA
        
        #ADD CODE TO FETCH DATA FROM DATABASE OF SELECTED IMAGE
        #UPDATES ON IMAGE THUMBNAIL CLICK
        
        self.imageResults_label = QLabel(self)
        self.imageResults_label.setText("Individual Results:")
        self.imageResults_label.setAlignment(Qt.AlignLeft)
        self.imageResults_label.setGeometry(540, 80, 350, 580)
        self.imageResults_label.setStyleSheet("""
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
        self.imageResults_area = QScrollArea(self)
        self.imageResults_area.setGeometry(550, 120, 330, 530)
        self.imageResults_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        #AVERAGE RESULTS AREA        
        #ADD CODE TO RETRIVE COLLECTION DATA
        #ADD CODE TO AVERAGE RESULTS OF DATA7, DATA8, DATA9, DATA10, DATA11, DATA12, DATA13
        
        self.avgResults_label = QLabel(self)
        self.avgResults_label.setText("Averaged Results:")
        self.avgResults_label.setAlignment(Qt.AlignLeft)
        self.avgResults_label.setGeometry(910, 80, 350, 580)
        self.avgResults_label.setStyleSheet("""
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
        self.avg_results_area = QScrollArea(self)
        self.avg_results_area.setGeometry(920, 120, 330, 530)
        self.avg_results_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        #GRID LAYOUT FOR DATA
        self.imageResults_area.setWidgetResizable(True)
        self.avg_results_area.setWidgetResizable(True)
        self.display_stats_average(self.avg_results_area)
        self.display_stats_individual(self.imageResults_area)
        
        #SAVE DATA BUTTON
        
        #ADD CODE TO UPDATE COLLECTION
        #USE UPDATECOLLECTION FROM DBHANDLER
        #EXPORT TO CSV AS WELL
        
        self.save_button = QPushButton("Save Data", self)
        self.save_button.setFont(QFont('Inter', 20))
        self.save_button.setGeometry(910, 680, 350, 60)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)
        self.save_button.clicked.connect(self.show_Save);
        
        #INSTRUCTIONS BUTTON
        self.instructions_button = QPushButton(self)
        self.instructions_button.setGeometry#571b23
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
    
    #REFRESHES IMAGE PREVIEW AREA    
    def refresh_image_preview(self):
        self.image_preview_area.clear()  # Clear the QListWidget
        for image in self.images:
            item = QListWidgetItem(image)
            self.image_preview_area.addItem(item)

    #PROMPTS USER FOR CONFIRMATION
    def remove_selected_images(self):
        selected_items = self.image_preview_area.selectedItems()        
        if not selected_items:
            return #NO IMAGES SELECTED

        #CONFIRMATION DIALOG BOX
        confirmation = QMessageBox.question(self, 'Confirmation', 
                                            "Are you sure you want to delete the selected images?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirmation == QMessageBox.Yes:
            for item in selected_items:
                image_name = item.text()
                if image_name in self.images:
                    self.images.remove(image_name)
            self.refresh_image_preview()
            
    #TITLES AND FIELDS FOR SHOWING STATS
    # Helper function to create grid layout for stats labels
    # Helper function to create grid layout for stats labels
    
    # Load title & data for Stats Individual Side
    def create_stats_grid_individual(self):
        grid_layout_average = QGridLayout()

        # Labels for each stat field
        stats = [
            ("Leaf Area", 0, 0),
            ("Scarred Area", 1, 0),
            ("Percentage Damage", 2, 0),
            ("Number of Scars", 3, 0),
            ("Length of Leaf", 4, 0),
            ("Width of Leaf", 5, 0),
            (f"X cm<sup>2</sup>", 0, 1),
            (f"X cm<sup>2</sup>", 1, 1),
            (f"X", 2, 1),
            (f"X", 3, 1),
            (f"X cm", 4, 1),
            (f"X cm", 5, 1)
        ]

        for text, row, col in stats:
            label = QLabel(text)
            
            # Apply different styles for the second column
            if col == 1:
                label.setAlignment(Qt.AlignRight)
                label.setStyleSheet("""
                    QLabel {
                        font-family: 'Inter';
                        font-weight: 400;
                        font-size: 18px;
                    }
                """)
            else:
                label.setAlignment(Qt.AlignLeft)
                label.setStyleSheet("""
                    QLabel {
                        font-family: 'Inter';
                        font-weight: 500;
                        font-size: 18px;
                    }
                """)        
            grid_layout_average.addWidget(label, row, col)

        return grid_layout_average

    # Load title & data for Stats Average Side
    def create_stats_grid_average(self):
        grid_layout_average = QGridLayout()

        # Labels for each stat field
        stats = [
            ("Leaf Area", 0, 0),
            ("Scarred Area", 1, 0),
            ("Percentage Damage", 2, 0),
            ("Number of Scars", 3, 0),
            ("Length of Leaf", 4, 0),
            ("Width of Leaf", 5, 0),
            (f"{round(DBObj.LeafArea(),4)} cm<sup>2</sup>", 0, 1),
            (f"{round(DBObj.ScarArea(),4)} cm<sup>2</sup>", 1, 1),
            (f"{round(DBObj.PercentageDamage(),4)}", 2, 1),
            (f"{round(DBObj.ScarsCount(),4)}", 3, 1),
            (f"{round(DBObj.LaminaLength(),4)} cm", 4, 1),
            (f"{round(DBObj.LaminaWidth(),4)} cm", 5, 1)
        ]

        for text, row, col in stats:
            label = QLabel(text)
            
            # Apply different styles for the second column
            if col == 1:
                label.setAlignment(Qt.AlignRight)
                label.setStyleSheet("""
                    QLabel {
                        font-family: 'Inter';
                        font-weight: 400;
                        font-size: 18px;
                    }
                """)
            else:
                label.setAlignment(Qt.AlignLeft)
                label.setStyleSheet("""
                    QLabel {
                        font-family: 'Inter';
                        font-weight: 500;
                        font-size: 18px;
                    }
                """)        
            grid_layout_average.addWidget(label, row, col)

        return grid_layout_average

# Displays stats layout in a scroll area with a transparent background
    def display_stats_average(self, scroll_area):
        container_widget = QWidget()
        grid_layout_average = self.create_stats_grid_average()
        container_widget.setLayout(grid_layout_average)
        container_widget.setStyleSheet("background-color: transparent;")  # Set container background to transparent
        scroll_area.setWidget(container_widget)

    def display_stats_individual(self, scroll_area):
        container_widget = QWidget()
        grid_layout_individual = self.create_stats_grid_individual()
        container_widget.setLayout(grid_layout_individual)
        container_widget.setStyleSheet("background-color: transparent;")  # Set container background to transparent
        scroll_area.setWidget(container_widget)
    
    def show_Save(self):
        instructions = (
            "Data Saved to output file located at\n" +
            "./assets/images/output.csv"
        )
        QMessageBox.information(self, "Data Saved", instructions)
        DBObj.SaveProcess()
    
    #CREATES POP-UP WITH INSTRUCTIONS WIP
    def show_instructions(self):
        instructions = (
            "Instructions for Output Page:\n\n"
            "1. Click on the images of the sample(s) you wish to remove.\n"
            "   (if none are needed skip to step 3)\n"
            "2. Click on the 'Remove selected' button to remove images from the dataset.\n"
            "3. Click on the 'Save Data' button to save the data as an Excel file\n"
            "4. Use the 'Home' button to navigate back to the main screen"
        )
        QMessageBox.information(self, "Instructions", instructions)