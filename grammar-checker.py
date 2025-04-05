import language_tool_python
import tkinter as tk
from tkinter import scrolledtext
import openai

class GrammarChecker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Grammar Checker")
        self.window.geometry("800x600")
        
        # Initialize the language tool
        self.tool = language_tool_python.LanguageTool('en-US')
        
        # Initialize OpenAI (replace with your API key)
        openai.api_key = 'your-api-key-here'
        
        self.create_widgets()
    
    def create_widgets(self):
        # Input text area
        input_label = tk.Label(self.window, text="Enter text to check:")
        input_label.pack(pady=5)
        
        self.input_text = scrolledtext.ScrolledText(self.window, height=8)
        self.input_text.pack(padx=10, pady=5)
        
        # Buttons frame
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=5)
        
        # Basic check button (LanguageTool)
        basic_check_button = tk.Button(button_frame, text="Basic Check", command=self.basic_check)
        basic_check_button.pack(side=tk.LEFT, padx=5)
        
        # AI check button (OpenAI)
        ai_check_button = tk.Button(button_frame, text="AI Check", command=self.ai_check)
        ai_check_button.pack(side=tk.LEFT, padx=5)
        
        # Output text area
        output_label = tk.Label(self.window, text="Corrected text:")
        output_label.pack(pady=5)
        
        self.output_text = scrolledtext.ScrolledText(self.window, height=8)
        self.output_text.pack(padx=10, pady=5)
        
        # Suggestions area
        suggestions_label = tk.Label(self.window, text="AI Suggestions:")
        suggestions_label.pack(pady=5)
        
        self.suggestions_text = scrolledtext.ScrolledText(self.window, height=6)
        self.suggestions_text.pack(padx=10, pady=5)
    
    def basic_check(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if text:
            try:
                matches = self.tool.check(text)
                corrected_text = language_tool_python.utils.correct(text, matches)
                
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", corrected_text)
                
                self.suggestions_text.delete("1.0", tk.END)
                self.suggestions_text.insert("1.0", "Basic grammar check completed.")
            except Exception as e:
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", f"Error: {str(e)}")
    
    def ai_check(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if text:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a professional editor. Provide both the corrected text and brief explanations of major improvements."},
                        {"role": "user", "content": f"Please correct this text and explain major improvements:\n\n{text}"}
                    ]
                )
                
                ai_response = response.choices[0].message.content
                
                # Split the response into corrected text and explanations
                parts = ai_response.split("\n\n", 1)
                corrected_text = parts[0]
                explanations = parts[1] if len(parts) > 1 else "No additional suggestions."
                
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", corrected_text)
                
                self.suggestions_text.delete("1.0", tk.END)
                self.suggestions_text.insert("1.0", explanations)
            except Exception as e:
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", f"Error: {str(e)}")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = GrammarChecker()
    app.run()
