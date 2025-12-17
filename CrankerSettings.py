import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QSpinBox,
                             QComboBox, QTextEdit, QFileDialog, QMessageBox)

SETTINGS_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'dependencies', 'settings.json')


class ConfigApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_settings()

    def initUI(self):
        self.setWindowTitle('App Scheduler Configurator')
        self.setGeometry(100, 100, 800, 300)

        layout = QVBoxLayout()

        # Target File Selection
        file_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(
            "Cesta k souboru (např. C:\\Apps\\app.exe)")
        browse_btn = QPushButton("Procházet")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(QLabel("Cesta k aplikaci:"))
        file_layout.addWidget(self.path_input)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)

        # Interpreter Selection (Optional)
        interpreter_layout = QHBoxLayout()
        self.interpreter_input = QLineEdit()
        self.interpreter_input.setPlaceholderText(
            "Interpret (nepovinné, např. perl, python)")
        interpreter_layout.addWidget(QLabel("Interpret:"))
        interpreter_layout.addWidget(self.interpreter_input)
        layout.addLayout(interpreter_layout)

        # Interval Selection
        interval_layout = QHBoxLayout()
        self.interval_val = QSpinBox()
        self.interval_val.setRange(1, 9999)
        self.interval_unit = QComboBox()
        self.interval_unit.addItems(["Minutes", "Hours"])
        interval_layout.addWidget(QLabel("Interval:"))
        interval_layout.addWidget(self.interval_val)
        interval_layout.addWidget(self.interval_unit)
        layout.addLayout(interval_layout)

        # Keywords
        layout.addWidget(
            QLabel("Keywords (oddělené čárkou nebo novým řádkem):"))
        self.keywords_input = QTextEdit()
        self.keywords_input.setPlaceholderText("Např: Joblist, Guide")
        layout.addWidget(self.keywords_input)

        # Save Button
        save_btn = QPushButton("Uložit nastavení")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Vybrat aplikaci", "", "All Files (*)")
        if filename:
            self.path_input.setText(filename)

    def save_settings(self):
        path = self.path_input.text()
        interpreter = self.interpreter_input.text()
        interval_val = self.interval_val.value()
        interval_unit = self.interval_unit.currentText()
        keywords_raw = self.keywords_input.toPlainText()

        # Parse keywords
        keywords = [k.strip() for k in keywords_raw.replace(
            '\n', ',').split(',') if k.strip()]

        if not path:
            QMessageBox.warning(
                self, "Chyba", "Musíte vybrat cestu k aplikaci.")
            return

        data = {
            "target_path": path,
            "interpreter": interpreter,
            "interval_value": interval_val,
            "interval_unit": interval_unit,
            "keywords": keywords
        }

        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(
                self, "Úspěch", f"Nastavení uloženo do:\n{SETTINGS_FILE}")
        except Exception as e:
            QMessageBox.critical(
                self, "Chyba", f"Nepodařilo se uložit nastavení:\n{e}")

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.path_input.setText(data.get("target_path", ""))
                    self.interpreter_input.setText(data.get("interpreter", ""))
                    self.interval_val.setValue(data.get("interval_value", 20))
                    unit = data.get("interval_unit", "Minutes")
                    index = self.interval_unit.findText(unit)
                    if index >= 0:
                        self.interval_unit.setCurrentIndex(index)

                    keywords = data.get("keywords", [])
                    self.keywords_input.setText(", ".join(keywords))
            except Exception as e:
                print(f"Error loading settings: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConfigApp()
    ex.show()
    sys.exit(app.exec())
