import ctypes
import os

DLL_NAME = "ext.dll"
FUNC_OFFSET = 0x9B9B8

class BugcheckData(ctypes.Structure):
    _fields_ = [
        ("BugcheckCode", ctypes.c_uint64),
        ("param1Value", ctypes.c_uint64),
        ("param2Value", ctypes.c_uint64),
        ("param3Value", ctypes.c_uint64),
        ("param4Value", ctypes.c_uint64),
        ("BugcheckName", ctypes.c_char_p),
        ("BugcheckDescription", ctypes.c_char_p),
        ("param1Description", ctypes.c_char_p),
        ("param2Description", ctypes.c_char_p),
        ("param3Description", ctypes.c_char_p),
        ("param4Description", ctypes.c_char_p),
    ]

# Returns True if the analysis was successful
ExtAnalyzeBugcheckFunction = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.POINTER(BugcheckData))

def print_field(name, field):
    if field:
        print(f"{name}: {field.decode('utf-8')}")
    else:
        print(f"{name}: (null)")

def call_analysis_function():
    try:
        dll_path = os.path.abspath(DLL_NAME)
        dll = ctypes.WinDLL(dll_path)
        print(f"Loaded DLL: {dll_path}")
    except OSError as e:
        raise Exception(f"Failed to load DLL '{DLL_NAME}': {e}")

    # Get base address as uintptr_t
    kernel32 = ctypes.windll.kernel32
    kernel32.GetModuleHandleW.restype = ctypes.c_void_p
    hModule = kernel32.GetModuleHandleW(DLL_NAME)
    if not hModule:
        raise Exception(f"GetModuleHandle failed for {DLL_NAME}")

    func_address = hModule + FUNC_OFFSET

    # Cast to function pointer
    analyzeBugcheck = ExtAnalyzeBugcheckFunction(func_address)

    data = BugcheckData()
    data.BugcheckCode = 0x85
    data.param1Value = 0x1
    data.param2Value = 0x3

    result = analyzeBugcheck(ctypes.byref(data))
    if result:
        print(data.BugcheckCode)
        print_field("Name", data.BugcheckName)
        print_field("Description", data.BugcheckDescription)
        print_field("Param1", data.param1Description)
        print_field("Param2", data.param2Description)
        print_field("Param3", data.param3Description)
        print_field("Param4", data.param4Description)
    else:
        print("Analyze bugcheck call failed")

if __name__ == "__main__":
    call_analysis_function()
