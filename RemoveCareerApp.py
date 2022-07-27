# -*- coding: utf-8 -*-

"""
Program Name: remove-career-app
Description: めんどくさいキャリアアプリを簡単に消去することができます
Author: aoi_satou(https://twitter.com/Chromium_Linux)
Code Rewriter: DarkRix
License: GPLv3-License
Copyright (C) 2022 aoi_satou(竹林人間)
"""

import io, urllib.request, math, os, platform, re, shutil, subprocess, sys, time, zipfile

def DeleteOrRestore():
    ans_dic = {'0':True, '1':False} # 0ならばTrue、1ならFalseにする
    while True:
        try:
            return ans_dic[input('[INFO] キャリアアプリの削除をしますか？(0)、または削除したキャリアアプリの復元をしますか？(1)[0/1]:').lower()]
        except KeyboardInterrupt: # Crt + Cが押された時の動作
            print('[INFO] 処理を中止しました')
            sys.exit(0) # 正常終了
        except SystemExit: # 正常終了時の動作
            sys.exit(0) # 正常終了
        except: # 例外が発生した場合
            print('[ERROR] 再度入力してください') # エラーの表示
            pass

def forMacInit():
    plat_toolsZip = urllib.request.urlopen('https://dl.google.com/android/repository/platform-tools_r33.0.1-darwin.zip').read() # ADBの入った「Platform-Tools」のダウンロード
    print('[INFO] 「Platform Tools」をダウンロードしました。')
    with zipfile.ZipFile(io.BytesIO(plat_toolsZip)) as plat_zip: # 「platform-tools」をダイレクトに~/Applicationsへ解凍
        plat_zip.extractall(path='{}/Applications/'.format(os.path.expanduser("~")))
    try:
        subprocess.check_call('export PATH="$PATH:{}/Applications/platform-tools"'.format(os.path.expanduser("~")), shell=True) # ~/Applications/platform-toolのパスを通す
    except:
        pass
    try:
        rZshrc = open('{}/.zshrc'.format(os.path.expanduser("~")), 'r').read() # zshrcがあるかの確認
    except:
        rZshrc = ''
    try:
        rBashrc = open('{}/.bashrc'.format(os.path.expanduser("~")), 'r').read() # bashrcがあるかの確認
    except:
        rBashrc = ''
    if not rZshrc == '': # zshrcがあれば以下を実行する
        with open('{}/.zshrc'.format(os.environ['HOME']), 'a') as wZshrc:
            wZshrc.write('export PATH="{}:{}"'.format(os.environ['PATH'], '{}/Applications/platform-tools'.format(os.path.expanduser("~"))))
    else: # zshrcがなければ以下を実行する
        with open('{}/.zshrc'.format(os.environ['HOME']), 'w') as wZshrc:
            wZshrc.write('export PATH="{}:{}"'.format(os.environ['PATH'], '{}/Applications/platform-tools'.format(os.path.expanduser("~"))))
    if not rBashrc == '': # bashrcがあれば以下を実行する
        with open('{}/.bashrc'.format(os.environ['HOME']), 'a') as wBashrc:
            wBashrc.write('export PATH="{}:{}"'.format(os.environ['PATH'], '{}/Applications/platform-tools'.format(os.path.expanduser("~"))))
    else: # bashrcがなければ以下を実行する
        with open('{}/.bashrc'.format(os.environ['HOME']), 'w') as wBashrc:
            wBashrc.write('export PATH="{}:{}"'.format(os.environ['PATH'], '{}/Applications/platform-tools'.format(os.path.expanduser("~"))))
    try:
        subprocess.check_call('source {}/.zshrc'.format(os.path.expanduser("~")), shell=True)
    except:
        pass

