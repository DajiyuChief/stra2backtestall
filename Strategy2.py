import multiprocessing
import os
import sys

from PyQt5.QtWidgets import QApplication

from Main import MainUI
from baseFun import kill_proc_tree

if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    mainui = MainUI()
    mainui.show()
    app.exec_()
    me = os.getpid()
    kill_proc_tree(me)



