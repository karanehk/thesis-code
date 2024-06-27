# Thesis: Evaluation of the Process of a Coursework Based on a Version Control Tool

This repository contains the code used for evaluating the process of a coursework based on a version control tool, specifically GitHub. The evaluation considers various criteria such as commit frequency, message quality, and overall commit density. We also use OpenAI's API for advanced analysis.

## 1. Download or Clone this Repository

To download or clone this repository, use the following command:

```bash
git clone https://github.com/karanehk/thesis-code.git 
cd thesis-code
```

## 2. Start a Virtual Environment

You can use either `venv` or `conda` to create a virtual environment. Here are the commands for both:

### Using `venv`:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```

### Using `conda`:

```bash
conda create --name thesis-env python=3.8
conda activate thesis-env
```

## 3. Install the Packages in `requirements.txt` to Your Environment

Install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

## 4. Define Your OpenAI API Key as an Environment Variable

Set your OpenAI API key as an environment variable named `OPENAI_API_KEY`:

### On macOS/Linux:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

### On Windows (Command Prompt):

```bash
set OPENAI_API_KEY='your-api-key-here'
```

### On Windows (PowerShell):

```bash
$env:OPENAI_API_KEY='your-api-key-here'
```

## 5. Run `main.py`

To start the evaluation process, run the `main.py` script:

```bash
python main.py
```

## 6. Provide Your Repository Link and the Desired Commit Range

When prompted, enter the GitHub repository link and the desired commit range for analysis.

### Example Input:

```
Enter the URL of the GitHub repository to analyze: https://github.com/username/repository
Enter the start of the commits: 4
Enter the end of the commits: 20
```

### *Note:*

*If you're in a restricted zone, ensure you have your VPN turned on because we use the OpenAI API, which may not be accessible from certain locations.*

---

By following these steps, you will be able to set up and run the evaluation process for your coursework repository. The results will help you understand the quality and characteristics of your commit history and overall development process.