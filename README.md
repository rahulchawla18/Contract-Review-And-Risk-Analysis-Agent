# Contract Review & Risk Analysis Agent

An intelligent AI-powered application that automatically analyzes legal contracts, extracts key clauses, assesses risks, and provides actionable revision suggestions. Built with FastAPI, Gradio, LangChain, and Groq (fast, cloud-based LLM).

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Deployment](#deployment)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Architecture](#architecture)
- [Performance Optimizations](#performance-optimizations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## ✨ Features

- **PDF Contract Analysis**: Upload and analyze PDF contracts automatically
- **Intelligent Clause Extraction**: Extracts 5 key clause types:
  - Termination clauses
  - Confidentiality agreements
  - Payment terms
  - Liability provisions
  - Governing law
- **Risk Assessment**: Classifies each clause as High, Medium, or Low risk with detailed explanations
- **Revision Suggestions**: Provides actionable, prioritized recommendations to reduce legal, financial, and operational risks
- **Modern Web UI**: Beautiful Gradio interface with drag-and-drop file upload
- **RESTful API**: FastAPI backend for programmatic access
- **Parallel Processing**: Optimized for speed with concurrent task execution
- **Progress Tracking**: Real-time progress indicators during analysis

## 📁 Project Structure

```
Contract_Review_And_Risk_Analysis_Agent/
├── app/
│   ├── __pycache__/
│   ├── config.py                 # Configuration settings
│   ├── gradio_ui.py              # Gradio web interface
│   ├── main.py                   # FastAPI application
│   ├── orchestrator.py           # Main orchestration logic
│   ├── models/
│   │   └── agent_models.py      # Pydantic models
│   └── services/
│       ├── clause_extractor.py   # Clause extraction service
│       ├── pdf_loader.py         # PDF loading service
│       ├── revision_agent.py     # Revision suggestions service
│       └── risk_classifier.py    # Risk classification service
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── pyproject.toml                # Project dependencies
├── README.md                     # This file
├── run_gradio.py                 # Gradio launcher script
└── uv.lock                       # Dependency lock file
```

## 🔧 Prerequisites

Before you begin, ensure you have the following:

1. **Python 3.13+** - The project requires Python 3.13 or higher
2. **UV Package Manager** - Modern Python package manager
   - Install from: https://github.com/astral-sh/uv
   - Or via: `pip install uv`
3. **Groq API Key** - Free API key for fast LLM inference
   - Get it from: https://console.groq.com/
   - Free tier: 14,400 requests per day
   - No local installation required

## 📦 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Contract_Review_And_Risk_Analysis_Agent
```

### Step 2: Install Dependencies

The project uses `uv` for dependency management. Install all dependencies:

```bash
uv sync
```

This will:
- Create a virtual environment (`.venv`)
- Install all required packages
- Lock dependencies in `uv.lock`

### Step 3: Get Groq API Key

The application uses Groq for fast, cloud-based LLM inference. Setup Groq:

1. **Visit Groq Console**: Go to https://console.groq.com/
2. **Sign up/Login**: Create an account or sign in
3. **Create API Key**: Navigate to API Keys section and generate a new key
4. **Copy the Key**: You'll need it for the next step

**Note**: Groq offers a generous free tier (14,400 requests per day) - perfect for development and testing!

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# .env file
# Groq API Key (required)
# Get your free API key from: https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here

# Groq model (optional - defaults to llama-3.1-8b-instant)
# Check https://console.groq.com/docs/models for latest models
GROQ_MODEL=llama-3.1-8b-instant
```

**Configuration Options:**

- `GROQ_API_KEY`: Your Groq API key (required)
  - Get it free from: https://console.groq.com/
  - Free tier: 14,400 requests per day
- `GROQ_MODEL`: The Groq model to use (default: `llama-3.1-8b-instant`)
  - Recommended models:
    - `llama-3.3-70b-versatile` - Best quality
    - `llama-3.1-8b-instant` - Fast and efficient (default)
    - `llama-3.2-90b-text-preview` - Very high quality
    - `mixtral-8x7b-32768` - Good balance
    - `gemma-7b-it` - Fast and efficient

## 🚀 Running the Application

### Option 1: Gradio Web UI (Recommended)

The easiest way to use the application is through the Gradio web interface:

```bash
uv run python run_gradio.py
```

Or directly:

```bash
uv run python -m app.gradio_ui
```

**What happens:**
- The application will find an available port (starting from 7860)
- You'll see a message: `🚀 Starting Gradio UI on http://127.0.0.1:7860`
- Open your browser and navigate to the displayed URL

**Features:**
- Drag-and-drop PDF upload
- Real-time progress tracking
- Three-tab interface for results
- Beautiful, responsive design

### Option 2: FastAPI Backend

Run the FastAPI server for API access:

```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Endpoints:**
- `GET /` - API information
- `GET /health` - Health check
- `POST /review` - Contract review endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

### Option 3: Development Mode

For development with auto-reload:

```bash
# Gradio UI with auto-reload (if supported)
uv run python -m app.gradio_ui

# FastAPI with auto-reload
uv run uvicorn app.main:app --reload
```

## 🚀 Deployment

### Deploy to Render (Recommended)

This application is ready to deploy to Render with minimal configuration.

**Quick Deploy:**

1. **Push to Git**: Push your code to GitHub/GitLab/Bitbucket
2. **Connect to Render**: 
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your repository
3. **Configure**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m app.gradio_ui`
   - **Environment Variables**: Add `GROQ_API_KEY` (get from https://console.groq.com/)
4. **Deploy**: Click "Create Web Service"

**Detailed Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions.

**Features:**
- ✅ Free tier available (750 hours/month)
- ✅ Automatic SSL certificates
- ✅ Auto-deploy on Git push
- ✅ Environment variable management
- ✅ Health checks and monitoring

**Note**: Free tier services spin down after 15 minutes of inactivity. Upgrade to paid plan for always-on service.

## 📖 Usage Guide

### Using the Gradio Web UI

1. **Start the Application**
   ```bash
   uv run python run_gradio.py
   ```

2. **Open in Browser**
   - Navigate to the URL shown in the terminal (e.g., `http://127.0.0.1:7860`)

3. **Upload a Contract**
   - Click the upload area or drag-and-drop a PDF file
   - Supported format: PDF files only
   - Maximum recommended size: 10MB (larger files may take longer)

4. **Analyze**
   - Click the "🔍 Analyze Contract" button
   - Watch the progress indicator for real-time updates
   - Results will appear in three tabs:
     - **Extracted Clauses**: Key contract provisions
     - **Risk Analysis**: Risk levels with color-coded indicators
     - **Revision Suggestions**: Prioritized improvement recommendations

5. **Review Results**
   - Navigate between tabs to see different aspects of the analysis
   - High-risk items are highlighted in red
   - Medium-risk items in yellow/orange
   - Low-risk items in green

### Using the API

#### Example: Python Request

```python
import requests

# Upload and analyze a contract
with open('contract.pdf', 'rb') as f:
    files = {'file': ('contract.pdf', f, 'application/pdf')}
    response = requests.post('http://127.0.0.1:8000/review', files=files)
    
result = response.json()
print(result)
```

#### Example: cURL Request

```bash
curl -X POST "http://127.0.0.1:8000/review" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@contract.pdf"
```

#### Response Format

```json
{
  "clauses": {
    "termination": "Either party may terminate with 30 days notice...",
    "confidentiality": "All proprietary information must be kept confidential...",
    "payment_terms": "Payment of $10,000 due within 30 days...",
    "liability": "Liability is limited to the contract value...",
    "governing_law": "This contract is governed by the laws of California..."
  },
  "risks": {
    "termination": "High Risk: No termination rights for 5 years...",
    "payment_terms": "Medium Risk: Standard terms but late fees are high...",
    "liability": "Low Risk: Reasonable liability cap at contract value"
  },
  "suggestions": "EXECUTIVE SUMMARY: The contract contains several high-risk provisions...\n\nHIGH PRIORITY REVISIONS:\n• Termination Clause: Add termination rights..."
}
```

## 📚 API Documentation

### POST /review

Analyze a contract PDF file.

**Request:**
- Method: `POST`
- Endpoint: `/review`
- Content-Type: `multipart/form-data`
- Body: `file` (PDF file)

**Response:**
- Status: `200 OK`
- Content-Type: `application/json`
- Body: `ReviewResponse` object

**ReviewResponse Model:**
```python
{
  "clauses": dict,      # Extracted clauses
  "risks": dict,        # Risk classifications
  "suggestions": str    # Revision suggestions
}
```

**Error Responses:**
- `400 Bad Request`: Invalid file or empty PDF
- `500 Internal Server Error`: Processing error

### GET /health

Check application health.

**Response:**
```json
{
  "status": "running"
}
```

## 🏗️ Architecture

### System Components

1. **PDF Loader** (`app/services/pdf_loader.py`)
   - Loads and extracts text from PDF files
   - Handles encrypted PDFs (requires cryptography)
   - Error handling for corrupted or empty files

2. **Clause Extractor** (`app/services/clause_extractor.py`)
   - Uses LLM to extract 5 key clause types
   - Returns structured JSON with clause summaries
   - Handles missing clauses gracefully

3. **Risk Classifier** (`app/services/risk_classifier.py`)
   - Analyzes extracted clauses for risk levels
   - Classifies as High/Medium/Low risk
   - Provides explanations for each classification

4. **Revision Agent** (`app/services/revision_agent.py`)
   - Generates actionable revision suggestions
   - Prioritizes recommendations by risk level
   - Provides specific, implementable changes

5. **Orchestrator** (`app/orchestrator.py`)
   - Coordinates the analysis pipeline
   - Implements parallel processing for independent tasks
   - Manages progress tracking

6. **Gradio UI** (`app/gradio_ui.py`)
   - Web-based user interface
   - File upload and progress display
   - Results visualization

7. **FastAPI Backend** (`app/main.py`)
   - RESTful API endpoints
   - File handling and validation
   - Error handling and cleanup

### Processing Flow

```
PDF Upload
    ↓
PDF Loader (extract text)
    ↓
Clause Extractor (LLM call #1)
    ↓
    ├─→ Risk Classifier (LLM call #2) ─┐
    │                                    ├─→ Results Aggregation
    └─→ Revision Agent (LLM call #3) ───┘
    ↓
Response to User
```

**Parallel Processing:**
- Risk classification and revision suggestions run in parallel
- Reduces total processing time by ~33-50%

## ⚡ Performance Optimizations

### Current Optimizations

1. **Parallel Processing**
   - Risk classification and revision suggestions execute concurrently
   - Uses `ThreadPoolExecutor` for task management

2. **Content Truncation**
   - PDFs longer than 8,000 characters are truncated
   - Keeps most important content while reducing processing time
   - Configurable in `app/gradio_ui.py` (line 32)

3. **Optimized Prompts**
   - Concise, direct prompts reduce token usage
   - Clear instructions improve response quality
   - Structured output formats reduce parsing overhead

4. **Progress Tracking**
   - Real-time updates keep users informed
   - Prevents perceived delays

### Performance Metrics

**With Groq (cloud-based LLM):**
- **Small PDFs (< 50KB)**: ~10-20 seconds ⚡
- **Medium PDFs (50-200KB)**: ~20-40 seconds ⚡
- **Large PDFs (> 200KB)**: ~30-60 seconds (with truncation) ⚡

**Performance Benefits:**
- 🆓 **Free tier** - 14,400 requests per day at no cost
- ⚡ **Very fast inference** - Groq's LPU (Language Processing Unit) technology
- 🌐 **Cloud-based** - No local installation or GPU required
- 🎯 **High quality** - State-of-the-art models like Llama 3.3
- 🔧 **Easy deployment** - No infrastructure management needed

### Further Optimization Tips

1. **Choose the Right Model**:
   - `llama-3.3-70b-versatile` - Best quality (recommended for production)
   - `llama-3.1-8b-instant` - Fastest, good for development (default)
   - `llama-3.2-90b-text-preview` - Very high quality
   - `mixtral-8x7b-32768` - Good balance
   - `gemma-7b-it` - Fast and efficient
2. **Adjust Truncation**: Increase limit in `gradio_ui.py` line 32 if needed (default: 8000 chars)
3. **Enable Caching**: Implement result caching for identical PDFs (future enhancement)
4. **Batch Processing**: Process multiple contracts in parallel (future enhancement)
5. **Monitor Usage**: Track API usage in Groq Console to stay within free tier limits

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Error:** `OSError: Cannot find empty port in range: 7860-7860`

**Solution:**
- The application automatically finds an available port
- If issues persist, kill the process using port 7860:
  ```bash
  # Windows
  netstat -ano | findstr :7860
  taskkill /PID <PID> /F
  
  # Linux/Mac
  lsof -ti:7860 | xargs kill -9
  ```

#### 2. Groq API Key Error

**Error:** `GROQ_API_KEY not found` or `Invalid API key`

**Solution:**
- Ensure you have set `GROQ_API_KEY` in your `.env` file
- Get your API key from: https://console.groq.com/
- Verify the key is correct (no extra spaces or quotes)
- Check API key usage limits in Groq Console
- Ensure you have internet connection for API calls

#### 3. PDF Loading Error

**Error:** `cryptography>=3.1 is required for AES algorithm`

**Solution:**
- Dependencies should auto-install, but if not:
  ```bash
  uv sync
  ```

**Error:** `PDF is password-protected`

**Solution:**
- Current version doesn't support password-protected PDFs
- Remove password protection or use an unencrypted PDF

#### 4. Slow Processing

**Issue:** Analysis takes too long

**Solutions:**
- Use a faster model: `GROQ_MODEL=llama-3.1-8b-instant` (fastest option)
- Reduce PDF size or content (truncation limit in `gradio_ui.py`)
- Ensure parallel processing is working (check logs)
- Check your internet connection speed
- Consider using `gemma-7b-it` for even faster responses

#### 5. Import Errors

**Error:** `ModuleNotFoundError: No module named 'gradio'`

**Solution:**
- Ensure you're using `uv run` prefix:
  ```bash
  uv run python -m app.gradio_ui
  ```
- Or activate virtual environment:
  ```bash
  source .venv/bin/activate  # Linux/Mac
  .venv\Scripts\activate     # Windows
  ```

#### 6. JSON Parsing Errors

**Error:** `Failed to parse JSON response`

**Solution:**
- This is handled gracefully with fallback responses
- Try a different model (some models are better at JSON formatting)
- Recommended: Use `llama-3.3-70b-versatile` for better JSON output
- Check logs for raw LLM responses to debug
- Ensure the model supports structured output (all Groq models do)

### Getting Help

1. Check the logs for detailed error messages
2. Verify all prerequisites are installed
3. Ensure `GEMINI_API_KEY` is set correctly in `.env`
4. Verify internet connection for API calls
5. Check API quota/limits in Google AI Studio
6. Review the configuration in `.env`
7. Check GitHub issues (if applicable)

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Submit a pull request

### Development Setup

```bash
# Install development dependencies
uv sync --dev

# Run linters
uv run black app/
uv run ruff check app/

# Run tests (if available)
uv run pytest
```

## 📝 License

[Add your license information here]

## 🙏 Acknowledgments

- **LangChain**: LLM integration framework
- **Google Gemini API**: Cloud-based AI model (free tier available)
- **Gradio**: Web UI framework
- **FastAPI**: Modern Python web framework
- **PyPDF**: PDF processing library

## 📧 Contact

[Add your contact information or project maintainer details]

---

**Note:** This application is for informational purposes only and should not replace professional legal advice. Always consult with qualified legal professionals for important contract decisions.

