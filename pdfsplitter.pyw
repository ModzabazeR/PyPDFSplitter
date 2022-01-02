from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import sys
import os
from PyPDF2 import PdfFileReader, PdfFileWriter

def reset_form():
    spin_from.setValue(1)
    spin_to.setValue(1)
    out_destination.setText("")
    start_button.setEnabled(False)
    out_destination_button.setEnabled(False)

def get_path(filename) -> str:
    return "/".join(filename.split("/")[:-1]) + "/"

def popup_message(msg):
    msg_box = QMessageBox()
    msg_box.setText(msg)
    msg_box.exec_()

def main():
    global start_button
    MITR_TITLE = QFont("Mitr", 24,)
    MITR_BUTTON = QFont("Mitr", 12, 1)

    app = QApplication(sys.argv)
    window = QWidget()
    window.setGeometry(720, 300, 500, 300)
    window.setWindowTitle("PyPDFSplitter")

    layout = QVBoxLayout()

    label = QLabel("PDF Splitter")
    label.setAlignment(QtCore.Qt.AlignCenter)
    label.setFont(MITR_TITLE)
    choose_file_button = QPushButton("เลือกไฟล์")
    choose_file_button.setFont(MITR_BUTTON)
    choose_file_button.clicked.connect(click_handler)

    start_button = QPushButton("เริ่มทำงาน")
    start_button.setFont(MITR_BUTTON)
    start_button.clicked.connect(lambda: pdf_splitter(file_name))
    start_button.setEnabled(False)

    layout.addWidget(label)
    layout.addWidget(choose_file_button)
    layout.addWidget(create_group())
    layout.addWidget(start_button)

    window.setLayout(layout)

    window.show()
    sys.exit(app.exec_())

def click_handler():
    global file_name
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getOpenFileName(None, "Choose PDF file", "", "PDF Files (*.pdf);;All Files (*)", options=options)
    if file_name:
        out_destination_button.setEnabled(True)
        num_page = PdfFileReader(file_name).getNumPages()
        spin_from.setRange(1, num_page)
        spin_to.setRange(1, num_page)
        spin_to.setValue(num_page)

def pdf_splitter(file_name):
    start, end = (spin_from.value(), spin_to.value())
    input_pdf = PdfFileReader(file_name)
    new_pdf = PdfFileWriter()
    start -= 1
    try:
        with open(out_destination.text(), "wb") as f:
            for i in range(start, end):
                new_pdf.addPage(input_pdf.getPage(i))
                new_pdf.write(f)
        popup_message("ทำงานเสร็จสิ้น")
        os.startfile(out_destination.text())
        reset_form()
    except Exception as e:
        print(e)
        popup_message(f"Error: {e}")

def create_group() -> QGroupBox:
    global spin_to, spin_to_label, spin_from, spin_from_label, out_destination, out_destination_button

    group_box = QGroupBox()
    spin_from = QSpinBox()
    spin_from.setRange(1, 1)
    spin_from_label = QLabel("ตั้งแต่หน้าที่:")
    spin_to = QSpinBox()
    spin_to.setRange(1, 1)
    spin_to_label = QLabel("ถึงหน้าที่:")
    out_destination_button = QPushButton("เลือก")
    out_destination_button.setEnabled(False)
    out_destination_button.clicked.connect(get_out_dir)
    out_destination = QLabel("")

    vbox = QFormLayout()
    vbox.addRow(spin_from_label, spin_from)
    vbox.addRow(spin_to_label, spin_to)
    vbox.addRow(QLabel("ที่อยู่ไฟล์ใหม่:"), out_destination_button)
    vbox.addRow(QLabel("ที่อยู่ไฟล์ใหม่ที่เลือกแล้ว:"), out_destination)
    group_box.setLayout(vbox)

    return group_box

def get_out_dir():
    options = QFileDialog.Options()
    out_dir, _ = QFileDialog.getSaveFileName(None, "Save file", f"{file_name[:-4]}_splitted.pdf", "PDF Files (*.pdf);;All Files (*)", options=options)
    if out_dir:
        out_destination.setText(out_dir)
        start_button.setEnabled(True)

if __name__ == "__main__":
    main()