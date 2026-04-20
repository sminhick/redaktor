import os
import time
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

class ImageProcessor():
    def __init__(self, image_lbl, workdir=""):
        self.image =  None
        self.original_image = None
        self.dir = workdir
        self.filename = None
        self.image_label = image_lbl
        self.active_filters = {}
        self.rotate_angle = 0
        self.mirror_h = False
        self.mirror_v = False
        self.target_size = None
        self.draw_x = 0
        self.draw_y = 0
        self.shape_size = 20
        self.current_color = (255, 0, 0, 255)
        self.shape_type = None
        self.text_content = ""
        self.text_font_size = 20
        self.text_color = (0, 0, 0, 255)
        self.temp_files = []
    
    def load_image(self, filename):
        if not self.dir:
            QMessageBox.warning(None, "Ошибка", "Сначала выберите папку с изображениями")
            return False
        
        self.filename = filename
        full_path = os.path.join(self.dir, filename)
        
        try:
            self.original_image = Image.open(full_path)
            if self.original_image.mode not in ('RGB', 'RGBA', 'L'):
                self.original_image = self.original_image.convert('RGB')
            
            self.image = self.original_image.copy()
            self.active_filters.clear()
            self.rotate_angle = 0
            self.mirror_h = False
            self.mirror_v = False
            self.target_size = None
            self.draw_x = 0
            self.draw_y = 0
            self.shape_size = 20
            self.current_color = (255, 0, 0, 255)
            self.shape_type = None
            self.text_content = ""
            self.text_font_size = 20
            self.text_color = (0, 0, 0, 255)

            self.cleanup_temp_files()
            
            self.show_image(full_path)
            return True
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Не удалось загрузить изображение:\n{str(e)}")
            return False

    def cleanup_temp_files(self):
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        self.temp_files.clear()

    
    def get_save_dir(self):
        if not self.dir:
            return os.path.join(os.getcwd(), "Modified")
        return os.path.join(self.dir, "Modified")
    
    def show_image(self, image_path=None):
        if self.image_label is None:
            return False
        
        try:
            if image_path is None:
                if self.image is not None:
                    temp_path = os.path.join(os.getcwd(), "temp_display.jpg")
                    self.image.save(temp_path)
                    self.temp_files.append(temp_path)
                    image_path = temp_path
                elif self.filename and self.dir:
                    image_path = os.path.join(self.dir, self.filename)
                else:
                    return False
            
            if not image_path or not os.path.exists(image_path):
                return False
            
            self.image_label.hide()
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                return False
            
            w = self.image_label.width()
            h = self.image_label.height() 
            if w > 0 and h > 0:
                pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_label.show()
            return True
        except Exception as e:
            print(f'Ошибка отображения: {e}')
            return False
    
    def apply_all_transformations(self):
        if self.original_image is None:
            return
        
        self.image = self.original_image.copy()
        
        filter_map = {
            'blur': lambda img: img.filter(ImageFilter.BLUR),
            'contour': lambda img: img.filter(ImageFilter.CONTOUR),
            'sharp': lambda img: img.filter(ImageFilter.SHARPEN),
        }
        
        for filter_name, filter_func in filter_map.items():
            if self.active_filters.get(filter_name, False):
                self.image = filter_func(self.image)
        
        if self.rotate_angle == 90:
            self.image = self.image.transpose(Image.ROTATE_90)
        elif self.rotate_angle == 180:
            self.image = self.image.transpose(Image.ROTATE_180)
        elif self.rotate_angle == 270:
            self.image = self.image.transpose(Image.ROTATE_270)
        
        if self.mirror_h:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        if self.mirror_v:
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        
        if self.target_size:
            width, height = self.target_size
            if width > 0 and height > 0:
                self.image = self.image.resize((width, height), Image.Resampling.LANCZOS)
        
        self.show_current_image()
    
    def show_current_image(self):
        if self.image is None:
            return False
        
        temp_path = os.path.join(os.getcwd(), f"temp_preview_{int(time.time())}.jpg")
        try:
            self.image.save(temp_path)
            self.temp_files.append(temp_path)
            return self.show_image(temp_path)
        except:
            return False
    
    def save_image(self):
        if self.image is None:
            QMessageBox.warning(None, "Ошибка", "Нет изображения для сохранения")
            return None
        
        try:
            save_dir = self.get_save_dir()
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            base, ext = os.path.splitext(self.filename)
            timestamp = str(int(time.time()))
            filename = f"{base}_modified_{timestamp}{ext}"
            save_path = os.path.join(save_dir, filename)
            
            self.image.save(save_path)
            QMessageBox.information(None, "Сохранено", f"Изображение сохранено:\n{save_path}")
            return save_path
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Не удалось сохранить изображение:\n{e}")
            return None
    
    def filter_toggle(self, filter_name, enable):
        self.active_filters[filter_name] = enable
        self.apply_all_transformations()
    
    def rotate_left(self):
        if self.original_image is None:
            return
        self.rotate_angle = (self.rotate_angle + 90) % 360
        self.apply_all_transformations()
    
    def rotate_right(self):
        if self.original_image is None:
            return
        self.rotate_angle = (self.rotate_angle - 90) % 360
        self.apply_all_transformations()
    
    def mirror_horizontal(self):
        if self.original_image is None:
            return
        self.mirror_h = not self.mirror_h
        self.apply_all_transformations()
    
    def mirror_vertical(self):
        if self.original_image is None:
            return
        self.mirror_v = not self.mirror_v
        self.apply_all_transformations()
    
    def resize_image(self, width=None, height=None):
        if self.original_image is None:
            return False
        
        original_width, original_height = self.original_image.size
        
        if width is not None and height is None:
            ratio = width / original_width
            height = int(original_height * ratio)
        elif height is not None and width is None:
            ratio = height / original_height
            width = int(original_width * ratio)
        
        if width <= 0 or height <= 0:
            return False
        
        self.target_size = (width, height)
        self.apply_all_transformations()
        return True

    def set_draw_position(self, x, y):
        if self.original_image is None:
            return

        width, height = self.original_image.size
        self.draw_x = int(x * width / 100)
        self.draw_y = int(y * height / 100)

        if self.shape_type:
            self.apply_shape()
    
    def set_shape_size(self, size):
        if self.original_image is None:
            return

        width, height = self.original_image.size
        min_dimension = min(width, height)
        self.shape_size = int(size * min_dimension / 100)
        if self.shape_size < 5:
            self.shape_size = 5

        if self.shape_type:
            self.apply_shape()


    def set_draw_color(self, rgba_tuple):
        self.current_color = rgba_tuple
        if self.shape_type:
            self.apply_shape()

    def draw_shape(self, shape_type):
        self.shape_type = shape_type
        self.apply_shape()

    def apply_shape(self):
        if self.original_image is None or self.shape_type is None:
            return
        
        self.image = self.original_image.copy()
        draw = ImageDraw.Draw(self.image, 'RGBA')

        half_size = self.shape_size // 2
        left = self.draw_x - half_size
        top = self.draw_y - half_size
        right = self.draw_x + half_size
        bottom = self.draw_y + half_size

        if self.shape_type == 'square':
            draw.rectangle([left, top , right, bottom] , fill=self.current_color)
        elif self.shape_type == 'circle':
            draw.ellipse([left, top , right, bottom], fill=self.current_color)
        elif self.shape_type == 'triangle':
            top_point = (self.draw_x, top)
            left_point = (left, bottom)
            right_point = (right, bottom)
            draw.polygon([top_point, left_point, right_point], fill=self.current_color)

        self.show_current_image()




    def set_text(self, text):
        self.text_content = text
        if text and self.original_image:
            self.apply_text()

    def set_text_size(self,size):
        self.text_font_size = size
        if self.text_content and self.original_image:
            self.apply_text()

    def set_text_color(self, rgba_tuple):
        self.text_color = rgba_tuple
        if self.text_content and self.original_image:
            self.apply_text()

    def apply_text(self):
        if self.original_image is None or not self.text_content:
            return
        
        self.image = self.original_image.copy()
        draw = ImageDraw.Draw(self.image, 'RGBA')

        try:
            import sys
            if sys.platform == 'win32':
                font_path = 'C:/Windows/Fonts/arial.ttf'

            font = ImageFont.truetype(font_path, self.text_font_size)
        except:
            font = None

        width, height = self.image.size

        if font:
            try:
                bbox = draw.textbbox((0,0), self.text_content, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except:
                text_width = len(self.text_content) * self.text_font_size * 0.6
                text_height = self.text_font_size

        else:
            text_width = len(self.text_content) * self.text_font_size * 0.6
            text_height = self.text_font_size

        x = (width - text_width) / 2
        y = (height - text_height) / 2

        if font:
            draw.text((x, y), self.text_content, fill=self.text_color, font=font)
        else:
            draw.text((x, y), self.text_content, fill=self.text_color)


        self.show_current_image()

    def clear_text(self):
        self.text_content = ''
        if self.original_image:
            self.image = self.original_image.copy()
            self.show_current_image()