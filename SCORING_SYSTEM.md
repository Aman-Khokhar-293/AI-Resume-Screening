# ResumeMatch AI - Scoring System

## How Match Scores Are Calculated

The match score is a **percentage (0-100%)** that represents how well a candidate matches a job posting.

### Scoring Formula

**Final Score = (Skills Match × 70%) + (Text Similarity × 30%)**

### Components

#### 1. Skills Match Score (70% weight)
- **Formula**: `(Matching Skills / Required Skills) × 100%`
- **Example**: 
  - Job requires: Python, SQL, AWS (3 skills)
  - Candidate has: Python, SQL (2 skills)
  - Skills Match = 2/3 = 66.7%

#### 2. Text Similarity Score (30% weight)
- Uses **TF-IDF** and **Cosine Similarity** between full resume text and job description
- Captures overall content alignment beyond just skill keywords
- Considers experience descriptions, project details, and qualifications

### Example Calculations

#### Example 1: Perfect Skills Match
- **Skills**: 2/2 matching = 100%
- **Text similarity**: 0.20 = 20%
- **Final Score**: (1.0 × 0.7) + (0.2 × 0.3) = 0.7 + 0.06 = **76%**

#### Example 2: Partial Skills Match
- **Skills**: 3/5 matching = 60%
- **Text similarity**: 0.50 = 50%
- **Final Score**: (0.6 × 0.7) + (0.5 × 0.3) = 0.42 + 0.15 = **57%**

#### Example 3: No Skills Match
- **Skills**: 0/4 matching = 0%
- **Text similarity**: 0.80 = 80%
- **Final Score**: (0.0 × 0.7) + (0.8 × 0.3) = 0 + 0.24 = **24%**

### Why This Approach?

✅ **Skills are prioritized** (70% weight) - If a candidate has the required technical skills, they get a good score

✅ **Context matters** (30% weight) - Text similarity ensures overall experience and qualifications align

✅ **Balanced scoring** - Prevents low scores when skills match but wording differs

❌ **Old approach problem** - Using only text similarity could give 2% score even with 100% skills match!

### Score Interpretation

| Score Range | Recommendation | Meaning |
|------------|----------------|---------|
| 80-100% | ⭐ Excellent Match | Highly recommended for interview |
| 60-79% | ✅ Good Match | Consider for interview |
| 40-59% | ⚠️ Moderate Match | May need additional training |
| 0-39% | ❌ Low Match | Not recommended |

### Skills Breakdown

The system also provides detailed skills analysis:

- **✓ Matching Skills** (Green) - Skills the candidate has that match job requirements
- **⚠ Missing Skills** (Orange) - Required skills the candidate lacks
- **💡 Additional Skills** (Blue) - Extra skills the candidate has beyond requirements

This gives recruiters a complete picture to make informed hiring decisions!
