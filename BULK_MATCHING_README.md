# Bulk Resume Matching & Ranking System

## 🚀 What's New

Transform your recruitment process with **bulk resume screening**! Upload up to 100 resumes at once and get an instant ranking board showing the best candidates for your job posting.

## ✨ Key Features

### 1. **Bulk Upload**
- Upload up to **100 resumes** simultaneously (PDF or TXT)
- No need to manually enter name or email
- Automatic extraction of candidate info from resumes

### 2. **Auto-Extract Contact Info**
- **Name extraction** - Intelligently finds candidate names from resume text
- **Email extraction** - Automatically detects email addresses
- **Phone extraction** - Finds phone numbers as fallback contact
- **Filename fallback** - Uses filename if name not found in resume

### 3. **Ranking Leaderboard**
- Candidates automatically sorted by match score (highest first)
- **🥇🥈🥉 Medal system** for top 3 candidates
- Color-coded scores:
  - 🟢 Green (80-100%): Excellent match
  - 🔵 Blue (60-79%): Good match
  - 🟠 Orange (40-59%): Moderate match
  - 🔴 Red (0-39%): Low match

### 4. **Stats Dashboard**
- Total candidates processed
- Average match score across all candidates
- Top score achieved

### 5. **Detailed Candidate View**
- Click "View" button on any candidate
- See full skills breakdown:
  - ✓ Matching skills
  - ⚠ Missing skills
  - 💡 All candidate skills
- Complete contact information
- Match percentage

## 📋 How to Use

### Step 1: Enter Job Details
```
Title: Senior Software Engineer
Description: We're looking for an experienced full-stack developer...
Skills: Python, React, AWS, Docker (comma-separated)
```

### Step 2: Upload Resumes
- Click "Choose files" or drag files
- Select multiple PDF or TXT resumes (up to 100)
- See file count update in real-time

### Step 3: Rank Candidates
- Click "🚀 Rank All Candidates"
- Wait for processing (usually a few seconds)
- View ranking board with all candidates sorted by score

### Step 4: Review Results
- Top candidates appear first with medals 🥇🥈🥉
- See match scores and skills match ratios
- Click "View" for detailed candidate analysis

## 🎯 Ranking Algorithm

Same accurate scoring as before:
- **70% Skills Match**: (Matching Skills / Required Skills)
- **30% Text Similarity**: TF-IDF cosine similarity

Example:
- Candidate has 4/5 required skills (80%)
- Text similarity: 0.40 (40%)
- **Final Score**: (0.80 × 0.7) + (0.40 × 0.3) = **68%** ✅

## 📊 Output Format

### Ranking Table Columns:
| Rank | Candidate Name | Contact | Match Score | Skills Match | Action |
|------|---------------|---------|-------------|--------------|--------|
| 🥇 | Jane Smith | jane@email.com | 85% | 5/5 | View |
| 🥈 | John Doe | john@email.com | 72% | 4/5 | View |
| #3 | Bob Wilson | bob@email.com | 58% | 3/5 | View |

### Stats Summary:
- **Total Candidates**: 50
- **Average Score**: 63%
- **Top Score**: 85%

## 🔧 Technical Details

### Name/Email Extraction Logic

**Name Extraction:**
1. Scans first 5 lines of resume
2. Skips common keywords (Resume, CV, Objective, etc.)
3. Looks for 1-4 word lines with >80% alphabetic characters
4. Falls back to filename if not found (e.g., "John_Doe_Resume.pdf" → "John Doe")

**Email Extraction:**
- Regex pattern: `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}`
- Scans first 15 lines

**Phone Extraction:**
- Pattern: `(555) 123-4567` or `555-123-4567` or `+1-555-123-4567`
- Used as fallback if email not found

### API Endpoint

**POST `/api/bulk-match`**

Form Data:
- `title` (required): Job title
- `description` (required): Job description
- `required_skills`: Comma-separated skills
- `resume_files`: Multiple files (PDF/TXT, max 100)

Response:
```json
{
  "job_id": 1,
  "job_title": "Senior Software Engineer",
  "total_candidates": 50,
  "candidates": [
    {
      "candidate_id": 123,
      "name": "Jane Smith",
      "contact": "jane@email.com",
      "score": 0.85,
      "overlap_skills": ["Python", "React", "AWS"],
      "missing_skills": ["Docker"],
      "all_skills": ["Python", "React", "AWS", "SQL", "Git"],
      "filename": "Jane_Smith_Resume.pdf"
    },
    ...
  ]
}
```

## 🎨 UI Components

- **File Upload Zone**: Drag-and-drop or click to select
- **Progress Bar**: Shows processing status
- **Ranking Table**: Sortable candidate list
- **Detail Modal**: Popup with full candidate info
- **Stats Cards**: Quick overview metrics

## 🚀 Getting Started

```bash
# Ensure pypdf is installed for PDF support
pip install pypdf

# Run the server
python app.py

# Open browser
# http://127.0.0.1:5000/

# Upload multiple resumes and get instant rankings!
```

## 💡 Tips

1. **File Naming**: Name files like "FirstName_LastName_Resume.pdf" for better name extraction
2. **Resume Format**: Include email at the top of resume for best extraction
3. **Batch Size**: For best performance, upload 20-50 resumes at a time
4. **Skills**: Be specific with required skills for better matching

## 🎯 Use Cases

- **Mass Recruitment**: Screen hundreds of applications quickly
- **Career Fairs**: Upload all collected resumes at once
- **LinkedIn Export**: Bulk screen downloaded profiles
- **Referral Programs**: Quickly evaluate multiple referrals
- **Internal Mobility**: Match existing employees to new roles

---

**Built with Flask, Machine Learning & AI** 🤖
