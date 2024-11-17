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

#HOME PAGE
class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
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
        icon = QIcon("./assets/images/book_icon.png")
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
            "<h2>Instructions for Using the Application:<br></h2>"
            "<ol type='1'><li>Click 'New Sample' to input new data samples.</li>"
            "<li>Click 'Data Review' to review existing data and analysis.</li>"
            "<li>Credits are listed at the bottom, featuring project contributors.</li></ol>"
        )
        QMessageBox.information(self, "Instructions", instructions)