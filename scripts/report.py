"""Builds the email digest body. Pure functions only -- no network/IO --
so this is fully unit-testable against synthetic fixtures.

Every optional field is rendered as "not specified" here, and nowhere
else, so a missing value is never accidentally invented upstream.
"""

from __future__ import annotations

from datetime import date, datetime
from html import escape

from scripts.config import NOT_SPECIFIED
from scripts.grouping import Grouped
from scripts.models import JobListing, SourceResult

NOT_SPECIFIED_DEADLINE = "not specified"
NOT_SPECIFIED_LOCATION = "not specified"


def _fmt_deadline(job: JobListing) -> str:
    if job.deadline:
        return job.deadline.isoformat()
    if job.deadline_raw:
        return f"{job.deadline_raw} (unparsed)"
    return NOT_SPECIFIED_DEADLINE


def _fmt_location(job: JobListing) -> str:
    return job.location_raw or NOT_SPECIFIED_LOCATION


def _fmt_contract(job: JobListing) -> str:
    tag = "stated" if job.contract_type_stated else "inferred"
    if job.contract_type_label == NOT_SPECIFIED:
        return NOT_SPECIFIED
    return f"{job.contract_type_label} ({tag})"


def _section_job_count(grouped: Grouped) -> int:
    return sum(
        len(jobs)
        for orgs in grouped.values()
        for contracts in orgs.values()
        for jobs in contracts.values()
    )


def _render_section_text(title: str, grouped: Grouped) -> list[str]:
    lines = [title, "=" * len(title)]
    if not grouped:
        lines.append("No matching jobs found this week.")
        lines.append("")
        return lines
    for region, orgs in grouped.items():
        lines.append(f"\n-- {region} --")
        for org, contracts in orgs.items():
            lines.append(f"  {org}")
            for contract_label, jobs in contracts.items():
                lines.append(f"    [{contract_label}]")
                for job in jobs:
                    lines.append(
                        f"      - {job.title} | {_fmt_location(job)} | "
                        f"deadline: {_fmt_deadline(job)} | "
                        f"contract: {_fmt_contract(job)} | {job.url}"
                    )
    lines.append("")
    return lines


def _render_section_html(title: str, grouped: Grouped) -> str:
    parts = [f"<h2>{escape(title)}</h2>"]
    if not grouped:
        parts.append("<p>No matching jobs found this week.</p>")
        return "\n".join(parts)
    for region, orgs in grouped.items():
        parts.append(f"<h3>{escape(region)}</h3>")
        for org, contracts in orgs.items():
            parts.append(f"<h4>{escape(org)}</h4>")
            for contract_label, jobs in contracts.items():
                parts.append(f"<p><strong>{escape(contract_label)}</strong></p>")
                parts.append("<ul>")
                for job in jobs:
                    parts.append(
                        "<li>"
                        f'<a href="{escape(job.url)}">{escape(job.title)}</a>'
                        f" &mdash; {escape(_fmt_location(job))}"
                        f" &mdash; deadline: {escape(_fmt_deadline(job))}"
                        f" &mdash; contract: {escape(_fmt_contract(job))}"
                        "</li>"
                    )
                parts.append("</ul>")
    return "\n".join(parts)


def build_email(
    psych_grouped: Grouped,
    main_grouped: Grouped,
    source_results: list[SourceResult],
    run_date: date | None = None,
) -> tuple[str, str, str]:
    run_date = run_date or datetime.utcnow().date()
    subject = f"Weekly Job Digest - {run_date.isoformat()}"

    failed = [r for r in source_results if r.error]
    succeeded = [r for r in source_results if not r.error]

    total_jobs = _section_job_count(psych_grouped) + _section_job_count(main_grouped)

    # --- text body ---
    text_lines = [f"Weekly Job Digest - {run_date.isoformat()}", ""]
    text_lines.append(f"{total_jobs} matching job(s) found across {len(succeeded)} source(s).")
    if failed:
        text_lines.append("")
        text_lines.append("Sources NOT retrieved this week:")
        for r in failed:
            text_lines.append(f"  - {r.source_name}: {r.error}")
    text_lines.append("")
    text_lines.extend(
        _render_section_text("Psychology & MHPSS (any location)", psych_grouped)
    )
    text_lines.extend(
        _render_section_text(
            "Other roles: Public Health, Information Management, "
            "Monitoring & Evaluation, Business Process, Project Management "
            "(Switzerland / EU / UK)",
            main_grouped,
        )
    )
    text_body = "\n".join(text_lines)

    # --- html body ---
    html_parts = [
        f"<h1>Weekly Job Digest - {escape(run_date.isoformat())}</h1>",
        f"<p>{total_jobs} matching job(s) found across {len(succeeded)} source(s).</p>",
    ]
    if failed:
        html_parts.append("<h3>Sources NOT retrieved this week</h3>")
        html_parts.append("<ul>")
        for r in failed:
            html_parts.append(f"<li>{escape(r.source_name)}: {escape(r.error)}</li>")
        html_parts.append("</ul>")
    html_parts.append(
        _render_section_html("Psychology &amp; MHPSS (any location)", psych_grouped)
    )
    html_parts.append(
        _render_section_html(
            "Other roles: Public Health, Information Management, "
            "Monitoring &amp; Evaluation, Business Process, Project "
            "Management (Switzerland / EU / UK)",
            main_grouped,
        )
    )
    html_body = "\n".join(html_parts)

    return subject, html_body, text_body
