import subprocess
import ctypes
from ctypes.wintypes import *

# Grabs spefically this title, the steam version uses something different.
MELTY_TITLE = "MELTY BLOOD Actress Again Current Code Ver.1.07*"

class ProcessHook:
    """Class that hooks onto Melty Blood"""

    # No idea what this stuff does, but it works.
    STRLEN = 1
    PROCESS_VM_READ = 0x0010

    k32 = ctypes.WinDLL('kernel32')
    k32.OpenProcess.argtypes = DWORD, BOOL, DWORD
    k32.OpenProcess.restype = HANDLE
    k32.ReadProcessMemory.argtypes = HANDLE,LPVOID,LPVOID,ctypes.c_size_t,ctypes.POINTER(ctypes.c_size_t)
    k32.ReadProcessMemory.restype = BOOL

    @classmethod
    def get_pid(cls):
        """Grabs the PID of the Melty Blood executable"""
        cmd = f"""tasklist /FI "WindowTitle eq {MELTY_TITLE}" /FO CSV /NH"""
        task_data = subprocess.check_output(cmd, creationflags=0x08000000).decode("UTF8")

        if not task_data.startswith("INFO: "):
            # Split the output up and grab the PID
            pid = task_data.replace("\"", "").split(",")[1]
            return int(pid)
        return None

    PROCESS_ID = None
    process = None

    @classmethod
    def look_for_melty(cls):
        """Looks for Melty Blood and sets the process"""

        # Get Melty's PID
        cls.PROCESS_ID = cls.get_pid()

        if cls.PROCESS_ID is not None:
            print("Melty Blood found! PID: " + str(cls.PROCESS_ID))

            # Define the process.
            cls.process = cls.k32.OpenProcess(cls.PROCESS_VM_READ, 0, cls.PROCESS_ID)

            return True
        return False

    # Create a buffer for the read function.
    buf = ctypes.create_string_buffer(STRLEN)
    s = ctypes.c_size_t()

    @classmethod
    def read(cls, addr):
        """Reads a part of memory from the process"""
        if cls.k32.ReadProcessMemory(cls.process, addr, cls.buf, cls.STRLEN, ctypes.byref(cls.s)):
            return int.from_bytes(cls.buf.raw, "big")
        return None
