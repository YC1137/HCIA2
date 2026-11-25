import json
import os
import runpy
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox, simpledialog

APP = runpy.run_path(str(Path(__file__).with_name("assignment-planner-server.py")))
LOCAL_CONFIG = Path(__file__).with_name("siliconflow.local.js")
KEY_FILE = Path(os.environ["LOCALAPPDATA"]) / "AssignmentPlanner" / "api-key.txt"


def start():
    root = tk.Tk()
    root.withdraw()
    try:
        config = {}
        if LOCAL_CONFIG.exists():
            config = json.loads(LOCAL_CONFIG.read_text(encoding="utf-8").split(" = ", 1)[1].strip().removesuffix(";"))
        key = config.get("apiKey", "") or (KEY_FILE.read_text(encoding="utf-8").strip() if KEY_FILE.exists() else "")
        if not key:
            key = simpledialog.askstring("Assignment Planner", "SiliconFlow API key", show="*", parent=root)
            if not key or not key.strip():
                return
            key = key.strip()
            KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
            KEY_FILE.write_text(key, encoding="utf-8")
        server = APP["ThreadingHTTPServer"](("127.0.0.1", 8765), APP["Handler"])
        server.api_key = key
        server.model = config.get("model") or os.environ.get("SILICONFLOW_MODEL") or APP["DEFAULT_MODEL"]
    except (OSError, ValueError, IndexError) as error:
        message = "Port 8765 is already in use. Close the previous planner, then try again." if getattr(error, "winerror", None) == 10048 else "Could not start the planner or read its saved key."
        messagebox.showerror("Assignment Planner", message, parent=root)
        return

    threading.Thread(target=server.serve_forever, daemon=True).start()
    root.title("Assignment Planner")
    root.resizable(False, False)
    model_label = tk.StringVar(value=server.model)
    tk.Label(root, textvariable=model_label).pack(padx=18, pady=(16, 0))
    tk.Button(root, text="Open planner", command=lambda: webbrowser.open(APP["ORIGIN"])).pack(padx=24, pady=(20, 8))
    tk.Button(root, text="Change API key", command=lambda: change_key(root, server)).pack(padx=24, pady=(0, 8))
    tk.Button(root, text="Change model", command=lambda: change_model(root, server, model_label)).pack(padx=24, pady=(0, 8))
    tk.Button(root, text="Stop planner", command=root.destroy).pack(padx=24, pady=(0, 20))
    root.deiconify()
    webbrowser.open(APP["ORIGIN"])
    try:
        root.mainloop()
    finally:
        server.shutdown()
        server.server_close()


def save_config(key, model):
    config = {"apiKey": key, "model": model}
    LOCAL_CONFIG.write_text(
        "window.assignmentPlannerConfig = " + json.dumps(config) + ";\n",
        encoding="utf-8",
    )


def change_key(root, server):
    key = simpledialog.askstring("Assignment Planner", "New SiliconFlow API key", show="*", parent=root)
    if key and key.strip():
        try:
            save_config(key.strip(), server.model)
        except OSError:
            messagebox.showerror("Assignment Planner", "Could not save the API key.", parent=root)
        else:
            server.api_key = key.strip()


def change_model(root, server, model_label):
    model = simpledialog.askstring(
        "Assignment Planner", "Full SiliconFlow model ID",
        initialvalue=server.model, parent=root,
    )
    if not model or not model.strip():
        return
    model = model.strip()
    try:
        save_config(server.api_key, model)
    except OSError:
        messagebox.showerror("Assignment Planner", "Could not save the model.", parent=root)
    else:
        server.model = model
        model_label.set(model)


if __name__ == "__main__":
    start()
