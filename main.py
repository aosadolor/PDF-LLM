import langchain_community
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_text_splitters import CharacterTextSplitter

from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
from langdetect import detect
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Set up the OpenAI API key
openai_api_key = ""

# Initialize the OpenAI model
openai = OpenAI(api_key=openai_api_key, model="gpt-4")

# Define prompt templates for different languages
prompt_templates = {
    "en":
    PromptTemplate(input_variables=["text"],
                   template="""
        You are a helpful assistant that processes and analyzes text. Here is the text:
        {text}
        Please summarize the key points and provide an analysis.
        """),
    "es":
    PromptTemplate(input_variables=["text"],
                   template="""
        Eres un asistente útil que procesa y analiza textos. Aquí está el texto:
        {text}
        Por favor, resume los puntos clave y proporciona un análisis.
        """),
    # Add more templates for other languages if needed
}

# Initialize the GPT tokenizer
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

# Initialize the TextSplitter
text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(
    tokenizer, chunk_size=100, chunk_overlap=0)


# Define a function to process and analyze text
def process_text(text, lang="en"):
    # Choose the appropriate prompt template based on the detected language
    prompt_template = prompt_templates.get(lang, prompt_templates["en"])

    # Split the text into manageable chunks
    chunks = text_splitter.split_text(text)

    # Initialize an empty list to store results
    results = []

    # Iterate over each chunk and get a response from the LLM
    for chunk in chunks:
        # Tokenize the chunk
        tokens = tokenizer.encode(chunk)

        # Convert tokens back to text for the LLM input
        chunk_text = tokenizer.decode(tokens)

        # Create a prompt for the LLM
        prompt = prompt_template.format(text=chunk_text)

        # Get the response from the LLM
      
          try:
            response = openai.generate(prompt)
            results.append(response["choices"][0]["text"])
        except Exception as e:
            results.append(f"Error processing chunk: {str(e)}")

    return results


# Define a function to load and process a PDF file
def process_pdf():
    try:
        # Load the PDF file
        loader = PyPDFLoader("MCDP1-1.pdf")
        documents = loader.load()

        # Extract text from the documents
        pdf_text = "MCDP1-1.pdf".join([doc.text for doc in documents])

        # Detect the language of the text
        lang = detect(pdf_text)

        # Process the extracted text
        return process_text(pdf_text, lang=lang)
    except Exception as e:
        return [f"Error loading PDF: {str(e)}"]
      # Define GUI functions
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_path_entry.delete(0, tk.END)
        pdf_path_entry.insert(0, file_path)


def process_file():
    pdf_path = pdf_path_entry.get()
    if not os.path.isfile("MCDP1-1.pdf"):
        messagebox.showerror("Error", f"File not found: {pdf_path}")
        return

    results = process_pdf("MCDP1-1.pdf")
    result_text.delete("1.0", tk.END)
    for i, result in enumerate(results, start=1):
        result_text.insert(tk.END, f"Chunk {i} Analysis:\n{result}\n\n")


# Create the main window
root = tk.Tk()
root.title("PDF Analyzer")

# Create and place the PDF path entry and browse button
pdf_path_entry = tk.Entry(root, width=50)
pdf_path_entry.grid(row=0, column=0, padx=10, pady=10)

browse_button = tk.Button(root, text="Browse", command=open_file)
browse_button.grid(row=0, column=1, padx=10, pady=10)

# Create and place the process button
process_button = tk.Button(root, text="Process", command=process_file)
process_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create and place the result text box
result_text = tk.Text(root, wrap=tk.WORD, height=20, width=80)
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Run the GUI event loop
root.mainloop()
