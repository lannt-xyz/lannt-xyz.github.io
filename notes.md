pip show llama-cpp-python
python -c "from llama_cpp import Llama; l=Llama(model_path=r'models\qwen-2.5-7b-instruct-gguf-Q4-K-M.gguf', n_ctx=2048, verbose=True); print(l.create_chat_completion(messages=[{'role':'user','content':'Translate to English: こんにちは'}]))"
