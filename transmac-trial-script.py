import winreg

def subkeys(key):
    i = 0
    while True:
        try:
            subkey = winreg.EnumKey(key, i)
            yield subkey
            i+=1
        except WindowsError as e:
            break

def traverse_registry_tree(hkey, keypath, tabs=0):
    notdone = True
    key = winreg.OpenKey(hkey, keypath, 0, winreg.KEY_READ)
    for subkeyname in subkeys(key):
        foundkey = '\t'*tabs + subkeyname
        subkeypath = "%s\\%s" % (keypath, subkeyname)
        traverse_registry_tree(hkey, subkeypath, tabs+1)
        if len(foundkey) == 38:
            fullp = keypath + '\\\\' + foundkey
            open_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, fullp, 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteKey(open_key, '')
            print("Deleted: " + fullp)
            print("")
            print("Trial has been reset!")
            notdone = False
    if notdone:
        print("No key to delete found! No changes were made to your registry.")

keypath = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Shell Extensions\\Approved"
traverse_registry_tree(winreg.HKEY_CURRENT_USER, keypath)
