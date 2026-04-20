from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import * 
from colorPicker import RGBAColorPicker
from imageWork import ImageWorkdir
from imageProcessor import ImageProcessor

#создание экрана
app = QApplication([])
main_win = QWidget()
main_win.resize(1000, 600)
main_win.setWindowTitle('Easy Editor')


#---ИНТЕРФЕЙС---

#ЛЕВАЯ СТОРОНА
papka = QPushButton('Папка')
list_w = QListWidget()

col1 = QVBoxLayout()
col1.addWidget(papka)
col1.addWidget(list_w)
papka_group = QGroupBox()
papka_group.setLayout(col1)

#ЦЕНТР
#вверх
def create_button(text):
    return QPushButton(text)

filters = ['Размытие', 'Контур', 'Резкость']
filter_widgets = {text: create_button(text) for text in filters}
filters_group = QGroupBox()
filters_group.setLayout(QHBoxLayout())
for btn in filter_widgets.values():
    filters_group.layout().addWidget(btn)

blur_btn = filter_widgets['Размытие']
contour_btn = filter_widgets['Контур']
sharp_btn = filter_widgets['Резкость']

#центр
image_lbl = QLabel('Картинка')
img_group = QGroupBox()
img_group.setLayout(QHBoxLayout())
img_group.layout().addWidget(image_lbl)
img_group.setFixedHeight(440)

#низ 
left = QPushButton('Лево')
right = QPushButton('Право')
goriz = QPushButton('По горизонтали')
vertic = QPushButton('По вертикали')
size = QPushButton('Размер')

row3 = QHBoxLayout()
row3.addWidget(left)
row3.addWidget(right)
row3.addWidget(goriz)
row3.addWidget(vertic)
row3.addWidget(size)
row3.setSpacing(20)
geom_group = QGroupBox()
geom_group.setLayout(row3)
geom_group.setFixedHeight(80)

#соединения 
col2 = QVBoxLayout()
col2.addWidget(filters_group)
col2.addWidget(img_group)
col2.addWidget(geom_group)
col2.addStretch()

#ПРАВО 
col3 = QVBoxLayout() #главная вертикальная линия стороны

#Фигуры
squa = QPushButton('Квадрат')
circle = QPushButton('Круг')
treg = QPushButton('Треугольник')
zalivka = QPushButton('Заливка')

geom_layout = QVBoxLayout()
geom_layout.addWidget(squa)
geom_layout.addWidget(circle)
geom_layout.addWidget(treg)
geom_layout.addWidget(zalivka)

#слайдеры
def create_slider():
    slider = QSlider(Qt.Horizontal)
    slider.setRange(0, 100)
    return slider

sliderX = create_slider()
sliderY = create_slider()
slider_lineWeight = create_slider()
sliderX.setValue(50)
sliderY.setValue(50)
slider_lineWeight.setValue(20)

slider_row1 = QHBoxLayout()
X_lbl = QLabel('X')
slider_row1.addWidget(X_lbl)
slider_row1.addWidget(sliderX)

slider_row2 = QHBoxLayout()
Y_lbl = QLabel('Y')
slider_row2.addWidget(Y_lbl)
slider_row2.addWidget(sliderY)

slider_row3 = QHBoxLayout()
Size_lbl = QLabel('Размер')
slider_row3.addWidget(Size_lbl)
slider_row3.addWidget(slider_lineWeight)

geom_layout.addLayout(slider_row1)
geom_layout.addLayout(slider_row2)
geom_layout.addLayout(slider_row3)

#палитра
color_pick = RGBAColorPicker()
geom_layout.addWidget(color_pick)
geom_layout.addStretch()

geomet_group = QGroupBox()
geomet_group.setLayout(geom_layout)

