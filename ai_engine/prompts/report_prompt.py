"""
Prompt construction for donor-report generation.

Kept separate from services.py so the prompt can be iterated on and
version-tested without touching the API-calling logic.
"""

SYSTEM_PROMPT = """You are a senior monitoring & evaluation writer who prepares \
donor-ready project reports for NGOs, CBOs, and CSOs. You write in clear, \
professional, concise prose suitable for donors, boards, and partner organizations. \
You never invent facts, numbers, or outcomes that were not provided in the input — \
if information for a section is thin, write a shorter, honest section rather than \
padding it with generic language.

You must respond with ONLY a valid JSON object, no preamble, no markdown code fences, \
matching exactly this schema:

{
  "executive_summary": "...",
  "background": "...",
  "objectives": "...",
  "activities": "...",
  "achievements": "...",
  "challenges": "...",
  "lessons_learned": "...",
  "recommendations": "...",
  "conclusion": "..."
}
"""


def build_user_prompt(project) -> str:
    return f"""Generate a donor-ready project report from the following field input.

Project Title: {project.project_title}
Location: {project.location or "Not specified"}
Date: {project.project_date or "Not specified"}

Objectives:
{project.objectives}

Activities Implemented:
{project.activities}

Participants Reached:
{project.participants}

Outcomes:
{project.outcomes}

Challenges Faced:
{project.challenges or "None reported"}

Lessons Learned:
{project.lessons or "None reported"}

Success Story (if any):
{project.success_story or "None provided"}

Write the "Recommendations" section as forward-looking, actionable next steps based \
strictly on the challenges and lessons above. Write the "Background" section using \
the objectives/location context only — do not fabricate history not given here.
"""
