# -*- coding: utf-8 -*-

"""
Program Name: remove-career-app
Description: めんどくさいキャリアアプリを簡単に消去することができます
Author: aoi_satou(https://twitter.com/Chromium_Linux)
Code Rewriter: DarkRix
License: GPLv3-License
Copyright (C) 2022 aoi_satou(竹林人間)
"""

from PySide6.QtCore import (QAbstractItemModel, QCoreApplication, QMetaObject, QModelIndex, QRect, QSize, Qt)
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QLineEdit,QListView, QPlainTextEdit, QMenu, QProgressBar, QPushButton, QStyledItemDelegate, QMainWindow)
import io, urllib.request, math, os, platform, shutil, subprocess, sys, zipfile

class ItemModel(QAbstractItemModel):
	def __init__(self, parent=None):
		super(ItemModel, self).__init__(parent)
		self.Items = []

	def addItems(self, Items):
		self.beginInsertRows(QModelIndex(), len(self.Items), len(self.Items) + len(Items) -1)
		self.Items.extend(Items)
		self.endInsertRows()

	def columnCount(self, parent):
		return 1

	def data(self, Index, Role=Qt.DisplayRole):
		if Role == Qt.EditRole or Role ==Qt.DisplayRole:
			return self.Items[Index.row()]

	def flags(self, Index):
		return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

	def headerData(self, I, Orientation, Role):
		if Orientation == Qt.Horizontal and Role == Qt.DisplayRole:
			return I
		if Orientation == Qt.Vertical and Role == Qt.DisplayRole:
			return I

	def index(self, Row, Column=0, Parent=QModelIndex()):
		return self.createIndex(Row, Column, Parent)

	def parent(self, Index):
		return QModelIndex()

	def removeItems(self, Rows):
		Sec = [ [Rows[0], Rows[0] + 1] ]
		for Rw in Rows[1:]:
			if Sec[-1][1] == Rw:
				Sec[-1][1] = Sec[-1][1] + 1
				continue
			Sec.append([Rw, Rw + 1])
		for sc in Sec[::-1]:
			self.beginRemoveRows(QModelIndex(), sc[0], sc[1])
			del self.Items[sc[0]:sc[1]]
			self.endRemoveRows()

	def rowCount(self, Parent=QModelIndex()):
		return len(self.Items)

	def setData(self, Index, Value, Role=Qt.EditRole):
		if Role == Qt.EditRole:
			self.Items[Index.row()] = Value
			return True
		return False

class ModelDeleGate(QStyledItemDelegate):
	def __int__(self, Parent=None, setModelDataEvent=None):
		super(ModelDeleGate, self).__init__(Parent)
		self.setModelDataEvent = setModelDataEvent

	def CreateEditor(self, Parent, _, __):
		return QLineEdit(Parent)

	def SetEditorData(self, Editor, Index):
		Value = Index.model().data(Index, Qt.DisplayRole)
		Editor.setText(str(Value))

	def SetModelData(self, Editor, Model, Index):
		Model.setData(Index, Editor.text())
		if not self.setModelDataEvent is None:
			self.setModelDataEvent()

