import os
import shutil
import xbmc
import xbmcgui
from xbmcvfs import translatePath
import platform

def clear_kodi_data():
    try:
        # Resolve userdata path
        kodi_data_path = translatePath("special://userdata/")
        xbmc.log(f"Resolved userdata path: {kodi_data_path}", level=xbmc.LOGDEBUG)

        # Verify path existence
        if not os.path.exists(kodi_data_path):
            xbmcgui.Dialog().ok("Error", f"Userdata path not found: {kodi_data_path}")
            return

        # Confirm action with the user
        dialog = xbmcgui.Dialog()
        if dialog.yesno(
            "Clear Kodi Data",
            f"This will erase all data in:\n{kodi_data_path}\nDo you want to continue?",
        ):
            # Delete userdata contents
            for item in os.listdir(kodi_data_path):
                item_path = os.path.join(kodi_data_path, item)
                xbmc.log(f"Attempting to delete: {item_path}", level=xbmc.LOGDEBUG)
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception as e:
                    xbmc.log(f"Failed to delete {item_path}: {str(e)}", level=xbmc.LOGERROR)

            xbmcgui.Dialog().ok("Success", "Kodi data has been erased. Please restart Kodi.")
        else:
            xbmcgui.Dialog().ok("Canceled", "No changes were made.")
    except Exception as e:
        xbmcgui.Dialog().ok("Error", f"An error occurred: {str(e)}")
        xbmc.log(f"Critical Error: {str(e)}", level=xbmc.LOGERROR)

if __name__ == "__main__":
    # Check for the platform and modify behavior if necessary
    system = platform.system()
    if system in ['Darwin', 'Windows', 'Linux', 'Android']:
        clear_kodi_data()
    elif system == 'iOS':
        xbmcgui.Dialog().ok("Error", "Clearing Kodi data is not supported on iOS.")
    else:
        xbmcgui.Dialog().ok("Error", f"Unsupported platform: {system}")
