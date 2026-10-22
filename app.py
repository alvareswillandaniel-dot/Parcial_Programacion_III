import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel

# Cargar e inspeccionar datos
df = pd.read_csv('datos.csv')
df['Valor_Total'] = df['Precio_Unitario'] * df['Stock']

print("=== INFORMACIÓN GENERAL DE DATOS ===")
print(df.info())
print("\n=== ESTADÍSTICAS BÁSICAS ===")
print(df.describe())

class InventarioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Consultoría de Inventario - UGB")
        self.setGeometry(100, 100, 900, 600)
        
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        title = QLabel("Dashboard de Inventario por Sucursales", self)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        self.figure, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Gráfico 1: Stock total por Sucursal
        stock_sucursal = df.groupby('Sucursal')['Stock'].sum()
        stock_sucursal.plot(kind='bar', ax=ax1, color='#2b5c8f')
        ax1.set_title('Stock Total por Sucursal')
        ax1.tick_params(axis='x', rotation=45)

        # Gráfico 2: Inversión total por Categoría
        valor_categoria = df.groupby('Categoria')['Valor_Total'].sum()
        valor_categoria.plot(kind='pie', ax=ax2, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Inversión ($) por Categoría')
        ax2.set_ylabel('')

        self.figure.tight_layout()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InventarioApp()
    window.show()
    sys.exit(app.exec_())