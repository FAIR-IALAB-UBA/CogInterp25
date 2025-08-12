# CogInterp25
Documentation, files and script used to prepare the paper presented at CogInterp - NeurIPS25

## Overview

This project generates synthetic medical records to evaluate Large Language Models (LLMs) on causal reasoning tasks in healthcare contexts. The system creates controlled datasets with cause-effect relationships and tests how well different AI models (Claude, Gemini, and ChatGPT) can identify causal patterns in medical data.

## Project Structure

- [`create_cont_list.ipynb`](create_cont_list.ipynb) - Jupyter notebook for generating synthetic medical record combinations
- [`git_run_heathcare.py`](git_run_heathcare.py) - Main script to evaluate AI models on medical reasoning tasks
- `medical_records_with_results_*.xlsx` - Generated datasets with AI model evaluation results
- [`LICENSE`](LICENSE) - Apache 2.0 license

## How it Works

1. **Data Generation**: The [`create_cont_list.ipynb`](create_cont_list.ipynb) notebook reads cause-effect variable pairs and generates synthetic medical records with controlled distributions
2. **Model Evaluation**: The [`git_run_heathcare.py`](git_run_heathcare.py) script sends these medical records to three AI models (Claude, Gemini, ChatGPT) and collects their causal reasoning responses
3. **Results**: Each model's effectiveness scores are saved in Excel files for analysis

## Setup

1. Install required dependencies:
```bash
pip install openai pandas tqdm google-generativeai anthropic openpyxl
```

2. Set up API keys in [`git_run_heathcare.py`](git_run_heathcare.py):
   - Replace `"GOOGLE_API_KEY"` with your Google/Gemini API key
   - Replace `"ANTHROPIC_API_KEY"` with your Anthropic/Claude API key  
   - Replace `"OPENAI_API_KEY"` with your OpenAI API key

3. Prepare your input file:
   - Update the filename [`git_run_heathcare.py`](git_run_heathcare.py): `medical_records = pd.read_excel('YOUR_FILE_NAME', sheet_name=0)`

## Usage

1. **Generate medical records** (optional if you already have data):
```bash
jupyter notebook create_cont_list.ipynb
```

2. **Run model evaluation**:
```bash
python git_run_heathcare.py
```

The script will process each row of medical records, query all three AI models, and save results incrementally to `medical_records_with_results.xlsx`.

## Output

The script generates Excel files containing:
- Original medical record data
- Claude model responses (`claude_results`)
- Gemini model responses (`gemini_results`) 
- ChatGPT model responses (`chatgpt_results`)

Each model returns JSON-formatted effectiveness scores for causal reasoning evaluation.