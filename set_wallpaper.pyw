"""
Set the wallpaper to the merge_path
"""
# Modify the relevant registry entries
cpkey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Control Panel', 0, _winreg.KEY_ALL_ACCESS)
dkey = _winreg.OpenKey(cpkey, 'Desktop', 0, _winreg.KEY_ALL_ACCESS)

_winreg.SetValueEx(dkey, 'Wallpaper', 0, _winreg.REG_SZ, merge_path)
_winreg.SetValueEx(dkey, 'WallpaperDF', 0, _winreg.REG_SZ, merge_path)
_winreg.CloseKey(dkey)
_winreg.CloseKey(cpkey) 

SPI_SETDESKWALLPAPER=0x0014
ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, merge_path.encode('utf-8'), 3)