class Ui_PyCareerAppRemover(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
	def setupUi(self, PyCareerAppRemover):
		if not PyCareerAppRemover.objectName():
			PyCareerAppRemover.setObjectName("PyCareerAppRemover")
		PyCareerAppRemover.resize(770, 780)
		font = QFont()
		self.ItemModel = ItemModel(self)
		font.setFamilies(["Meiryo"])
		font.setPointSize(15)
		PyCareerAppRemover.setFont(font)
		self.DeleteMode = QCheckBox(PyCareerAppRemover)
		self.DeleteMode.setObjectName("DeleteMode")
		self.DeleteMode.setGeometry(QRect(380, 432, 151, 61))
		self.DeleteMode.setIconSize(QSize(24, 24))
		self.DeleteMode.setTristate(False)
		self.RestoreMode = QCheckBox(PyCareerAppRemover)
		self.RestoreMode.setObjectName("RestoreMode")
		self.RestoreMode.setGeometry(QRect(381, 493, 151, 61))
		self.RestoreMode.setIconSize(QSize(24, 24))
		self.RestoreMode.setTristate(False)
		self.GetPackager = QPushButton(PyCareerAppRemover)
		self.GetPackager.setObjectName("GetPackager")
		self.GetPackager.setGeometry(QRect(20, 360, 241, 41))
		self.GetPackager.pressed.connect(self.GetPackageList)
		self.PrintPackages = QListView(PyCareerAppRemover)
		self.PrintPackages.setModel(self.ItemModel)
		self.PrintPackages.setItemDelegate(ModelDeleGate())
		self.PrintPackages.setContextMenuPolicy(Qt.CustomContextMenu)
		self.PrintPackages.customContextMenuRequested.connect(self.ContextMenu)
		self.PrintPackages.setAlternatingRowColors(True)
		self.PrintPackages.setObjectName("PrintPackages")
		self.PrintPackages.setGeometry(QRect(10, 40, 751, 311))
		self.label = QLabel(PyCareerAppRemover)
		self.label.setObjectName("label")
		self.label.setGeometry(QRect(10, 20, 181, 20))
		self.label.setAlignment(Qt.AlignCenter)
		self.addButton = QPushButton(PyCareerAppRemover)
		self.addButton.setObjectName("addButton")
		self.addButton.setGeometry(QRect(650, 360, 111, 41))
		self.addButton.pressed.connect(self.addItem)
		self.ListEdit = QLineEdit(PyCareerAppRemover)
		self.ListEdit.setObjectName("ListEdit")
		self.ListEdit.setGeometry(QRect(430, 360, 211, 41))
		self.ListEdit.setClearButtonEnabled(True)
		self.Debug_Log = QPlainTextEdit(PyCareerAppRemover)
		self.Debug_Log.setObjectName("Debug_Log")
		self.Debug_Log.setGeometry(QRect(10, 610, 751, 121))
		self.Debug_Log.setUndoRedoEnabled(False)
		self.Debug_Log.setReadOnly(True)
		self.InitSetting = QPushButton(PyCareerAppRemover)
		self.InitSetting.setObjectName("InitSetting")
		self.InitSetting.setGeometry(QRect(600, 560, 161, 51))
		self.InitSetting.pressed.connect(self.AutoDriverInstallation)
		self.Logos = QLabel(PyCareerAppRemover)
		LogoFont = QFont()
		LogoFont.setFamilies(["Meiryo"])
		LogoFont.setPointSize(14)
		self.Logos.setObjectName("Logos")
		self.Logos.setGeometry(QRect(30, 410, 321, 161))
		self.Logos.setFont(LogoFont)
		self.Logos.setTextFormat(Qt.PlainText)
		self.Logos.setAlignment(Qt.AlignCenter)
		self.ConsoleLabel = QLabel(PyCareerAppRemover)
		self.ConsoleLabel.setObjectName("ConsoleLabel")
		self.ConsoleLabel.setGeometry(QRect(0, 590, 121, 20))
		self.ConsoleLabel.setAlignment(Qt.AlignCenter)
		self.AllPackageRemove = QPushButton(PyCareerAppRemover)
		self.AllPackageRemove.setObjectName("AllPackageRemove")
		self.AllPackageRemove.setGeometry(QRect(540, 460, 211, 51))
		self.AllPackageRemove.pressed.connect(self.RestoreOrRemoving)
		self.InputLabel = QLabel(PyCareerAppRemover)
		self.InputLabel.setObjectName("InputLabel")
		self.InputLabel.setGeometry(QRect(270, 370, 161, 16))
		self.InputLabel.setTextFormat(Qt.PlainText)
		self.InstallText = QLabel(PyCareerAppRemover)
		self.InstallText.setObjectName("InstallText")
		self.InstallText.setGeometry(QRect(330, 570, 271, 31))
		self.InstallText.setTextFormat(Qt.PlainText)
		self.InstallText.setAlignment(Qt.AlignCenter)
		self.WorkprogressBar = QProgressBar(PyCareerAppRemover)
		self.WorkprogressBar.setObjectName("WorkprogressBar")
		self.WorkprogressBar.setGeometry(QRect(10, 740, 611, 23))
		self.WorkprogressBar.setValue(0)
		self.WorkprogressBar.setAlignment(Qt.AlignCenter)
		self.WorkprogressBar.setOrientation(Qt.Horizontal)
		self.ProgressNum = QLabel(PyCareerAppRemover)
		self.ProgressNum.setObjectName("ProgressNum")
		self.ProgressNum.setGeometry(QRect(624, 743, 78, 21))
		self.ProgressNum.setAlignment(Qt.AlignCenter)
		self.ProgressPercent = QLabel(PyCareerAppRemover)
		self.ProgressPercent.setObjectName("ProgressPercent")
		self.ProgressPercent.setGeometry(QRect(705, 742, 55, 21))
		self.ProgressPercent.setAlignment(Qt.AlignCenter)

		self.retranslateUi(PyCareerAppRemover)
		self.setModeSelector()
		QMetaObject.connectSlotsByName(PyCareerAppRemover)

	def ContextMenu(self, Point):
		self.Menu = QMenu(self)
		self.Menu.addAction('削除', self.delItem)
		self.Menu.exec(self.PrintPackages.mapToGlobal(Point))

	def addItem(self):
		if not self.ListEdit.text() == '':
			self.ItemModel.addItems([self.ListEdit.text()])
		else:
			self.print('[INFO] パッケージ名を入力してください')

	def delItem(self):
		if len(self.PrintPackages.selectedIndexes()) == 0:
			return
		Rows = [Index.row() for Index in self.PrintPackages.selectedIndexes()]
		self.ItemModel.removeItems(Rows)

	def setModeSelector(self):
		self.DeleteMode.stateChanged.connect(self.SelectModeCallBack)
		self.RestoreMode.stateChanged.connect(self.SelectModeCallBack)

	def SelectModeCallBack(self):
		OneRun = ['0']
		if self.RestoreMode.checkState() == Qt.Checked and self.DeleteMode.checkState() == Qt.Unchecked:
			self.AllPackageRemove.setText('選択したパッケージを復元')
			OneRun[0] = '0'
		if self.DeleteMode.checkState() == Qt.Checked and self.RestoreMode.checkState() == Qt.Unchecked:
			self.AllPackageRemove.setText('選択したパッケージを削除')
			OneRun[0] = '0'
		if self.DeleteMode.checkState() == Qt.Checked and self.RestoreMode.checkState() == Qt.Checked and OneRun[0] == '0':
			self.AllPackageRemove.setText('エラー')
			self.DeleteMode.setCheckState(Qt.Unchecked)
			self.RestoreMode.setCheckState(Qt.Unchecked)
			self.print('[INFO] チェックボックスは同時に選択できません。')
			OneRun[0] = '1'

	def print(self, AppendText):
		self.Debug_Log.appendPlainText(AppendText)

	def is_Linux(self):
		self.print('[INFO] オペレーションシステムのタイプを判別しています。しばらくお待ちください........')
		OSType = ['0']
		OSDetectCommandList = ['apt --version', 'pacman --version', 'yum --version', 'dnf --version', 'xbps-install --version']
		for ProgNum, DetectCMD in enumerate(OSDetectCommandList):
			try:
				subprocess.check_call(DetectCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Silent Check
				if DetectCMD == 'apt --version':
					OSType[0] = 'Ubuntu'
					break
				elif DetectCMD == 'pacman --version':
					OSType[0] = 'Arch'
					break
				elif DetectCMD == 'yum --version':
					OSType[0] = 'RedHat'
					break
				elif DetectCMD == 'dnf --version':
					OSType[0] = 'Fedora'
					break
				elif DetectCMD == 'xbps-install --version':
					OSType[0] = 'VoidLinux'
					break
				else:
					OSType[0] = 'None'
					break
			except:
				pass
			try:
				ProgPercent = math.floor(ProgNum / len(OSDetectCommandList) * 100)
			except:
				ProgPercent = 0
			self.WorkprogressBar.setValue(ProgPercent)
			if not ProgPercent == 100:
				self.ProgressNum.setText('{} / {}'.format(ProgNum, len(OSDetectCommandList)))
				self.ProgressPercent.setText('{}%'.format(ProgPercent))
			else:
				self.ProgressNum.setText('{} / {}'.format(ProgNum, len(OSDetectCommandList)))
				self.ProgressPercent.setText('{}%'.format(ProgPercent))
				self.print('[INFO] オペレーションシステムのタイプが判別し終わりました')
		self.WorkprogressBar.setValue(0)
		self.WorkprogressBar.maximum(0)
		if OSType[0] == 'Ubuntu':
			try:
				subprocess.check_call('sudo apt update', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				subprocess.check_call('sudo apt install adb fastboot -y', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				self.print('[INFO] adbのインストールに成功しました')
				self.WorkprogressBar.setMaximum(100)
				self.WorkprogressBar.setValue(100)
			except:
				self.print('[ERROR] adbのインストールに失敗しました。本アプリをrootで実行していますか？')
				self.WorkprogressBar.setMaximum(100)
				self.WorkprogressBar.setValue(0)
		elif OSType[0] == 'Arch':
			try:
				subprocess.check_call('sudo pacman -Sy --noconfirm android-tools', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				self.print('[INFO] adbのインストールに成功しました')
				self.WorkprogressBar.setMaximum(100)
				self.WorkprogressBar.setValue(100)
			except:
				self.print('[ERROR] adbのインストールに失敗しました。本アプリをrootで実行していますか？')
				self.WorkprogressBar.setMaximum(100)
				self.WorkprogressBar.setValue(0)
		elif OSType[0] == 'RedHat':
			try:
				subprocess.check_call('sudo yum makecache', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				subprocess.check_call('sudo yum -y install android-tools', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				self.print('[INFO] adbのインストールに成功しました')
				self.WorkprogressBar.setMaximum(100)
				self.WorkprogressBar.setValue(100)
			except:
				self.print('[ERROR] adbのインストールに失敗しました。本アプリをrootで実行していますか？')
				self.WorkprogressBar.setMaximum(100)
				self.WorkprogressBar.setValue(0)
		elif OSType[0] == 'Fedora':
			try:
				subprocess.check_call('sudo dnf makecache', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				subprocess.check_call('sudo dnf -y install android-tools', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				self.print('[INFO] adbのインストールに成功しました')
				self.WorkprogressBar.setMaximum(100)
				self.WorkprogressBar.setValue(100)
			except:
				self.print('[ERROR] adbのインストールに失敗しました。本アプリをrootで実行していますか？')
				self.WorkprogressBar.setMaximum(100)
				self.WorkprogressBar.setValue(0)
		elif OSType[0] == 'VoidLinux':
			try:
				subprocess.check_call('sudo xbps-install -Su android-tools', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				self.print('[INFO] adbのインストールに成功しました')
				self.WorkprogressBar.setMaximum(100)
				self.WorkprogressBar.setValue(100)
			except:
				self.print('[ERROR] adbのインストールに失敗しました。本アプリをrootで実行していますか？')
				self.WorkprogressBar.setMaximum(100)
				self.WorkprogressBar.setValue(0)
		elif OSType[0] == 'None':
			self.print('[ERROR] 未対応のOSです。')
			self.WorkprogressBar.setMaximum(100)
			self.WorkprogressBar.setValue(0)
		self.WorkprogressBar.setValue(0)

	def is_Mac(self):
		self.print('[INFO] Mac用のadbをダウンロードします。しばらくお待ちください......')
		self.WorkprogressBar.setMaximum(0)
		plat_toolsZip = urllib.request.urlopen('https://dl.google.com/android/repository/platform-tools_r33.0.1-darwin.zip').read()
		self.print('[INFO] 「Platform Tools」をダウンロードしました。')
		with zipfile.ZipFile(io.BytesIO(plat_toolsZip)) as plat_zip:
			plat_zip.extractall(path='{}/Applications/'.format(os.path.expanduser("~")))
		self.WorkprogressBar.setMaximum(100)
		self.WorkprogressBar.setValue(10)
		try:
			subprocess.check_call('export PATH="$PATH:{}/Applications/platform-tools"'.format(os.path.expanduser("~")), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		except:
			pass
		self.WorkprogressBar.setValue(20)
		try:
			rZshrc = open('{}/.zshrc'.format(os.path.expanduser("~")), 'r').read()
		except:
			rZshrc = ''
		self.WorkprogressBar.setValue(30)
		try:
			rBashrc = open('{}/.bashrc'.format(os.path.expanduser("~")), 'r').read()
		except:
			rBashrc = ''
		self.WorkprogressBar.setValue(40)
		if not rZshrc == '':
			with open('{}{}.zshrc'.format(os.path.expanduser("~"), os.sep), 'a') as wZshrc:
				wZshrc.write('export PATH="{}:{}"'.format(os.environ['PATH'], '{}/Applications/platform-tools'.format(os.path.expanduser("~"))))
			self.print('[INFO] ZShの環境変数にplatform-toolsを追加しました。')
		else:
			with open('{}{}.zshrc'.format(os.path.expanduser("~"), os.sep), 'w') as wZshrc:
				wZshrc.write('export PATH="{}:{}"'.format(os.environ['PATH'], '{}/Applications/platform-tools'.format(os.path.expanduser("~"))))
			self.print('[INFO] ZShの環境変数にplatform-toolsを追加しました。')
		self.WorkprogressBar.setValue(50)
		if not rBashrc == '':
			with open('{}{}.bashrc'.format(os.path.expanduser("~"), os.sep), 'a') as wBashrc:
				wBashrc.write('export PATH="{}:{}"'.format(os.environ['PATH'], '{}/Applications/platform-tools'.format(os.path.expanduser("~"))))
			self.print('[INFO] Bashの環境変数にplatform-toolsを追加しました。')
		else:
			with open('{}{}.bashrc'.format(os.path.expanduser("~"), os.sep), 'w') as wBashrc:
				wBashrc.write('export PATH="{}:{}"'.format(os.environ['PATH'], '{}/Applications/platform-tools'.format(os.path.expanduser("~"))))
			self.print('[INFO] Bashの環境変数にplatform-toolsを追加しました。')
		self.WorkprogressBar.setValue(60)
		self.WorkprogressBar.setMaximum(0)
		try:
			subprocess.check_call('source {}{}.zshrc'.format(os.path.expanduser("~"), os.sep), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			self.print('[INFO] 環境変数を即座に反映させました。')
		except:
			self.print('[ERROR] エラー。環境変数をシステムに反映できませんでした。')
			pass
		self.WorkprogressBar.setMaximum(100)
		self.WorkprogressBar.setValue(100)
		self.WorkprogressBar.setValue(0)

	def is_Windows(self):
		self.print('[INFO] 本機能はまだ試験段階の機能であることを留意してください')
		self.print('[INFO] Windows用のadbをダウンロードします。しばらくお待ちください..........')
		self.WorkprogressBar.setMaximum(0)
		DriverZip = urllib.request.urlopen('https://dl-ssl.google.com/android/repository/latest_usb_driver_windows.zip').read()
		self.print('[INFO] 「Android USB Driver」をダウンロードしました。')
		self.WorkprogressBar.setMaximum(100)
		self.WorkprogressBar.setValue(100)
		self.WorkprogressBar.setValue(0)
		self.WorkprogressBar.setMaximum(0)
		PlatToolZip = urllib.request.urlopen('https://dl.google.com/android/repository/platform-tools-latest-windows.zip').read()
		self.print('[INFO] 「Platform Tools」をダウンロードしました。')
		self.WorkprogressBar.setMaximum(100)
		self.WorkprogressBar.setValue(100)
		self.WorkprogressBar.setValue(0)
		self.WorkprogressBar.setMaximum(0)
		TMPDIR = os.path.join(os.path.expanduser("~"), '.rmcareerap', 'tmpdir')
		os.makedirs('{}'.format(TMPDIR), exist_ok=True)
		self.WorkprogressBar.setMaximum(100)
		self.WorkprogressBar.setValue(100)
		self.print('[INFO] 「{}」を作成しました'.format(TMPDIR))
		self.WorkprogressBar.setValue(0)
		self.WorkprogressBar.setMaximum(0)
		with zipfile.ZipFile(io.BytesIO(DriverZip)) as D_zip:
			D_zip.extractall(path=TMPDIR)
		self.WorkprogressBar.setMaximum(100)
		self.WorkprogressBar.setValue(100)
		self.print('[INFO] 「{}{}usb_driver」にドライバーファイルを解凍しました。'.format(TMPDIR, os.sep))
		self.WorkprogressBar.setValue(0)
		self.WorkprogressBar.setMaximum(0)
		with zipfile.ZipFile(io.BytesIO(PlatToolZip)) as Plat_zip:
			Plat_zip.extractall(path=TMPDIR)
		self.WorkprogressBar.setMaximum(100)
		self.print('[INFO] 「{}{}platform-tools」にadb類を解凍しました。'.format(TMPDIR, os.sep))
		self.WorkprogressBar.setValue(100)
		self.WorkprogressBar.setValue(0)
		self.WorkprogressBar.setMaximum(0)
		try:
			if not os.path.splitdrive(os.environ['windir'])[0] == '':
				WorkDrive = os.path.splitdrive(os.environ['windir'])[0] + os.sep
			else:
				WorkDrive = os.environ['windir'].split(os.sep)[0] + os.sep
		except:
			self.print('[ERROR] ドライブレターの取得においてエラーが発生しました。ドライブレターを「C:\\」で固定します。')
			WorkDrive = 'C:\\'
		try:
			shutil.move('{}{}platform-tools'.format(TMPDIR, os.sep), os.path.join(WorkDrive, 'platform-tools'))
			self.print('[INFO] 「{}」にadbを移動しました。'.format(os.path.join(WorkDrive, 'platform-tools')))
		except:
			self.print('[ERROR] 「{}」への移動に失敗しました。手動で移動させる必要があります。'.format(os.path.join(WorkDrive, 'platform-tools')))
		try:
			subprocess.check_call('SETX /M PATH %PATH%;{}'.format(os.path.join(WorkDrive, 'platform-tools')), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			self.print('[INFO] 「{}」を環境変数に追加しました。'.format(os.path.join(WorkDrive, 'platform-tools')))
		except:
			self.print('[ERROR] 「{}」を環境変数に追加できませんでした。手動で環境変数に追加する必要があります'.format(os.path.join(WorkDrive, 'platform-tools')))
		self.WorkprogressBar.setMaximum(100)
		currentdir = os.getcwd()
		os.chdir('{}{}usb_driver'.format(TMPDIR, os.sep))
		DriverFilePath = '{}{}'.format(os.getcwd(), os.sep)
		DriverInstallCommandList = ['rundll32 syssetup,SetupInfObjectInstallAction DefaultInstall 128 {}android_winusb.inf'.format(DriverFilePath),
									'rundll32.exe setupapi.dll,InstallHinfSection DiskInstall 128 {}android_winusb.inf'.format(DriverFilePath),
									'rundll32.exe advpack.dll,LaunchINFSection {}android_winusb.inf,DefaultInstall_SingleUser,1,N'.format(DriverFilePath),
									'drvinst.exe /i {}android_winusb.inf'.format(DriverFilePath),
									'pnputil /add-driver {}android_winusb.inf /install /subdirs'.format(DriverFilePath)]
		for IndexNum, infInstallcmd in enumerate(DriverInstallCommandList):
			try:
				self.print('[INFO] 次のコマンドを実行中.....: {}'.format(infInstallcmd))
				subprocess.check_call(infInstallcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				self.print('[INFO] ドライバーのインストールに成功しました。')
				self.ProgressPercent.setText('{}%'.format('100'))
				self.WorkprogressBar.setValue(100)
				break
			except:
				self.print('[ERROR] ドライバーのインストールに失敗しました。別のコマンドで再試行します。')
				if IndexNum+1 == len(DriverInstallCommandList):
					self.print('[ERROR] ドライバーのインストールに失敗しました。全ての手順で失敗したため、手動でドライバーをインストールする必要があります。ドライバーの場所: {}'.format(DriverFilePath))
					self.WorkprogressBar.setValue(0)
			try:
				ProgPercent = math.floor(IndexNum / len(DriverInstallCommandList) * 100)
			except:
					ProgPercent = 0
			self.WorkprogressBar.setValue(ProgPercent)
			if not ProgPercent == 100:
				self.ProgressNum.setText('{} / {}'.format(IndexNum, len(DriverInstallCommandList)))
				self.ProgressPercent.setText('{}%'.format(ProgPercent))
			else:
				self.ProgressNum.setText('{} / {}'.format(IndexNum, len(DriverInstallCommandList)))
				self.ProgressPercent.setText('{}%'.format(ProgPercent))
		self.WorkprogressBar.setValue(0)

	def CareerAppList(self, PackList):
		RemovePackList = []
		InstalledApps = PackList.decode().split('\n')
		for rpk in InstalledApps:
			if 'rakuten' in rpk:
				RemovePackList.append(rpk.split('package:')[1])
			if 'softbank' in rpk:
				RemovePackList.append(rpk.split('package:')[1])
			if 'docomo' in rpk:
				RemovePackList.append(rpk.split('package:')[1])
			if 'auone' in rpk:
				RemovePackList.append(rpk.split('package:')[1])
			if 'ntt' in rpk:
				RemovePackList.append(rpk.split('package:')[1])
			if 'kddi' in rpk:
				RemovePackList.append(rpk.split('package:')[1])
		return list(set(RemovePackList))

	def GetPackageList(self):
		ErrorDetector = ['']
		try:
			subprocess.check_call('adb kill-server', shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			subprocess.check_call('adb shell exit', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			ErrorDetector[0] = '0'
		except:
			ErrorDetector[0] = '1'
		if ErrorDetector[0] == '0':
			if self.RestoreMode.checkState() == Qt.Checked:
				try:
					RestoreTextFile = open('{}{}.rmcareerapp{}RestoreList.txt'.format(os.path.expanduser("~"), os.sep, os.sep), 'r').read()
					self.ItemModel.addItems(RestoreTextFile.split('\n'))
				except:
					self.print('[ERROR] 復元用のファイルが読み込めませんでした。')
			if self.DeleteMode.checkState() == Qt.Checked:
				PackageList, _ = subprocess.Popen('adb shell pm list package', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
				self.ItemModel.addItems(sorted(self.CareerAppList(PackageList)))
				PackageNameList = [self.ItemModel.data(self.ItemModel.index(row, 1)) for row in range(self.ItemModel.rowCount())]
				try:
					os.makedirs(os.path.join(os.path.expanduser("~"), '.rmcareerapp'), exist_ok=True)
					with open('{}{}.rmcareerapp{}RestoreList.txt'.format(os.path.expanduser("~"), os.sep, os.sep), 'w',encoding='utf-8') as WRestore:
						WRestore.write('\n'.join(PackageNameList))
				except:
					self.print('[ERROR] 復元リストの作成に失敗しましたこのままですと復元ができなくなります。')
		else:
			self.print('[ERROR] デバイスが接続されていないまたはadbがインストールされていない可能性があります')

	def AutoDriverInstallation(self):
		self.print('[INFO] オペレーションシステムの検出中.....')
		if platform.system() == 'Windows':
			self.print('[INFO] オペレーションシステム:「Windows」。処理を続行します.....')
			self.is_Windows()
		elif platform.system() == 'Darwin':
			self.print('[INFO] オペレーションシステム:「Mac」。処理を続行します.....')
			self.is_Mac()
		elif platform.system() == 'Linux':
			self.print('[INFO] オペレーションシステム:「Linux」。処理を続行します.....')
			self.is_Linux()

	def RestoreOrRemoving(self):
		ErrorDetect = ['']
		if self.DeleteMode.checkState() == Qt.Unchecked and self.RestoreMode.checkState() == Qt.Unchecked:
			self.print('[ERROR] モードを選択してパッケージ一覧を取得してから押してください')
		if self.DeleteMode.checkState() == Qt.Checked:
			self.print('[INFO] 削除を実行します')
			DeletingList = [self.ItemModel.data(self.ItemModel.index(row, 1)) for row in range(self.ItemModel.rowCount())]
			for IndexNum, Pack in enumerate(DeletingList):
				try:
					self.print('[INFO] 試行中: {}'.format('adb shell pm uninstall --user 0 {}'.format(Pack)))
					subprocess.check_call('adb shell pm uninstall --user 0 {}'.format(Pack), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					self.print('[INFO] 削除に成功しました')
				except:
					self.print('[ERROR] エラーが発生しましたが、もう一つのコマンドで試してみます')
					try:
						self.print('[INFO] 試行中: {}'.format('adb shell pm block {}'.format(Pack)))
						self.print('[INFO] 試行中: {}'.format('adb shell pm clear {}'.format(Pack)))
						subprocess.check_call('adb shell pm block {}'.format(Pack), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
						subprocess.check_call('adb shell pm clear {}'.format(Pack), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
						self.print('[INFO] 削除に成功しました')
					except:
						self.print('[ERROR] エラーが発生しました')
				try:
					ProgPrecent = math.floor(IndexNum / len(DeletingList) * 100)
				except:
					ProgPrecent = 0
				self.WorkprogressBar.setValue(ProgPrecent)
				if not ProgPrecent == 100:
					self.ProgressNum.setText('{} / {}'.format(IndexNum, len(DeletingList)))
					self.ProgressPercent.setText('{}%'.format(ProgPrecent))
				else:
					self.ProgressNum.setText('{} / {}'.format(IndexNum, len(DeletingList)))
					self.ProgressPercent.setText('{}%'.format(ProgPrecent))
		if self.RestoreMode.checkState() == Qt.Checked:
			RestoringList = [self.ItemModel.data(self.ItemModel.index(row, 1)) for row in range(self.ItemModel.rowCount())]
			for IndexNum, rPack in enumerate(RestoringList):
				try:
					self.print('[INFO] 試行中: {}'.format('adb shell cmd package install-existing {}'.format(rpack)))
					subprocess.check_call('adb shell cmd package install-existing {}'.format(rPack), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					self.print('[INFO] 復元に成功しました')
				except:
					self.print('[ERROR] エラーが発生しましたが、もう一つのコマンドで試してみます')
					try:
						self.print('[INFO] 試行中: {}'.format('adb shell pm enable --user 0 {}'.format(rPack)))
						subprocess.check_call('adb shell pm enable --user 0 {}'.format(rPack), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
						self.print('[INFO] 復元に成功しました')
					except:
						self.print('[ERROR] エラーが発生しました')
				try:
					ProgPrecent = math.floor(IndexNum / len(RestoringList) * 100)
				except:
					ProgPrecent = 0
				self.WorkprogressBar.setValue(ProgPrecent)
				if not ProgPrecent == 100:
					self.ProgressNum.setText('{} / {}'.format(IndexNum, len(RestoringList)))
					self.ProgressPercent.setText('{}%'.format(ProgPrecent))
				else:
					self.ProgressNum.setText('{} / {}'.format(IndexNum, len(RestoringList)))
					self.ProgressPercent.setText('{}%'.format(ProgPrecent))

	def retranslateUi(self, PyCareerAppRemover):
		PyCareerAppRemover.setWindowTitle(QCoreApplication.translate("PyCareerAppRemover", u"pyCareerAppRemover", None))
		self.DeleteMode.setText(QCoreApplication.translate("PyCareerAppRemover", "削除モードで実行", None))
		self.RestoreMode.setText(QCoreApplication.translate("PyCareerAppRemover", "復元モードで実行", None))
		self.GetPackager.setText(QCoreApplication.translate("PyCareerAppRemover", "パッケージ一覧を取得", None))
		self.label.setText(QCoreApplication.translate("PyCareerAppRemover", "取得したパッケージ一覧", None))
		self.addButton.setText(QCoreApplication.translate("PyCareerAppRemover", "リストに追加", None))
		self.ListEdit.setInputMask("")
		self.InitSetting.setText(QCoreApplication.translate("PyCareerAppRemover", "インストールする", None))
		self.ConsoleLabel.setText(QCoreApplication.translate("PyCareerAppRemover", "デバッグログ", None))
		self.AllPackageRemove.setText(QCoreApplication.translate("PyCareerAppRemover", "", None))
		self.Logos.setText(
			'\t-------------------------------------------------\n\t|           PyCareerAppRemoveTool            |\n\t|       Copyright (C) 2022 aoi_satou         |\n\t|  (https://twitter.com/Chromium_Linux) |\n\t-------------------------------------------------\n'
			)
		self.InputLabel.setText(QCoreApplication.translate("PyCareerAppRemover", "追加するパッケージ名:", None))
		self.InstallText.setText(QCoreApplication.translate("PyCareerAppRemover", "ツールとドライバの自動インストール:", None))
		self.ProgressNum.setText(QCoreApplication.translate("PyCareerAppRemover", "0 / 0", None))
		self.ProgressPercent.setText(QCoreApplication.translate("PyCareerAppRemover", "[0%]", None))

def main():
	app = QApplication(sys.argv)
	main_window = QMainWindow()
	ui_window = Ui_PyCareerAppRemover()
	ui_window.setupUi(main_window)
	main_window.setFixedSize(main_window.size())
	main_window.show()
	sys.exit(app.exec())

if __name__ == '__main__':
	main()