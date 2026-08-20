Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

projectFolder = fso.GetParentFolderName(WScript.ScriptFullName)
homeFile = projectFolder & "\Home.py"

shell.CurrentDirectory = projectFolder

shell.Run "cmd /c python -m streamlit run """ & homeFile & """", 0, False
