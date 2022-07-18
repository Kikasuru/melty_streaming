"""Process Handler, hooks onto Melty Blood and reads it's sweet succulent memory."""

import subprocess
import logging
import ctypes
from ctypes.wintypes import *

log = logging.getLogger(__name__)

# Grabs spefically this title, the steam version uses something different.
MELTY_TITLE = "MELTY BLOOD Actress Again Current Code Ver.1.07*"

# No idea what this stuff does, but it works.
STRLEN = 1
PROCESS_VM_READ = 0x0010

k32 = ctypes.WinDLL('kernel32')
k32.OpenProcess.argtypes = DWORD, BOOL, DWORD
k32.OpenProcess.restype = HANDLE
k32.ReadProcessMemory.argtypes = HANDLE,LPVOID,LPVOID,ctypes.c_size_t,ctypes.POINTER(ctypes.c_size_t)
k32.ReadProcessMemory.restype = BOOL

def get_pid():
	"""Grabs the PID of the Melty Blood executable"""
	cmd = f"""tasklist /FI "WindowTitle eq {MELTY_TITLE}" /FO CSV /NH"""
	task_data = subprocess.check_output(cmd, creationflags=0x08000000).decode('UTF8')

	if not task_data.startswith('INFO: '):
		# Split the output up and grab the PID
		pid = task_data.replace('"', '').split(',')[1]
		return int(pid)
	return None

PROCESS_ID = None
process = None

def look_for_melty():
	"""Looks for Melty Blood and sets the process"""
	global PROCESS_ID, process

	# Get Melty's PID
	PROCESS_ID = get_pid()

	if PROCESS_ID is not None:
		log.info('Melty Blood found! PID: ' + str(PROCESS_ID))

		# Define the process.
		process = k32.OpenProcess(PROCESS_VM_READ, 0, PROCESS_ID)

		return True
	return False

def read(addr: int, size: int):
	"""Reads a part of memory from the process"""

	# Create a buffer.
	buf = ctypes.create_string_buffer(size)
	s = ctypes.c_size_t()

	if k32.ReadProcessMemory(process, addr, buf, size, ctypes.byref(s)):
		return int.from_bytes(buf.raw, 'big')
	return None