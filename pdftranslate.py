import pymupdf
import torch
import argparse
from datetime import datetime
from transformers import MarianMTModel, MarianTokenizer

def format_time_delta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

def log_chronograph(page_index, total_pages, start_time):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elapsed = datetime.now() - start_time
    elapsed_str = format_time_delta(elapsed)
    print(f"[{now_str}] (Elapsed: {elapsed_str}) Processing page {page_index + 1}/{total_pages}")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

local_model_path = "./models/opus-mt-sv-en"

tokenizer = MarianTokenizer.from_pretrained(local_model_path)
model = MarianMTModel.from_pretrained(local_model_path).to(device)

def translate_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    outputs = model.generate(**inputs)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

def process_pdf(input_pdf_path: str, output_pdf_path: str, start_page:int, end_page: int, debug: bool = False):

    start_time = datetime.now()
    print(f"Started processing PDF at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    doc = pymupdf.open(input_pdf_path)
    new_doc = pymupdf.open()
    total_pages = len(doc)
    print(f"Total pages in input PDF: {total_pages}")

    if end_page > 0 and end_page <= total_pages:
        pages_to_process = list(range(start_page -1, end_page))
    else:
        pages_to_process = list(range(start_page -1, total_pages))
    print(f"Processing pages: {[p + 1 for p in pages_to_process]}")

    for page_index in pages_to_process:

        log_chronograph(page_index, len(pages_to_process), start_time)

        original_page = doc[page_index]
        original_blocks = original_page.get_text("blocks")

        if debug:
            print(f"\n--- Debug: Original Page {page_index +1} Blocks---")
            for block in original_blocks:
                print(block)

        new_doc.insert_pdf(doc, from_page=page_index, to_page=page_index)

        new_page = new_doc.new_page(
            width=original_page.rect.width,
            height=original_page.rect.height
        )

        padding = 10
        for block in original_blocks:
            #rect = fitz.Rect(block[:4])
            rect = pymupdf.Rect(
                block[0] - padding,
                block[1] - padding,
                block[2] + padding,
                block[3] + padding
            )
            original_text = block[4].strip()
            if original_text:
                translated = translate_text(original_text)
                new_page.insert_textbox(
                    rect,
                    translated,
                    fontsize=8,
                    fontname="helv",
                    align=0,
                    overlay=True
                )
            if debug:
                print("-----")
                print("Original text: ", original_text)
                print("Translated text: ", translated)

        if debug:
            new_page_blocks = new_page.get_text("blocks")
            print(f"\n--- Debug: Translated page (Output) {page_index +1} Blocks ---")
            for block in new_page_blocks:
                print(block)

    new_doc.save(output_pdf_path)

    end_time = datetime.now()
    total_elapsed = format_time_delta(end_time - start_time)
    print(f"Finished processing at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Processed {len(pages_to_process)} pages.")
    print(f"Total time : {total_elapsed}")
    print(f"Translated PDF saved as: {output_pdf_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description= "Translate a range of pages from Swedish PDF to English"
    )
    parser.add_argument("--input", type=str, default="./docs/input.pdf", help="Path to the Swedish PDF")
    parser.add_argument("--output", type=str, default="./docs/output.pdf", help="Path to output the translated PDF")
    parser.add_argument("--start", type=int, default=1, help="Start page (1-indexed)")
    parser.add_argument("--end", type=int, default=0, help="End page (1-indexed, 0 means until the last page")
    parser.add_argument("--debug", action="store_true", help="Enables debugging output of text blocks")
    args = parser.parse_args()

    process_pdf(args.input, args.output, args.start, args.end, args.debug)