#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyPack 2.0 -  自动化构建工具
支持引擎: PyInstaller / Nuitka / cx_Freeze
"""

import sys
import os
import shutil
import subprocess
import tempfile
import re
import time
import stat
import ast
import locale
import math
from pathlib import Path

os.environ["QT_LOGGING_RULES"] = "qt.text.font.db=false"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
                             QPushButton, QLabel, QLineEdit, QFileDialog, QCheckBox,
                             QComboBox, QFrame, QStackedLayout, QFormLayout, QTextEdit, 
                             QGraphicsOpacityEffect, QGroupBox, QGridLayout, QTabWidget,
                             QMessageBox, QInputDialog, QFileIconProvider, QSizePolicy, QScrollArea,
                             QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QFileInfo, QVariantAnimation, QTimer, QPointF, QRectF, QRect
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent, QTextCursor, QIcon, QPixmap, QPainter, QColor, QPen
from PyQt5.QtSvg import QSvgRenderer

# ======================== Material Design 内置 SVG 引擎 ========================
MATERIAL_ICONS = {
    'settings': 'M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.06-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.73,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.06,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.43-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.49-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z',
    'refresh': 'M17.65,6.35C16.2,4.9,14.21,4,12,4c-4.42,0-7.99,3.58-7.99,8s3.57,8,7.99,8c3.73,0,6.84-2.55,7.73-6h-2.08 c-0.82,2.33-3.04,4-5.65,4c-3.31,0-6-2.69-6-6s2.69-6,6-6c1.66,0,3.14,0.69,4.22,1.78L13,11h7V4L17.65,6.35z',
    'play': 'M8 5v14l11-7z',
    'stop': 'M6 6h12v12H6z',
    'folder': 'M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z',
    'expand_more': 'M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z',
    'expand_less': 'M12 8l-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z',
    'check': 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z',
    'package': 'M20,2H4C3,2,2,2.9,2,4v3.01C2,7.73,2.43,8.35,3,8.7V20c0,1.1,1.1,2,2,2h14c0.9,0,2-0.9,2-2V8.7c0.57-0.35,1-0.97,1-1.69V4 C22,2.9,21,2,20,2z M19,20H5V9h14V20z M20,7H4V4h16V7z M9,12h6v2H9V12z',
    'back': 'M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z',
    'info': 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z',
    'python': 'M12.06,1.48c-3.14,0-3.52,0.67-3.52,0.67l-0.01,2.44h3.63v0.52H7.43C5.12,5.11,4.5,6.58,4.5,8.81c0,2.34,0.38,3.48,2.3,3.48 h1.14v-1.62c0-1.48,1.23-2.65,2.7-2.65h3.69c1.47,0,2.66-1.19,2.66-2.65V3.88C16.99,1.83,14.67,1.48,12.06,1.48z M10.22,2.83 c0.41,0,0.73,0.33,0.73,0.74c0,0.41-0.33,0.74-0.73,0.74c-0.4,0-0.73-0.33-0.73-0.74C9.49,3.16,9.82,2.83,10.22,2.83z M16.71,9.89 v1.62c0,1.48-1.23,2.65-2.7,2.65H10.3c-1.47,0-2.66,1.19-2.66,2.65v1.49c0,2.05,2.32,2.41,4.92,2.41c3.14,0,3.52-0.67,3.52-0.67 l0.01-2.44h-3.63v-0.52h4.73c2.31,0,2.93-1.47,2.93-3.7c0-2.34-0.38-3.48-2.3-3.48H16.71z M13.88,18.96c0.41,0,0.73,0.33,0.73,0.74 c0,0.41-0.33,0.74-0.73,0.74c-0.4,0-0.73-0.33-0.73-0.74C13.15,19.29,13.48,18.96,13.88,18.96z',
    'close': 'M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z'
}

def get_svg_icon(name, color="#5F6368", size=24):
    path_data = MATERIAL_ICONS.get(name, "")
    svg_str = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}"><path fill="{color}" d="{path_data}"/></svg>'
    renderer = QSvgRenderer(svg_str.encode('utf-8'))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)

def get_svg_pixmap(name, color="#5F6368", size=64):
    return get_svg_icon(name, color, size).pixmap(size, size)


# ======================== 工具与配置 ========================
def get_stdlib_names():
    libs = {'os', 'sys', 're', 'math', 'time', 'datetime', 'json', 'urllib', 'sqlite3', 'csv', 
            'subprocess', 'shutil', 'threading', 'multprocessing', 'queue', 'socket', 
            'collections', 'itertools', 'functools', 'random', 'hashlib', 'base64', 
            'binascii', 'xml', 'logging', 'argparse', 'typing', 'pathlib', 'traceback', 
            'warnings', 'tempfile', 'platform', 'zipfile', 'tarfile', 'gzip', 'bz2', 
            'lzma', 'hmac', 'ssl', 'email', 'http', 'uuid', 'io', 'contextlib', 'winreg'}
    if sys.version_info >= (3, 10): libs.update(sys.stdlib_module_names)
    return libs

STD_LIBS = get_stdlib_names()
KNOWN_MAPPINGS = {
    'win32com': 'pywin32', 'win32api': 'pywin32', 'win32con': 'pywin32', 'win32gui': 'pywin32',
    'cv2': 'opencv-python', 'PIL': 'pillow', 'bs4': 'beautifulsoup4', 'sklearn': 'scikit-learn',
    'yaml': 'pyyaml', 'fitz': 'pymupdf', 'dotenv': 'python-dotenv'
}

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

def get_python_executable():
    if getattr(sys, 'frozen', False): return shutil.which("python") or shutil.which("python3") or "python"
    return sys.executable

def remove_readonly(func, path, exc_info):
    try: os.chmod(path, stat.S_IWRITE); func(path)
    except: pass

def robust_rmtree(path: Path, retries=15, delay=0.8):
    if not path.exists(): return True
    for _ in range(retries):
        try:
            shutil.rmtree(path, onerror=remove_readonly)
            if not path.exists(): return True
        except: time.sleep(delay)
    return False


# ======================== 界面动效组件 ========================
class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        
        self.animation_group = QParallelAnimationGroup()
        self.pos_anim = QPropertyAnimation(self, b"geometry")
        self.pos_anim.setDuration(150)
        self.pos_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        self.op_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.op_anim.setDuration(200)
        self.op_anim.setEasingCurve(QEasingCurve.InOutCubic)
        
        self.is_hovered = False

    def enterEvent(self, event):
        if not self.is_hovered and self.isEnabled():
            self.is_hovered = True
            geom = self.geometry()
            self.pos_anim.setStartValue(geom)
            self.pos_anim.setEndValue(geom.adjusted(0, -2, 0, -2))
            self.op_anim.setStartValue(1.0)
            self.op_anim.setEndValue(0.85)
            self.animation_group.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.is_hovered and self.isEnabled():
            self.is_hovered = False
            geom = self.geometry()
            self.pos_anim.setStartValue(geom)
            self.pos_anim.setEndValue(geom.adjusted(0, 2, 0, 2))
            self.op_anim.setStartValue(0.85)
            self.op_anim.setEndValue(1.0)
            self.animation_group.start()
        super().leaveEvent(event)

class TargetIconWidget(QWidget):
    """自定义图标渲染组件，接管无损抗锯齿与复合重绘效果"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.pixmap = None
        self.base_pixmap = None
        self.file_pixmap = None  # 用于专门记住当前加载文件的专属图标
        self.current_size = 88
        
        self.is_building = False
        self.spin_angle = 0
        self.pulse_value = 0
        
        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(16) # ~60fps
        self.anim_timer.timeout.connect(self._update_frame)
        
        self.success_effect = QGraphicsDropShadowEffect(self)
        self.success_effect.setOffset(0, 0)
        self.success_effect.setColor(QColor(0, 0, 0, 0))
        self.success_effect.setBlurRadius(0)
        self.setGraphicsEffect(self.success_effect)
        
        self.burst_value = 0.0
        self.burst_anim = QVariantAnimation(self)
        self.burst_anim.setDuration(600)
        self.burst_anim.setLoopCount(1)
        self.burst_anim.setStartValue(0.0)
        self.burst_anim.setEndValue(1.0)
        self.burst_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.burst_anim.valueChanged.connect(self._animate_burst)

        # 抖动动画配置（用于构建失败）
        self.shake_offset = 0
        self.shake_anim = QVariantAnimation(self)
        self.shake_anim.setDuration(500)
        self.shake_anim.setStartValue(0)
        self.shake_anim.setEndValue(0)
        self.shake_anim.setKeyValueAt(0.0, 0)
        self.shake_anim.setKeyValueAt(0.1, -12)
        self.shake_anim.setKeyValueAt(0.3, 12)
        self.shake_anim.setKeyValueAt(0.5, -12)
        self.shake_anim.setKeyValueAt(0.7, 12)
        self.shake_anim.setKeyValueAt(0.9, -6)
        self.shake_anim.setKeyValueAt(1.0, 0)
        self.shake_anim.valueChanged.connect(self._animate_shake)

    def set_default_pixmap(self, pixmap, size=88):
        self.base_pixmap = pixmap
        self.pixmap = pixmap
        self.current_size = size
        self.update()
        
    def set_custom_pixmap(self, pixmap, size=88):
        self.pixmap = pixmap
        self.current_size = size
        self.update()

    def set_file_pixmap(self, pixmap, size=88):
        self.file_pixmap = pixmap
        self.pixmap = pixmap
        self.current_size = size
        self.update()

    def start_building(self):
        # 恢复之前保存的文件专属图标，覆盖掉可能残留的“成功”或“失败”图标
        if getattr(self, 'file_pixmap', None) and not self.file_pixmap.isNull():
            self.pixmap = self.file_pixmap
            self.current_size = 88
            
        self.is_building = True
        self.spin_angle = 0
        self.pulse_value = 0
        self.burst_value = 0.0
        self.shake_offset = 0
        self.success_effect.setColor(QColor(0, 0, 0, 0))
        self.burst_anim.stop()
        self.shake_anim.stop()
        self.anim_timer.start()
        
    def stop_building(self):
        self.is_building = False
        self.anim_timer.stop()
        self.update()
        
    def start_success(self):
        self.stop_building()
        self.success_effect.setBlurRadius(40)
        self.success_effect.setColor(QColor(255, 193, 7, 180))
        self.burst_anim.start()

    def start_failure(self):
        self.stop_building()
        self.success_effect.setBlurRadius(40)
        self.success_effect.setColor(QColor(217, 48, 37, 180)) # 红色警告发光
        self.shake_anim.start()
        
    def reset(self):
        self.stop_building()
        self.burst_anim.stop()
        self.shake_anim.stop()
        self.burst_value = 0.0
        self.shake_offset = 0
        self.success_effect.setColor(QColor(0, 0, 0, 0))
        self.file_pixmap = None  # 清空文件专属图标
        self.pixmap = self.base_pixmap
        self.current_size = 88
        self.update()
        
    def _update_frame(self):
        self.spin_angle = (self.spin_angle + 4) % 360
        self.pulse_value += 0.05
        self.update()
        
    def _animate_burst(self, val):
        self.burst_value = val
        self.update()

    def _animate_shake(self, val):
        self.shake_offset = val
        self.update()

    def paintEvent(self, event):
        if not self.pixmap or self.pixmap.isNull():
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        center = self.rect().center()
        center_x = center.x() + int(self.shake_offset)
        icon_center_y = center.y()
        draw_size = self.current_size
        
        if self.is_building:
            radius = (self.current_size / 2) + 12
            pen = QPen(QColor(26, 115, 232, 200))
            pen.setWidth(4)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            
            rect = QRectF(center_x - radius, center.y() - radius, radius * 2, radius * 2)
            span_angle = int((140 + 60 * math.sin(self.pulse_value * 1.5)) * 16)
            start_angle = int(-self.spin_angle * 16)
            painter.drawArc(rect, start_angle, span_angle)
            
        elif self.burst_value > 0.0:
            pop_scale = 1.0 + math.sin(self.burst_value * math.pi) * 0.15
            draw_size = int(self.current_size * pop_scale)
            
            if self.burst_value < 1.0:
                alpha = int(255 * (1.0 - self.burst_value))
                painter.setPen(Qt.NoPen)
                
                painter.setBrush(QColor(26, 115, 232, alpha))
                burst_radius_1 = (self.current_size / 2) + 10 + self.burst_value * 40
                dot_size_1 = 8 * (1.0 - self.burst_value)
                for i in range(8):
                    angle = math.radians(i * 45)
                    dx = center_x + math.cos(angle) * burst_radius_1
                    dy = center.y() + math.sin(angle) * burst_radius_1
                    painter.drawEllipse(QPointF(dx, dy), dot_size_1, dot_size_1)
                
                painter.setBrush(QColor(255, 193, 7, alpha))
                burst_radius_2 = (self.current_size / 2) + self.burst_value * 65
                dot_size_2 = 6 * (1.0 - self.burst_value)
                for i in range(8):
                    angle = math.radians(i * 45 + 22.5)
                    dx = center_x + math.cos(angle) * burst_radius_2
                    dy = center.y() + math.sin(angle) * burst_radius_2
                    painter.drawEllipse(QPointF(dx, dy), dot_size_2, dot_size_2)
        
        pix_rect = QRect(
            int(center_x - draw_size / 2), 
            int(icon_center_y - draw_size / 2), 
            draw_size, 
            draw_size
        )
        scaled_pix = self.pixmap.scaled(draw_size, draw_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        painter.drawPixmap(pix_rect, scaled_pix)
        painter.end()


class DropArea(QFrame):
    fileDropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DropArea") 
        self.setAcceptDrops(True)
        self.setFrameStyle(QFrame.NoFrame)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            #DropArea { background-color: #f8f9fa; border: 2px dashed #dadce0; border-radius: 12px; }
            #DropArea:hover { background-color: #f1f3f4; border: 2px dashed #bdc1c6; }
        """)
        self.init_ui()

    def _get_default_pixmap(self, size=88):
        icon_path = get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            pixmap = QIcon(icon_path).pixmap(size, size)
            if not pixmap.isNull():
                return pixmap
        return get_svg_pixmap('python', color="#9AA0A6", size=size)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(0)
        
        layout.addStretch(1)
        
        self.icon_widget = TargetIconWidget(self)
        self.icon_widget.set_default_pixmap(self._get_default_pixmap(88))
        
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(self.icon_widget)
        h_layout.addStretch(1)
        layout.addLayout(h_layout)
        
        layout.addSpacing(18)
        
        self.label = QLabel("将脚本(.py)拖拽至此处\n或 点击浏览")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel { background: transparent; color: #5F6368; font-size: 16px; font-weight: bold; border: none; }")
        layout.addWidget(self.label)
        
        layout.addSpacing(8)
        
        self.sub_label = QLabel("智能解析工程依赖、附件及隐藏模块")
        self.sub_label.setAlignment(Qt.AlignCenter)
        self.sub_label.setStyleSheet("QLabel { background: transparent; color: #9AA0A6; font-size: 13px; border: none; }")
        layout.addWidget(self.sub_label)
        
        layout.addStretch(1)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and event.mimeData().urls()[0].toLocalFile().lower().endswith('.py'):
            event.acceptProposedAction()
            self.setStyleSheet("#DropArea { background-color: #E8F0FE; border: 2px dashed #1A73E8; border-radius: 12px; }")

    def dragLeaveEvent(self, event):
        self.setStyleSheet("#DropArea { background-color: #f8f9fa; border: 2px dashed #dadce0; border-radius: 12px; } #DropArea:hover { background-color: #f1f3f4; border: 2px dashed #bdc1c6; }")

    def dropEvent(self, event: QDropEvent):
        self.dragLeaveEvent(event)
        urls = event.mimeData().urls()
        if urls and urls[0].toLocalFile().lower().endswith('.py'):
            self.fileDropped.emit(urls[0].toLocalFile())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            fp, _ = QFileDialog.getOpenFileName(self, "选择 Python 源代码文件", "", "Python Scripts (*.py)")
            if fp: self.fileDropped.emit(fp)

    def set_success(self, filename, custom_icon_path=None):
        pixmap = None
        if custom_icon_path and Path(custom_icon_path).exists():
            pixmap = QIcon(str(custom_icon_path)).pixmap(88, 88)
            if pixmap.isNull():
                pixmap = None
                
        if not pixmap:
            pixmap = get_svg_pixmap('package', color="#1A73E8", size=88)
            
        # 使用 set_file_pixmap，避免覆盖 base_pixmap 导致复位失败
        self.icon_widget.set_file_pixmap(pixmap, 88)
            
        self.label.setText(f"已加载：{filename}")
        self.label.setStyleSheet("QLabel { background: transparent; color: #1A73E8; font-size: 16px; font-weight: bold; border: none; }")
        self.sub_label.setText("准备就绪，随时可开始构建")

    def start_build_anim(self):
        self.sub_label.setText("正在执行模块提取与打包...")
        self.icon_widget.start_building()

    def stop_build_anim(self):
        self.icon_widget.stop_building()

    def show_success(self, custom_icon_path=None):
        size = 128
        pixmap_set = False
        if custom_icon_path and Path(custom_icon_path).exists():
            pix = QIcon(str(custom_icon_path)).pixmap(size, size)
            if not pix.isNull():
                self.icon_widget.set_custom_pixmap(pix, size)
                pixmap_set = True
                
        if not pixmap_set:
            if self.icon_widget.base_pixmap and not self.icon_widget.base_pixmap.isNull():
                self.icon_widget.set_custom_pixmap(self.icon_widget.base_pixmap, size)
            else:
                self.icon_widget.set_custom_pixmap(get_svg_pixmap('check', color="#1E8E3E", size=size), size)
            
        self.icon_widget.start_success()
            
        self.label.setText("构建完成！")
        self.label.setStyleSheet("QLabel { background: transparent; color: #1E8E3E; font-size: 20px; font-weight: bold; border: none; }")
        self.sub_label.setText("可打开目录查看或重置工作区")

    def show_failure(self):
        size = 128
        self.icon_widget.set_custom_pixmap(get_svg_pixmap('close', color="#D93025", size=size), size)
        self.icon_widget.start_failure()
        
        self.label.setText("构建失败！")
        self.label.setStyleSheet("QLabel { background: transparent; color: #D93025; font-size: 20px; font-weight: bold; border: none; }")
        self.sub_label.setText("请检查下方的日志诊断报告")
        
    def reset(self):
        self.icon_widget.reset()
        self.label.setText("将脚本(.py)拖拽至此处\n或 点击浏览")
        self.label.setStyleSheet("QLabel { background: transparent; color: #5F6368; font-size: 16px; font-weight: bold; border: none; }")
        self.sub_label.setText("智能解析工程依赖、附件及隐藏模块")


# ======================== 设置面板 ========================
class SettingsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_win = parent
        self.setStyleSheet("""
            SettingsPanel { background-color: white; }
            QLabel { color: #3c4043; font-size: 13px; font-weight: bold; background: transparent; }
            QComboBox, QLineEdit { color: #3c4043; font-size: 13px; padding: 6px 10px; border: 1px solid #dadce0; border-radius: 6px; background: #fff; min-height: 24px; }
            QComboBox:hover, QLineEdit:hover { border-color: #bdc1c6; }
            QComboBox:focus, QLineEdit:focus { border-color: #1A73E8; }
            QGroupBox { border: 1px solid #e8eaed; border-radius: 8px; margin-top: 15px; padding-top: 15px; background-color: #f8f9fa; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; left: 15px; top: 0px; color: #1A73E8; font-weight: bold; font-size: 13px; padding: 0 5px; background: transparent; }
            QCheckBox { font-size: 13px; color: #3c4043; spacing: 8px; background: transparent; }
            QCheckBox::indicator { width: 16px; height: 16px; border: 1px solid #bdc1c6; border-radius: 4px; background: white; }
            QCheckBox::indicator:checked { background: #1A73E8; border-color: #1A73E8; image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='white'><path d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/></svg>"); }
            QPushButton.ToolBtn { padding: 5px 12px; border: 1px solid #dadce0; border-radius: 6px; background: #f1f3f4; font-size: 12px; font-weight: bold; color: #5f6368;}
            QPushButton.ToolBtn:hover { background: #e8eaed; color: #202124; }
            QTabWidget::pane { border: 1px solid #e8eaed; border-radius: 8px; background: white; top: -1px; }
            QTabBar::tab { background: #f1f3f4; border: 1px solid #e8eaed; padding: 10px 20px; margin-right: 4px; border-top-left-radius: 8px; border-top-right-radius: 8px; color: #5f6368; font-weight: bold; font-size: 13px; }
            QTabBar::tab:selected { background: white; border-bottom-color: white; color: #1A73E8; }
            QTabBar::tab:hover:!selected { background: #e8eaed; }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15) 
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.tabs = QTabWidget()
        self.tab_basic = QWidget()
        self.tab_env = QWidget()
        self.tab_adv = QWidget()
        self.tab_meta = QWidget()
        
        self.tabs.addTab(self.tab_basic, get_svg_icon('package', "#1A73E8"), " 基础打包")
        self.tabs.addTab(self.tab_env, get_svg_icon('python', "#1A73E8"), " 环境与依赖")
        self.tabs.addTab(self.tab_adv, get_svg_icon('settings', "#1A73E8"), " 高级选项")
        self.tabs.addTab(self.tab_meta, get_svg_icon('info', "#1A73E8"), " 版本信息")
        
        self.build_basic_tab()
        self.build_env_tab()
        self.build_adv_tab()
        self.build_meta_tab()
        layout.addWidget(self.tabs)
        
        btn_lay = QHBoxLayout()
        btn_lay.setContentsMargins(0, 5, 0, 0)
        btn_lay.setSpacing(12)
        
        self.btn_reset = AnimatedButton("")
        self.btn_reset.setFixedSize(44, 44)
        self.btn_reset.setIcon(get_svg_icon('refresh', "#5F6368"))
        self.btn_reset.setToolTip("恢复默认配置")
        self.btn_reset.setStyleSheet(self.parent_win.icon_btn_style)
        self.btn_reset.clicked.connect(self.parent_win.reset_all)
        btn_lay.addWidget(self.btn_reset)
        
        self.btn_save = AnimatedButton(" 保存并返回工作区")
        self.btn_save.setFixedHeight(44)
        self.btn_save.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_save.setIcon(get_svg_icon('check', "white"))
        self.btn_save.setStyleSheet(self.parent_win.primary_btn_style)
        self.btn_save.clicked.connect(self.parent_win.show_main)
        btn_lay.addWidget(self.btn_save)

        self.btn_back = AnimatedButton("")
        self.btn_back.setFixedSize(44, 44)
        self.btn_back.setIcon(get_svg_icon('back', "#5F6368"))
        self.btn_back.setToolTip("放弃修改并返回")
        self.btn_back.setStyleSheet(self.parent_win.icon_btn_style)
        self.btn_back.clicked.connect(self.parent_win.show_main)
        btn_lay.addWidget(self.btn_back)
        
        layout.addLayout(btn_lay)

    def build_basic_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        content.setStyleSheet("background: white;")
        lay = QVBoxLayout(content)
        lay.setContentsMargins(15, 15, 15, 15)
        
        grp_core = QGroupBox("核心参数")
        form_core = QFormLayout(grp_core)
        form_core.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_core.setContentsMargins(15, 20, 15, 15)
        form_core.setVerticalSpacing(12)
        
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["PyInstaller", "Nuitka", "cx_Freeze"])
        self.engine_combo.currentIndexChanged.connect(self.on_engine_changed)
        form_core.addRow("构建引擎:", self.engine_combo)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("留空则与入口脚本同名")
        form_core.addRow("输出名称:", self.name_edit)
        
        self.icon_edit = QLineEdit()
        self.icon_preview = QLabel()
        self.icon_preview.setFixedSize(28, 28)
        self.icon_preview.setScaledContents(True)
        self.icon_edit.textChanged.connect(self.update_icon_preview)
        btn_icon = QPushButton("浏览...")
        btn_icon.setProperty("class", "ToolBtn")
        btn_icon.clicked.connect(self.select_icon)
        h_icon = QHBoxLayout()
        h_icon.addWidget(self.icon_edit)
        h_icon.addWidget(self.icon_preview)
        h_icon.addWidget(btn_icon)
        form_core.addRow("应用图标:", h_icon)
        lay.addWidget(grp_core)

        grp_mode = QGroupBox("输出模式与行为")
        grid_mode = QGridLayout(grp_mode)
        grid_mode.setContentsMargins(15, 20, 15, 15)
        grid_mode.setVerticalSpacing(15)
        
        self.onefile_check = QCheckBox("单文件模式 (OneFile)")
        self.onefile_check.setChecked(True)
        self.noconsole_check = QCheckBox("隐藏控制台 (GUI模式)")
        self.noconsole_check.setChecked(True)
        self.clean_all_check = QCheckBox("编译后自动清理缓存")
        self.clean_all_check.setChecked(True)
        self.auto_icon_check = QCheckBox("自动匹配同目录图标")
        self.auto_icon_check.setChecked(True)
        
        grid_mode.addWidget(self.onefile_check, 0, 0)
        grid_mode.addWidget(self.noconsole_check, 0, 1)
        grid_mode.addWidget(self.clean_all_check, 1, 0)
        grid_mode.addWidget(self.auto_icon_check, 1, 1)
        lay.addWidget(grp_mode)
        
        lay.addStretch() 
        scroll.setWidget(content)
        main_lay = QVBoxLayout(self.tab_basic)
        main_lay.setContentsMargins(0,0,0,0)
        main_lay.addWidget(scroll)

    def build_env_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        content.setStyleSheet("background: white;")
        lay = QVBoxLayout(content)
        lay.setContentsMargins(15, 15, 15, 15)
        
        grp_env = QGroupBox("隔离与网络")
        form_env = QFormLayout(grp_env)
        form_env.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_env.setContentsMargins(15, 20, 15, 15)
        form_env.setVerticalSpacing(12)
        
        self.pip_source_edit = QLineEdit("https://pypi.tuna.tsinghua.edu.cn/simple")
        form_env.addRow("PIP 镜像:", self.pip_source_edit)
        
        self.venv_check = QCheckBox("启用独立虚拟环境 (推荐，保证依赖纯净)")
        self.venv_check.setChecked(True)
        form_env.addRow("", self.venv_check)
        lay.addWidget(grp_env)

        grp_dep = QGroupBox("包与依赖分析机制")
        dep_lay = QVBoxLayout(grp_dep)
        dep_lay.setContentsMargins(15, 20, 15, 15)
        dep_lay.setSpacing(15)

        grid_dep = QGridLayout()
        self.reqs_check = QCheckBox("优先读取 requirements.txt")
        self.reqs_check.setChecked(True)
        self.pipreqs_check = QCheckBox("启用 pipreqs 深度代码分析")
        self.pipreqs_check.setChecked(True)
        grid_dep.addWidget(self.reqs_check, 0, 0)
        grid_dep.addWidget(self.pipreqs_check, 0, 1)
        dep_lay.addLayout(grid_dep)

        form_dep = QFormLayout()
        form_dep.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.hidden_edit = QLineEdit()
        self.hidden_edit.setPlaceholderText("例如: pandas, PyQt5 (逗号分隔)")
        btn_scan = QPushButton("AST 扫描")
        btn_scan.setProperty("class", "ToolBtn")
        btn_scan.clicked.connect(self.auto_scan_hidden)
        h_hid = QHBoxLayout()
        h_hid.addWidget(self.hidden_edit)
        h_hid.addWidget(btn_scan)
        form_dep.addRow("隐式依赖:", h_hid)
        dep_lay.addLayout(form_dep)
        
        lay.addWidget(grp_dep)
        lay.addStretch()
        
        scroll.setWidget(content)
        main_lay = QVBoxLayout(self.tab_env)
        main_lay.setContentsMargins(0,0,0,0)
        main_lay.addWidget(scroll)

    def build_adv_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        content.setStyleSheet("background: white;")
        lay = QVBoxLayout(content)
        lay.setContentsMargins(15, 15, 15, 15)
        
        grp_res = QGroupBox("附加资源与优化")
        form_res = QFormLayout(grp_res)
        form_res.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_res.setContentsMargins(15, 20, 15, 15)
        form_res.setVerticalSpacing(12)
        
        self.add_data_edit = QLineEdit()
        self.add_data_edit.setPlaceholderText("例如: data/*:data (跨平台自动处理路径)")
        btn_add = QPushButton("添加...")
        btn_add.setProperty("class", "ToolBtn")
        btn_add.clicked.connect(self.add_resource)
        h_res = QHBoxLayout()
        h_res.addWidget(self.add_data_edit)
        h_res.addWidget(btn_add)
        form_res.addRow("附加资源:", h_res)
        
        self.upx_check = QCheckBox("启用 UPX 压缩优化 (仅 PyInstaller)")
        form_res.addRow("", self.upx_check)
        lay.addWidget(grp_res)
        lay.addStretch()
        
        scroll.setWidget(content)
        main_lay = QVBoxLayout(self.tab_adv)
        main_lay.setContentsMargins(0,0,0,0)
        main_lay.addWidget(scroll)

    def build_meta_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        content.setStyleSheet("background: white;")
        lay = QVBoxLayout(content)
        lay.setContentsMargins(15, 15, 15, 15)
        
        self.grp_meta = QGroupBox("版本元数据 (Metadata)")
        meta_form = QFormLayout(self.grp_meta)
        meta_form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        meta_form.setContentsMargins(15, 20, 15, 15)
        meta_form.setVerticalSpacing(12)
        
        self.ver_ver = QLineEdit("1.0.0")
        self.ver_comp = QLineEdit("My Studio")
        self.ver_desc = QLineEdit("Python Executable")
        meta_form.addRow("版本序列:", self.ver_ver)
        meta_form.addRow("发行公司:", self.ver_comp)
        meta_form.addRow("文件描述:", self.ver_desc)
        lay.addWidget(self.grp_meta)
        
        tip = QLabel("注：仅 PyInstaller 和 Nuitka 引擎支持写入 EXE 版本信息。")
        tip.setStyleSheet("color: #9AA0A6; font-size: 12px; font-weight: normal; background: transparent;")
        lay.addWidget(tip)
        lay.addStretch()
        
        scroll.setWidget(content)
        main_lay = QVBoxLayout(self.tab_meta)
        main_lay.setContentsMargins(0,0,0,0)
        main_lay.addWidget(scroll)

    def on_engine_changed(self):
        engine = self.engine_combo.currentText()
        self.onefile_check.setVisible(engine in ("PyInstaller", "Nuitka"))
        self.upx_check.setVisible(engine == "PyInstaller")
        self.tabs.setTabEnabled(3, engine != "cx_Freeze")

    def update_icon_preview(self, path):
        if path and Path(path).exists():
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                self.icon_preview.setPixmap(pixmap.scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                return
        self.icon_preview.clear()

    def select_icon(self):
        p, _ = QFileDialog.getOpenFileName(self, "选择图标", "", "Icon Files (*.ico)")
        if p: self.icon_edit.setText(Path(p).resolve().as_posix())

    def auto_scan_hidden(self):
        script_path = self.parent_win.script_path
        if not script_path: return QMessageBox.warning(self, "提示", "请先在主界面加载脚本！")
        try:
            raw = Path(script_path).read_bytes()
            if b"__CLOUDSYNC_ENC__" in raw[:1024]: return QMessageBox.critical(self, "错误", "脚本被云盘加密，请解密！")
            try: code = raw.decode('utf-8-sig')
            except: code = raw.decode('gbk', errors='ignore')
            
            hidden = set()
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names: hidden.add(alias.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                        hidden.add(node.module.split('.')[0])
            except:
                hidden = set(re.findall(r'^\s*(?:from|import)\s+([a-zA-Z0-9_]+)', code, re.M))

            hidden = [m for m in hidden if m not in STD_LIBS]
            self.hidden_edit.setText(','.join(hidden))
            QMessageBox.information(self, "扫描完成", f"捕获到 {len(hidden)} 项依赖。")
        except Exception as e: QMessageBox.critical(self, "错误", f"扫描失败: {e}")

    def add_resource(self):
        choice = QMessageBox.question(self, "添加资源", "Yes=文件, No=文件夹", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            files, _ = QFileDialog.getOpenFileNames(self, "选择文件", "", "All Files (*)")
            for f in files:
                f = Path(f).resolve().as_posix()
                default_dest = Path(f).name
                dest, ok = QInputDialog.getText(self, "相对路径", f"目标位置:", text=default_dest)
                if ok:
                    dest = dest.strip().replace('\\', '/') if dest else default_dest
                    curr = self.add_data_edit.text().strip()
                    self.add_data_edit.setText(f"{curr}, {f}:{dest}" if curr else f"{f}:{dest}")
        else:
            folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
            if folder:
                folder = Path(folder).resolve().as_posix()
                default_dest = Path(folder).name
                dest, ok = QInputDialog.getText(self, "相对路径", f"目标位置:", text=default_dest)
                if ok:
                    dest = dest.strip().replace('\\', '/') if dest else default_dest
                    curr = self.add_data_edit.text().strip()
                    self.add_data_edit.setText(f"{curr}, {folder}:{dest}" if curr else f"{folder}:{dest}")


# ======================== 核心构建引擎 ========================
class PackingThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, params):
        super().__init__()
        self.params = params
        self.process = None
        self._is_cancelled = False
        self.venv_dir = None
        self.temp_workpath = None
        self.temp_out_dir = None

    def cancel(self):
        self._is_cancelled = True
        if self.process:
            try:
                if os.name == "nt": subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.pid)], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                else: self.process.kill()
            except: pass

    def run_cmd(self, cmd, cwd=None):
        if self._is_cancelled: return False
        try:
            kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT, "cwd": cwd, "text": True, "errors": "replace"}
            if os.name == 'nt': kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
            
            self.process = subprocess.Popen(cmd, **kwargs)
            for line in self.process.stdout:
                if self._is_cancelled:
                    self.process.terminate()
                    return False
                self.progress.emit(line.strip())
            
            self.process.wait()
            return self.process.returncode == 0
        except Exception as e:
            self.progress.emit(f"[系统异常] 进程执行失败: {e}")
            return False

    def sanitize_script(self, orig_path: Path):
        try:
            raw = orig_path.read_bytes()
            if b"__CLOUDSYNC_ENC__" in raw[:1024]: 
                return None, False, "目标脚本被云盘锁定加密！"
        except Exception:
            pass
        # 移除了所有重命名及生成 pypack_temp_ 前缀文件的死代码
        # 直接透传原始文件可防止 Nuitka 生成带有临时前缀的 DLL 触发 Windows 智能应用控制的启发式拦截
        return orig_path, False, ""

    def run(self):
        os.environ["NUITKA_ACCEPT_DOWNLOADS"] = "yes"
        engine = self.params['engine']
        pip_idx = self.params.get('pip_index_url', '').strip()
        is_temp = False
        build_script_path = None
        ext = ".exe" if os.name == "nt" else ""

        try:
            self.progress.emit("[清理] 初始化构建管线...")
            robust_rmtree(Path.cwd() / "build")
            robust_rmtree(Path.cwd() / "dist")
            
            script_path = Path(self.params['script_path']).resolve()
            script_dir = script_path.parent
            
            build_script_path, is_temp, err_msg = self.sanitize_script(script_path)
            if not build_script_path and err_msg: return self.finished.emit(False, f"[安全拦截] {err_msg}")
            script_posix = build_script_path.as_posix()

            if self.params['use_venv']:
                self.progress.emit("[环境] 初始化虚拟隔离沙盒...")
                self.venv_dir = Path(tempfile.mkdtemp(prefix="pypack_env_")).resolve()
                if not self.run_cmd([get_python_executable(), "-m", "venv", self.venv_dir.as_posix()]):
                    return self.finished.emit(False, "虚拟环境初始化失败。")
                python_exe = (self.venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")).as_posix()
            else: python_exe = Path(get_python_executable()).resolve().as_posix()

            pip_args = ["-i", pip_idx] if pip_idx else []
            engine_pkg = "nuitka[onefile]" if engine == "Nuitka" else "cx_Freeze" if engine == "cx_Freeze" else "pyinstaller"
            
            self.progress.emit(f"[环境] 下载核心组件...")
            core_pkgs = [engine_pkg]
            if engine == "PyInstaller": core_pkgs.append("pillow")
            self.run_cmd([python_exe, "-m", "pip", "install", "-q"] + core_pkgs + pip_args)
            
            req_success = False
            if self.params.get('use_reqs'):
                req_file = script_dir / "requirements.txt"
                if req_file.exists():
                    self.progress.emit("[依赖] 部署 requirements.txt...")
                    try:
                        raw_req = req_file.read_bytes()
                        if b"__CLOUDSYNC_ENC__" in raw_req[:1024]: raise ValueError("文件被锁定")
                        try: req_content = raw_req.decode('utf-8-sig')
                        except: req_content = raw_req.decode(locale.getpreferredencoding(), errors='ignore')
                        temp_req = script_dir / "pypack_temp_reqs.txt"
                        temp_req.write_text(req_content, encoding='utf-8')
                        if self.run_cmd([python_exe, "-m", "pip", "install", "-q", "-r", temp_req.as_posix()] + pip_args):
                            req_success = True
                        temp_req.unlink(missing_ok=True)
                    except Exception as e: self.progress.emit(f"[警告] {e}")
            if self.params.get('use_pipreqs') and not req_success:
                self.progress.emit("[依赖] 执行 pipreqs 深度推导...")
                self.run_cmd([python_exe, "-m", "pip", "install", "pipreqs", "-q"] + pip_args)
                temp_pipreqs = script_dir / "pypack_pipreqs_out.txt"
                self.run_cmd([python_exe, "-m", "pipreqs.pipreqs", script_dir.as_posix(), "--encoding", "utf-8", "--force", "--savepath", temp_pipreqs.as_posix()])
                if temp_pipreqs.exists():
                    if self.run_cmd([python_exe, "-m", "pip", "install", "-q", "-r", temp_pipreqs.as_posix()] + pip_args): req_success = True
                    temp_pipreqs.unlink(missing_ok=True)
            if not req_success and (self.params.get('use_reqs') or self.params.get('use_pipreqs')):
                self.progress.emit("[依赖] 执行 AST 语法树降级解析...")
                try:
                    code = build_script_path.read_text(encoding='utf-8', errors='ignore')
                    third_party = set()
                    try:
                        for node in ast.walk(ast.parse(code)):
                            if isinstance(node, ast.Import):
                                for alias in node.names: third_party.add(alias.name.split('.')[0])
                            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                                third_party.add(node.module.split('.')[0])
                    except: third_party = set(re.findall(r'^\s*(?:from|import)\s+([a-zA-Z0-9_]+)', code, re.M))
                    
                    pkgs_to_install = [KNOWN_MAPPINGS.get(m, m) for m in third_party if m not in STD_LIBS]
                    if pkgs_to_install:
                        self.progress.emit(f"[依赖] 同步外部模块: {', '.join(pkgs_to_install)}")
                        self.run_cmd([python_exe, "-m", "pip", "install", "-q"] + pkgs_to_install + pip_args)
                except Exception as e: self.progress.emit(f"[异常] {e}")

            if self._is_cancelled: return self.finished.emit(False, "构建已被中断。")

            self.progress.emit(f"[编译] 启动 {engine} 封装引擎...")
            cmd = []
            app_name = self.params['app_name']
            icon_path = Path(self.params['icon']).resolve().as_posix() if self.params.get('icon') else None

            if engine == "PyInstaller":
                self.temp_workpath = Path(tempfile.mkdtemp(prefix="pypack_build_")).resolve()
                cmd = [python_exe, "-m", "PyInstaller", "--clean", "-y", f"--workpath={self.temp_workpath.as_posix()}", f"--name={app_name}"]
                if self.params.get('onefile'): cmd.append("--onefile")
                else: cmd.append("--onedir")
                if self.params.get('noconsole'): cmd.append("--noconsole")
                
                if icon_path: 
                    cmd.extend(["--icon", icon_path])
                    sep = ';' if os.name == 'nt' else ':'
                    cmd.extend(["--add-data", f"{icon_path}{sep}."])
                    
                if self.params.get('version_file') and os.name == "nt": cmd.extend(["--version-file", self.params['version_file']])
                if self.params.get('upx'):
                    upx_dir = (Path.cwd() / "upx").resolve()
                    if upx_dir.exists(): cmd.append(f"--upx-dir={upx_dir.as_posix()}")
                
                for imp in self.params.get('hidden_imports', '').split(','):
                    if imp.strip(): cmd.extend(["--hidden-import", imp.strip()])
                for d in self.params.get('add_data', '').split(','):
                    d = d.strip()
                    if d:
                        d = d.replace('\\', '/')
                        if os.name == 'nt' and ':' in d and ';' not in d:
                            parts = d.rsplit(':', 1)
                            if len(parts) == 2: d = f"{parts[0]};{parts[1]}"
                        cmd.extend(["--add-data", d])
                        
            elif engine == "Nuitka":
                self.temp_out_dir = Path(tempfile.mkdtemp(prefix="nuitka_out_")).resolve()
                cmd = [python_exe, "-m", "nuitka", "--remove-output", "--assume-yes-for-downloads",
                       f"--output-dir={self.temp_out_dir.as_posix()}", f"--output-filename={app_name}{ext}"]
                
                cmd.append(f"--jobs={os.cpu_count() or 4}")
                
                if self.params.get('onefile'): cmd.append("--onefile")
                else: cmd.append("--standalone")
                if self.params.get('noconsole'): cmd.append("--windows-console-mode=disable")
                
                if icon_path: 
                    if os.name == "nt":
                        cmd.append(f"--windows-icon-from-ico={icon_path}")
                    elif sys.platform == "darwin" and icon_path.endswith(".icns"):
                        cmd.append(f"--macos-app-icon={icon_path}")
                    # 使用精确的文件名作为目标部署位置，以避开 Nuitka '.' 校验致命错误
                    cmd.append(f"--include-data-files={icon_path}={Path(icon_path).name}")
                    
                if os.name == "nt":
                    if self.params.get('ver_comp'): cmd.append(f"--company-name={self.params['ver_comp']}")
                    if self.params.get('ver_desc'): cmd.append(f"--product-name={self.params['ver_desc']}")
                    if self.params.get('ver_ver'): cmd.append(f"--file-version={self.params['ver_ver']}")
                    
                try:
                    if 'PyQt5' in build_script_path.read_text(encoding='utf-8', errors='ignore'):
                        cmd.append("--enable-plugin=pyqt5")
                except: pass
                
                for imp in self.params.get('hidden_imports', '').split(','):
                    if imp.strip(): cmd.append(f"--include-module={imp.strip()}")
                for d in self.params.get('add_data', '').split(','):
                    d = d.strip()
                    if d:
                        d = d.replace('\\', '/')
                        parts = d.split(':', 1)
                        if len(parts) == 2: 
                            cmd.append(f"--include-data-files={parts[0]}={parts[1]}")
                            
            elif engine == "cx_Freeze":
                cmd = [python_exe, "-m", "cx_Freeze", script_posix, f"--target-dir=dist/{app_name}", f"--target-name={app_name}{ext}"]
                if self.params.get('noconsole'): cmd.append("--base=Win32GUI")
                else: cmd.append("--base=Console")
                
                add_data_list = []
                if icon_path: 
                    cmd.extend(["--icon", icon_path])
                    add_data_list.append(f"{icon_path}={Path(icon_path).name}")
                for imp in self.params.get('hidden_imports', '').split(','):
                    if imp.strip(): cmd.extend(["--include-modules", imp.strip()])
                for d in self.params.get('add_data', '').split(','):
                    d = d.strip()
                    if d:
                        d = d.replace('\\', '/')
                        parts = d.split(':', 1)
                        if len(parts) == 2: add_data_list.append(f"{parts[0]}={parts[1]}")
                if add_data_list: cmd.append(f"--include-files={','.join(add_data_list)}")

            if engine in ["PyInstaller", "Nuitka"]: cmd.append(script_posix)

            success = self.run_cmd(cmd, cwd=Path.cwd().resolve().as_posix())
            if self._is_cancelled: return self.finished.emit(False, "构建已被中断。")

            self.progress.emit("[收尾] 归档可执行文件...")
            cwd = Path.cwd().resolve()
            if engine == "PyInstaller": src_out = cwd / "dist" / (f"{app_name}{ext}" if self.params['onefile'] else app_name)
            elif engine == "Nuitka": src_out = self.temp_out_dir / (f"{app_name}{ext}" if self.params['onefile'] else f"{app_name}.dist")
            elif engine == "cx_Freeze": src_out = cwd / "dist" / app_name

            final_out = script_dir / src_out.name
            if success and src_out.exists():
                try:
                    if final_out.exists():
                        if final_out.is_dir(): shutil.rmtree(final_out, ignore_errors=True)
                        else: final_out.unlink(missing_ok=True)
                    shutil.move(src_out.as_posix(), final_out.as_posix())
                except Exception as e: self.progress.emit(f"[归档异常] 程序被占用: {e}")
            else: self.progress.emit(f"[错误] 未找到程序: {src_out}")

            if success and final_out.exists(): 
                self.progress.emit("[收尾] 执行收尾指令...")
                self.finished.emit(True, f"[构建成功] 程序路径: {final_out.resolve().as_posix()}")
            else: 
                self.finished.emit(False, "[构建失败] 请检查日志。")
        except Exception as e:
            self.finished.emit(False, f"[系统异常] {str(e)}")
        finally:
            if is_temp and build_script_path and build_script_path.exists():
                try: build_script_path.unlink()
                except: pass
                
            if self.params.get('clean_all'):
                self.progress.emit("[清理] 抹除环境与沙盒...")
                for p in [self.venv_dir, self.temp_workpath, self.temp_out_dir]:
                    if p and p.exists(): robust_rmtree(p)
                
                cwd = Path.cwd().resolve()
                app_name = self.params.get('app_name', 'app')
                robust_rmtree(cwd / "dist")
                for p in ["build", "__pycache__", f"{app_name}.build", f"{app_name}.dist", f"{app_name}.onefile-build"]:
                    robust_rmtree(cwd / p)
                Path(cwd / f"{app_name}.spec").unlink(missing_ok=True)
                if self.params.get('version_file'): Path(self.params['version_file']).unlink(missing_ok=True)


# ======================== 界面主窗口 ========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.script_path = ""
        self.thread = None
        self.current_state = "idle" 
        self.init_style()
        self.init_ui()

    def init_style(self):
        self.setWindowTitle("PyPack 2.0")
        self.setMinimumSize(580, 520)
        self.resize(600, 560)
        
        icon_path = get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        elif getattr(sys, 'frozen', False):
            provider = QFileIconProvider()
            exe_icon = provider.icon(QFileInfo(sys.executable))
            if not exe_icon.isNull(): self.setWindowIcon(exe_icon)

        self.setStyleSheet("""
            QMainWindow { background-color: #ffffff; }
            QTextEdit { border: 1px solid #e8eaed; border-radius: 8px; background-color: #f8f9fa; font-family: Consolas, monospace; font-size: 13px; color: #3c4043; padding: 10px; }
            QStatusBar { background-color: #f8f9fa; color: #5f6368; border-top: 1px solid #e8eaed; padding: 5px; }
            QStatusBar QLabel { color: #5f6368; font-size: 13px; padding: 2px; background: transparent; }
        """)
        
        self.icon_btn_style = """
            QPushButton { background-color: #f1f3f4; border: 1px solid transparent; border-radius: 8px; }
            QPushButton:hover { background-color: #e8eaed; }
            QPushButton:pressed { background-color: #dadce0; }
        """
        self.primary_btn_style = """
            QPushButton { background-color: #1A73E8; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: bold; }
            QPushButton:hover { background-color: #1B66C9; } QPushButton:pressed { background-color: #174EA6; }
        """
        self.danger_btn_style = """
            QPushButton { background-color: #D93025; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: bold; }
            QPushButton:hover { background-color: #C5221F; } QPushButton:pressed { background-color: #A50E0E; }
        """
        self.success_btn_style = """
            QPushButton { background-color: #1E8E3E; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: bold; }
            QPushButton:hover { background-color: #188038; } QPushButton:pressed { background-color: #137333; }
        """

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        self.stacked_layout = QStackedLayout(central)

        self.main_panel = QWidget()
        layout = QVBoxLayout(self.main_panel)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.drop_area = DropArea(self)
        self.drop_area.fileDropped.connect(self.on_script_selected)
        layout.addWidget(self.drop_area, stretch=1)

        self.log_container = QWidget()
        log_lay = QVBoxLayout(self.log_container)
        log_lay.setContentsMargins(0, 0, 0, 0)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(120) 
        log_lay.addWidget(self.log)
        self.log_container.hide()
        layout.addWidget(self.log_container)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        btn_layout.setContentsMargins(0, 5, 0, 0)

        self.btn_left = AnimatedButton("")
        self.btn_left.setFixedSize(44, 44)
        self.btn_left.setStyleSheet(self.icon_btn_style)
        self.btn_left.clicked.connect(self.on_left_btn_clicked)
        btn_layout.addWidget(self.btn_left)

        self.btn_main = AnimatedButton("")
        self.btn_main.setFixedHeight(44)
        self.btn_main.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_main.clicked.connect(self.on_main_btn_clicked)
        btn_layout.addWidget(self.btn_main)

        self.btn_right = AnimatedButton("")
        self.btn_right.setFixedSize(44, 44)
        self.btn_right.setIcon(get_svg_icon('settings', "#5F6368"))
        self.btn_right.setToolTip("构建配置")
        self.btn_right.setStyleSheet(self.icon_btn_style)
        self.btn_right.clicked.connect(self.show_settings)
        btn_layout.addWidget(self.btn_right)

        layout.addLayout(btn_layout)
        self.stacked_layout.addWidget(self.main_panel)

        self.settings_panel = SettingsPanel(self)
        self.stacked_layout.addWidget(self.settings_panel)
        self.stacked_layout.setCurrentWidget(self.main_panel)
        
        self.statusBar = self.statusBar()
        self.status_label = QLabel(" 状态: 就绪")
        self.statusBar.addWidget(self.status_label)

        self.update_ui_state("idle")

    def update_ui_state(self, state):
        self.current_state = state
        
        self.btn_right.setEnabled(state != "building")
        self.drop_area.setAcceptDrops(state != "building")
        
        if state in ("idle", "ready"):
            is_log_open = self.log_container.isVisible()
            icon_name = 'expand_less' if is_log_open else 'expand_more'
            self.btn_left.setIcon(get_svg_icon(icon_name, "#5F6368"))
            self.btn_left.setToolTip("显示/隐藏执行日志")
            
            self.btn_main.setText(" 开始构建")
            self.btn_main.setIcon(get_svg_icon('play', "white"))
            self.btn_main.setStyleSheet(self.primary_btn_style)
            
        elif state == "building":
            is_log_open = self.log_container.isVisible()
            icon_name = 'expand_less' if is_log_open else 'expand_more'
            self.btn_left.setIcon(get_svg_icon(icon_name, "#5F6368"))
            self.btn_left.setToolTip("显示/隐藏执行日志")
            
            self.btn_main.setText(" 停止构建")
            self.btn_main.setIcon(get_svg_icon('stop', "white"))
            self.btn_main.setStyleSheet(self.danger_btn_style)
            
        elif state in ("done", "failed"):
            self.btn_left.setIcon(get_svg_icon('refresh', "#5F6368"))
            self.btn_left.setToolTip("重置工作区")
            
            if state == "done":
                self.btn_main.setText(" 打开输出目录")
                self.btn_main.setIcon(get_svg_icon('folder', "white"))
                self.btn_main.setStyleSheet(self.success_btn_style)
            else:
                self.btn_main.setText(" 重新构建")
                self.btn_main.setIcon(get_svg_icon('refresh', "white"))
                self.btn_main.setStyleSheet(self.danger_btn_style)

    def on_left_btn_clicked(self):
        if self.current_state in ("done", "failed"):
            self.reset_all()
        else:
            self.toggle_log()

    def on_main_btn_clicked(self):
        if self.current_state in ("idle", "ready", "failed"):
            self.start_pack()
        elif self.current_state == "building":
            self.cancel_pack()
        elif self.current_state == "done":
            self.open_dist()

    def toggle_log(self):
        if self.log_container.isVisible():
            self.log_container.hide()
        else:
            self.log_container.show()
        self.update_ui_state(self.current_state)

    def show_settings(self):
        self._animate_switch(self.settings_panel)

    def show_main(self):
        self._animate_switch(self.main_panel)

    def _animate_switch(self, target_widget):
        self.anim = QPropertyAnimation(self.stacked_layout.currentWidget(), b"geometry")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.setStartValue(self.stacked_layout.currentWidget().geometry())
        self.stacked_layout.setCurrentWidget(target_widget)
        self.anim.setEndValue(target_widget.geometry())
        self.anim.start()

    def on_script_selected(self, path):
        path = Path(path).resolve().as_posix()
        try:
            if b"__CLOUDSYNC_ENC__" in Path(path).read_bytes()[:1024]:
                QMessageBox.critical(self, "加载失败", "脚本已被锁定！")
                return
        except: pass

        self.script_path = path
        self.settings_panel.name_edit.setText(Path(path).stem)
        
        script_dir = Path(path).parent
        auto_icon = None
        
        if self.settings_panel.auto_icon_check.isChecked():
            for name in ["ICON.ICO", "icon.ico", "logo.ico", "icon.svg", "logo.svg"]:
                trial = script_dir / name
                if trial.exists():
                    auto_icon = trial
                    curr = self.settings_panel.icon_edit.text()
                    if not curr or not Path(curr).exists():
                        self.settings_panel.icon_edit.setText(trial.resolve().as_posix())
                    break
                
        self.drop_area.set_success(Path(path).name, custom_icon_path=auto_icon)
        self.status_label.setText(f" 状态: 已锁定源文件 {Path(path).name}")
        
        if not self.log_container.isVisible(): self.toggle_log()
        self.log.clear()
        self.append_log(f"已识别脚本: {path}")
        self.update_ui_state("ready")

    def cancel_pack(self):
        if self.thread and self.thread.isRunning():
            self.thread.cancel()
            self.status_label.setText(" 状态: 已被用户终止")
            self.drop_area.stop_build_anim()
            self.update_ui_state("ready")

    def start_pack(self):
        if not self.script_path or not Path(self.script_path).exists():
            QMessageBox.warning(self, "提示", "请先加载需要打包的 Python 脚本！")
            return

        sp = self.settings_panel
        app_name = sp.name_edit.text().strip() or Path(self.script_path).stem
        engine = sp.engine_combo.currentText()

        version_file = None
        if engine == "PyInstaller" and sp.ver_ver.text().strip():
            try:
                content = f'''VSVersionInfo(ffi=FixedFileInfo(filevers=(1,0,0,0),prodvers=(1,0,0,0),mask=0x3f,flags=0x0,OS=0x40004,fileType=0x1,subtype=0x0,date=(0,0)),kids=[StringFileInfo([StringTable('040904B0',[StringStruct('CompanyName','{sp.ver_comp.text()}'),StringStruct('FileDescription','{sp.ver_desc.text()}'),StringStruct('FileVersion','{sp.ver_ver.text()}'),StringStruct('ProductVersion','{sp.ver_ver.text()}'),StringStruct('OriginalFilename','{app_name}.exe')])])])'''
                version_file = Path(tempfile.gettempdir()) / f"pypack_{app_name}_version.txt"
                version_file.write_text(content, encoding='utf-8')
            except: pass

        params = {
            'engine': engine,
            'script_path': self.script_path,
            'app_name': app_name,
            'onefile': sp.onefile_check.isChecked() if engine != "cx_Freeze" else False,
            'noconsole': sp.noconsole_check.isChecked(),
            'icon': sp.icon_edit.text().strip(),
            'use_reqs': sp.reqs_check.isChecked(),
            'use_pipreqs': sp.pipreqs_check.isChecked(),
            'hidden_imports': sp.hidden_edit.text(),
            'add_data': sp.add_data_edit.text(),
            'upx': sp.upx_check.isChecked() if engine == "PyInstaller" else False,
            'use_venv': sp.venv_check.isChecked(),
            'clean_all': sp.clean_all_check.isChecked(),
            'version_file': version_file.as_posix() if version_file else None,
            'ver_comp': sp.ver_comp.text() if engine != "cx_Freeze" else "",
            'ver_desc': sp.ver_desc.text() if engine != "cx_Freeze" else "",
            'ver_ver': sp.ver_ver.text() if engine != "cx_Freeze" else "",
            'pip_index_url': sp.pip_source_edit.text().strip()
        }

        self.log.clear()
        if not self.log_container.isVisible(): self.toggle_log()
            
        self.thread = PackingThread(params)
        self.thread.progress.connect(self.append_log)
        self.thread.finished.connect(self.on_pack_finished)
        self.thread.start()
        
        self.status_label.setText(f" 状态: 正在使用 {engine} 执行构建...")
        self.update_ui_state("building")
        self.drop_area.start_build_anim()

    def on_pack_finished(self, success, msg):
        self.append_log("\n" + "━"*50 + "\n" + msg)
        self.drop_area.stop_build_anim()
        if success:
            icon_path = self.settings_panel.icon_edit.text().strip()
            self.drop_area.show_success(icon_path)
            self.status_label.setText(" 状态: 构建完成 ✅")
            self.update_ui_state("done")
        else:
            self.drop_area.show_failure()
            self.status_label.setText(" 状态: 构建失败 ❌")
            self.update_ui_state("failed")

    def open_dist(self):
        if self.settings_panel.clean_all_check.isChecked() and self.script_path:
            target = Path(self.script_path).parent
        else: target = Path.cwd() / "dist"
        if target.exists():
            try:
                if os.name == 'nt': os.startfile(target)
                elif sys.platform == 'darwin': subprocess.call(('open', target.as_posix()))
                else: subprocess.call(('xdg-open', target.as_posix()))
            except: pass

    def reset_all(self):
        self.script_path = ""
        self.settings_panel.name_edit.clear()
        self.settings_panel.icon_edit.clear()
        self.settings_panel.hidden_edit.clear()
        self.settings_panel.add_data_edit.clear()
        self.log.clear()
        if self.log_container.isVisible(): self.toggle_log()
        self.drop_area.reset()
        self.status_label.setText(" 状态: 工作区已重置")
        self.update_ui_state("idle")

    def append_log(self, msg):
        self.log.append(msg)
        self.log.moveCursor(QTextCursor.End)


if __name__ == "__main__":
    if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Microsoft YaHei", 9))
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
