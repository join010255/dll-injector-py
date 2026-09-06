import os
import sys
import psutil
import win32process
import win32con
import win32api
import win32event
from colorama import Fore, Style, init

init()


class DllInjection:
    def __init__(self, process_name=None, process_id=None, dll_path: str) -> None:
        if process_name:
            pid: int = self.get_pid(process_name)
            if pid:
                self.inject(pid, dll_path)
        else:
            self.inject(process_id, dll_path)


    def get_pid(process_name: str) -> int:
        for process in psutil.process_iter(["name", "pid"]):
            if process.info["name"].lower() == process:
                parent: bool = process.parent()
                if parent:
                    return parent.pid()
    
    def inject(self, process_id: int, dll_path: str) -> None:
        process_acess = win32con.PROCESS_ALL_ACCESS
        hProcess = win32api.OpenProcess(process_acess, False, 1612)
        if not hProcess:
            raise Exception("[-] Failed to create process")
            
        print(f"[+] Process created with PID: {1612}")
        dll_path_bytes: bytes = self.dll_path.encode("mbcs")+b'/x00'

        dll_path_size: int = len(dll_path_bytes)

        address = win32process.VirtualAllocEx(
            hProcess,
            0,  # NULL = 0
            dll_path_size,
            win32con.MEM_COMMIT | win32con.MEM_RESERVE,
            win32con.PAGE_READWRITE
        )
        if not address:
            raise Exception("[-] Failed to allocate memory")
        writeProcess_memory: int = win32process.WriteProcessMemory(hProcess, address, dll_path_bytes)

        if not writeProcess_memory:
            raise Exception("[-] Failed to allocate memory")
        
        handel = win32api.GetModuleHandle("kernel32.dll")
        loadlibrary_address = win32api.GetProcAddress(handel, b"LoadLibraryA")
        if not loadlibrary_address:
            return Exception("[-] loade is not true")

        hThread = win32process.CreateRemoteThread(
            hProcess,
            None,
            0,
            loadlibrary_address,
            address,
            0
        )
        if not hThread:
            print("lala")

            
        result = win32event.WaitForSingleObject(hThread[0], 5000)  # 5 second timeout
        win32api.CloseHandle(hThread[0])
        win32api.CloseHandle(hProcess)
if __name__ == "__main__":
    try:
        print(Fore.RED+r"""
            ________  .__  .__    .___            __               __                
            \______ \ |  | |  |   |   | ____     |__| ____   _____/  |_  ___________ 
             |    |  \|  | |  |   |   |/    \    |  |/ __ \_/ ___\   __\/  _ \_  __ \
             |    `   \  |_|  |__ |   |   |  \   |  \  ___/\  \___|  | (  <_> )  | \/
            /_______  /____/____/ |___|___|  /\__|  |\___  >\___  >__|  \____/|__|   
                    \/                     \/\______|    \/     \/                   
        """+Style.NORMAL)
        print("-"*121)
        dll_path: str = input(Fore.YELLOW+"[+] Enter Dll Path: "+Style.NORMAL).strip()
        if not os.path.exists(dll_path):
            print(Fore.RED+"[-] Dll Path Is Not Exists"+Style.NORMAL)
            sys.exit(0)
            
        process_id: str = input(Fore.YELLOW+"[+]  Process Id (scape): "+Style.NORMAL).strip()
        if not process_id:
            process_name: str = input(Fore.YELLOW+"[+] Process Name : "+Style.NORMAL)
            DllInjection(process_name=process_name, dll_path=dll_path)
            
        else:
            DllInjection(process_id=process_id, dll_path=dll_path)
        
        
    except Exception as e:
        print(f"[-] Error: {e}")