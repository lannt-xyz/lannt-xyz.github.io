import sys
import threading
from pathlib import Path

if sys.argv[1:] == ["b"]:
    import llama_cpp  # b: nạp llama trước Tk
import tkinter
from xlsx_trans import config, llama_local

root = tkinter.Tk()
cfg = config.load_config()
cfg.backend = 'llama_cpp'
cfg.model_path = Path(r'models/qwen-2.5-7b-instruct-gguf-Q4-K-M.gguf')
cfg.refresh()
out = []

def work():
    try:
        out.append(llama_local.translate_text('こんにちは', cfg))
    except Exception as e:
        out.append('ERR ' + repr(e))

t = threading.Thread(target=work, daemon=True)
t.start()

def poll():
    if t.is_alive():
        root.after(200, poll)
    else:
        root.destroy()

root.after(200, poll)
root.mainloop()
print(sys.argv[1:], out)
