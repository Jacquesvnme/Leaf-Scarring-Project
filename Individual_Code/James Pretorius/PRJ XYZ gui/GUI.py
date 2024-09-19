import sys
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QWidget, QMessageBox, 
    QFileDialog, QListWidget, QCheckBox, QVBoxLayout, QLineEdit,
    QDateEdit, QListWidgetItem, QStackedWidget
)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush, QIcon, QColor
from PyQt5.QtCore import Qt, QDate, QSize

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BCASAA")
        self.setGeometry(100, 100, 1300, 780)
        self.stacked_widget = QStackedWidget(self)

        #CREATE PAGES
        self.main_page = MainPage(self)
        self.new_sample_page = NewSamplePage(self)

        #ADD TO STACK
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.new_sample_page)

        # Set layout to hold the stacked widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        #BUTTONS FOR NAVIGATION
        self.main_page.new_sample_button.clicked.connect(self.show_new_sample_page)
        self.new_sample_page.home_button.clicked.connect(self.show_main_page)

    def show_main_page(self):
        self.stacked_widget.setCurrentWidget(self.main_page)

    def show_new_sample_page(self):
        self.stacked_widget.setCurrentWidget(self.new_sample_page)
   
#HOME PAGE
class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(20, 20, 1280, 720)  #SETS SIZE OF APPLICATION
        self.set_background_image()
        
        #MAIN TITLE
        self.title_label = QLabel(self)
        self.title_label.setText("Welcome to the BioControl Agent\n"+
                                 "Statistical Analysis Application")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setGeometry(100, 20, 1080, 300)
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
        self.new_sample_button.setGeometry(250, 350, 300, 100)
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
        self.data_review_button.setGeometry(700, 350, 300, 100)
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
            "Credits:\n"
            "Group names D Giovannoni - Project Supervisor\n"
            "Dr. K English - Project Sponsor\n"
            "Belgium ITversity, RSA Center of Biological Control, Rhodes University, US"
        )
        self.credit_label.setFont(QFont('Inter', 20))
        self.credit_label.setAlignment(Qt.AlignCenter)
        self.credit_label.setGeometry(20, 480, 1240, 220)
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

    def set_background_image(self):
        palette = QPalette()
        background = QPixmap("./Images/BG.jpg")
        scaled_background = background.scaled(QSize(1280, 720), Qt.KeepAspectRatioByExpanding)
        palette.setBrush(QPalette.Background, QBrush(scaled_background))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    #CREATES POP-UP WITH INSTRUCTIONS WIP
    def show_instructions(self):
        instructions = (
            "Instructions for Using the Application:\n\n"
            "1. Click 'New Sample' to input new data samples.\n"
            "2. Click 'Data Review' to review existing data and analysis.\n"
            "3. Credits are listed at the bottom for project contributors."
        )
        QMessageBox.information(self, "Instructions", instructions)

class NewSamplePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("BCASAA")
        self.setGeometry(100, 100, 1280, 720)
        self.set_background_image()

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
        
        #CHECKLIST
        self.checklist_label = QLabel(self)
        self.checklist_label.setGeometry(820, 330, 400, 60)
        self.checklist_label.setText("Please select which statistics you\n"
                                "want to view:")
        self.checklist_label.setStyleSheet("""
            QLabel {
                font-family: 'Inter';
                font-style: italic;
                font-weight: 400;
                font-size: 20px;
            }
        """)
        
        #CHECKLIST        
        def handle_checkbox_state(checkbox):
            if checkbox.isChecked():
                print(f"{checkbox.text()} is checked")
            else:
                print(f"{checkbox.text()} is unchecked")
        
        self.checklist = QListWidget(self)
        self.checklist.setGeometry(820, 400, 400, 200)
        items = ["Surface Area of Leaf", "Surface Area of Scarring", "Number of Scars", "Percentage Damage", "Approximate Dimensions of Leaf", "Length of Petiole"]
        for item in items:
            checkbox = QCheckBox(item, self)
            checkbox.stateChanged.connect(lambda state, cb=checkbox: handle_checkbox_state(cb))
            list_item = QListWidgetItem(self.checklist)
            self.checklist.addItem(list_item)
            self.checklist.setItemWidget(list_item, checkbox)
        self.checklist.setSpacing(8)
        self.checklist.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
            }
            QCheckBox {
                font-family: 'Inter';
                font-style: italic;
                font-weight: 100;
                font-size: 18px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:checked {
                image: url(./Images/checked_box.png);
            }
            QCheckBox::indicator:unchecked {
                image: url(./Images/unchecked_box.png);
        """)

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

    def set_background_image(self):
        palette = QPalette()
        background = QPixmap("./Images/BG.jpg")
        scaled_background = background.scaled(QSize(1280, 720), Qt.KeepAspectRatioByExpanding)
        palette.setBrush(QPalette.Background, QBrush(scaled_background))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

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
        
    def handle_checkbox_state(checkbox):
        if checkbox.isChecked():
            print(f"{checkbox.text()} is checked")
        else:
            print(f"{checkbox.text()} is unchecked")
            
    #CREATES POP-UP WITH INSTRUCTIONS WIP
    def show_instructions(self):
        instructions = (
            "Instructions for New Sample Page:\n\n"
            "1. Use 'Add Images' to upload image files (.png, .jpg).\n"
            "2. Fill out the location and date fields.\n"
            "3. Use the checklist to select options.\n"
            "4. Click 'Next' to proceed to the next step."
        )
        QMessageBox.information(self, "Instructions", instructions)

#class DataReviewPage(QWidget):
#class OutputPage(QWidget):

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
