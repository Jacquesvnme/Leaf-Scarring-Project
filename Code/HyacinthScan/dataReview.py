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

#DATA REVIEW PAGE
class DataReviewPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        self.dataSets_table.setColumnCount(12)
        header = self.dataSets_table.horizontalHeader()       

        self.dataSets_table.setHorizontalHeaderLabels(['imagedata_id', 'imagelocation', 'imagedate', 'imagepath', 'imagelable', 'lamina_area', 'lamina_length', 'lamina_width', 'scar_count', 'scar_area', 'damagepercentage', 'petiole_length'])
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
        
    #LOADS ALL SAMPLES FROM DB FOR THE TABLE WIP
    def load_table_data(self):
        try:
            rows = DBObj.selectAllCollection()

            #POPULATES TABLE
            self.dataSets_table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    self.dataSets_table.setItem(row_idx, col_idx, item)

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
        imagedata_id = self.dataSets_table.item(selected_row, 0).text()
        imagelocation = self.dataSets_table.item(selected_row, 1).text()
        imagedate = self.dataSets_table.item(selected_row, 2).text()
        imagepath = self.dataSets_table.item(selected_row, 3).text()
        imagelable = self.dataSets_table.item(selected_row, 4).text()
        lamina_area = self.dataSets_table.item(selected_row, 5).text()
        lamina_length = self.dataSets_table.item(selected_row, 6).text()
        lamina_width = self.dataSets_table.item(selected_row, 7).text()
        scar_count = self.dataSets_table.item(selected_row, 8).text()
        scar_area = self.dataSets_table.item(selected_row, 9).text()
        damagepercentage = self.dataSets_table.item(selected_row, 10).text()
        petiole_length = self.dataSets_table.item(selected_row, 11).text()
        
        try:
            result = DBObj.selectCollection(imagedata_id)
            if result:
                QMessageBox.information(self, "Sample Selected", f"Data: {result[0]}")
            else:
                QMessageBox.warning(self, "No Data", "No matching data found in the database.")

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