#текст
text_group = QGroupBox()
text_layout = QVBoxLayout()
textInput = QLineEdit()
textInput.setPlaceholderText('Введите текст...')
text_btn = create_button('Добавить')
textClear_btn = create_button('Очистить текст')
textSize_spin = QSpinBox()
textSize_spin.setRange(10, 200)
textSize_spin.setValue(50)
textSize_spin.setFixedWidth(60)

text_row = QHBoxLayout()
text_row.addWidget(textInput)
text_row.addWidget(QLabel('Размер:'))
text_row.addWidget(textSize_spin)

text_layout.addLayout(text_row)
text_layout.addWidget(text_btn)
text_layout.addWidget(textClear_btn)
text_group.setLayout(text_layout)

# доп группа
save = QPushButton('Сохранить')
dop1 = QPushButton('Доп.кнопка 1')
dop2 = QPushButton('Доп.кнопка 2')
dop3 = QPushButton('Доп.кнопка 3')
dop4 = QPushButton('Доп.кнопка 4')

extra_group = QGroupBox()
extra_line = QVBoxLayout()
extra_line.addWidget(save)
extra_group.setLayout(extra_line)

#соединение
col3.addWidget(geomet_group)
col3.addWidget(text_group)
col3.addWidget(extra_group)


#ОБЪЕДИНЕНИЕ ГРУПП
main_row = QHBoxLayout()
main_row.addWidget(papka_group, 10)
main_row.addLayout(col2, 70)
main_row.addLayout(col3, 20)


main_win.setStyleSheet('''
    background-image: url("./фон.jpg");
''')
    

papka.setStyleSheet('''
    QPushButton{
        background-color:#edb561;
        font-size: 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #ebca98
    }
''')

geom_style = '''
    QPushButton{
        background-color:#326ea6;
        font-size: 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #5b90c2
    }
'''
left.setStyleSheet(geom_style)
right.setStyleSheet(geom_style)
goriz.setStyleSheet(geom_style)
vertic.setStyleSheet(geom_style)
size.setStyleSheet(geom_style)



fig_style = '''
    QPushButton{
        background-color:#d1ed61;
        font-size: 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #ebfaaf
    }
'''
squa.setStyleSheet(fig_style)
circle.setStyleSheet(fig_style)
zalivka.setStyleSheet(fig_style)
treg.setStyleSheet(fig_style)

save.setStyleSheet('''
    QPushButton{
        background-color:#edb561;
        font-size: 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #ebca98
    }
''')


filter_style = '''
    QPushButton{
        background-color:#326ea6;
        font-size: 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #5b90c2
    }
'''
blur_btn.setStyleSheet(filter_style)
sharp_btn.setStyleSheet(filter_style)
contour_btn.setStyleSheet(filter_style)


textClear_btn.setStyleSheet('''
    QPushButton{
        background-color: #d98e6f;
        font-size: 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #e3b6a3
    }
''')

text_btn.setStyleSheet('''
    QPushButton{
        background-color: #d98e6f;
        font-size: 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #e3b6a3
    }
''')


# Функционал
# ---1 часть---
imageWorkspace = ImageWorkdir()
workimage = ImageProcessor(image_lbl)


def show_images():
    imageWorkspace.show_filenames_in_list(list_w)

def showChosenImage():
    if list_w.currentRow() >= 0:
        filename = list_w.currentItem().text()
        workimage.dir = imageWorkspace.workdir
        workimage.load_image(filename)

papka.clicked.connect(show_images)
list_w.currentRowChanged.connect(showChosenImage)

#Фильтры 
# ---2 часть---
filter_handlers = {
    'Размытие': 'blur',
    'Контур' : 'contour',
    'Резкость': 'sharp',
}
filter_states = {name: False for name in filter_handlers.keys()}

def toggle_filter(filter_name, handler):
    filter_states[filter_name] = not filter_states[filter_name]
    workimage.filter_toggle(handler, filter_states[filter_name])

for text, handler in filter_handlers.items():
    filter_widgets[text].clicked.connect(
        lambda checked, t=text, h=handler: toggle_filter(t, h)
    )

