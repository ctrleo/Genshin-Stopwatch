import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc
import PySide6.QtNetwork as qtn

import tempfile, platform, zipfile, sys, os, shutil

from constants import ICON, LOGGER
from PySide6.QtCore import Slot


class updateApp(qtw.QDialog):
    def __init__(self):
        super().__init__()

        LOGGER.info("Downloading update")
        self.setWindowTitle("Downloading update...")
        self.setWindowIcon(qtg.QIcon(ICON))
        
        layout = qtw.QVBoxLayout(self)

        self.resize(400, 300)
        self.message = qtw.QLabel(self, text="Downloading...")
        layout.addWidget(self.message)
        self.progress = qtw.QProgressBar(self)
        layout.addWidget(self.progress)

        self.target_dir = tempfile.mkdtemp(prefix="Genshin-Stopwatch_", suffix="_UPDATE")
        if platform.system() == "Darwin":
            self.platform = "MacOS"
        elif platform.system() == "Linux":
            self.platform = "Ubuntu"
            # In GH releases, linux version is under ubuntu -_-
        elif platform.system() == "Windows":
            self.platform = "Windows"
        self.url = qtc.QUrl(f"https://github.com/Wolfmyths/Genshin-Stopwatch/releases/latest/download/Genshin-Stopwatch-{self.platform}.zip")
        self.path = qtc.QDir(self.target_dir).filePath(self.url.fileName())
        self.file = qtc.QSaveFile(self.path)
        self.manager = qtn.QNetworkAccessManager(self)
        # appending bytes
        if self.file.open(qtc.QIODevice.WriteOnly):
            LOGGER.info(f"Downloading from {self.url.toString()}")
            self.reply = self.manager.get(qtn.QNetworkRequest(self.url))
            self.reply.downloadProgress.connect(self.on_progress)
            self.reply.finished.connect(self.on_finished)
            self.reply.readyRead.connect(self.on_ready_read)
            self.reply.errorOccurred.connect(self.on_error)
        else:
            error = self.file.errorString()
            LOGGER.error(f"Cannot open device: {error}")

    def install(self):
        LOGGER.info("Installing update")
        with zipfile.ZipFile(self.path) as openzip:
            openzip.extractall(self.target_dir)
        latestExec = os.path.join(self.target_dir, f"Genshin-Stopwatch-{self.platform.lower()}-latest", "GenshinStopwatch")
        execPath = sys.executable
        if self.platform == "Windows":
            latestExec += ".exe"
            os.rename(sys.executable, "Genshin-Stopwatch_OLD.exe")
        else:
            os.remove(sys.executable)
        
        shutil.copyfile(latestExec, execPath)
        shutil.rmtree(self.target_dir)
        LOGGER.info("Installed latest version")
        try:
            os.startfile(execPath)
        except:
            os.chmod(execPath, 755)
            os.system(f".{execPath} & ")
        finally:
            qtc.QCoreApplication.quit()

    @Slot()
    def on_ready_read(self):
        if self.reply:
            if self.reply.error() == qtn.QNetworkReply.NoError:
                self.file.write(self.reply.readAll())
    
    @Slot()
    def on_finished(self):
        LOGGER.info("Download Finished")
        if self.reply:
            self.reply.deleteLater()
        if self.file:
            self.file.commit()
        self.install()
    
    @Slot(int, int)
    def on_progress(self, bytesReceived: int, bytesTotal: int):
        self.progress.setRange(0, bytesTotal)
        self.progress.setValue(bytesReceived)

    @Slot(qtn.QNetworkReply.NetworkError)
    def on_error(self, code: qtn.QNetworkReply.NetworkError):
        if self.reply:
            qtw.QMessageBox.warning(self, "Error Occurred", self.reply.errorString())
            LOGGER.error(f"Error: {self.reply.errorString()}")