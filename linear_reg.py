from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit ,QListWidget ,QTableView ,QComboBox,QLabel,QLineEdit,QTextBrowser
import sys

from PyQt5 import uic, QtWidgets ,QtCore, QtGui
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
import data_visualise
import table_display
import pandas as pd

class UI(QMainWindow):
    def __init__(self,df,target):
        super(UI, self).__init__()
        uic.loadUi("LinearRegression.ui", self)
        global data 
        data=data_visualise.data_()
        self.X=df
        
        self.target_value=str(target)
        self.df=data.drop_columns(self.X,self.target_value)
        self.column_list=data.get_column_list(self.df)
        self.setvalue()
        # find the widgets in the xml file
 
        #self.textedit = self.findChild(QTextEdit, "textEdit")
        #self.button = self.findChild(QPushButton, "pushButton")
        #self.button.clicked.connect(self.clickedBtn
        self.target = self.findChild(QLabel,"target")
        self.columns= self.findChild(QLabel,"columns")
        self.train_size= self.findChild(QLabel,"train_size")
        self.test_size= self.findChild(QLabel,"test_size")
        
        self.test_data=self.findChild(QLineEdit,"test_data")
        self.test_size_btn=self.findChild(QPushButton,"test_size_btn")
        self.fit_inter =self.findChild(QComboBox,"fit_inter")
        self.normalize=self.findChild(QComboBox,"normalize")
        self.train_btn=self.findChild(QPushButton,"train")
        self.intercept=self.findChild(QLabel,"intercept")
        self.weights=self.findChild(QTextBrowser,"weights")
        self.output_btn=self.findChild(QPushButton,"output")
        self.bar_plot_btn=self.findChild(QPushButton,"bar_plot")
        self.mae=self.findChild(QLabel,"mae")
        self.mse=self.findChild(QLabel,"mse")
        self.rmse=self.findChild(QLabel,"rmse")


        self.test_size_btn.clicked.connect(self.test_split)
        self.train_btn.clicked.connect(self.training)
        self.output_btn.clicked.connect(self.output_)
        self.bar_plot_btn.clicked.connect(self.barplot)
        self.show()

    def setvalue(self):
               
        
        self.target.setText(self.target_value)
        self.columns.clear()
        self.columns.addItems(self.column_list)
       

    def test_split(self):

        self.x_train,self.x_test,self.y_train,self.y_test = train_test_split(self.df,self.X[self.target_value],test_size=float(self.test_data.text()),random_state=0)
        print(self.y_train.shape)
        print(self.y_test.shape)
        self.train_size.setText(str(self.x_train.shape))
        self.test_size.setText(str(self.x_test.shape))

    def training(self):

        self.reg=LinearRegression().fit(self.x_train,self.y_train)
        str1=""

        coef=' '.join(map(str, self.reg.coef_)) 
        
        self.intercept.setText(str(self.reg.intercept_))
        self.weights.setText(coef)

        pre=self.reg.predict(self.x_test)
        self.mae.setText(str(metrics.mean_absolute_error(self.y_test,pre)))
        self.mse.setText(str(metrics.mean_squared_error(self.y_test,pre)))
        self.rmse.setText(str(np.sqrt(metrics.mean_squared_error(self.y_test,pre))))

    def output_(self):
        
        prediction = self.reg.predict(self.x_test)
        plt.scatter(self.x_test, self.y_test,  color='gray')
        plt.plot(self.x_test, prediction, color='red', linewidth=2)
        plt.show()

    def barplot(self):

        y_pred = self.reg.predict(self.x_test)
        df = pd.DataFrame({'Actual': self.y_test, 'Predicted': y_pred})
        df1=df.head(20)
        
        df1.plot(kind='bar')
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        plt.show()