import re
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
def compress_html(html):
    html = re.sub(r'<!--(.*?)-->', '', html, flags=re.DOTALL)
    html = re.sub(r'>\s+<', '><', html)
    # html = re.sub(r'\s+', ' ', html) # THIS IS WHAT BREAKS SOME WEBSITES (HTML files) DO NOT ENABLE IT UNLESS YOU DONT HAVE SOME ADVANCED JAVASCRIPT
    html = html.strip()
    def preserve(match):
        return match.group().replace(' ', '&nbsp;')
    html = re.sub(r'<(pre|textarea).*?>.*?</\1>', preserve, html, flags=re.DOTALL)
    return html
def compress_thread():
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            input_html = file.read()
        compressed_html = compress_html(input_html)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(compressed_html)
        root.after(0, lambda: status_label.config(text="Compression complete!"))
    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
    finally:
        root.after(0, enable_button)
def compress_button_click():
    global input_file_path, output_file_path
    input_file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if not input_file_path:
        return
    output_file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if not output_file_path:
        return
    compress_button.config(state=tk.DISABLED)
    status_label.config(text="Compressing...")
    threading.Thread(target=compress_thread, daemon=True).start()
def enable_button():
    compress_button.config(state=tk.NORMAL)
root = tk.Tk()
root.title("HTML Compressor")
root.geometry("400x150")
compress_button = tk.Button(root, text="Select and Compress HTML File", command=compress_button_click)
compress_button.pack(pady=20)
status_label = tk.Label(root, text="")
status_label.pack(pady=10)
root.mainloop()
