import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data  # Now expecting a list of datasets
        self.current_time_step = 0

        self.initUI()

    def initUI(self):
        self.setWindowTitle("3D Data Visualization")
        self.setGeometry(100, 100, 800, 600)

        widget = QWidget()
        self.setCentralWidget(widget)
        
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.slider = QSlider(Qt.Horizontal)
        # Assuming all datasets have the same number of time steps
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.data[0].shape[1] - 1)
        self.slider.setValue(0)
        self.slider.valueChanged[int].connect(self.update_plot)
        layout.addWidget(self.slider)

        self.update_plot(0)

    def update_plot(self, value):
        self.current_time_step = value
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')
        
        # Colors for each dataset
        colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k']
        
        for i, dataset in enumerate(self.data):
            color = colors[i % len(colors)]  # Cycle through colors
            xs = dataset[0, self.current_time_step, :, 0]
            ys = dataset[0, self.current_time_step, :, 1]
            zs = dataset[0, self.current_time_step, :, 2]
            ax.scatter(xs, ys, zs, color=color)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Time step: {self.current_time_step}')

        # Adjust view
        ax.view_init(elev=30, azim=-60)
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_zlim(-3, 3)

        self.canvas.draw()


app = None
mainWin = None

def set_visualization(x):
    global app, mainWin

    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    mainWin = MainWindow(x)
    mainWin.show()
    app.exec_()
