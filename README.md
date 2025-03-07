# PDF Translate

PDFTranslate is a ~~robust and efficient~~ quick and dirty translation tool designed for organizations that prioritize data privacy and security. Unlike other solutions that depend on external APIs, PDFTranslate leverages pre-trained models for offline translation, ensuring that sensitive information remains in-house and protected.

## TODO List

- [x] Load the PDF
- [x] Select Pages
- [x] Extract Text
- [x] Translate Text
- [x] Create New PDF
- [x] Save the PDF
- [ ] Integrate automatic model downloads
- [ ] Implement language recognition for automatic translation
- [ ] Add a user interface
- [ ] Provide an API to use PDFTranslate as a service
- [ ] Integrate optical character recognition (OCR)
- [ ] Support right-to-left languages

This is an early proof of concept that will eventually be updated to integrate automatic model downloads, language recognition to automatically translate from the correct language to the preferred output language, a user interface, an API to use PDFTranslate as a service, optical character recognition (OCR), and support for right-to-left languages.

## How It Works

1. **Load the PDF**: The program starts by loading the input PDF file that you want to translate.
2. **Select Pages**: You can specify the range of pages to be translated. If no end page is specified, it will translate until the last page.
3. **Extract Text**: The program extracts text blocks from each page of the PDF. Each block is a tuple containing the position and the text. The structure of the tuple is as follows:

    ```python
    (x0, y0, x1, y1, text, block_no, block_type)
    ```

    - `x0, y0`: The coordinates of the top-left corner of the text block.
    - `x1, y1`: The coordinates of the bottom-right corner of the text block.
    - `text`: The extracted text block.
    - `block_no`: The block number.
    - `block_type`: The type of the block.

4. **Translate Text**: Each extracted text block is translated from Swedish to English using a pre-trained translation model.
5. **Create New PDF**: A new PDF is created where each original page is followed by a page with the translated text blocks.
6. **Save the PDF**: The translated PDF is saved to the specified output path.

This process ensures that your sensitive data remains secure as the translation is done offline without relying on external services.

## Version History

- 0.1b Translates from Swedeish(sv) to English(en). Extracts blocks from PDF documents using [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) (formerly fitz) then translates the blocks using the [Helsinki-NLP/opus-nt-sv-en](https://huggingface.co/Helsinki-NLP/opus-mt-sv-en) and then copies original page followed by translated blocks on every other page.

## Usage

Tested with [Python 3.11.9](https://www.python.org/downloads/release/python-3119/)

To avoid conflicts, it is recommended to use a virtual environment. [PyCharm - Configure a virtualenv environment](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)

Alternatively, you can use [Anaconda](https://docs.anaconda.com/anaconda/install/) or [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) to set up and manage your virtual environments.



### Install the required packages:

If you want to use CPU only
```bash
pip install -r requirements_cpu.txt
```

If you have a CUDA capable GPU
```bash
pip install -r requirements_cuda.txt
```
### Model Download

To use PDFTranslate, you need to download the pre-trained translation model. The model used in this project is `opus-mt-sv-en` from Helsinki-NLP. You can download the model from the [Helsinki-NLP/opus-mt-sv-en](https://huggingface.co/Helsinki-NLP/opus-mt-sv-en) repository. Since the repository uses Git Large File Storage (LFS), you need to have `git-lfs` installed on your system.

#### Steps to Download the Model

1. **Install Git LFS**:
    ```bash
    git lfs install
    ```

2. **Clone the Model Repository**:
    Navigate to the directory where you want to store the model and run the following command:
    ```bash
    git clone https://huggingface.co/Helsinki-NLP/opus-mt-sv-en ./models/opus-mt-sv-en
    ```

Make sure the model is placed in the `./models/opus-mt-sv-en` directory relative to your project root, as the script expects the model to be in this location.

If you want to translate other languages, you can download different models in the same manner. However, you will need to modify the code to use the correct model and tokenizer.

### Example: Using English to French Model

To use the English to French model, follow these steps:

1. **Clone the English to French Model Repository**:
    Navigate to the directory where you want to store the model and run the following command:
    ```bash
    git clone https://huggingface.co/Helsinki-NLP/opus-mt-en-fr ./models/opus-mt-en-fr
    ```

2. **Modify the Code**:
    Update the code to use the English to French model and tokenizer. For example, in `pdftranslate.py`, change the model and tokenizer paths:

    ```python
    from transformers import MarianMTModel, MarianTokenizer

    # Load the English to French model and tokenizer
    model_name = './models/opus-mt-en-fr'
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    ```

    Ensure that the rest of your code uses these variables for translation.

### Running the script

To use the script, run the following command in your terminal:

```commandline
(.venv) PS C:\PDFTranslate> python pdftranslate.py --input <path_to_input_pdf> --output <path_to_output_pdf> --start <start_page> --end <end_page> [--debug]
```

### Example

```commandline
(.venv) PS C:\PDFTranslate> python pdftranslate.py --input ./docs/input.pdf --output ./docs/output.pdf --start 9 --end 10 --debug
```

## Arguments

- `--input` (type: `str`, default: `./docs/input.pdf`): Path to the Swedish PDF.
- `--output` (type: `str`, default: `./docs/output.pdf`): Path to output the translated PDF.
- `--start` (type: `int`, default: `1`): Start page (1-indexed).
- `--end` (type: `int`, default: `0`): End page (1-indexed, 0 means until the last page).
- `--debug` (action: `store_true`): Enables debugging output of text blocks.

---

Wheel packages available on [PyPi.org](https://pypi.org/) can be downloaded manually and installed with the following command.

```commandline
(.venv) PS C:\PDFTranslate> pip install --no-index --find-links=. .\pymupdf-1.25.3-cp39-abi3-win_amd64.whl 
```

---
 