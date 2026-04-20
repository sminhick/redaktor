import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, pyqtSignal

class RGBAColorPicker(QWidget):
    colorChanged = pyqtSignal(QColor)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_color = QColor(255, 0, 0, 255)
        self.initUI()
    
    def initUI(self):
        self.setMinimumSize(200, 150)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        top_layout = QHBoxLayout()
        top_layout.setSpacing(5)
        
        self.color_preview = ColorPreview(self.current_color)
        self.color_preview.setFixedSize(60, 60)
        
        sliders_panel = QWidget()
        sliders_layout = QVBoxLayout(sliders_panel)
        sliders_layout.setSpacing(2)
        sliders_layout.setContentsMargins(0, 0, 0, 0)
        
        self.sliders = {}
        for label, value in [("R", 255), ("G", 0), ("B", 0), ("A", 255)]:
            widget, slider = self.create_color_slider(label, 0, 255, value)
            self.sliders[label.lower()] = slider
            sliders_layout.addWidget(widget)
        
        self.red_slider = self.sliders['r']
        self.green_slider = self.sliders['g']
        self.blue_slider = self.sliders['b']
        self.alpha_slider = self.sliders['a']
        
        top_layout.addWidget(self.color_preview)
        top_layout.addSpacing(5)
        top_layout.addWidget(sliders_panel)
        
        bottom_panel = QWidget()
        bottom_layout = QGridLayout(bottom_panel)
        bottom_layout.setHorizontalSpacing(2)
        bottom_layout.setVerticalSpacing(1)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        self.spins = {}
        labels = ['R', 'G', 'B', 'A']
        for i, (label, value) in enumerate([("R", 255), ("G", 0), ("B", 0), ("A", 255)]):
            spin = QSpinBox()
            spin.setRange(0, 255)
            spin.setValue(value)
            spin.setFixedWidth(40)
            spin.setFixedHeight(22)
            self.spins[label.lower()] = spin
            
            row = i // 2
            col = (i % 2) * 2
            bottom_layout.addWidget(QLabel(f"{label}:"), row, col, Qt.AlignRight)
            bottom_layout.addWidget(spin, row, col + 1)
        
        main_layout.addLayout(top_layout)
        main_layout.addWidget(bottom_panel)
        self.setLayout(main_layout)
        self.connect_signals()
    
    def create_color_slider(self, label, min_val, max_val, default_val):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        
        top_layout = QHBoxLayout()
        top_layout.setSpacing(2)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        label_widget = QLabel(label)
        label_widget.setFixedWidth(10)
        value_label = QLabel(str(default_val))
        value_label.setFixedWidth(20)
        value_label.setAlignment(Qt.AlignRight)
        
        top_layout.addWidget(label_widget)
        top_layout.addWidget(value_label)
        top_layout.addStretch()
        
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default_val)
        
        gradients = {
            "R": "stop:0 rgba(0,0,0,255), stop:1 rgba(255,0,0,255)",
            "G": "stop:0 rgba(0,0,0,255), stop:1 rgba(0,255,0,255)",
            "B": "stop:0 rgba(0,0,0,255), stop:1 rgba(0,0,255,255)",
            "A": "stop:0 rgba(255,255,255,0), stop:1 rgba(255,255,255,255)"
        }
        
        style = f"""
            QSlider::groove:horizontal {{
                height: 4px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, {gradients[label]});
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: white;
                border: 1px solid #555;
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }}
        """
        slider.setStyleSheet(style)
        
        widget.slider = slider
        widget.value_label = value_label
        slider.value_label = value_label
        
        layout.addLayout(top_layout)
        layout.addWidget(slider)
        return widget, slider
    
    def connect_signals(self):
        for label in ['r', 'g', 'b', 'a']:
            self.sliders[label].valueChanged.connect(self.on_slider_changed)
            self.spins[label].valueChanged.connect(self.on_spin_changed)
    
    def on_slider_changed(self, value):
        slider = self.sender()
        if hasattr(slider, 'value_label'):
            slider.value_label.setText(str(value))
        
        slider_map = {
            self.red_slider: 'r',
            self.green_slider: 'g',
            self.blue_slider: 'b',
            self.alpha_slider: 'a'
        }
        
        if slider in slider_map:
            self.spins[slider_map[slider]].setValue(value)
            self.update_color()
    
    def on_spin_changed(self, value):
        spin = self.sender()
        spin_map = {
            self.spins['r']: self.red_slider,
            self.spins['g']: self.green_slider,
            self.spins['b']: self.blue_slider,
            self.spins['a']: self.alpha_slider
        }
        
        if spin in spin_map:
            spin_map[spin].setValue(value)
            self.update_color()
    
    def update_color(self):
        r = self.red_slider.value()
        g = self.green_slider.value()
        b = self.blue_slider.value()
        a = self.alpha_slider.value()
        
        self.current_color = QColor(r, g, b, a)
        self.color_preview.set_color(self.current_color)
        self.colorChanged.emit(self.current_color)
    
    def get_color(self):
        return self.current_color
    
    def get_color_rgba(self):
        return (self.current_color.red(), self.current_color.green(),
                self.current_color.blue(), self.current_color.alpha())
    
    def set_color(self, color):
        if isinstance(color, QColor):
            r, g, b, a = color.red(), color.green(), color.blue(), color.alpha()
        elif isinstance(color, (tuple, list)) and len(color) >= 3:
            r, g, b = color[0], color[1], color[2]
            a = color[3] if len(color) > 3 else 255
        else:
            return
        
        self.red_slider.setValue(r)
        self.green_slider.setValue(g)
        self.blue_slider.setValue(b)
        self.alpha_slider.setValue(a)
        
        self.spins['r'].setValue(r)
        self.spins['g'].setValue(g)
        self.spins['b'].setValue(b)
        self.spins['a'].setValue(a)
        
        self.update_color()

class ColorPreview(QFrame):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(1)
        self.setStyleSheet("border-color: #555; border-width: 1px;")
    
    def set_color(self, color):
        self.color = color
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        cell_size = 6
        
        for y in range(0, self.height(), cell_size):
            for x in range(0, self.width(), cell_size):
                color = QColor(220, 220, 220) if (x // cell_size + y // cell_size) % 2 == 0 else QColor(255, 255, 255)
                painter.fillRect(x, y, cell_size, cell_size, color)
        
        painter.fillRect(0, 0, self.width(), self.height(), self.color)
        painter.setPen(QPen(QColor(85, 85, 85), 1))
        painter.drawRect(0, 0, self.width()-1, self.height()-1)