def forLinuxInit():
    OSType = ['0']
    try: # Ubuntuだった場合
        subprocess.check_call('apt --version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        OSType[0] = 'Ubuntu'
    except:
        try: # ArchLinuxだった場合
            subprocess.check_call('pacman --version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            OSType[0] = 'Arch'
        except:
            try: # RedHatだった場合
                subprocess.check_call('yum --version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                OSType[0] = 'RedHat'
            except:
                try: # Fedoraだった場合
                    subprocess.check_call('dnf --version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    OSType[0] = 'Fedora'
                except:
                    try: # VoidLinuxだった場合
                        subprocess.check_call('xbps-install --version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        OSType[0] = 'VoidLinux'
                    except:
                        print('[ERROR] 未対応のOSです。')
                        sys.exit(1)
    if OSType[0] == 'Ubuntu': # Ubuntu
        try:
            subprocess.check_call('sudo apt update', shell=True)
            subprocess.check_call('sudo apt install adb fastboot -y', shell=True)
            print('[INFO] adbのインストールに成功しました')
        except:
            print('[ERROR] adbのインストールに失敗しました')
            sys.exit(1)
    if OSType[0] == 'Arch': # ArchLinux
        try:
            subprocess.check_call('sudo pacman -Sy --noconfirm android-tools', shell=True)
            print('[INFO] adbのインストールに成功しました')
        except:
            print('[ERROR] adbのインストールに失敗しました')
            sys.exit(1)
    if OSType[0] == 'RedHat': # RedHat
        try:
            subprocess.check_call('sudo yum makecache', shell=True)
            subprocess.check_call('sudo yum -y install android-tools', shell=True)
            print('[INFO] adbのインストールに成功しました')
        except:
            print('[ERROR] adbのインストールに失敗しました')
            sys.exit(1)
    if OSType[0] == 'Fedora': # Fedora
        try:
            subprocess.check_call('sudo dnf makecache', shell=True)
            subprocess.check_call('sudo dnf -y install android-tools', shell=True)
            print('[INFO] adbのインストールに成功しました')
        except:
            print('[ERROR] adbのインストールに失敗しました')
            sys.exit(1)
    if OSType[0] == 'VoidLinux': # VoidLinux
        try:
            subprocess.check_call('sudo xbps-install -Su android-tools', shell=True)
            print('[INFO] adbのインストールに成功しました')
        except:
            print('[ERROR] adbのインストールに失敗しました')
            sys.exit(1)

def forWindowsInit():
    print('[INFO] 自動インストール機能をオンにしました。')
    print('[INFO] 本機能はまだ試験段階の機能であることを留意してください')
    input('続行する場合は「Enter」または「Return」キーを押してください')
    DriverZip = urllib.request.urlopen('https://dl-ssl.google.com/android/repository/latest_usb_driver_windows.zip').read() # ドライバーのダウンロード。メーカー別にあるなら要書き換え
    print('[INFO] 「Android USB Driver」をダウンロードしました。')
    PlatToolZip = urllib.request.urlopen('https://dl.google.com/android/repository/platform-tools-latest-windows.zip').read() # ADBの入った「Platform-Tools」のダウンロード
    print('[INFO] 「Platform Tools」をダウンロードしました。')
    os.makedirs('tmpdir', exist_ok=True) # 一時的な作業フォルダの作成
    print('[INFO] 「tmpdir」を作成しました')
    with zipfile.ZipFile(io.BytesIO(DriverZip)) as D_zip: # ダウンロードしたドライバーを「tmpdir/usb_driver」へ解凍
        D_zip.extractall(path='{}{}tmpdir'.format(os.getcwd(), os.sep))
    print('[INFO] 「{}{}tmpdir{}usb_driver」にドライバーファイルを解凍しました。'.format(os.getcwd(), os.sep, os.sep))
    with zipfile.ZipFile(io.BytesIO(PlatToolZip)) as Plat_zip: # ダウンロードしたADB類を「tmpdir/platform-tools」へ解凍
        Plat_zip.extractall(path='{}{}tmpdir'.format(os.getcwd(), os.sep))
    print('[INFO] 「{}{}tmpdir{}platform-tools」にadb類を解凍しました。'.format(os.getcwd(), os.sep, os.sep))
    try:
        if not os.path.splitdrive(os.environ['windir'])[0] == '': # ドライブレターの検索
            WorkDrive = os.path.splitdrive(os.environ['windir'])[0] + os.sep
        else:
            WorkDrive = os.environ['windir'].split(os.sep)[0] + os.sep
    except:
        print('[ERROR] ドライブレターの取得においてエラーが発生しました。ドライブレターを「C:\\」で固定します。')
        WorkDrive = 'C:\\'
    try:
        shutil.move('{}{}tmpdir{}platform-tools'.format(os.getcwd(), os.sep, os.sep), os.path.join(WorkDrive, 'platform-tools')) # platform-toolsを最上階層へ移動
        print('[INFO] 「{}」にadbを移動しました。'.format(os.path.join(WorkDrive, 'platform-tools')))
    except:
        print('[ERROR] 「{}」の移動に失敗しました。手動で移動させる必要があります。'.format(os.path.join(WorkDrive, 'platform-tools')))
    try:
        subprocess.check_call('SETX /M PATH %PATH%;{}'.format(os.path.join(WorkDrive, 'platform-tools'))) # SETXコマンドでシステムの環境変数に移動した「platform-tools」を追記
        print('[INFO] 「{}」を環境変数に追加しました。'.format(os.path.join(WorkDrive, 'platform-tools')))
    except:
        print('[ERROR] 「{}」を環境変数に追加できませんでした。手動で環境変数に追加する必要があります'.format(os.path.join(WorkDrive, 'platform-tools')))
    currentdir = os.getcwd() # 今いるフォルダーのパスを取得
    os.chdir('{}{}tmpdir{}usb_driver'.format(os.getcwd(), os.sep, os.sep)) # 一時作業フォルダに入る
    DriverFilePath = '{}{}'.format(os.getcwd(), os.sep)
    try:
        print('[INFO] 次のコマンドを実行中.....: {}'.format('rundll32 syssetup,SetupInfObjectInstallAction DefaultInstall 128 {}android_winusb.inf'.format(DriverFilePath)))
        subprocess.check_call('rundll32 syssetup,SetupInfObjectInstallAction DefaultInstall 128 {}android_winusb.inf'.format(DriverFilePath), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('[INFO] ドライバーのインストールに成功しました。')
    except:
        print('[ERROR] ドライバーのインストールに失敗しました。別のコマンドで再試行します。')
        try:
            print('[INFO] 次のコマンドを実行中.....: {}'.format('rundll32.exe setupapi.dll,InstallHinfSection DiskInstall 128 {}android_winusb.inf'.format(DriverFilePath)))
            subprocess.check_call('rundll32.exe setupapi.dll,InstallHinfSection DiskInstall 128 {}android_winusb.inf'.format(DriverFilePath), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print('[INFO] ドライバーのインストールに成功しました。')
        except:
            print('[ERROR] ドライバーのインストールに失敗しました。別のコマンドで再試行します。')
            try:
                print('[INFO] 次のコマンドを実行中.....: {}'.format('rundll32.exe advpack.dll,LaunchINFSection {}android_winusb.inf,DefaultInstall_SingleUser,1,N'.format(DriverFilePath)))
                subprocess.check_call('rundll32.exe advpack.dll,LaunchINFSection {}android_winusb.inf,DefaultInstall_SingleUser,1,N'.format(DriverFilePath), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print('[INFO] ドライバーのインストールに成功しました。')
            except:
                print('[ERROR] ドライバーのインストールに失敗しました。別のコマンドで再試行します。')
                try:
                    print('[INFO] 次のコマンドを実行中.....: {}'.format('drvinst.exe /i {}android_winusb.inf'.format(DriverFilePath)))
                    subprocess.check_call('drvinst.exe /i {}android_winusb.inf'.format(DriverFilePath), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print('[INFO] ドライバーのインストールに成功しました。')
                except:
                    print('[ERROR] ドライバーのインストールに失敗しました。別のコマンドで再試行します。')
                    try:
                        print('[INFO] 次のコマンドを実行中.....: {}'.format('pnputil /add-driver {}android_winusb.inf /install /subdirs'.format(DriverFilePath)))
                        subprocess.check_call('pnputil /add-driver {}android_winusb.inf /install /subdirs'.format(DriverFilePath), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        print('[INFO] ドライバーのインストールに成功しました。')
                    except:
                        print('[ERROR] ドライバーのインストールに失敗しました。全ての手順で失敗したため、手動でドライバーをインストールする必要があります。ドライバーの場所: {}'.format(os.getcwd()))
                        sys.exit(1)
    os.chdir(currentdir) # 元のフォルダに戻る

def CareerAppList(PackList):
    RemovePackList = []
    InstalledApps = PackList.decode().split('\n') # インストールされたアプリのリストを作成
    for rpk in InstalledApps:
        if 'rakuten' in rpk: # 楽天
            RemovePackList.append(rpk.split('package:')[1])
        if 'softbank' in rpk: # ソフトバンク
            RemovePackList.append(rpk.split('package:')[1])
        if 'docomo' in rpk: # ドコモ
            RemovePackList.append(rpk.split('package:')[1])
        if 'auone' in rpk: # AU
            RemovePackList.append(rpk.split('package:')[1])
        if 'ntt' in rpk: # NTT
            RemovePackList.append(rpk.split('package:')[1])
        if 'kddi' in rpk: # KDDI
            RemovePackList.append(rpk.split('package:')[1])
    return list(set(RemovePackList))

def Logo():
    """
-----------------------------------------------------
|                 remove-career-app                 |
|           Copyright (C) 2022 aoi_satou            |
|        (https://twitter.com/Chromium_Linux)       |
-----------------------------------------------------
    """
    return '\t\t\t\t\t-----------------------------------------------------\n\t\t\t\t\t|                 remove-career-app                 |\n\t\t\t\t\t|           Copyright (C) 2022 aoi_satou            |\n\t\t\t\t\t|        (https://twitter.com/Chromium_Linux)       |\n\t\t\t\t\t-----------------------------------------------------\n'

def AutoInstaller():
    dics = {'y':True, 'yes':True, 'n':False, 'no':False} # yかyesならばTrue、nかnoならFalseにする
    while True:
        try:
            return answer[input('[INFO] ドライバーおよびツールの自動インストール機能を使いますか？(※Windowsはベータ機能となります) [y/N]:').lower()]
        except KeyboardInterrupt: # Crt + Cが押された時の動作
            print('[INFO] 処理を中止しました')
            sys.exit(0) # 正常終了
        except SystemExit: # 正常終了時の動作
            sys.exit(0) # 正常終了
        except: # 例外が発生した場合
            print('[ERROR] 再度入力してください') # エラーの表示
            pass

def DeleteExclusion():
    answer = {'n':True, 'no':True, 'y':False, 'yes':False} # yかyesならばFalse、nかnoならTrueにする
    while True:
        try:
            return answer[input('[INFO] 削除するパッケージのリストから除外したいパッケージはありますか？ [N/y]:').lower()]
        except KeyboardInterrupt: # Crt + Cが押された時の動作
            print('[INFO] 処理を中止しました')
            sys.exit(0) # 正常終了
        except SystemExit: # 正常終了時の動作
            sys.exit(0) # 正常終了
        except: # 例外が発生した場合
            print('[ERROR] 再度入力してください') # エラーの表示
            pass

def RestoreExclusion():
    Ranswer = {'y':True, 'yes':True, 'n':False, 'no':False} # yかyesならばFalse、nかnoならTrueにする
    while True:
        try:
            return Ranswer[input('[INFO] 復元するパッケージのリストから除外したいパッケージはありますか？ [y/N]:').lower()]
        except KeyboardInterrupt: # Crt + Cが押された時の動作
            print('[INFO] 処理を中止しました')
            sys.exit(0) # 正常終了
        except SystemExit: # 正常終了時の動作
            sys.exit(0) # 正常終了
        except: # 例外が発生した場合
            print('[ERROR] 再度入力してください') # エラーの表示
            pass

def Confirm(package_num):
    dic = {'y':True, 'yes':True, 'n':False, 'no':False} # yかyesならばTrue、nかnoならFalseにする
    while True:
        try:
            return dic[input('[INFO] {} 個のパッケージが消去されます [y/N]:'.format(package_num)).lower()]
        except KeyboardInterrupt: # Crt + Cが押された時の動作
            print('[INFO] 処理を中止しました')
            sys.exit(0) # 正常終了
        except SystemExit: # 正常終了時の動作
            sys.exit(0) # 正常終了
        except: # 例外が発生した場合
           print('[ERROR] 再度入力してください') # エラーの表示
           pass

def RestoreConfirm(RpN):
    Rdic = {'y':True, 'yes':True, 'n':False, 'no':False} # yかyesならばTrue、nかnoならFalseにする
    while True:
        try:
            return dic[input('[INFO] {} 個のパッケージが復元されます [y/N]:'.format(RpN)).lower()]
        except KeyboardInterrupt: # Crt + Cが押された時の動作
            print('[INFO] 処理を中止しました')
            sys.exit(0) # 正常終了
        except SystemExit: # 正常終了時の動作
            sys.exit(0) # 正常終了
        except: # 例外が発生した場合
           print('[ERROR] 再度入力してください') # エラーの表示
           pass

def main():
    ErrorDetect = ['']
    print(Logo()) # ロゴの表示
    if DeleteOrRestore():
        print('[INFO] 削除を選択しました')
        print('[INFO] オペレーションシステムの検出中.....\n')
        time.sleep(1)
        if platform.system() == 'Windows':
            print('[INFO] オペレーションシステムが「Windows」でしたので処理を続行します.....')
            try:
                ReadSetting = open('{}{}.rmcareerapp{}setting.conf'.format(os.path.expanduser("~"), os.sep, os.sep), 'r').read() # 設定ファイルの読み込み
                setting = ''
            except:
                os.makedirs(os.path.join(os.path.expanduser("~"), '.rmcareerapp'), exist_ok=True)
                setting = open('{}{}.rmcareerapp{}setting.conf'.format(os.path.expanduser("~"), os.sep, os.sep), 'w', encoding='utf-8') # 設定ファイルがなかった場合
                ReadSetting = ''
            if not ReadSetting == 'setting=1': # 設定ファイルに「setting=1」が書き込まれていなかった場合以下を実行する
                if AutoInstaller(): # 自動インストール機能をオンにするかの確認
                    forWindowsInit() # 自動インストールの実行
                    try:
                        setting.write('setting=1') # 次回実行時に再びインストール機能を使わない様にする為に設定ファイルに書き込み
                    except:
                        print('[ERROR] 設定ファイルに書き込めませんでした。次回実行時に再び自動インストール機能をオンにするかを確認されます。')
                else:
                    print('[INFO] 自動インストール機能をオフにしました。事前にドライバーのインストールやツールを環境変数に登録する必要があります。')
                    input('[INFO] 続行するには「Enter」または「Return」キーを押してください')
                    try:
                        setting.write('setting=1') # 次回実行時に再びインストール機能を使わない様にする為に設定ファイルに書き込み
                    except:
                        print('[ERROR] 設定ファイルに書き込めませんでした。次回実行時に再び自動インストール機能をオンにするかを確認されます。')
                try:   
                    setting.close()
                except:
                    pass
            else:
                try:
                    ReadSetting.close()
                except:
                    pass
                print('[INFO] 前回の実行履歴が見つかりました。自動インストール機能をオフにして実行します。')
                input('[INFO] 続行するには「Enter」または「Return」キーを押してください')
            try:
                subprocess.check_call('adb kill-server', shell=True)
                subprocess.check_call('adb shell exit', shell=True)
                ErrorDetect[0] = '0' # エラーがなかった場合は「０」とする
            except:
                ErrorDetect[0] = '1' # エラーだった場合は「１」とする
            if ErrorDetect[0] == '0':
                PackageList, _ = subprocess.Popen('adb shell pm list package', stdout=subprocess.PIPE,  shell=True).communicate() # adbからパッケージリストの取得
                PackageNameList = '\n'.join(CareerAppList(PackageList)) # リストから「package:」を消す
                print('{}\n|\t\t\t見つかったキャリアパッケージ一覧\t\t|\n{}\n{}'.format('-'*73, '-'*73 ,''.join('|-\t{}\n'.format(''.join(sorted(PackageNameList.split('\n'))[indx:indx + 1])) for indx in range(0, len(sorted(PackageNameList.split('\n'))), 1)))) # パッケージ名を一覧表示
                if not DeleteExclusion(): # 除外したいパッケージの選択
                    ReInput1 = [0]
                    for ReI1 in ReInput1:
                        DelExclusionList1 = input('[INFO] 削除から除外するパッケージ名を入力してください。複数の場合は「,」で区切ってください(例: com.example.carria,jp.example.carria):').replace(' ', '')
                        if DelExclusionList1 == '': # 入力が空白だった場合
                            print('[ERROR] 入力が空白でした、入力し直してください')
                            ReInput1.append(1+ReI1) # 「ReInput」にループした回数 + １して戻る
                        elif '，' in DelExclusionList1: # 「,」が全角だった場合
                            print('[ERROR] 「,」が全角でした、入力し直してください')
                            ReInput1.append(1+ReI1) # 「ReInput」にループした回数 + １して戻る
                        else:
                            break # 正常な入力だった場合ループから抜け出す
                    ReCreateList1 = PackageNameList.split('\n') # 改行で分割してリスト化
                    for DelEx1 in DelExclusionList1.split(','):
                        try:
                            while DelEx1 in ReCreateList1: # 除外するパッケージがなくなるまで実行
                                ReCreateList1.remove(DelEx1) # リストから除外するパッケージの削除
                        except:
                            print('[ERROR] 不明なエラー。処理を終了します')
                            sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
                    PackageNameList = '\n'.join(ReCreateList1) # 再度一覧化
                    print('{}\n|\t\t\t見つかったキャリアパッケージ一覧\t\t|\n{}\n{}'.format('-'*73, '-'*73 ,''.join('|-\t{}\n'.format(''.join(sorted(PackageNameList.split('\n'))[indx:indx + 1])) for indx in range(0, len(sorted(PackageNameList.split('\n'))), 1)))) # パッケージ名を一覧表示
                try:
                    os.makedirs(os.path.join(os.path.expanduser("~"), '.rmcareerapp'), exist_ok=True)
                    
                    with open('{}{}.rmcareerapp{}RestoreList.txt'.format(os.path.expanduser("~"), os.sep, os.sep), 'w', encoding='utf-8') as WRestore:
                        WRestore.write(PackageNameList)
                except:
                    print('[ERROR] 復元リストの作成に失敗しましたこのままですと復元ができなくなります。')
                    input('[INFO] それでも実行する場合は「Enter」または「Return」キーを押してください')
                DeleteList = ['adb shell pm uninstall --user 0 {}'.format(Pack) for Pack in PackageNameList.split('\n')] # リストにアンインストールコマンドを追記
                if Confirm(len(PackageNameList.split('\n'))): # パッケージの総数を表示し、yかyesならば以下を実行
                    print('[INFO] 削除を実行します')
                    for c, cmd in enumerate(DeleteList):
                        try:
                            subprocess.check_call(cmd, shell=True) # adbコマンドでアプリを消去を試行
                        except: # エラーならば
                            try:
                                os.system(cmd) # os.systemで実行してみる
                            except: # それでもエラーが出るなら
                                print('[ERROR] エラーが発生しました')
                                sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
                        try:
                            Percent = math.floor(c / len(DeleteList) * 100)
                        except:
                            Percent = 0
                        if not Percent == 100:
                            print('[  {}  中  {}  ] ({}%) 進みました'.format(len(DeleteList), c, Percent), end='\r', flush=True)
                        else:
                            print('[INFO] 作業が完了しました')
                else: # nかnoなら以下を実行
                    print('[INFO] 処理を中止しました')
                    input('[INFO] 続行する場合はEnterを押してください.....')
                    sys.exit(0) # 正常終了
                input('[INFO] アプリの削除が完了しました!(Enterを押して下さい.......)')
                sys.exit(0) # 正常終了
            else:
                print('[ERROR] デバイスが接続されていない可能性があります')
                sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
        elif platform.system() == 'Darwin': # Mac版と判断された場合
            print('[INFO] オペレーションシステムが「Mac」でしたので処理を続行します.....')
            currentdir = os.getcwd()
            os.chdir(os.environ['HOME'])
            try:
                ReadSettingMac = open('{}{}.rmcareerapp{}setting.conf'.format(os.path.expanduser("~"), os.sep, os.sep), 'r').read() # 設定ファイルの読み込み
                settingmac = ''
            except:
                os.makedirs(os.path.join(os.path.expanduser("~"), '.rmcareerapp'), exist_ok=True)
                settingmac = open('{}{}.rmcareerapp{}setting.conf'.format(os.path.expanduser("~"), os.sep, os.sep), 'w', encoding='utf-8') # 設定ファイルがなかった場合
                ReadSettingMac = ''
            if not ReadSettingMac == 'setting=1': # 設定ファイルに「setting=1」が書き込まれていなかった場合以下を実行する
                if AutoInstaller(): # 自動インストール機能をオンにするかの確認
                    forMacInit() # 初期設定の実行
                    try:
                        settingmac.write('setting=1') # 次回実行時に再びインストール機能を使わない様にする為に設定ファイルに書き込み
                    except:
                        print('[ERROR] 設定ファイルに書き込めませんでした。次回実行時に再び自動インストール機能をオンにするかを確認されます。')
                else:
                    print('[INFO] 自動インストール機能をオフにしました。事前にドライバーのインストールやツールを環境変数に登録する必要があります。')
                    input('[INFO] 続行するには「Enter」または「Return」キーを押してください')
                    try:
                        settingmac.write('setting=1') # 次回実行時に再びインストール機能を使わない様にする為に設定ファイルに書き込み
                    except:
                        print('[ERROR] 設定ファイルに書き込めませんでした。次回実行時に再び自動インストール機能をオンにするかを確認されます。')
                try:   
                    settingmac.close()
                except:
                    pass
            else:
                try:
                    ReadSettingMac.close()
                except:
                    pass
                print('[INFO] 前回の実行履歴が見つかりました。自動インストール機能をオフにして実行します。')
                input('[INFO] 続行するには「Enter」または「Return」キーを押してください')
            os.chdir(currentdir)
            try:
                subprocess.check_call('adb kill-server', shell=True)
                subprocess.check_call('adb shell exit', shell=True)
                ErrorDetect[0] = '0' # エラーがなかった場合は「０」とする
            except:
                ErrorDetect[0] = '1' # エラーだった場合は「１」とする
            if ErrorDetect[0] == '0':
                PackageList, _ = subprocess.Popen('adb shell pm list package', stdout=subprocess.PIPE,  shell=True).communicate() # adbからパッケージリストの取得
                PackageNameList = '\n'.join(CareerAppList(PackageList)) # リストから「package:」を消す
                print('{}\n|\t\t\t見つかったキャリアパッケージ一覧\t\t|\n{}\n{}'.format('-'*73, '-'*73 ,''.join('|-\t{}\n'.format(''.join(sorted(PackageNameList.split('\n'))[indx:indx + 1])) for indx in range(0, len(sorted(PackageNameList.split('\n'))), 1)))) # パッケージ名を一覧表示
                if not DeleteExclusion(): # 除外したいパッケージの選択
                    ReInput2 = [0]
                    for ReI2 in ReInput2:
                        DelExclusionList2 = input('[INFO] 削除から除外するパッケージ名を入力してください。複数の場合は「,」で区切ってください(例: com.example.carria,jp.example.carria):').replace(' ', '')
                        if DelExclusionList2 == '': # 入力が空白だった場合
                            print('[ERROR] 入力が空白でした、入力し直してください')
                            ReInput2.append(1+ReI2) # 「ReInput」にループした回数 + １して戻る
                        elif '，' in DelExclusionList: # 「,」が全角だった場合
                            print('[ERROR] 「,」が全角でした、入力し直してください')
                            ReInput2.append(1+ReI2) # 「ReInput」にループした回数 + １して戻る
                        else:
                            break # 正常な入力だった場合ループから抜け出す
                    ReCreateList2 = PackageNameList.split('\n') # 改行で分割してリスト化
                    for DelEx2 in DelExclusionList2.split(','):
                        try:
                            while DelEx2 in ReCreateList2: # 除外するパッケージがなくなるまで実行
                                ReCreateList2.remove(DelEx2) # リストから除外するパッケージの削除
                        except:
                            print('[ERROR] 不明なエラー。処理を終了します')
                            sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
                    PackageNameList = '\n'.join(ReCreateList2) # 再度一覧化
                    print('{}\n|\t\t\t見つかったキャリアパッケージ一覧\t\t|\n{}\n{}'.format('-'*73, '-'*73 ,''.join('|-\t{}\n'.format(''.join(sorted(PackageNameList.split('\n'))[indx:indx + 1])) for indx in range(0, len(sorted(PackageNameList.split('\n'))), 1)))) # パッケージ名を一覧表示
                try:
                    os.makedirs(os.path.join(os.path.expanduser("~"), '.rmcareerapp'), exist_ok=True)
                    with open('{}{}.rmcareerapp{}RestoreList.txt'.format(os.path.expanduser("~"), os.sep, os.sep), 'w', encoding='utf-8') as MRestore:
                        MRestore.write(PackageNameList)
                except:
                    print('[ERROR] 復元リストの作成に失敗しましたこのままですと復元ができなくなります。')
                    input('[INFO] それでも実行する場合は「Enter」または「Return」キーを押してください')
                DeleteList = ['adb shell pm uninstall --user 0 {}'.format(Pack) for Pack in PackageNameList.split('\n')] # リストにアンインストールコマンドを追記
                if Confirm(len(PackageNameList.split('\n'))): # パッケージの総数を表示し、yかyesならば以下を実行
                    print('[INFO] 削除を実行します')
                    for c, cmd in enumerate(DeleteList):
                        try:
                            subprocess.check_call(cmd, shell=True) # adbコマンドでアプリを消去を試行
                        except: # エラーならば
                            try:
                                os.system(cmd) # os.systemで実行してみる
                            except: # それでもエラーが出るなら
                                print('[ERROR] エラーが発生しました')
                                sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
                        try:
                            Percent = math.floor(c / len(DeleteList) * 100)
                        except:
                            Percent = 0
                        if not Percent == 100:
                            print('[  {}  中  {}  ] ({}%) 進みました'.format(len(DeleteList), c, Percent), end='\r', flush=True)
                        else:
                            print('[INFO] 作業が完了しました')
                else: # nかnoなら以下を実行
                    print('[INFO] 処理を中止しました')
                    input('[INFO] 続行する場合はEnterを押してください.....')
                    sys.exit(0) # 正常終了
                input('[INFO] アプリの削除が完了しました!(Enterを押して下さい.......)')
                sys.exit(0) # 正常終了
            else:
                print('[ERROR] デバイスが接続されていない可能性があります')
                sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する) 
        elif platform.system() == 'Linux':
            print('[INFO] オペレーションシステムが「Linux」でしたので処理を続行します.....')
            try:
                ReadSettingLinux = open('{}{}.rmcareerapp{}setting.conf'.format(os.path.expanduser("~"), os.sep, os.sep), 'r').read() # 設定ファイルの読み込み
                settingL = ''
            except:
                os.makedirs(os.path.join(os.path.expanduser("~"), '.rmcareerapp'), exist_ok=True)
                settingL = open('{}{}.rmcareerapp{}setting.conf'.format(os.path.expanduser("~"), os.sep, os.sep), 'w', encoding='utf-8') # 設定ファイルがなかった場合
                ReadSettingLinux = ''
            if not ReadSettingLinux == 'setting=1': # 設定ファイルに「setting=1」が書き込まれていなかった場合以下を実行する
                if AutoInstaller(): # 自動インストール機能をオンにするかの確認
                    forLinuxInit() # 初期設定の実行
                    try:
                        settingL.write('setting=1') # 次回実行時に再びインストール機能を使わない様にする為に設定ファイルに書き込み
                    except:
                        print('[ERROR] 設定ファイルに書き込めませんでした。次回実行時に再び自動インストール機能をオンにするかを確認されます。')
                else:
                    print('[INFO] 自動インストール機能をオフにしました。事前にドライバーのインストールやツールを環境変数に登録する必要があります。')
                    try:
                        settingL.write('setting=1') # 次回実行時に再びインストール機能を使わない様にする為に設定ファイルに書き込み
                    except:
                        print('[ERROR] 設定ファイルに書き込めませんでした。次回実行時に再び自動インストール機能をオンにするかを確認されます。')
                    input('[INFO] 続行するには「Enter」または「Return」キーを押してください')
                try:   
                    settingL.close()
                except:
                    pass
            else:
                try:
                    ReadSettingLinux.close()
                except:
                    pass
                print('[INFO] 前回の実行履歴が見つかりました。自動インストール機能をオフにして実行します。')
                input('[INFO] 続行するには「Enter」または「Return」キーを押してください')
            try:
                subprocess.check_call('adb kill-server', shell=True)
                subprocess.check_call('adb shell exit', shell=True)
                ErrorDetect[0] = '0' # エラーがなかった場合は「０」とする
            except:
                ErrorDetect[0] = '1' # エラーだった場合は「１」とする
            if ErrorDetect[0] == '0':
                PackageList, _ = subprocess.Popen('adb shell pm list package', stdout=subprocess.PIPE,  shell=True).communicate() # adbからパッケージリストの取得
                PackageNameList = '\n'.join(CareerAppList(PackageList)) # リストから「package:」を消す
                print('{}\n|\t\t\t見つかったキャリアパッケージ一覧\t\t|\n{}\n{}'.format('-'*73, '-'*73 ,''.join('|-\t{}\n'.format(''.join(sorted(PackageNameList.split('\n'))[indx:indx + 1])) for indx in range(0, len(sorted(PackageNameList.split('\n'))), 1)))) # パッケージ名を一覧表示
                if not DeleteExclusion(): # 除外したいパッケージの選択
                    ReInput3 = [0]
                    for ReI3 in ReInput3:
                        DelExclusionList3 = input('[INFO] 削除から除外するパッケージ名を入力してください。複数の場合は「,」で区切ってください(例: com.example.carria,jp.example.carria):').replace(' ', '')
                        if DelExclusionList3 == '': # 入力が空白だった場合
                            print('[ERROR] 入力が空白でした、入力し直してください')
                            ReInput3.append(1+ReI3) # 「ReInput」にループした回数 + １して戻る
                        elif '，' in DelExclusionList3: # 「,」が全角だった場合
                            print('[ERROR] 「,」が全角でした、入力し直してください')
                            ReInput3.append(1+ReI3) # 「ReInput」にループした回数 + １して戻る
                        else:
                            break # 正常な入力だった場合ループから抜け出す
                    ReCreateList3 = PackageNameList.split('\n') # 改行で分割してリスト化
                    for DelEx3 in DelExclusionList3.split(','):
                        try:
                            while DelEx3 in ReCreateList3: # 除外するパッケージがなくなるまで実行
                                ReCreateList3.remove(DelEx3) # リストから除外するパッケージの削除
                        except:
                            print('[ERROR] 不明なエラー。処理を終了します')
                            sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
                    PackageNameList = '\n'.join(ReCreateList3) # 再度一覧化
                    print('{}\n|\t\t\t見つかったキャリアパッケージ一覧\t\t|\n{}\n{}'.format('-'*73, '-'*73 ,''.join('|-\t{}\n'.format(''.join(sorted(PackageNameList.split('\n'))[indx:indx + 1])) for indx in range(0, len(sorted(PackageNameList.split('\n'))), 1)))) # パッケージ名を一覧表示
                try:
                    os.makedirs(os.path.join(os.path.expanduser("~"), '.rmcareerapp'), exist_ok=True)
                    with open('{}{}.rmcareerapp{}RestoreList.txt'.format(os.path.expanduser("~"), os.sep, os.sep), 'w', encoding='utf-8') as LRestore:
                        LRestore.write(PackageNameList)
                except:
                    print('[ERROR] 復元リストの作成に失敗しましたこのままですと復元ができなくなります。')
                    input('[INFO] それでも実行する場合は「Enter」または「Return」キーを押してください')
                DeleteList = ['adb shell pm uninstall --user 0 {}'.format(Pack) for Pack in PackageNameList.split('\n')] # リストにアンインストールコマンドを追記
                if Confirm(len(PackageNameList.split('\n'))): # パッケージの総数を表示し、yかyesならば以下を実行
                    print('[INFO] 削除を実行します')
                    for c, cmd in enumerate(DeleteList):
                        try:
                            subprocess.check_call(cmd, shell=True) # adbコマンドでアプリを消去を試行
                        except: # エラーならば
                            try:
                                os.system(cmd) # os.systemで実行してみる
                            except: # それでもエラーが出るなら
                                print('[ERROR] エラーが発生しました')
                                sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
                        try:
                            Percent = math.floor(c / len(DeleteList) * 100)
                        except:
                            Percent = 0
                        if not Percent == 100:
                            print('[  {}  中  {}  ] ({}%) 進みました'.format(len(DeleteList), c, Percent), end='\r', flush=True)
                        else:
                            print('[INFO] 作業が完了しました')
                else: # nかnoなら以下を実行
                    print('[INFO] 処理を中止しました')
                    input('[INFO] 続行する場合はEnterを押してください.....')
                    sys.exit(0) # 正常終了
                input('[INFO] アプリの削除が完了しました!(Enterを押して下さい.......)')
                sys.exit(0) # 正常終了
            else:
                print('[ERROR] デバイスが接続されていない可能性があります')
                sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
        else:
            print('[ERROR] 未対応のオペレーションシステムです。終了します。')
            sys.exit(1)
    else:
        print('[INFO] 復元を選択しました')
        print('[INFO] オペレーションシステムの検出中.....\n')
        if platform.system() == 'Windows':
            print('[INFO] オペレーションシステムが「Windows」でしたので処理を続行します.....')
            try:
                ReadSetting = open('{}{}.rmcareerapp{}setting.conf'.format(os.path.expanduser("~"), os.sep, os.sep), 'r').read() # 設定ファイルの読み込み
                setting = ''
            except:
                os.makedirs(os.path.join(os.path.expanduser("~"), '.rmcareerapp'), exist_ok=True)
                setting = open('{}{}.rmcareerapp{}setting.conf'.format(os.path.expanduser("~"), os.sep, os.sep), 'w') # 設定ファイルがなかった場合
                ReadSetting = ''
            if not ReadSetting == 'setting=1': # 設定ファイルに「setting=1」が書き込まれていなかった場合以下を実行する
                if AutoInstaller(): # 自動インストール機能をオンにするかの確認
                    forWindowsInit() # 自動インストールの実行
                    try:
                        setting.write('setting=1') # 次回実行時に再びインストール機能を使わない様にする為に設定ファイルに書き込み
                    except:
                        print('[ERROR] 設定ファイルに書き込めませんでした。次回実行時に再び自動インストール機能をオンにするかを確認されます。')
                else:
                    print('[INFO] 自動インストール機能をオフにしました。事前にドライバーのインストールやツールを環境変数に登録する必要があります。')
                    input('[INFO] 続行するには「Enter」または「Return」キーを押してください')
                    try:
                        setting.write('setting=1') # 次回実行時に再びインストール機能を使わない様にする為に設定ファイルに書き込み
                    except:
                        print('[ERROR] 設定ファイルに書き込めませんでした。次回実行時に再び自動インストール機能をオンにするかを確認されます。')
                try:   
                    setting.close()
                except:
                    pass
            else:
                try:
                    ReadSetting.close()
                except:
                    pass
                print('[INFO] 前回の実行履歴が見つかりました。自動インストール機能をオフにして実行します。')
                input('[INFO] 続行するには「Enter」または「Return」キーを押してください')
            try:
                subprocess.check_call('adb kill-server', shell=True)
                subprocess.check_call('adb shell exit', shell=True)
                ErrorDetect[0] = '0' # エラーがなかった場合は「０」とする
            except:
                ErrorDetect[0] = '1' # エラーだった場合は「１」とする
            if ErrorDetect[0] == '0':
                try:
                    RestoreTextFile = open('{}{}.rmcareerapp{}RestoreList.txt'.format(os.path.expanduser("~"), os.sep, os.sep), 'r').read()
                except:
                    print('[ERROR] 復元用のファイルが読み込めませんでした。終了します。')
                    sys.exit(1)
                print('{}\n|\t\t\t復元するキャリアパッケージ一覧\t\t|\n{}\n{}'.format('-'*73, '-'*73 ,''.join('|-\t{}\n'.format(''.join(sorted(RestoreTextFile.split('\n'))[indx:indx + 1])) for indx in range(0, len(sorted(RestoreTextFile.split('\n'))), 1)))) # パッケージ名を一覧表示
                if RestoreExclusion():
                    ResInputW = [0]
                    for ResW in ResInputW:
                        RestoreExclusionListW = input('[INFO] 復元から除外するパッケージ名を入力してください。複数の場合は「,」で区切ってください(例: com.example.carria,jp.example.carria):').replace(' ', '')
                        if RestoreExclusionListW == '': # 入力が空白だった場合
                            print('[ERROR] 入力が空白でした、入力し直してください')
                            ResInputW.append(1+ResW) # 「ReInput」にループした回数 + １して戻る
                        elif '，' in RestoreExclusionListW: # 「,」が全角だった場合
                            print('[ERROR] 「,」が全角でした、入力し直してください')
                            ResInputW.append(1+ResW) # 「ReInput」にループした回数 + １して戻る
                        else:
                            break # 正常な入力だった場合ループから抜け出す
                    ReCreateRestoreListW = RestoreTextFile.split('\n') # 改行で分割してリスト化
                    for ResExW in RestoreExclusionListW.split(','):
                        try:
                            while ResW in ReCreateRestoreListW: # 除外するパッケージがなくなるまで実行
                                ReCreateRestoreListW.remove(DelEx3) # リストから除外するパッケージの削除
                        except:
                            print('[ERROR] 不明なエラー。処理を終了します')
                            sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
                    RestoreTextFile = '\n'.join(ReCreateRestoreListW) # 再度一覧化
                RestoringList = ['adb shell pm enable --user 0 {}'.format(RPack) for RPack in RestoreTextFile.split('\n')] # リストに復元コマンドを追記
                print('{}\n|\t\t\t復元するキャリアパッケージ一覧\t\t|\n{}\n{}'.format('-'*73, '-'*73 ,''.join('|-\t{}\n'.format(''.join(sorted(RestoreTextFile.split('\n'))[indx:indx + 1])) for indx in range(0, len(sorted(RestoreTextFile.split('\n'))), 1)))) # パッケージ名を一覧表示
                if RestoreConfirm(len(RestoreTextFile.split('\n'))):
                    print('[INFO] 復元を実行します')
                    for IndexCount, RestoreCMD in enumerate(RestoringList):
                        try:
                            subprocess.check_call(RestoreCMD, shell=True) # adbコマンドでアプリを復元を試行
                        except: # エラーならば
                            try:
                                os.system(RestoreCMD) # os.systemで実行してみる
                            except: # それでもエラーが出るなら
                                print('[ERROR] エラーが発生しました')
                                sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
                        try:
                            Percent = math.floor(IndexCount / len(RestoringList) * 100)
                        except:
                            Percent = 0
                        if not Percent == 100:
                            print('[  {}  中  {}  ] ({}%) 進みました'.format(len(RestoringList), IndexCount, Percent), end='\r', flush=True)
                        else:
                            print('[INFO] 作業が完了しました')
                else: # nかnoなら以下を実行
                    print('[INFO] 処理を中止しました')
                    input('[INFO] 続行する場合はEnterを押してください.....')
                    sys.exit(0) # 正常終了
                input('[INFO] アプリの復元が完了しました!(Enterを押して下さい.......)')
                sys.exit(0) # 正常終了
            else:
                print('[ERROR] デバイスが接続されていない可能性があります')
                sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
        elif platform.system() == 'Darwin': # Mac版と判断された場合
            print('[INFO] オペレーションシステムが「Mac」でしたので処理を続行します.....')
            currentdir = os.getcwd()
            os.chdir(os.environ['HOME'])
            try:
                ReadSettingMac = open('{}{}.rmcareerapp{}setting.conf'.format(os.path.expanduser("~"), os.sep, os.sep), 'r').read() # 設定ファイルの読み込み
                settingmac = ''
            except:
                os.makedirs(os.path.join(os.path.expanduser("~"), '.rmcareerapp'), exist_ok=True)
                settingmac = open('{}{}.rmcareerapp{}setting.conf'.format(os.path.expanduser("~"), os.sep, os.sep), 'w') # 設定ファイルがなかった場合
                ReadSettingMac = ''
            if not ReadSettingMac == 'setting=1': # 設定ファイルに「setting=1」が書き込まれていなかった場合以下を実行する
                if AutoInstaller(): # 自動インストール機能をオンにするかの確認
                    forMacInit() # 初期設定の実行
                    try:
                        settingmac.write('setting=1') # 次回実行時に再びインストール機能を使わない様にする為に設定ファイルに書き込み
                    except:
                        print('[ERROR] 設定ファイルに書き込めませんでした。次回実行時に再び自動インストール機能をオンにするかを確認されます。')
                else:
                    print('[INFO] 自動インストール機能をオフにしました。事前にドライバーのインストールやツールを環境変数に登録する必要があります。')
                    input('[INFO] 続行するには「Enter」または「Return」キーを押してください')
                    try:
                        settingmac.write('setting=1') # 次回実行時に再びインストール機能を使わない様にする為に設定ファイルに書き込み
                    except:
                        print('[ERROR] 設定ファイルに書き込めませんでした。次回実行時に再び自動インストール機能をオンにするかを確認されます。')
                try:   
                    settingmac.close()
                except:
                    pass
            else:
                try:
                    ReadSettingMac.close()
                except:
                    pass
                print('[INFO] 前回の実行履歴が見つかりました。自動インストール機能をオフにして実行します。')
                input('[INFO] 続行するには「Enter」または「Return」キーを押してください')
            os.chdir(currentdir)
            try:
                subprocess.check_call('adb kill-server', shell=True)
                subprocess.check_call('adb shell exit', shell=True)
                ErrorDetect[0] = '0' # エラーがなかった場合は「０」とする
            except:
                ErrorDetect[0] = '1' # エラーだった場合は「１」とする
            if ErrorDetect[0] == '0':
                try:
                    RestoreTextFile = open('{}{}.rmcareerapp{}RestoreList.txt'.format(os.path.expanduser("~"), os.sep, os.sep), 'r').read()
                except:
                    print('[ERROR] 復元用のファイルが読み込めませんでした。終了します。')
                    sys.exit(1)
                print('{}\n|\t\t\t復元するキャリアパッケージ一覧\t\t|\n{}\n{}'.format('-'*73, '-'*73 ,''.join('|-\t{}\n'.format(''.join(sorted(RestoreTextFile.split('\n'))[indx:indx + 1])) for indx in range(0, len(sorted(RestoreTextFile.split('\n'))), 1)))) # パッケージ名を一覧表示
                if RestoreExclusion():
                    ResInputM = [0]
                    for ResM in ResInputM:
                        RestoreExclusionListM = input('[INFO] 復元から除外するパッケージ名を入力してください。複数の場合は「,」で区切ってください(例: com.example.carria,jp.example.carria):').replace(' ', '')
                        if RestoreExclusionListM == '': # 入力が空白だった場合
                            print('[ERROR] 入力が空白でした、入力し直してください')
                            ResInputM.append(1+ResM) # 「ReInput」にループした回数 + １して戻る
                        elif '，' in RestoreExclusionListW: # 「,」が全角だった場合
                            print('[ERROR] 「,」が全角でした、入力し直してください')
                            ResInputM.append(1+ResM) # 「ReInput」にループした回数 + １して戻る
                        else:
                            break # 正常な入力だった場合ループから抜け出す
                    ReCreateRestoreListM = RestoreTextFile.split('\n') # 改行で分割してリスト化
                    for ResExM in RestoreExclusionListM.split(','):
                        try:
                            while ResM in ReCreateRestoreListM: # 除外するパッケージがなくなるまで実行
                                ReCreateRestoreListM.remove(DelEx3) # リストから除外するパッケージの削除
                        except:
                            print('[ERROR] 不明なエラー。処理を終了します')
                            sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
                    RestoreTextFile = '\n'.join(ReCreateRestoreListM) # 再度一覧化
                RestoringList = ['adb shell pm enable --user 0 {}'.format(RPack) for RPack in RestoreTextFile.split('\n')] # リストに復元コマンドを追記
                print('{}\n|\t\t\t復元するキャリアパッケージ一覧\t\t|\n{}\n{}'.format('-'*73, '-'*73 ,''.join('|-\t{}\n'.format(''.join(sorted(RestoreTextFile.split('\n'))[indx:indx + 1])) for indx in range(0, len(sorted(RestoreTextFile.split('\n'))), 1)))) # パッケージ名を一覧表示
                if RestoreConfirm(len(RestoreTextFile.split('\n'))):
                    print('[INFO] 復元を実行します')
                    for IndexCount, RestoreCMD in enumerate(RestoringList):
                        try:
                            subprocess.check_call(RestoreCMD, shell=True) # adbコマンドでアプリを復元を試行
                        except: # エラーならば
                            try:
                                os.system(RestoreCMD) # os.systemで実行してみる
                            except: # それでもエラーが出るなら
                                print('[ERROR] エラーが発生しました')
                                sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
                        try:
                            Percent = math.floor(IndexCount / len(RestoringList) * 100)
                        except:
                            Percent = 0
                        if not Percent == 100:
                            print('[  {}  中  {}  ] ({}%) 進みました'.format(len(RestoringList), IndexCount, Percent), end='\r', flush=True)
                        else:
                            print('[INFO] 作業が完了しました')
                else: # nかnoなら以下を実行
                    print('[INFO] 処理を中止しました')
                    input('[INFO] 続行する場合はEnterを押してください.....')
                    sys.exit(0) # 正常終了
                input('[INFO] アプリの復元が完了しました!(Enterを押して下さい.......)')
                sys.exit(0) # 正常終了
            else:
                print('[ERROR] デバイスが接続されていない可能性があります')
                sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
        elif platform.system() == 'Linux':
            print('[INFO] オペレーションシステムが「Linux」でしたので処理を続行します.....')
            try:
                ReadSettingLinux = open('{}{}.rmcareerapp{}setting.conf'.format(os.path.expanduser("~"), os.sep, os.sep), 'r').read() # 設定ファイルの読み込み
                settingL = ''
            except:
                os.makedirs(os.path.join(os.path.expanduser("~"), '.rmcareerapp'), exist_ok=True)
                settingL = open('{}{}.rmcareerapp{}setting.conf'.format(os.path.expanduser("~"), os.sep, os.sep), 'w') # 設定ファイルがなかった場合
                ReadSettingLinux = ''
            if not ReadSettingLinux == 'setting=1': # 設定ファイルに「setting=1」が書き込まれていなかった場合以下を実行する
                if AutoInstaller(): # 自動インストール機能をオンにするかの確認
                    forLinuxInit() # 初期設定の実行
                    try:
                        settingL.write('setting=1') # 次回実行時に再びインストール機能を使わない様にする為に設定ファイルに書き込み
                    except:
                        print('[ERROR] 設定ファイルに書き込めませんでした。次回実行時に再び自動インストール機能をオンにするかを確認されます。')
                else:
                    print('[INFO] 自動インストール機能をオフにしました。事前にドライバーのインストールやツールを環境変数に登録する必要があります。')
                    try:
                        settingL.write('setting=1') # 次回実行時に再びインストール機能を使わない様にする為に設定ファイルに書き込み
                    except:
                        print('[ERROR] 設定ファイルに書き込めませんでした。次回実行時に再び自動インストール機能をオンにするかを確認されます。')
                    input('[INFO] 続行するには「Enter」または「Return」キーを押してください')
                try:   
                    settingL.close()
                except:
                    pass
            else:
                try:
                    ReadSettingLinux.close()
                except:
                    pass
                print('[INFO] 前回の実行履歴が見つかりました。自動インストール機能をオフにして実行します。')
                input('[INFO] 続行するには「Enter」または「Return」キーを押してください')
            try:
                subprocess.check_call('adb kill-server', shell=True)
                subprocess.check_call('adb shell exit', shell=True)
                ErrorDetect[0] = '0' # エラーがなかった場合は「０」とする
            except:
                ErrorDetect[0] = '1' # エラーだった場合は「１」とする
            if ErrorDetect[0] == '0':
                try:
                    RestoreTextFile = open('{}{}.rmcareerapp{}RestoreList.txt'.format(os.path.expanduser("~"), os.sep, os.sep), 'r').read()
                except:
                    print('[ERROR] 復元用のファイルが読み込めませんでした。終了します。')
                    sys.exit(1)
                print('{}\n|\t\t\t復元するキャリアパッケージ一覧\t\t|\n{}\n{}'.format('-'*73, '-'*73 ,''.join('|-\t{}\n'.format(''.join(sorted(RestoreTextFile.split('\n'))[indx:indx + 1])) for indx in range(0, len(sorted(RestoreTextFile.split('\n'))), 1)))) # パッケージ名を一覧表示
                if RestoreExclusion():
                    ResInputL = [0]
                    for ResL in ResInputL:
                        RestoreExclusionListL = input('[INFO] 復元から除外するパッケージ名を入力してください。複数の場合は「,」で区切ってください(例: com.example.carria,jp.example.carria):').replace(' ', '')
                        if RestoreExclusionListL == '': # 入力が空白だった場合
                            print('[ERROR] 入力が空白でした、入力し直してください')
                            ResInputL.append(1+ResL) # 「ReInput」にループした回数 + １して戻る
                        elif '，' in RestoreExclusionListL: # 「,」が全角だった場合
                            print('[ERROR] 「,」が全角でした、入力し直してください')
                            ResInputL.append(1+ResL) # 「ReInput」にループした回数 + １して戻る
                        else:
                            break # 正常な入力だった場合ループから抜け出す
                    ReCreateRestoreListL = RestoreTextFile.split('\n') # 改行で分割してリスト化
                    for ResExL in RestoreExclusionListL.split(','):
                        try:
                            while ResL in ReCreateRestoreListL: # 除外するパッケージがなくなるまで実行
                                ReCreateRestoreListL.remove(DelEx3) # リストから除外するパッケージの削除
                        except:
                            print('[ERROR] 不明なエラー。処理を終了します')
                            sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
                    RestoreTextFile = '\n'.join(ReCreateRestoreListL) # 再度一覧化
                RestoringList = ['adb shell pm enable --user 0 {}'.format(RPack) for RPack in RestoreTextFile.split('\n')] # リストに復元コマンドを追記
                print('{}\n|\t\t\t復元するキャリアパッケージ一覧\t\t|\n{}\n{}'.format('-'*73, '-'*73 ,''.join('|-\t{}\n'.format(''.join(sorted(RestoreTextFile.split('\n'))[indx:indx + 1])) for indx in range(0, len(sorted(RestoreTextFile.split('\n'))), 1)))) # パッケージ名を一覧表示
                if RestoreConfirm(len(RestoreTextFile.split('\n'))):
                    print('[INFO] 復元を実行します')
                    for IndexCount, RestoreCMD in enumerate(RestoringList):
                        try:
                            subprocess.check_call(RestoreCMD, shell=True) # adbコマンドでアプリを復元を試行
                        except: # エラーならば
                            try:
                                os.system(RestoreCMD) # os.systemで実行してみる
                            except: # それでもエラーが出るなら
                                print('[ERROR] エラーが発生しました')
                                sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
                        try:
                            Percent = math.floor(IndexCount / len(RestoringList) * 100)
                        except:
                            Percent = 0
                        if not Percent == 100:
                            print('[  {}  中  {}  ] ({}%) 進みました'.format(len(RestoringList), IndexCount, Percent), end='\r', flush=True)
                        else:
                            print('[INFO] 作業が完了しました')
                else: # nかnoなら以下を実行
                    print('[INFO] 処理を中止しました')
                    input('[INFO] 続行する場合はEnterを押してください.....')
                    sys.exit(0) # 正常終了
                input('[INFO] アプリの復元が完了しました!(Enterを押して下さい.......)')
                sys.exit(0) # 正常終了
            else:
                print('[ERROR] デバイスが接続されていない可能性があります')
                sys.exit(1) # エラーで終了した判定にする(0は正常終了、１は異常終了を意味する)
        else:
            print('[ERROR] 未対応のオペレーションシステムです。終了します。')
            sys.exit(1)
if __name__ == '__main__':
    main() # 削除を実行する