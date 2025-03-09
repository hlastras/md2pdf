# Markdown to PDF Converter

This tool converts Markdown documents to PDF files using Pandoc. It:
1. Extracts links from the Markdown and creates a BibTeX file
2. Replaces links with citation references
3. Replaces Unicode special characters with LaTeX commands
4. Converts the preprocessed Markdown to PDF using Pandoc

## Prerequisites

- Docker

## Building the Docker Image

```bash
docker build -t md2pdf .
```

## Usage

### Using Docker

```bash
docker run --rm -v $(pwd):/data md2pdf /data/input.md /data/output.pdf
```

Where:
- `input.md` is your Markdown file
- `output.pdf` is the name of the output PDF file

### Without Docker

If you prefer not to use Docker, ensure you have the following installed:
- Python 3 with the `mistune` package
- Pandoc with LaTeX support (xelatex)
- The required fonts: Latin Modern Roman, Latin Modern Math, DejaVu Sans, Noto Sans CJK JP

Then run:

```bash
./convert.sh input.md output.pdf
```

## Files Included

- `process.py`: Python script to preprocess Markdown
- `convert.sh`: Bash script to orchestrate the conversion
- `preamble.tex`: LaTeX preamble with font configurations
- `cites.csl`: Citation Style Language file
- `requirements.txt`: Python dependencies

## Local Development

To facilitate development and debugging without rebuilding the Docker image, you can override the entrypoint and run scripts locally while still using the containerized environment.

### Running Scripts Locally with Docker

#### Running the Bash Script (`convert.sh`)
```bash
docker run --rm -v $(pwd):/data  -w /data --entrypoint /bin/bash md2pdf -c "/data/convert.sh /data/input.md /data/output.pdf"
```

#### Running the Python Script (`process.py`)
```bash
docker run --rm -v $(pwd):/data -w /data --entrypoint python md2pdf /data/process.py /data/input.md /data/output.md
```

This setup allows you to modify the scripts, CSL, or LaTeX preamble locally and test changes immediately using the existing Docker image. Once everything works as expected, you can rebuild the image and use the updated version.

