from PyQt5.QtWidgets import *
import sys , pickle
from PyQt5 import uic , QtWidgets 
from data_visualize import data_
from table_display import DataFrameModel
import linear_reg , logistic_reg, mlp, RandomForest , add_steps

class UI(QMainWindow):
    def __init__(self):
        super(UI , self).__init__()
        uic.loadUi('ui_files/mainwindow.ui' , self)
        
        global data , steps
        data = data_()
        steps = add_steps.add_steps()
        
        self.Browse = self.findChild(QPushButton , "Browse")
        self.columns = self.findChild(QListWidget , "listWidget")
        self.table = self.findChild(QTableView , "tableView")
        self.data_shape = self.findChild(QLabel , "shape")
        self.Submit = self.findChild(QPushButton , "Submit")
        self.target_name = self.findChild(QLabel , "target_name")
        self.dropcolumn = self.findChild(QComboBox , "dropcolumn")
        self.drop = self.findChild(QPushButton , "drop")
        
        self.scaler = self.findChild(QComboBox , "scaler")
        self.scale_btn = self.findChild(QPushButton , "scale_btn")
        
        self.cat_column = self.findChild(QComboBox , "cat_column")
        self.convert_btn = self.findChild(QPushButton , "convert_btn")
        
        self.empty_column = self.findChild(QComboBox , "empty_column")
        self.fillmean = self.findChild(QPushButton , "fillmean")
        self.fillna = self.findChild(QPushButton , "fillna")
        
        self.scatter_x = self.findChild(QComboBox , "scatter_x")
        self.scatter_y = self.findChild(QComboBox , "scatter_y")
        self.scatter_c = self.findChild(QComboBox , "scatter_c")
        self.scatter_mark = self.findChild(QComboBox , "scatter_mark")
        self.scatter_btn = self.findChild(QPushButton , "scatter_btn")
        
        self.line_x = self.findChild(QComboBox , "line_x")
        self.line_y = self.findChild(QComboBox , "line_y")
        self.line_c = self.findChild(QComboBox , "line_c")
        self.line_mark = self.findChild(QComboBox , "line_mark")
        self.line_btn = self.findChild(QPushButton , "line_btn")
        
        self.model_select = self.findChild(QComboBox , "model_select")
        self.train = self.findChild(QPushButton , "train")
        
        
        
        self.Browse.clicked.connect(self.get_csv)
        self.columns.clicked.connect(self.target)
        self.Submit.clicked.connect(self.set_target)
        self.drop.clicked.connect(self.dropc)
        self.convert_btn.clicked.connect(self.convert_cat)
        self.scale_btn.clicked.connect(self.scale_value)
        self.fillmean.clicked.connect(self.fillme)
        self.fillna.clicked.connect(self.fill_na)
        self.scatter_btn.clicked.connect(self.scatter_plot)
        self.line_btn.clicked.connect(self.line_plot)
        self.train.clicked.connect(self.train_func)
        
        # self.show()
    def filldetails(self, fleg = 1):
        if fleg == 0:
            self.df = data.read_file(self.file_path)
        
        self.columns.clear()
        self.column_list = data.get_column_list(self.df)
        # print(self.column_list)
        
        for i , j in enumerate(self.column_list):
            stri = f'{j} ------ {str(self.df[j].dtype)}'
            print(stri)
            self.columns.insertItem(i , stri)
        
        x , y  = self.df.shape
        self.data_shape.setText(f'({x} , {y})')
        self.fill_combo_box()
        
    def fill_combo_box(self):
        
        self.line_x.clear()
        self.line_x.addItems(self.column_list)
        
        self.line_y.clear()
        self.line_y.addItems(self.column_list)
        
        self.scatter_x.clear()
        self.scatter_x.addItems(self.column_list)
        
        self.scatter_y.clear()
        self.scatter_y.addItems(self.column_list)
        
        self.empty_column.clear()
        self.empty_column.addItems(self.column_list)
        
        self.dropcolumn.clear()
        self.dropcolumn.addItems(self.column_list)
        
        self.cat_column.clear()
        self.cat_column.addItems(self.column_list)
        
        x = DataFrameModel(self.df)
        self.table.setModel(x)
        
    def target(self):
        self.item = self.columns.currentItem().text().split(' ')[0]
        print(self.columns.currentItem().text().split(' ')[0])
    
    def set_target(self):
        self.target_value = self.item
        self.target_name.setText(self.target_value)
    
    def dropc(self):
        selected = self.dropcolumn.currentText()
        self.df = data.drop_columns(self.df , selected)
        self.filldetails()
    
    
    
    def scale_value(self):
        if self.scaler.currentText() == "StandardScale":
            self.df = data.StandardScale(self.df, self.target_value )
        
        elif self.scaler.currentText() == "MinMaxScale":
            self.df = data.MinMaxScale(self.df, self.target_value )
        
        else :
            self.df = data.PowerScale(self.df, self.target_value )
            
        self.filldetails()
    
    def convert_cat(self):
        selected = self.cat_column.currentText()
        # print(selected)
        self.df[selected] = data.convert_category(self.df , selected)
        print(self.df)
        self.filldetails()
    
    def fillme(self):
        selected = self.empty_column.currentText()
        type = self.df[selected].dtype
        # print(type)
        if type !='object':
            self.df[selected] = data.fillmean(self.df , selected)
            self.filldetails()
        else:
            print('datatype is object')
            
    def fill_na(self):
        selected = self.empty_column.currentText()
        self.df[selected] = data.fillna(self.df, selected)
        self.filldetails()
        
    def scatter_plot(self):
        x = self.scatter_x.currentText()
        y = self.scatter_y.currentText()
        c = self.scatter_c.currentText()
        marker = self.scatter_mark.currentText()
        data.scatter_plot(df=self.df, x=x , y=y ,c=c ,marker=marker)
    
    def line_plot(self):
        x = self.line_x.currentText()
        y = self.line_y.currentText()
        c = self.line_c.currentText()
        marker = self.line_mark.currentText()
        data.line_plot(df=self.df, x=x , y=y ,c=c ,marker=marker)
    
    def train_func(self):
        myModel={"LinearRegression":linear_reg , "RandomForest":RandomForest, "LogisticRegression":logistic_reg, "MLP":mlp}
        selected = self.model_select.currentText()
        self.win = myModel[selected].UI(self.df, self.target_value ,steps)
                   
    def get_csv(self):
        self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "C:/apps/ml/datasets/", "csv(*.csv)")
        self.columns.clear()
        
        if self.file_path !="":
            self.filldetails(0)
    
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()
    
    
    sys.exit(app.exec_())
        

