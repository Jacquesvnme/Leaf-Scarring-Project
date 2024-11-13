"""Pip installs needed: PyQT5, psycopg2, openCV"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QWidget, QMessageBox, QFileDialog, QListWidget, QVBoxLayout, QLineEdit,
    QDateEdit, QListWidgetItem, QStackedWidget, QTableWidget, QTableWidgetItem, QScrollArea, QHeaderView,
    QWidget, QGridLayout)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush, QIcon
from PyQt5.QtCore import Qt, QDate, QSize

import psycopg2
from psycopg2 import sql

import DBHandler as DBObj

#import FilteringTest as FTObj

#import count.ipynb

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BCASAA")
        self.setGeometry(100, 100, 1300, 780)
        self.stacked_widget = QStackedWidget(self)

        #CREATE PAGES
        self.main_page = MainPage(self)
        self.new_sample_page = NewSamplePage(self)
        self.data_review_page = DataReviewPage(self)
        self.output_page = OutputPage(self)

        #ADD TO STACK
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.new_sample_page)
        self.stacked_widget.addWidget(self.data_review_page)
        self.stacked_widget.addWidget(self.output_page)

        # Set layout to hold the stacked widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        #BUTTONS FOR NAVIGATION        
        self.main_page.new_sample_button.clicked.connect(self.show_new_sample_page)
        self.main_page.data_review_button.clicked.connect(self.show_data_review_page)
        self.new_sample_page.home_button.clicked.connect(self.show_main_page)
        self.new_sample_page.next_button.clicked.connect(self.show_output_page)
        self.data_review_page.home_button.clicked.connect(self.show_main_page)
        self.data_review_page.next_button.clicked.connect(self.show_output_page)
        self.output_page.home_button.clicked.connect(self.show_main_page)

    def show_main_page(self):
        self.stacked_widget.setCurrentWidget(self.main_page)

    def show_new_sample_page(self):
        self.stacked_widget.setCurrentWidget(self.new_sample_page)
        
    def show_data_review_page(self):
        self.stacked_widget.setCurrentWidget(self.data_review_page)
        
    def show_output_page(self):
        self.stacked_widget.setCurrentWidget(self.output_page)
        
    def set_background_image(self):
        palette = QPalette()
        background = QPixmap("./Images/BG.jpg")
        scaled_background = background.scaled(QSize(1280, 720), Qt.KeepAspectRatioByExpanding)
        palette.setBrush(QPalette.Background, QBrush(scaled_background))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

#HOME PAGE
class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(20, 20, 1280, 720)  #SETS SIZE OF APPLICATION
        MainWindow.set_background_image(self)
        
        #MAIN TITLE
        self.title_label = QLabel(self)
        self.title_label.setText("Welcome to the BioControl Agent\n"+
                                 "Statistical Analysis Application")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setGeometry(100, 70, 1080, 300)
        self.title_label.setStyleSheet("""
            QLabel {
                font-family: 'Inter';
                font-style: italic;
                font-weight: 600;
                font-size: 50px;
                line-height: 80px;
                text-align: center;
                color: #000000;
            }
        """)
        
        #NEW SAMPLE BUTTON
        self.new_sample_button = QPushButton('New Sample', self)
        self.new_sample_button.setFont(QFont('Inter', 35))
        self.new_sample_button.setGeometry(250, 360, 300, 100)
        self.new_sample_button.setStyleSheet("""
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

        #DATA REVIEW BUTTON
        self.data_review_button = QPushButton('Data Review', self)
        self.data_review_button.setFont(QFont('Inter', 35))
        self.data_review_button.setGeometry(700, 360, 300, 100)
        self.data_review_button.setStyleSheet("""
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
        icon = QIcon("./Images/book_icon.png")
        self.instructions_button.setIcon(icon)
        self.instructions_button.setIconSize(QSize(44,44))
        self.instructions_button.clicked.connect(self.show_instructions)

        #CREDITS SECTION
        self.credit_label = QLabel(self)
        self.credit_label.setText(
            "<h2 style='font-size: 22px;'>Credits:</h2>"
            "<p style='font-size: 20px;'>"
            "D Giovannoni - Project Supervisor<br>"
            "Dr. K English - Project Sponsor<br>"
            "Belgium ITversity, RSA Center of Biological Control, Rhodes University, US</p>\n"
            "<p style='font-size: 18px;'>H Holl, H Roux, H Reddy, J v Niekerk, J Pretorius, JA Mentz</p>"
        )
        self.credit_label.setFont(QFont('Inter', 20))
        self.credit_label.setAlignment(Qt.AlignCenter)
        self.credit_label.setGeometry(20, 520, 1240, 220)
        self.credit_label.setStyleSheet("""
            QLabel {
                background-color: qlineargradient(spread:pad, x1:0.474459, y1:1, x2:0.476, y2:0, stop:0 rgba(167, 210, 167, 230), stop:0.813312 rgba(255, 255, 255, 200));
                border-radius: 10px;
                border: 2px solid rgba(255, 255, 255, 0.4);
                color: #000000;
                font-family: 'Inter';
                font-style: normal;
                font-weight: 400;
                font-size: 20px;
                line-height: 36px;
                text-align: center;
            }
        """)
        self.credit_label.setWordWrap(True)

    #CREATES POP-UP WITH INSTRUCTIONS WIP
    def show_instructions(self):
        instructions = (
            "Instructions for Using the Application:\n\n"
            "1. Click 'New Sample' to input new data samples.\n"
            "2. Click 'Data Review' to review existing data and analysis.\n"
            "3. Credits are listed at the bottom for project contributors."
        )
        QMessageBox.information(self, "Instructions", instructions)

#NEW SAMPLE PAGE
class NewSamplePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("BCASAA")
        self.setGeometry(100, 100, 1280, 720)
        MainWindow.set_background_image(self)

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
        icon = QIcon("./Images/book_icon.png")
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
        icon = QIcon("./Images/home_icon.png")
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
        item = QListWidgetItem()
        item.setIcon(thumbnail)
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

#DATA REVIEW PAGE
class DataReviewPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("BCASAA")
        self.setGeometry(100, 100, 1280, 720)
        MainWindow.set_background_image(self)

        #DATA SET TABLE
        self.dataSets_label = QLabel(self)
        self.dataSets_label.setText("Data Sets:")
        self.dataSets_label.setAlignment(Qt.AlignLeft)
        self.dataSets_label.setGeometry(20, 100, 1240, 570)
        self.dataSets_label.setStyleSheet("""
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
        self.dataSets_table = QTableWidget(self)
        self.dataSets_table.setGeometry(40, 140, 1200, 510)
        self.dataSets_table.setColumnCount(3)
        header = self.dataSets_table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.dataSets_table.setHorizontalHeaderLabels(['Date', 'Location', 'Miscellaneous'])
        self.dataSets_table.setSortingEnabled(True)  #CAN SORT BY COLUMN
        self.load_table_data()

        #SELECT SAMPLE BUTTON
        self.selectSample_button = QPushButton('Select Sample', self)
        self.selectSample_button.setFont(QFont('Inter', 20))
        self.selectSample_button.setGeometry(20, 680, 720, 60)
        self.selectSample_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: #000000;
            }
        """)
        self.selectSample_button.clicked.connect(self.fetch_selected_sample)
        
        #NEXT BUTTON
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
        icon = QIcon("./Images/book_icon.png")
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
        icon = QIcon("./Images/home_icon.png")
        self.home_button.setIcon(icon)
        self.home_button.setIconSize(QSize(44, 44))
        
    #LOADS ALL SAMPLES FROM DB FOR THE TABLE WIP
    def load_table_data(self):
        try:
            #CONNECTS TO DB
            conn = psycopg2.connect(
                host="localhost",    #DB HOST NAME
                database="tester",   #DB NAME
                user="postgres",     #DB USER
                password="admin"     #DB PASSWORD
            )
            cursor = conn.cursor()

            #FETCHES DATA
            cursor.execute("SELECT date, location, miscellaneous FROM datasets")
            rows = cursor.fetchall()

            #POPULATES TABLE
            self.dataSets_table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    self.dataSets_table.setItem(row_idx, col_idx, item)
            conn.close()

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error connecting to the database: {e}")
            print(f"Database error: {e}")

    #SELECTS SPECIFIC DATA SET FROM DB WIP
    def fetch_selected_sample(self):
        selected_row = self.dataSets_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a data set from the table.")
            return

        # Get selected values from the table
        date = self.dataSets_table.item(selected_row, 0).text()
        location = self.dataSets_table.item(selected_row, 1).text()
        misc = self.dataSets_table.item(selected_row, 2).text()
        
        try:
            # Connect to PostgreSQL database
            conn = psycopg2.connect(
                host="localhost",    #DB HOST NAME
                database="tester",   #DB NAME
                user="postgres",     #DB USER
                password="admin"     #DB PASSWORD
            )
            cursor = conn.cursor()

            #QUERY TO FETCH SPESIFIC DATASET WIP
            query = sql.SQL("SELECT * FROM datasets WHERE date = %s AND location = %s AND miscellaneous = %s")
            cursor.execute(query, (date, location, misc))

            #PLACEHOLDER CODE TO TEST
            result = cursor.fetchone()
            if result:
                QMessageBox.information(self, "Sample Selected", f"Data: {result}")
            else:
                QMessageBox.warning(self, "No Data", "No matching data found in the database.")
                
            conn.close()

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error fetching data from the database: {e}")
            print(f"Database error: {e}")
            
    #CREATES POP-UP WITH INSTRUCTIONS WIP
    def show_instructions(self):
        instructions = (
            "Instructions for Data Review Page:\n\n"
            "1. Click on the dataset from the list you want to review.\n"
            "2. Click on the 'Select Sample' button.\n"
            "3. Click on the 'Next' button to continue to the next page.\n"
            "4. Click on the 'Home' button to return to the main screen.\n\n"
            "Please note that the datasets can be sorted by date and\n"
            " by location. To do so click on the column header\n"
            "(Date or Location) to sort decendingly or accendingly"
        )
        QMessageBox.information(self, "Instructions", instructions)

#OUTPUT PAGE
class OutputPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("BCASAA")
        self.setGeometry(100, 100, 1280, 720)
        MainWindow.set_background_image(self)

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
        self.display_stats(self.imageResults_area)
        self.display_stats(self.avg_results_area)
        
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
        icon = QIcon("./Images/book_icon.png")
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
        icon = QIcon("./Images/home_icon.png")
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
    def create_stats_grid(self): 
        grid_layout = QGridLayout()

        # Labels for each stat field
        stats = [
            ("Leaf Area", 0, 0),
            ("Scarred Area", 1, 0),
            ("Percentage Damage", 2, 0),
            ("Number of Scars", 3, 0),
            ("Length of Leaf", 4, 0),
            ("Width of Leaf", 5, 0),
            ("X cm<sup>2</sup>", 0, 1),
            ("X cm<sup>2</sup>", 1, 1),
            ("X %", 2, 1),
            ("X", 3, 1),
            ("X cm", 4, 1),
            ("X cm", 5, 1)
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
            grid_layout.addWidget(label, row, col)

        return grid_layout

# Displays stats layout in a scroll area with a transparent background
    def display_stats(self, scroll_area):
        container_widget = QWidget()
        grid_layout = self.create_stats_grid()
        container_widget.setLayout(grid_layout)
        container_widget.setStyleSheet("background-color: transparent;")  # Set container background to transparent
        scroll_area.setWidget(container_widget)

    
    
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
