# CV-JD Match API

An intelligent REST API that compares CVs (Curricula Vitae) against job descriptions using Google's Gemini AI model. This tool provides detailed matching analysis to help both job seekers and recruiters assess alignment between candidate qualifications and job requirements.

## Features

- **Intelligent Matching**: Uses Google Gemini 3.1 Flash Lite for advanced AI-powered CV-JD comparison
- **Comprehensive Analysis**: Returns detailed matching metrics across multiple dimensions:
  - Overall compatibility score (0-100)
  - Skill match percentage
  - Experience match percentage
  - Education match percentage
  - List of missing critical skills
  - Identified candidate strengths
  - Personalized recommendation
- **RESTful API**: Simple HTTP endpoint for easy integration
- **Data Validation**: Pydantic models ensure data integrity and quality
- **JSON Response**: Structured JSON output for seamless integration with other tools

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- google-genai
- Google Gemini API key

## Installation

### 1. Clone or Navigate to Project Directory

```bash
cd RankCV_MVP
```

### 2. Install Dependencies

```bash
pip install fastapi uvicorn google-genai pydantic
```

### 3. Set Up API Key

Export your Google Gemini API key as an environment variable:

**Linux/macOS:**
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_gemini_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your_gemini_api_key_here
```

## Running the Server

Start the FastAPI development server:

```bash
uvicorn app:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

### Endpoint: `/evaluate`

**Method**: `POST`

**Description**: Evaluates the match between a CV and a job description.

### Request Schema

```json
{
  "cv_text": "string (minimum 50 characters)",
  "job_text": "string (minimum 50 characters)"
}
```

### Response Schema

```json
{
  "overall_score": 0,
  "skill_match": 0,
  "experience_match": 0,
  "education_match": 0,
  "missing_skills": ["string"],
  "strengths": ["string"],
  "recommendation": "string"
}
```

### Example Request

```bash
curl -X POST "http://localhost:8000/evaluate" \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

Or using Python:

```python
import requests

url = "http://localhost:8000/evaluate"
data = {
    "cv_text": "Your CV text here...",
    "job_text": "Job description here..."
}

response = requests.post(url, json=data)
print(response.json())
```

### Example Response

```json
{
  "overall_score": 75,
  "skill_match": 80,
  "experience_match": 70,
  "education_match": 75,
  "missing_skills": ["Apache Airflow", "dbt", "Spark Advanced Optimization"],
  "strengths": ["Strong Python foundation", "SQL expertise", "ETL pipeline experience", "Cloud basics with AWS"],
  "recommendation": "Strong candidate with solid data engineering fundamentals. Would benefit from hands-on experience with Airflow and dbt before starting."
}
```

## Usage Examples

### 1. Basic Usage with cURL

```bash
curl -X POST "http://localhost:8000/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "cv_text": "Your CV content...",
    "job_text": "Job description content..."
  }'
```

### 2. Using Python Requests

```python
import requests
import json

with open('test_request.json', 'r') as f:
    payload = json.load(f)

response = requests.post(
    'http://localhost:8000/evaluate',
    json=payload
)

result = response.json()
print(f"Overall Score: {result['overall_score']}/100")
print(f"Missing Skills: {', '.join(result['missing_skills'])}")
print(f"Recommendation: {result['recommendation']}")
```

### 3. Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive documentation where you can test the API directly.

## Architecture

The application uses:
- **FastAPI**: Modern Python web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Google Gemini API**: AI-powered content analysis and matching
- **JSON Schema**: Structured response format for consistency

## Error Handling

The API returns HTTP 500 errors with descriptive messages if:
- CV text is less than 50 characters
- Job text is less than 50 characters
- Gemini API request fails
- Invalid JSON format in request

## Notes

- Minimum text length for both CV and job description is 50 characters
- API responses are deterministic based on the Gemini model's output
- Consider rate limiting for production deployment
- Store API responses for analytics and improvement

## Future Enhancements

- Batch evaluation endpoint for multiple CV-JD pairs
- Confidence scores for each matching metric
- Support for file uploads (PDF, DOCX)
- Detailed feedback on specific gaps
- Custom matching criteria weights
- Caching for identical requests

## Support

For issues or questions, please refer to the project documentation or contact the development team.

## License

This project is part of the RankCV MVP initiative.