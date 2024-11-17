#OUTPUT PAGE (APPROX LINE 242 - 327)

#ON CLICK IMAGE SELECTION
    def on_click_selection(self):
        item = self.image_preview_area.selectedItems()
        '''image_path = item[0].text()
        print(f"selected Image Path: {image_path}")
        imagedata_id = DBObj.getPathID(image_path)
        self.create_stats_grid_individual(self, imagedata_id)'''
        
        if item:
            image_path = item[0].text()
            print(f"Selected Image Path: {image_path}")
            imagedata_id = DBObj.getPathID(image_path)
            print(f"Selected Image Data ID: {imagedata_id}")  # Output imagedata_id
            self.create_stats_grid_individual(imagedata_id)
            return imagedata_id
        else:
            print("No item selected.")
            return None
    
    #TITLES AND FIELDS FOR SHOWING STATS
    # Load title & data for Stats Individual Side
    def create_stats_grid_individual(self, imagedata_id):
        grid_layout_individual = QGridLayout()
        
        if imagedata_id is None:
            noData_label = QLabel("No image selected.")
            noData_label.setAlignment(Qt.AlignCenter)
            grid_layout_individual.addWidget(noData_label, 0, 0, 1, 2)
            return grid_layout_individual
        
        data = DBObj.selectSpecificData(imagedata_id)

        if data:
            # Unpack data (assuming the data structure from your example)
            (_,  # imagedata_id, not used in display
            lamina_area,
            lamina_length,
            lamina_width,
            scar_count,
            scar_area,
            damagepercentage) = data[0]

            # Labels for each stat field
            stats = [
                ("Leaf Area", 0, 0),
                ("Scarred Area", 1, 0),
                ("Percentage Damage", 2, 0),
                ("Number of Scars", 3, 0),
                ("Length of Leaf", 4, 0),
                ("Width of Leaf", 5, 0),
                (f"{lamina_area} cm<sup>2</sup>", 0, 1),
                (f"{scar_area} cm<sup>2</sup>", 1, 1),
                (f"{damagepercentage}", 2, 1),
                (f"{scar_count}", 3, 1),
                (f"{lamina_length} cm", 4, 1),
                (f"{lamina_width} cm", 5, 1)
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
                grid_layout_individual.addWidget(label, row, col)
        else:
            noData_label = QLabel("No data available for this ID.")
            noData_label.setAlignment(Qt.AlignCenter)
            grid_layout_individual.addWidget(noData_label, 0, 0, 1, 2)

        return grid_layout_individual



# NEW SAMPLE PAGE (APPROX LINE 38 - 50) (add QListView TO PyQt5.QtWidgets import)

#         self.image_preview_area = QListWidget(self)
#         self.image_preview_area.setGeometry(40, 60, 680, 580)
#         self.image_preview_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
#         self.image_preview_area.setViewMode(QListView.IconMode)         # Set to Icon Mode
#         self.image_preview_area.setIconSize(QSize(150, 150))            # Set larger icon size for thumbnails
#         self.image_preview_area.setSpacing(10)                          # Add spacing between icons
#         self.image_preview_area.setResizeMode(QListWidget.Adjust)       # Adjust layout to fit contents
#         self.image_preview_area.setStyleSheet("""
#             QListWidget {
#                 background-color: rgb(250, 250, 250);
#                 border-radius: 10px;
#             }
#         """)


# NEW SAMPLE PAGE (APROX LINE 232 - 242)

#     #CREATES POP-UP WITH INSTRUCTIONS WIP
#     def show_instructions(self):
#         instructions = (
#             "<h2>Instructions for New Sample Page:<br></h2>"
#             "<ol type='1'><li>Use the 'Add Images' button to upload image files (.png, .jpg).</li>"
#             "<li>Follow on screen prompts and pop-ups as needed</li>"
#             "<li>Fill out the location and date fields.</li>"
#             "<li>Click 'Next' to proceed to the next step.</li>"
#             "<li>Use the 'Home' button to navigate back to the main screen</li></ol>"
#         )
#         QMessageBox.information(self, "Instructions", instructions)



