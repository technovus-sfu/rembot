#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
License is available in LICENSE
@brief CoreUI
@author eeshiken
@since 2017-DEC-28
"""

import os
from PyQt5.QtWidgets import QWidget, QSizePolicy, QLayout, QVBoxLayout, QHBoxLayout, \
 QLabel, QGroupBox, QLineEdit, QGridLayout, QPushButton, QTextEdit, QSpacerItem
from PyQt5.QtCore import Qt, pyqtSignal, QMetaObject, QCoreApplication, QSize
from PyQt5.QtGui import QFont, QPixmap, QCursor

from system_status import Log


class CoreUI(QWidget):
    ''' Core Ui class '''
    status_message = pyqtSignal(str)
    images_path = "interface/rembot/assets/images/"

    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

        # Log class
        self.log = Log(self)
        self.log.log_data[str].connect(self.to_log)

    def init_ui(self):
        ''' Rembot UI '''
        self.setObjectName("CoreUI")

        # UI Contaier
        self.ui_container = QVBoxLayout(self)
        self.ui_container.setObjectName("ui_container")

        ## Header
        ### Box
        self.header_box = QHBoxLayout()
        self.header_box.setObjectName("header_box")
        self.header_box.setContentsMargins(10, 10, 10, 10)
        ### title
        font = QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(40)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.header_title = QLabel()
        self.header_title.setFont(font)
        self.header_title.setCursor(QCursor(Qt.ArrowCursor))
        self.header_title.setLayoutDirection(Qt.LeftToRight)
        self.header_title.setStyleSheet("color: rgb(108, 204, 227);")
        self.header_title.setScaledContents(False)
        self.header_title.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.header_title.setContentsMargins(0, 0, 0, 0)
        self.header_title.setObjectName("header_title")
        self.header_box.addWidget(self.header_title) # add title to header
        ### version
        font = QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.version_number = QLabel()
        self.version_number.setFont(font)
        self.version_number.setStyleSheet("color: rgb(85, 85, 85);")
        self.version_number.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.version_number.setObjectName("version_number")
        self.header_box.addWidget(self.version_number) # add version number to header

        # Add to UI Container
        self.ui_container.addLayout(self.header_box) # add header box to layout

        # Content
        self.content_box = QHBoxLayout()
        self.content_box.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.content_box.setContentsMargins(10, 10, 10, 10)
        self.content_box.setObjectName("content_box")
        ## Left Box
        self.left_box = QVBoxLayout()
        self.left_box.setSizeConstraint(QLayout.SetFixedSize)
        self.left_box.setContentsMargins(10, 10, 10, 10)
        self.left_box.setObjectName("left_box")
        ### File box
        self.file_box = QHBoxLayout()
        self.file_box.setContentsMargins(10, 10, 10, 10)
        self.file_box.setObjectName("file_box")
        #### File label
        font = QFont()
        font.setPointSize(10)
        self.file_label = QLabel()
        self.file_label.setFont(font)
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.file_label.sizePolicy().hasHeightForWidth())
        self.file_label.setSizePolicy(size_policy)
        self.file_label.setObjectName("file_label")
        ### Add label to File box
        self.file_box.addWidget(self.file_label)

        #### File Input
        font = QFont()
        font.setPointSize(20)
        self.file_input = QLineEdit()
        self.file_input.setFont(font)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.file_input.sizePolicy().hasHeightForWidth())
        self.file_input.setSizePolicy(size_policy)
        self.file_input.setMinimumSize(QSize(0, 0))
        self.file_input.setAcceptDrops(True)
        self.file_input.setLayoutDirection(Qt.LeftToRight)
        self.file_input.setText("")
        self.file_input.setFrame(True)
        self.file_input.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.file_input.setObjectName("file_input")
        #### Add File input to File box
        self.file_box.addWidget(self.file_input)

        ### Add File box to Left Box
        self.left_box.addLayout(self.file_box)

        #### Add Button box
        self.button_box = QGridLayout()
        self.button_box.setContentsMargins(10, 10, 10, 10)
        self.button_box.setObjectName("button_box")
        ##### Start Button
        self.start_button = QPushButton()
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(size_policy)
        self.start_button.setObjectName("start_button")
        ##### Stop Button
        self.stop_button = QPushButton()
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
        self.stop_button.setSizePolicy(size_policy)
        self.stop_button.setObjectName("stop_button")
        ##### Test Button
        self.test_button = QPushButton()
        self.test_button.setEnabled(False)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.test_button.sizePolicy().hasHeightForWidth())
        self.test_button.setSizePolicy(size_policy)
        self.test_button.setObjectName("test_button")
        ##### Quit Button
        self.quit_button = QPushButton()
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.quit_button.sizePolicy().hasHeightForWidth())
        self.quit_button.setSizePolicy(size_policy)
        self.quit_button.setObjectName("quit_button")
        #### Add Buttons to Button Box
        self.button_box.addWidget(self.start_button, 0, 0, 1, 1)
        self.button_box.addWidget(self.stop_button, 0, 1, 1, 1)
        self.button_box.addWidget(self.test_button, 1, 0, 1, 1)
        self.button_box.addWidget(self.quit_button, 1, 1, 1, 1)

        ### Add Button box to Left box
        self.left_box.addLayout(self.button_box)

        #### Log Box and Layout
        self.log_box = QGroupBox()
        self.log_box.setFlat(True)
        self.log_box.setObjectName("log_box")
        self.log_layout = QVBoxLayout(self.log_box)
        self.log_layout.setContentsMargins(0, 10, 0, 0)
        self.log_layout.setObjectName("log_layout")
        ##### Log output
        self.log_output = QTextEdit(self.log_box)
        self.log_output.setMinimumSize(QSize(720, 600))
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(1)
        size_policy.setHeightForWidth(self.log_output.sizePolicy().hasHeightForWidth())
        self.log_output.setSizePolicy(size_policy)
        self.log_output.setReadOnly(True)
        self.log_output.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.log_output.setObjectName("log_output")
        #### Add Log Output to Log box | Log layout
        self.log_layout.addWidget(self.log_output)
        ### Add Log box to Left box
        self.left_box.addWidget(self.log_box)
        #### Left spacer
        self.spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        ### Add spacer to Log box
        self.left_box.addItem(self.spacer_item)
        ## Add Left box to Content box
        self.content_box.addLayout(self.left_box)

        ### Right Box
        self.right_box = QVBoxLayout()
        self.right_box.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.right_box.setContentsMargins(10, 10, 10, 10)
        self.right_box.setObjectName("right_box")
        #### Origninal image box
        self.original_img_box = QGroupBox()
        self.original_img_box.setFlat(True)
        self.original_img_box.setObjectName("original_img_box")
        self.original_img_layout = QVBoxLayout(self.original_img_box)
        self.original_img_layout.setContentsMargins(0, 0, 0, 0)
        self.original_img_layout.setObjectName("original_img_layout")
        ##### Original image
        self.original_img = QLabel(self.original_img_box)
        self.original_img.setMinimumSize(QSize(720, 400))
        self.original_img.setText("")
        default = self.images_path + "default.jpg"
        self.original_img.setPixmap(QPixmap(default))
        self.original_img.setScaledContents(True)
        self.original_img.setObjectName("original_img")
        #### Add Original image to Original image Layout
        self.original_img_layout.addWidget(self.original_img)

        ### Add Original image box to Right box
        self.right_box.addWidget(self.original_img_box)

        #### Output image box
        self.output_img_box = QGroupBox()
        self.output_img_box.setFlat(True)
        self.output_img_box.setObjectName("output_img_box")
        self.output_img_layout = QHBoxLayout(self.output_img_box)
        self.output_img_layout.setContentsMargins(0, 0, 0, 0)
        self.output_img_layout.setObjectName("output_img_layout")
        ##### Output image
        self.output_img = QLabel(self.output_img_box)
        self.output_img.setMinimumSize(QSize(720, 400))
        self.output_img.setText("")
        self.output_img.setPixmap(QPixmap(default))
        self.output_img.setScaledContents(True)
        self.output_img.setObjectName("output_img")
        #### Add Output img to output image layout
        self.output_img_layout.addWidget(self.output_img)

        ### Add Output image box to Right box
        self.right_box.addWidget(self.output_img_box)

        ## Add Right box to Content box
        self.content_box.addLayout(self.right_box)

        # Add Content box to UI Container
        self.ui_container.addLayout(self.content_box) # add content box to layout

        # Labelling
        self.retranslate_ui()
        QMetaObject.connectSlotsByName(self)

        # Attach signals
        self.attach_events()

    def retranslate_ui(self):
        ''' UI Text '''
        _translate = QCoreApplication.translate
        self.header_title.setText(_translate("CoreUI", "REMBOT"))
        self.version_number.setText(_translate("CoreUI", ""))
        self.file_label.setText(_translate("CoreUI", "File name"))
        self.file_input.setPlaceholderText(_translate("CoreUI", "image.ext"))
        self.start_button.setText(_translate("CoreUI", "START"))
        self.stop_button.setText(_translate("CoreUI", "STOP"))
        self.test_button.setText(_translate("CoreUI", "TEST"))
        self.quit_button.setText(_translate("CoreUI", "QUIT"))
        self.log_box.setTitle(_translate("CoreUI", "Log"))
        self.original_img_box.setTitle(_translate("CoreUI", "Original Image"))
        self.output_img_box.setTitle(_translate("CoreUI", "Output Image"))

    def attach_events(self):
        ''' Attach signals to events '''
        self.start_button.clicked.connect(self.start)
        # self.stop_button.clicked.connect()

    def start(self):
        ''' Start program '''

        file_path = self.images_path + self.file_input.text() # specify filepath
        if  os.path.exists(file_path) and file_path[-1] != '/':
            self.log.info_log("Loading File") # log
            self.original_img.setPixmap(QPixmap(file_path)) # update display image
        else:
            self.log.warning_log("File does not exist") # log

    def update_status(self, msg):
        ''' Update the program statusbar string and log '''
        self.status_message.emit(msg)

    def to_log(self, msg):
        ''' Output message in ui window '''
        self.log_output.append(msg)