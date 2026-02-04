import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog, ttk
import threading
import sys
import os
from crawler import crawl_local, crawl_pdf
from summarizer import init_gemini, summarize, init_ollama
from utils import save_local_original, save_summary
import requests

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

API_FILE = os.path.join(get_base_dir(), "api_key.txt")

def load_api_key():
    if os.path.exists(API_FILE):
        with open(API_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

#api key 입력
def get_or_create_api_key():
    key = load_api_key()
    if key:
        return key

    root = tk.Tk()
    root.withdraw()

    key = simpledialog.askstring(
        "API KEY 입력",
        "Gemini API Key를 입력하세요:",
        #show="*"
    )

    if not key:
        messagebox.showerror("오류", "API Key가 입력되지 않았습니다.")
        sys.exit(1)

    try:
        save_api_key(key)
    except PermissionError:
        messagebox.showerror(
            "권한 오류",
            "api_key.txt를 저장할 수 없습니다.\n"
            "프로그램을 쓰기 가능한 위치에서 실행하세요."
        )
        sys.exit(1)

    return key

def save_api_key(key):
    with open(API_FILE, "w", encoding="utf-8") as f:
        f.write(key)

def start_gui():
    def log(msg):
        if int(log_box.index('end-1c').split('.')[0]) > 500:
            log_box.delete("1.0", "100.0")
        log_box.insert(tk.END, msg + "\n")

    def gui_log(msg):
        root.after(0, lambda: log(msg))

    def gui_info(title, msg):
        root.after(0, lambda: messagebox.showinfo(title, msg))

    def gui_error(msg):
        root.after(0, lambda: messagebox.showerror("에러", msg))

    def run():
        try:
            selected_model = model_var.get()

            if selected_model == "Gemma3":
                gui_log("모델: Gemma3")
                model = init_ollama("gemma3:4b") #올라마 모델 선택 (젬마3)
            elif selected_model == "Gemini":
                gui_log("모델: Gemini")
                api_key = get_or_create_api_key()
                model = init_gemini(api_key)
            elif selected_model == "Exaone":
                gui_log("모델: Exaone")
                model = init_ollama("exaone-deep") #올라마 모델 선택 (엑시온)
            elif selected_model == "llama":
                gui_log("모델: llama")
                model = init_ollama("llama3.1:8b") #올라마 모델 선택 (라마3)
            elif selected_model == "Mistral":
                gui_log("모델: Mistral")
                model = init_ollama("Mistral") #올라마 모델 선택 (미스트랄)

            url = url_entry.get().strip()
            if not url:
                gui_error("URL을 입력하세요.")
                return

            gui_log("크롤링 시작")

            if ".pdf" in url.lower():
                gui_log("PDF 크롤링 감지")
                title, local_text = crawl_pdf(url)
            else:
                gui_log("HTML 크롤링 감지")
                title, local_text = crawl_local(url)

            gui_log("크롤링 완료")
            gui_log(f"제목: {title}")

            gui_log("크롤링 내용 요약 중...")
            summary = summarize(model, local_text)

            local_path = save_local_original(local_text, title)
            summ_path = save_summary(summary, title)

            gui_log("저장완료:")
            gui_log(f"로컬: {os.path.basename(local_path)}")
            gui_log(f"요약: {os.path.basename(summ_path)}")

            gui_info("완료", f"2개 파일 저장됨!\n{title}")

        except requests.exceptions.ConnectionError as e:
            if "11434" in str(e):
                gui_error("Ollama 서버가 실행 중인지 확인하세요.")
            else:
                gui_error("네트워크 연결 오류가 발생했습니다.")

        except Exception as e:
            gui_log(f"에러: {e}")
            gui_error(str(e))

    def start_thread():
        threading.Thread(target=run, daemon=True).start()

    root = tk.Tk()
    root.title("크롤링 → Gemini 요약 자동화")
    root.geometry("700x500")

    def on_close():
        root.quit()
        root.destroy()
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(root, text="크롤링 URL").pack(pady=5)
    url_entry = tk.Entry(root, width=80)
    url_entry.pack(pady=5)

    control_frame = tk.Frame(root)
    control_frame.pack(pady=10)

    #기본선택
    model_var = tk.StringVar(value="Gemini")

    model_combo = ttk.Combobox(
        control_frame,
        textvariable=model_var,
        values=["Gemma3", "Gemini", "Exaone", "llama", "Mistral"],
        state="readonly",
        width=15
    )
    model_combo.pack(side=tk.LEFT, padx=5)

    tk.Button(
        control_frame,   # ✅ control_frame에 붙이기
        text="크롤링 + 요약 시작",
        command=start_thread,
        height=2
    ).pack(side=tk.LEFT, padx=5)

    log_box = scrolledtext.ScrolledText(root, width=85, height=20)
    log_box.pack(pady=10)

    root.mainloop()