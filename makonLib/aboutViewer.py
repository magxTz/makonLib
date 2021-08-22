from about import *
import sys
class abt(QtWidgets.QMainWindow,Ui_MainWindow):
     def __init__(self,parent=None):
        super(abt,self).__init__(parent)
        self.setupUi(self)

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    form=abt()
    form.show()
    sys.exit(app.exec_())
