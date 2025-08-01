import tkinter as tk
from tkinter import messagebox, PhotoImage, filedialog, ttk
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import langid
import os
import re



# Ensuring consistent results from langdetect
DetectorFactory.seed = 0


# Enhanced language detection function that combines multiple methods
def detect_language_combined(text):
    # Clean the text
    text = text.strip()
    if not text:
        return 'und'
    
    
    # Simple language patterns for better recognition
    patterns = {
        # English patterns
        'en': [r'\b(the|and|is|in|to|of|a|for|that|this|you|it|with|on|at|by|from|are|have|has|been|was|were|will|would|can|could|should|may|might|must)\b'],
        # Spanish patterns
        'es': [r'\b(el|la|los|las|y|en|de|un|una|que|es|para|por|con|su|al|del|se|no|como|más|lo|las|esto|esta|estos|estas|muy)\b'],
        # French patterns
        'fr': [r'\b(le|la|les|un|une|des|et|en|à|de|du|que|qui|ce|cette|ces|il|elle|ils|elles|nous|vous|je|tu|on|pour|par|avec|sans|dans|sur|sous)\b'],
        # German patterns
        'de': [r'\b(der|die|das|und|in|zu|den|dem|ein|eine|einer|eines|mit|für|auf|ist|sind|sein|haben|hat|wird|werden|kann|nicht|auch|von|bei|nach)\b'],
        # Russian patterns
        'ru': [r'[а-яА-Я]+', r'\b(и|в|на|с|по|для|от|к|за|из|у|о|об|как|что|это|так|но|да|нет|все|они|мы|вы|он|она|оно)\b'],
        # Chinese patterns (simplified)
        'zh': [r'[\u4e00-\u9fff]+'],
        # Japanese patterns
        'ja': [r'[\u3040-\u309F\u30A0-\u30FF]+'],
        # Korean patterns
        'ko': [r'[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]+'],
        # Arabic patterns
        'ar': [r'[\u0600-\u06FF]+'],
        # Hindi patterns
        'hi': [r'[\u0900-\u097F]+'],
        # Malayalam patterns
        'ml': [r'[\u0D00-\u0D7F]+'],
        # Tamil patterns
        'ta': [r'[\u0B80-\u0BFF]+'],
        # Telugu patterns
        'te': [r'[\u0C00-\u0C7F]+'],
        # Kannada patterns
        'kn': [r'[\u0C80-\u0CFF]+'],
        # Bengali patterns
        'bn': [r'[\u0980-\u09FF]+'],
        # Gujarati patterns
        'gu': [r'[\u0A80-\u0AFF]+'],
        # Marathi uses Devanagari script like Hindi
        'mr': [r'[\u0900-\u097F]+']
    }
    
    
    # Check for script-based patterns first (strongest indicator)
    for lang, pattern_list in patterns.items():
        for pattern in pattern_list:
            if re.search(pattern, text, re.IGNORECASE):
                # If strong script match (for non-Latin scripts), return immediately
                if lang in ['zh', 'ja', 'ko', 'ar', 'hi', 'ml', 'ta', 'te', 'kn', 'bn', 'gu', 'mr', 'ru'] and len(re.findall(pattern, text)) > 2:
                    return lang
    
    
    # Try langdetect first
    try:
        langdetect_code = detect(text)
        if langdetect_code != 'und':
            return langdetect_code
    except LangDetectException:
        pass
    
    # Try langid
    try:
        langid_code, _ = langid.classify(text)
        if langid_code != 'und':
            return langid_code
    except Exception:
        pass
    
    # If nothing worked well, return undetermined
    return 'und'



