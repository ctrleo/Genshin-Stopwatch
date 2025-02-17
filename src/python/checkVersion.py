import json

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from semantic_version import Version

from constants import VERSION, LOGGER

class checkUpdate(QObject):
    '''
    Instancing this object will run a series of 
    functions to get the latest Myth Mod Manager version.

    `checkUpdate` will delete itself after it's finished.
    '''

    updateDetected = Signal(Version, str)
    upToDate = Signal()
    error = Signal()

    def __init__(self) -> None:
        super().__init__()
        LOGGER.debug('Checking for updates')

        link = 'https://api.github.com/repos/Wolfmyths/Genshin-Stopwatch/releases/latest'
        
        network = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(link))
        
        self.reply = network.get(request)
        self.reply.finished.connect(self.__reply_handler)
    
    def __reply_handler(self) -> None:
        reply: QNetworkReply = self.sender()

        if reply.error() == QNetworkReply.NetworkError.NoError:
            self.__checkVersion()
        else:
            self.error.emit()
            self.deleteLater()
    
    def __checkVersion(self) -> None:
        reply: QNetworkReply = self.sender()

        try:
            data: dict = json.loads(reply.readAll().data().decode())
        except Exception as e:
            LOGGER.error(f'Error: {e}')
            self.error.emit()
            return
        
        # Removing letters from version string
        version: str = data['tag_name']

        for s in version:
            if not s.isdigit() and s != '.':
                version = version.replace(s, '')

        latestVersion = Version.coerce(version)

        if latestVersion > VERSION:
            self.updateDetected.emit(latestVersion, data['body'])
        else:
            self.upToDate.emit()

        self.deleteLater()
