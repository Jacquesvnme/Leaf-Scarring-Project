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

        #STARTS IMAGE ARRAY
        counter = DBObj.rowCount()
        data = DBObj.ImagePaths()
        arr = []
        
        # Added change
        if len(data) != 0 :
            for i in range(counter):
                arr.append(data[i][0])
            
            self.images = arr  #IMAGES STORED AS STRINGS/FILE PATHS
        
        # Samples Image Preview section
        self.sample_label = QLabel(self)
        self.sample_label.setText("Samples:")
        self.sample_label.setAlignment(Qt.AlignLeft)
        self.sample_label.setGeometry(20, 20, 500, 300)
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
        self.image_preview_area.setGeometry(40, 60, 460, 240)
        self.image_preview_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.image_preview_area.setSelectionMode(QListWidget.SingleSelection)
        self.image_preview_area.setStyleSheet("""
            QListWidget {
                background-color: rgb(250, 250, 250);
                border-radius: 10px;
            }
        """)
        self.image_preview_area.itemClicked.connect(self.update_individual_stats)
        # Added change
        self.refresh_image_preview()
        
        # IMAGE PREVIEW SECTION
        self.image_preview_label = QLabel(self)
        self.image_preview_label.setText("Preview:")
        self.image_preview_label.setAlignment(Qt.AlignLeft)
        self.image_preview_label.setGeometry(20, 340, 500, 320)
        self.image_preview_label.setStyleSheet("""
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
        
        # IMAGE PREVIEW
        self.image_preview_image = QLabel(self)
        image_path = './assets/images/placeholder.jpg'
        pixmap = QPixmap(image_path)
        self.image_preview_image.setGeometry(40, 380, 500, 250)
        pixmap_resized = pixmap.scaled(200, 260, Qt.KeepAspectRatio)
        self.image_preview_image.setPixmap(pixmap_resized)
        
        # IMAGE SCARRING PREVIEW
        self.image_scarring_preview = QLabel(self)
        image_path = './assets/images/placeholder.jpg'
        pixmap2 = QPixmap(image_path)
        self.image_scarring_preview.setGeometry(300, 380, 500, 250)
        pixmap2_resized = pixmap2.scaled(200, 260, Qt.KeepAspectRatio)
        self.image_scarring_preview.setPixmap(pixmap2_resized)
        
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
        # Added change
        self.display_stats_average(self.avg_results_area)
        # Added change
        self.display_stats_individual(self.imageResults_area)
        
        
        
        #SAVE DATA BUTTON
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
        self.save_button.clicked.connect(self.show_Save)
        
        
        
        #INSTRUCTIONS / HELP  BUTTON
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
    
        self.refresh_button = QPushButton(self)
        self.refresh_button.setGeometry(1090, 20, 50, 50)
        self.refresh_button.setStyleSheet("""
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
        icon = QIcon("./assets/images/refresh.png") 
        self.refresh_button.setIcon(icon)
        self.refresh_button.setIconSize(QSize(44, 44))
        self.refresh_button.clicked.connect(self.refresh_image_preview)
        self.refresh_button.clicked.connect(self.update_average_stats)
    
    #REFRESHES IMAGE PREVIEW AREA    
    def refresh_image_preview(self):
        counter = DBObj.rowCount()
        data = DBObj.ImagePaths()
        self.images = [data[i][0] for i in range(counter)]
        # Clear and repopulate the image preview area
        self.image_preview_area.clear()
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
                    pathID = DBObj.getPathID(image_name)
                    DBObj.deleteImageNameCollection(pathID)
            self.refresh_image_preview()
            self.display_stats_average(self.avg_results_area)
            self.display_stats_individual(self.imageResults_area)

    #TITLES AND FIELDS FOR SHOWING STATS
    #Loads and populates individual picture results
    def create_stats_grid_individual(self):
        grid_layout_average = QGridLayout()
        
        selected_items = self.image_preview_area.selectedItems()    #get current selected image, if any
        if selected_items:
            image_path = selected_items[0].text()
            path_id = DBObj.getPathID(image_path)

            pixmap = QPixmap(image_path)
            pixmap_resized = pixmap.scaled(200, 260, Qt.KeepAspectRatio)
            self.image_preview_image.setPixmap(pixmap_resized)
            
            fileFirstCut = image_path.rfind("/") + 1
            fileSecondCut = image_path.rfind(".")
            captionName = image_path[fileFirstCut:fileSecondCut]
            
            pixmap2 = QPixmap(f"./assets/output/images/ContourScan_{captionName}.jpg")
            pixmap2_resized = pixmap2.scaled(200, 260, Qt.KeepAspectRatio)
            self.image_scarring_preview.setPixmap(pixmap2_resized)
            
            if path_id:
                stats_data = DBObj.getIndividualStatsCollection(path_id[0][0])  #gets stats via dbhandler
                
                if stats_data:
                    stats = [
                        ("Leaf Area", 0, 0),
                        ("Scarred Area", 1, 0),
                        ("Percentage Damage", 2, 0),
                        ("Number of Scars", 3, 0),
                        ("Length of Leaf", 4, 0),
                        ("Width of Leaf", 5, 0),
                        (f"{round(stats_data[0], 4)} cm<sup>2</sup>", 0, 1),  # lamina_area
                        (f"{round(stats_data[4], 4)} cm<sup>2</sup>", 1, 1),  # scar_area
                        (f"{round(stats_data[5], 4)} %", 2, 1),                 # damagepercentage
                        (f"{round(stats_data[3], 4)}", 3, 1),                 # scar_count
                        (f"{round(stats_data[1], 4)} cm", 4, 1),              # lamina_length
                        (f"{round(stats_data[2], 4)} cm", 5, 1)               # lamina_width
                    ]

                else:
                    stats = self.get_placeholder_stats()
            else:
                stats = self.get_placeholder_stats()
        else:
            stats = self.get_placeholder_stats()

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
    
    def get_placeholder_stats(self):
        #Return placeholder stats when no image is selected or data is unavailable
        return [
            ("Leaf Area", 0, 0),
            ("Scarred Area", 1, 0),
            ("Percentage Damage", 2, 0),
            ("Number of Scars", 3, 0),
            ("Length of Leaf", 4, 0),
            ("Width of Leaf", 5, 0),
            ("- cm²", 0, 1),
            ("- cm²", 1, 1),
            ("-", 2, 1),
            ("-", 3, 1),
            ("- cm", 4, 1),
            ("- cm", 5, 1)
        ]
    
    #Updates individual stats grid when image is clicked
    def update_individual_stats(self, item):
        self.display_stats_individual(self.imageResults_area)

    # Load title & data for Stats Average Side
    def create_stats_grid_average(self):
        grid_layout_average = QGridLayout()

        # Labels for each stat field
        
        # Added Change
        stat1 = DBObj.LeafArea()
        stat2 = DBObj.ScarArea()
        stat3 = DBObj.PercentageDamage()
        stat4 = DBObj.ScarsCount()
        stat5 = DBObj.LaminaLength()
        stat6 = DBObj.LaminaWidth()
        
        if stat1 == None or stat2 == None or stat3 == None or stat4 == None or stat5 == None or stat6 == None:
            stat1 = 0
            stat2 = 0
            stat3 = 0
            stat4 = 0
            stat5 = 0
            stat6 = 0
        
        stats = [
            ("Leaf Area", 0, 0),
            ("Scarred Area", 1, 0),
            ("Percentage Damage", 2, 0),
            ("Number of Scars", 3, 0),
            ("Length of Leaf", 4, 0),
            ("Width of Leaf", 5, 0),
            (f"{round(stat1,4)} cm<sup>2</sup>", 0, 1),
            (f"{round(stat2,4)} cm<sup>2</sup>", 1, 1),
            (f"{round(stat3,4)} %", 2, 1),
            (f"{round(stat4,4)}", 3, 1),
            (f"{round(stat5,4)} cm", 4, 1),
            (f"{round(stat6,4)} cm", 5, 1)
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

    def update_average_stats(self, item):
        self.display_stats_average(self.avg_results_area)

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
            "<h3>Instructions for Output Page:</h3>"
            "<p>Click on the images of the sample(s) you wish to remove.<br>"
            "   (if none are needed skip to step 3)</p>"
            "<p>Click on the 'Remove selected' button to remove images from the dataset.</p>"
            "<p>Click on the 'Save Data' button to save the data as an CSV file.</p>"
            "<p>Use the 'Home' button to navigate back to the main screen.</p>"
        )
        QMessageBox.information(self, "Instructions", instructions)