#include <cstdint>
#include <windows.h>
#include <iostream>

#define DLL_NAME        L"ext.dll"     // Name of the DLL
#define FUNC_OFFSET     0x983E4        // Offset of the function

struct BugcheckData
{
    uint64_t BugcheckCode;
    uint64_t param1Value;
    uint64_t param2Value;
    uint64_t param3Value;
    uint64_t param4Value;
    const char* BugcheckName;
    const char* BugcheckDescription;
    const char* param1Description;
    const char* param2Description;
    const char* param3Description;
    const char* param4Description;
};

typedef bool(__stdcall* ExtAnalyzeBugcheckFunction)(BugcheckData*);

void print_field(const std::string& name, const char* member) {
    if (member != nullptr) {
        std::cout << name << ": " << member << std::endl;
    }
}

void call_analysis_function() {
    HMODULE dll = LoadLibraryW(DLL_NAME);
    if (!dll) {
        std::cout << "Failed to load DLL" << std::endl;
        return;
    }
    std::cout << "Loaded DLL" << std::endl;

    // Get base address
    HMODULE hModule = GetModuleHandleW(DLL_NAME);
    if (!hModule) {
        std::cerr << "GetModuleHandle failed." << std::endl;
        return;
    }
    uintptr_t func_address = reinterpret_cast<uintptr_t>(hModule) + FUNC_OFFSET;

    // Cast to function pointer
    ExtAnalyzeBugcheckFunction analyzeBugcheck = reinterpret_cast<ExtAnalyzeBugcheckFunction>(func_address);

    BugcheckData data = {};
    data.BugcheckCode = 0x85;
    data.param1Value = 0x1;
    data.param2Value = 0x3;

    bool result = analyzeBugcheck(&data);

    if (result) {
        print_field("Name", data.BugcheckName);
        print_field("Description", data.BugcheckDescription);
        print_field("Param1", data.param1Description);
        print_field("Param2", data.param2Description);
        print_field("Param3", data.param3Description);
        print_field("Param4", data.param4Description);
    }
    else {
        std::cout << "Analyze bugcheck call failed" << std::endl;
    }

}

int main() {
    call_analysis_function();
    return 0;
}
