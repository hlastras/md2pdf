FROM pandoc/latex:latest-ubuntu

# Install Python and required packages
# Start of Selection
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# End of Selection

# Set up a virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"


RUN apt-get update && \
    apt-get install -y fonts-lmodern fonts-dejavu fonts-noto-cjk && \
    fc-cache -fv

# Install required Python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy all necessary files
COPY process.py /app/
COPY convert.sh /app/
COPY cites.csl /app/
COPY preamble.tex /app/

# Set working directory
WORKDIR /app

# Make the script executable
RUN chmod +x /app/convert.sh

# Create a volume for input/output files
VOLUME /data

ENTRYPOINT ["/app/convert.sh"] 