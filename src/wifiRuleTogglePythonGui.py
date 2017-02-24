import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import paramiko
from threading import Thread

RULE_INDEX_STRING = "-2"
IP_STRING = "192.168.0.1"
USER_NAME = "<< Your User Name >>"
USER_PASSWORD = "<< Password for that user >>"

class Connection(object):
    # Connects and logs into the specified hostname.
    # Arguments that are not given are guessed from the environment.

    def __init__(self, host, username, password, port = 22):
        self._username = username
        self._password = password
        self._transport = paramiko.Transport((host, port))
        self._isOpen = False

    def open(self):
        if self._isOpen and self._transport is not None:
            pass
        try:
            print("creating connection")
            self._transport.connect(username = self._username, password = self._password)
            print("connected")
        except Exception:
            print("Exception: closing connection : " + Exception)
            self._transport.close()
            self._transport = None
            print("closed")

    def execute(self, command):
        # Execute the given commands on a remote machine.
        if self._isOpen == False:
            self.open()
        channel = self._transport.open_session()
        channel.exec_command(command)
        output = channel.makefile('rt', -1).readlines()
        if len(output) == 0:
            output = channel.makefile_stderr('rt', -1).readlines()
        channel.close()
        ret='\r\n'.join([str(x) for x in output])
        return ret

    def close(self):
        # Closes the connection and cleans up.
        if self._transport:
            print("closing normally")
            self._transport.close()
            self._transport = None
            print("closed")

    def __del__(self):
        # Attempt to clean up if not explicitly closed.
        self.close()



class Window1(QWidget):
    
    def __init__(self):
        super().__init__()
        self._isBlocked = False
        self._thread = Thread(target=self.background_stuff)
        self._thread.start()
        self.initUI()

    def runSshCommand(self, command):
        ip_string = IP_STRING
        user_name = USER_NAME
        password = USER_PASSWORD
        myssh = Connection(ip_string, user_name, password)
        ret = myssh.execute(command)
        myssh.close()
        return ret

    @staticmethod
    def center(c,parent):
        childGeom = c.frameGeometry()
        if parent is None:
            parentCenter = QDesktopWidget().availableGeometry().center()
        else:
            parentCenter = parent.geometry().center()
        childGeom.moveCenter(parentCenter)
        c.move(childGeom.topLeft())

    def setSize(self, w, h):
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        Window1.center(self, None)

    def initUI(self):      
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Toggle State')

        self.lbl = QLabel()
        self.lbl.setText("Wait...")
        self.lbl.move(60, 40)
        font = QFont('Serif', 7, QFont.Light)
        self.lbl.setFont(font)

        self.okButton = QPushButton("Yes")
        self.okButton.clicked.connect(self.toggleRuleState)
        self.cancelButton = QPushButton("No")
        self.cancelButton.clicked.connect(QCoreApplication.instance().quit)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.okButton)
        hbox.addWidget(self.cancelButton)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        Window1.center(self, None)
        self.show()

    def closeEvent(self, event):
        if self._thread:
            self._thread.join()

    def toggleRuleState(self):
        QCoreApplication.instance().setOverrideCursor(Qt.WaitCursor)
        if self._isBlocked:
            msg = self.runSshCommand('ubus call uci set \'{"config":"firewall", "section":"@rule[' + RULE_INDEX_STRING + ']", "values":{ "enabled":"0" } }\'\nuci commit firewall.@rule[' + RULE_INDEX_STRING + ']\n/etc/init.d/network reload')
            self.lbl.setText("Phone enabled.")
        else:
            msg = self.runSshCommand('uci delete firewall.@rule[' + RULE_INDEX_STRING + '].enabled\nuci commit firewall.@rule[' + RULE_INDEX_STRING + ']\n/etc/init.d/network reload')
            self.lbl.setText("Phone disabled.")
        print(msg)
        self.lbl.adjustSize()
        QCoreApplication.instance().restoreOverrideCursor()
        self.okButton.setVisible(False)
        self.cancelButton.setText("Close")


    def background_stuff(self):
        QCoreApplication.instance().setOverrideCursor(Qt.WaitCursor)

        msg = self.runSshCommand('uci get firewall.@rule[' + RULE_INDEX_STRING + '].enabled')
        if msg.find('Entry not found') != -1:
            msg = "The phone is blocked. Do you want it to be unblocked?"
            self._isBlocked = True
        else:
            msg = "The phone is unblocked. Do you want it to be blocked?"
            self._isBlocked = False

        #self._qaApp.setOverrideCursor(Qt.ArrowCursor)
        QCoreApplication.instance().restoreOverrideCursor()

        print(msg)
        self.lbl.setText(msg)
        self.lbl.adjustSize()

        # Window1.center(self.lbl, self)

        print('Exiting the thread')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window1()
    ex.setSize(400, 100)
    sys.exit(app.exec_())
