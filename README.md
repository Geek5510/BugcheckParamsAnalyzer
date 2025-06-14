# BugcheckParamsAnalyzer
Returns the description of a bugcheck code and its parameters, as provided by WinDbg's `!analyze` command.

Included is a Python script and a C++ scratch file that use `ext.dll` — the `!analyze` debugger extension —
to call an unexported function that analyzes a bugcheck's parameters to retrieve their descriptions.

Since this function is not exported, its offset will vary between different versions of the binary. If you don't feel comfortable
downloading and running the one included here, its version is 10.0.25200.1003. This version was chosen because it was the most recent one I could find
where the required analysis function was not inlined and thus could still be called directly.

The patched DLL has had all its imports to other debugging binaries removed, so it should be able to run independently without requiring any special
environment (e.g. no need for WinDbg to be installed). However, this hasn't been thoroughly tested, so it may not work in all cases.

# Research Notes

The function was pretty easy to find — by searching for bugcheck name strings, it led to functions that referenced them. It turned out there was some
kind of table with function pointers and integers, where the integer before each pointer seemed to be the bugcheck code the function handled. Each
function filled in a struct it received with descriptions related to that bugcheck.

Looking at references to this table, one of them was a function that looped over the entries, compared the bugcheck code in the table to one in a
struct, and called the matching function — that’s the one used in these scripts.

After that, the individual analysis functions were checked to figure out what other fields in the struct they filled out to add more info.