def get_language_name(code):
    languages = {
        "en": "English", "es": "Spanish", "ml": "Malayalam", "fr": "French",
        "de": "German", "it": "Italian", "pt": "Portuguese", "nl": "Dutch",
        "ru": "Russian", "ja": "Japanese", "zh": "Chinese", "ar": "Arabic",
        "ko": "Korean", "hi": "Hindi", "ta": "Tamil", "te": "Telugu", "kn": "Kannada", 
        "gu": "Gujarati", "mr": "Marathi", "bn": "Bengali", "pa": "Punjabi", "or": "Odia", 
        "as": "Assamese", "ur": "Urdu", "tr": "Turkish", "pl": "Polish", "sv": "Swedish", 
        "no": "Norwegian", "da": "Danish", "fi": "Finnish", "cs": "Czech", "ro": "Romanian", 
        "sk": "Slovak", "sr": "Serbian", "el": "Greek", "he": "Hebrew", "hu": "Hungarian",
        "bg": "Bulgarian", "id": "Indonesian", "ms": "Malay", "th": "Thai", "vi": "Vietnamese",
        "fa": "Persian", "tl": "Tagalog", "uk": "Ukrainian", "lt": "Lithuanian", "lv": "Latvian",
        "et": "Estonian", "sl": "Slovenian", "hr": "Croatian", "ca": "Catalan", "gl": "Galician",
        "eu": "Basque", "cy": "Welsh", "ga": "Irish", "lb": "Luxembourgish", "mt": "Maltese",
        "so": "Somali", "af": "Afrikaans", "sq": "Albanian", "am": "Amharic", "hy": "Armenian",
        "az": "Azerbaijani", "be": "Belarusian", "bs": "Bosnian", "ce": "Chechen", "ny": "Chichewa",
        "zh-cn": "Chinese (Simplified)", "zh-tw": "Chinese (Traditional)", "co": "Corsican",
        "eo": "Esperanto", "fil": "Filipino", "fy": "Frisian", "ka": "Georgian", "gd": "Scots Gaelic",
        "ha": "Hausa", "haw": "Hawaiian", "hmn": "Hmong", "ig": "Igbo", "is": "Icelandic",
        "jw": "Javanese", "rw": "Kinyarwanda", "ku": "Kurdish", "ky": "Kyrgyz", "lo": "Lao",
        "la": "Latin", "mk": "Macedonian", "mg": "Malagasy", "mi": "Maori", "mn": "Mongolian",
        "my": "Myanmar (Burmese)", "ne": "Nepali", "ps": "Pashto", "sm": "Samoan", "gd": "Scots Gaelic",
        "st": "Sesotho", "sn": "Shona", "sd": "Sindhi", "si": "Sinhala", "sw": "Swahili",
        "tg": "Tajik", "tt": "Tatar", "und": "Unknown"
    }
    return languages.get(code, "Unknown Language")



def detect_language():
    try:
        text = text_box.get("1.0", "end-1c").strip()
        if text:
            language_code = detect_language_combined(text)
            language_name = get_language_name(language_code)
            
            # Update the result display
            result_label.config(text=f"{language_name}", font=("Helvetica", 24, "bold"), 
                               fg="lime" if language_code != "und" else "orange")
            
            # Add the detected language to the history
            add_to_history(text[:30] + "..." if len(text) > 30 else text, language_name)
            
            # Update status
            status_label.config(text=f"Detection complete: {language_name}")
        else:
            messagebox.showwarning("Input Error", "Please enter some text to detect the language.")
    except Exception as e:
        messagebox.showerror("Error", f"Error detecting language: {e}")

def clear_input():
    text_box.delete("1.0", "end")
    result_label.config(text="", font=("Helvetica", 24, "bold"), fg="cyan")
    status_label.config(text="Ready")

