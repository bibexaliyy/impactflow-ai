"""
Report generation service.

The one place in the codebase that talks to an AI provider. Views
should never call a provider SDK directly — always go through
`generate_report_for_project` so retry/error handling and provider
switching stay centralized.
"""

import json
import time

import anthropic
from django.conf import settings

from reports.models import Report

from .prompts.report_prompt import SYSTEM_PROMPT, build_user_prompt

MAX_RETRIES = 2

# Base URLs for providers that speak the OpenAI-compatible API
OPENAI_COMPATIBLE_BASE_URLS = {
    "groq": "https://api.groq.com/openai/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/",
}


class ReportGenerationError(Exception):
    """Raised when the AI call fails or returns output we can't use."""


def _parse_json_response(raw_text: str) -> dict:
    raw_text = raw_text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()
    return json.loads(raw_text)


def _call_claude(project) -> dict:
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=settings.ANTHROPIC_MODEL,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(project)}],
    )
    raw_text = "".join(
        block.text for block in response.content if block.type == "text"
    )
    return _parse_json_response(raw_text)


def _call_openai_compatible(project) -> dict:
    # Groq and Gemini both speak the OpenAI-compatible API — one code path
    from openai import OpenAI

    base_url = OPENAI_COMPATIBLE_BASE_URLS.get(settings.AI_PROVIDER)
    if not base_url:
        raise ReportGenerationError(f"Unknown AI_PROVIDER: {settings.AI_PROVIDER}")

    client = OpenAI(api_key=settings.AI_API_KEY, base_url=base_url,timeout=30.0)
    response = client.chat.completions.create(
        model=settings.AI_MODEL,
        max_tokens=2000,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(project)},
        ],
    )
    raw_text = response.choices[0].message.content
    return _parse_json_response(raw_text)


def _call_mock(project) -> dict:
    required_fields = [field for field, _ in Report.SECTION_ORDER]
    return {
        field: f"[Mock content for '{field}' — set MOCK_AI_RESPONSES=False for real output]"
        for field in required_fields
    }


def _call_ai(project) -> dict:
    if settings.MOCK_AI_RESPONSES:
        return _call_mock(project)

    last_error = None
    for attempt in range(1, MAX_RETRIES + 2):
        try:
            if settings.AI_PROVIDER == "anthropic":
                return _call_claude(project)
            else:
                return _call_openai_compatible(project)
        except (json.JSONDecodeError, anthropic.APIError, Exception) as exc:
            last_error = exc
            if attempt <= MAX_RETRIES:
                time.sleep(1.5 * attempt)
                continue
            break

    raise ReportGenerationError(
        f"Report generation failed after {MAX_RETRIES + 1} attempts: {last_error}"
    )


def generate_report_for_project(project) -> Report:
    """
    Calls the AI, validates the response has the sections we need, and
    saves a new Report row. Raises ReportGenerationError on failure —
    callers decide how to surface that (never fail silently on a
    donor-facing document).
    """
    start = time.monotonic()
    sections = _call_ai(project)

    required_fields = [field for field, _ in Report.SECTION_ORDER]
    missing = [f for f in required_fields if f not in sections]
    if missing:
        raise ReportGenerationError(f"AI response missing sections: {missing}")

    elapsed = time.monotonic() - start

    report = Report.objects.create(
        project=project,
        generation_seconds=round(elapsed, 2),
        **{field: sections[field] for field in required_fields},
    )
    return report

