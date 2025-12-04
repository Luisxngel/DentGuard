import streamlit.web.cli as stcli
import os, sys

def resolve_path(path):
    if getattr(sys, '_MEIPASS', False):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.abspath("."), path)

if __name__ == "__main__":
    file_path = resolve_path("app.py")
    sys.argv = [
        "streamlit",
        "run",
        file_path,
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())