def browse_file():
    try:
        file_path = filedialog.askopenfilename(
            title="Select a text file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        
        if file_path:
            # Update the file path entry
            file_path_var.set(file_path)
            
            # Read the file content
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                file_content = file.read()
                
            # Clear the text box and insert the file content
            text_box.delete("1.0", "end")
            text_box.insert("1.0", file_content)
            
            # Update status
            status_label.config(text=f"File loaded: {os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error loading file: {e}")

def add_to_history(text_preview, language):
    history_tree.insert("", 0, values=(text_preview, language))

def export_history():
    try:
        file_path = filedialog.asksaveasfilename(
            title="Save Detection History",
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("Language Detection History\n")
                file.write("-----------------------\n\n")
                
                for item in history_tree.get_children():
                    text, lang = history_tree.item(item)["values"]
                    file.write(f"Text: {text}\n")
                    file.write(f"Language: {lang}\n")
                    file.write("-----------------------\n")
                    
            messagebox.showinfo("Export Complete", f"History exported to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error exporting history: {e}")

def clear_history():
    for item in history_tree.get_children():
        history_tree.delete(item)

# Create the main window with a dark theme
root = tk.Tk()
root.title("Advanced Language Detector")
root.configure(bg="#121212")
root.geometry("800x700")

# Configure styles for a dark theme
style = ttk.Style()
style.theme_use('default')
style.configure('TFrame', background='#121212')
style.configure('TButton', background='#333333', foreground='white')
style.configure('TLabel', background='#121212', foreground='white')
style.configure('TNotebook', background='#121212', foreground='white')
style.configure('TNotebook.Tab', background='#333333', foreground='white')
style.map('TNotebook.Tab', background=[('selected', '#0078D7')])

# Create notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Create the main tab
main_tab = ttk.Frame(notebook)
notebook.add(main_tab, text="Detector")

# Create the history tab
history_tab = ttk.Frame(notebook)
notebook.add(history_tab, text="History")

# Configure the main tab
try:
    # Try to load the logo
    logo_path = "C:/Users/abint/OneDrive/Documents/pyt8/download.png"
    logo_img = PhotoImage(file=logo_path)
    logo_label = tk.Label(main_tab, image=logo_img, bg="#121212")
    logo_label.pack(pady=10)
except Exception:
    # If logo can't be loaded, create a text label instead
    logo_label = tk.Label(main_tab, text="LANGUAGE DETECTOR", font=("Helvetica", 16, "bold"), bg="#121212", fg="#0078D7")
    logo_label.pack(pady=10)

# File selection frame
file_frame = ttk.Frame(main_tab)
file_frame.pack(fill="x", padx=10, pady=5)

file_path_var = tk.StringVar()
file_path_entry = ttk.Entry(file_frame, textvariable=file_path_var, width=50)
file_path_entry.pack(side="left", padx=5, fill="x", expand=True)

browse_button = ttk.Button(file_frame, text="Browse File", command=browse_file)
browse_button.pack(side="right", padx=5)

# Text input area
text_box = tk.Text(main_tab, height=10, width=60, bg="#1E1E1E", fg="#FFFFFF", insertbackground="#FFFFFF")
text_box.pack(pady=10, padx=10, fill="both", expand=True)

# Button frame
button_frame = ttk.Frame(main_tab)
button_frame.pack(fill="x", padx=10, pady=5)

detect_button = ttk.Button(button_frame, text="Detect Language", command=detect_language)
detect_button.pack(side="left", padx=5)

clear_button = ttk.Button(button_frame, text="Clear", command=clear_input)
clear_button.pack(side="left", padx=5)

# Result display
result_frame = ttk.Frame(main_tab)
result_frame.pack(fill="x", padx=10, pady=10)

result_label = tk.Label(result_frame, text="", font=("Helvetica", 24, "bold"), bg="#121212", fg="cyan")
result_label.pack()

# Status bar
status_label = ttk.Label(main_tab, text="Ready", relief="sunken", anchor="w")
status_label.pack(side="bottom", fill="x", padx=10, pady=5)

# Configure the history tab
history_frame = ttk.Frame(history_tab)
history_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Create treeview for history
history_tree = ttk.Treeview(history_frame, columns=("Text", "Language"), show="headings")
history_tree.heading("Text", text="Text")
history_tree.heading("Language", text="Detected Language")
history_tree.column("Text", width=350)
history_tree.column("Language", width=150)
history_tree.pack(fill="both", expand=True, side="left")

# Add scrollbar to history
scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=history_tree.yview)
scrollbar.pack(side="right", fill="y")
history_tree.configure(yscrollcommand=scrollbar.set)

# History button frame
history_button_frame = ttk.Frame(history_tab)
history_button_frame.pack(fill="x", padx=10, pady=5)

export_button = ttk.Button(history_button_frame, text="Export History", command=export_history)
export_button.pack(side="left", padx=5)

clear_history_button = ttk.Button(history_button_frame, text="Clear History", command=clear_history)
clear_history_button.pack(side="left", padx=5)

root.mainloop()