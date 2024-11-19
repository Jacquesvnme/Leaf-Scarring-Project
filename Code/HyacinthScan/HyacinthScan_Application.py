import sys

import cv2
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QWidget, QMessageBox, QFileDialog, QListWidget, QVBoxLayout, QLineEdit,
    QDateEdit, QListWidgetItem, QStackedWidget, QTableWidget, QTableWidgetItem, QScrollArea, QHeaderView,
    QWidget, QGridLayout)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush, QIcon
from PyQt5.QtCore import Qt, QDate, QSize

import psycopg2
from psycopg2 import sql

from home import MainPage
from newSample import NewSamplePage
from dataReview import DataReviewPage
from output import OutputPage

from database import DBHandler as DBObj
from sections import NewData as DataValidation 

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        MainWindow.set_background_image(self)

        self.setWindowTitle("BCASAA")
        self.setWindowIcon(QIcon("./assets/images/App_Icon.png"))
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
        # background = QPixmap("./assets/images/BG.jpg")
        background = QPixmap("./assets/images/background.png")
        scaled_background = background.scaled(QSize(1300, 780), Qt.KeepAspectRatioByExpanding)
        palette.setBrush(QPalette.Background, QBrush(scaled_background))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
