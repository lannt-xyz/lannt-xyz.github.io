python -c "
import threading
from pathlib import Path
from xlsx_trans import config, llama_local
cfg = config.load_config()
cfg.backend = 'llama_cpp'
cfg.model_path = Path(r'models/qwen-2.5-7b-instruct-gguf-Q4-K-M.gguf')
cfg.refresh()
print('MAIN  :', llama_local.translate_text('こんにちは', cfg))
r = []
def w():
    try: r.append(llama_local.translate_text('よろしくお願いします', cfg))
    except Exception as e: r.append('ERR ' + repr(e))
t = threading.Thread(target=w); t.start(); t.join()
print('THREAD:', r[0])
"
