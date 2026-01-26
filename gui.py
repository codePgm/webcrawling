import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import sys
import os
from crawler import crawl_local
from summarizer import summarize_best,summarize, get_ai_content
from utils import save_local_original, save_ai_original, save_summary

def start_gui():
    def log(msg):
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)

    def gui_log(msg):
        root.after(0, lambda: log(msg))

    def gui_info(title, msg):
        root.after(0, lambda: messagebox.showinfo(title, msg))

    def gui_error(msg):
        root.after(0, lambda: messagebox.showerror("에러", msg))

    def run():
        try:
            url = url_entry.get().strip()
            if not url:
                gui_error("URL을 입력하세요.")
                return

            gui_log("크롤링 시작")
            title, local_text = crawl_local(url)
            ai_content = get_ai_content(url)
            gui_log(f"제목: {title}")

            gui_log("크롤링 내용 최적화 + 요약 중...")
            best_crawler = summarize_best(url)
            summary = summarize(best_crawler)
            
            # 제목으로 파일명 저장
            from utils import save_local_original, save_ai_original, save_summary
            
            local_path = save_local_original(local_text, title)
            ai_path = save_ai_original(ai_content, title)
            summ_path = save_summary(summary, title)
            
            gui_log(f"저장완료:")
            gui_log(f"로컬: {os.path.basename(local_path)}")
            gui_log(f"AI :   {os.path.basename(ai_path)}")
            gui_log(f"요약: {os.path.basename(summ_path)}")
            
            gui_info("완료", f"3개 파일 저장됨!\n{title}")
            
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

    tk.Button(
        root,
        text="크롤링 + 요약 시작",
        command=start_thread,
        height=2
    ).pack(pady=10)

    log_box = scrolledtext.ScrolledText(root, width=85, height=20)
    log_box.pack(pady=10)

    root.mainloop()