#--- 3 часть---
left.clicked.connect(workimage.rotate_left)
right.clicked.connect(workimage.rotate_right)
goriz.clicked.connect(workimage.mirror_horizontal)
vertic.clicked.connect(workimage.mirror_vertical) 

def resize_dialog():
    if workimage.original_image is None:
        QMessageBox.warning(main_win, "Ошибка", "Сначала загрузите изображение!")
        return
    
    current_width, current_height = workimage.original_image.size
    dialog = QDialog(main_win)
    dialog.setWindowTitle("Изменение размера")
    dialog.setFixedSize(300, 200)
    
    layout = QVBoxLayout()
    width_spin = QSpinBox()
    width_spin.setRange(1, 10000)
    width_spin.setValue(current_width)
    height_spin = QSpinBox()
    height_spin.setRange(1, 10000)
    height_spin.setValue(current_height)
    keep_ratio_cb = QCheckBox("Сохранять пропорции")
    keep_ratio_cb.setChecked(True)
    
    layout.addWidget(QLabel("Ширина:"))
    layout.addWidget(width_spin)
    layout.addWidget(QLabel("Высота:"))
    layout.addWidget(height_spin)
    layout.addWidget(keep_ratio_cb)
    
    def adjust_height():
        if keep_ratio_cb.isChecked():
            ratio = width_spin.value() / current_width
            height_spin.setValue(int(current_height * ratio))
    
    def adjust_width():
        if keep_ratio_cb.isChecked():
            ratio = height_spin.value() / current_height
            width_spin.setValue(int(current_width * ratio))
    
    width_spin.valueChanged.connect(adjust_height)
    height_spin.valueChanged.connect(adjust_width)
    
    button_layout = QHBoxLayout()
    ok_btn = create_button("Применить")
    cancel_btn = create_button("Отмена")
    
    def apply_resize():
        if workimage.resize_image(width_spin.value(), height_spin.value()):
            dialog.accept()
    
    ok_btn.clicked.connect(apply_resize)
    cancel_btn.clicked.connect(dialog.reject)
    
    button_layout.addWidget(ok_btn)
    button_layout.addWidget(cancel_btn)
    layout.addLayout(button_layout)
    dialog.setLayout(layout)
    dialog.exec_()

size.clicked.connect(resize_dialog)


# Фигуры
#---4 часть---
squa.clicked.connect(lambda: workimage.draw_shape('square'))
circle.clicked.connect(lambda: workimage.draw_shape('circle'))
treg.clicked.connect(lambda: workimage.draw_shape('triangle'))

def on_slider_x_changed(value):
    workimage.set_draw_position(value, sliderY.value())

def on_slider_y_changed(value):
    workimage.set_draw_position(sliderX.value(), value)

def on_line_weight_changed(value):
    workimage.set_shape_size(value)

sliderX.valueChanged.connect(on_slider_x_changed)
sliderY.valueChanged.connect(on_slider_y_changed)
slider_lineWeight.valueChanged.connect(on_line_weight_changed)

color_pick.colorChanged.connect(lambda color: workimage.set_draw_color((color.red(), color.green(), color.blue(), color.alpha())))


def add_text():
    text = textInput.text().strip()
    if text and workimage.original_image:
        workimage.set_text_size(textSize_spin.value())
        workimage.set_text(text)
        textInput.clear()
    elif not text:
        QMessageBox.warning(main_win, 'Внимание', 'Введите текст для добавления')
    else:
        QMessageBox.warning(main_win, 'Внимание', 'Сначала загрузите изображение')
    
text_btn.clicked.connect(add_text)
textInput.returnPressed.connect(add_text)
textClear_btn.clicked.connect(workimage.clear_text)
textSize_spin.valueChanged.connect(lambda value:
    workimage.set_text_size(value) if workimage.text_content else None)

#ЗАПУСК
main_win.setLayout(main_row)
main_win.show()
app.exec_()