import winreg
import subprocess

class get_installed_software():
    def foo(hive, flag):
        aReg = winreg.ConnectRegistry(None, hive)
        aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                            0, winreg.KEY_READ | flag)

        count_subkey = winreg.QueryInfoKey(aKey)[0]

        software_list = []

        for i in range(count_subkey):
            software = {}
            try:
                asubkey_name = winreg.EnumKey(aKey, i)
                asubkey = winreg.OpenKey(aKey, asubkey_name)
                software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]
                software_list.append(software)
            except EnvironmentError:
                continue

        return software_list

    #This list contains dictionary items with key being name and value being software name
    software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + foo(winreg.HKEY_CURRENT_USER, 0)

    #Filter for particular software. You can print(software_list) to verify software name
    look_for_zoom = list(filter(lambda software: software['name'] == 'Zoom', software_list))
    look_for_teams = list(filter(lambda software: software['name'] == 'Microsoft Teams', software_list))
    look_for_webex = list(filter(lambda software: software['name'] == 'Webex', software_list))

    #Check if filter found particular software, else begin installation silently
    if len(look_for_zoom) == 1:
        print('Zoom is already installed')
    else:
        print('begin installing Zoom now')
        subprocess.call("C:\py_checkinstall_taurus\ZoomInstaller.exe /QUIET", shell=True)

    if len(look_for_teams) == 1:
        print('Teams is already installed')  
    else:
        print('begin installing Teams now')
        subprocess.call("C:\py_checkinstall_taurus\TeamsInstaller.exe /QUIET", shell=True)

    if len(look_for_webex) == 1:
        print('Webex is already installed')  
    else:
        print('begin installing Webex now')
        subprocess.call("C:\py_checkinstall_taurus\WebexInstaller.msi /QUIET", shell=True)



if __name__ == "__main__":
    get_installed_software()