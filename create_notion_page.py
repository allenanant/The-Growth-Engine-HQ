#!/usr/bin/env python3
"""
SideXSide Client Brief → Notion Page Creator

Creates a fully formatted Notion page with all the content from the
SideXSide Client Brief, including tables, checklists, headings, and callouts.

Usage:
    python3 create_notion_page.py

Requirements:
    pip install requests

You'll need:
    1. A Notion Integration Token (from https://www.notion.so/profile/integrations)
    2. A parent page in Notion that's been shared with your integration
"""

import json
import os
import sys
import requests

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
if not NOTION_TOKEN:
    NOTION_TOKEN = input("Enter your Notion Integration Token: ").strip()
    if not NOTION_TOKEN:
        print("❌ No token provided. Set NOTION_TOKEN env var or enter it when prompted.")
        sys.exit(1)
NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}


# ─────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────
def rich_text(content, bold=False, italic=False, code=False, color="default"):
    """Create a Notion rich_text object."""
    return {
        "type": "text",
        "text": {"content": content},
        "annotations": {
            "bold": bold,
            "italic": italic,
            "code": code,
            "color": color,
        },
    }


def heading_1(text):
    return {
        "object": "block",
        "type": "heading_1",
        "heading_1": {"rich_text": [rich_text(text)]},
    }


def heading_2(text):
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [rich_text(text)]},
    }


def heading_3(text):
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {"rich_text": [rich_text(text)]},
    }


def paragraph(*parts):
    """Create a paragraph. Each part is a rich_text object or a string."""
    rt = []
    for p in parts:
        if isinstance(p, str):
            rt.append(rich_text(p))
        else:
            rt.append(p)
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": rt},
    }


def bold_paragraph(label, rest=""):
    """A paragraph that starts with bold text."""
    parts = [rich_text(label, bold=True)]
    if rest:
        parts.append(rich_text(rest))
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": parts},
    }


def bullet(*parts):
    """Bulleted list item."""
    rt = []
    for p in parts:
        if isinstance(p, str):
            rt.append(rich_text(p))
        else:
            rt.append(p)
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rt},
    }


def numbered(*parts):
    """Numbered list item."""
    rt = []
    for p in parts:
        if isinstance(p, str):
            rt.append(rich_text(p))
        else:
            rt.append(p)
    return {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {"rich_text": rt},
    }


def todo(text, checked=False):
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [rich_text(text)],
            "checked": checked,
        },
    }


def divider():
    return {"object": "block", "type": "divider", "divider": {}}


def callout(text, emoji="💡"):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [rich_text(text)],
            "icon": {"type": "emoji", "emoji": emoji},
        },
    }


def quote_block(text):
    return {
        "object": "block",
        "type": "quote",
        "quote": {"rich_text": [rich_text(text)]},
    }


def table(headers, rows):
    """
    Create a table block.
    headers: list of strings for the header row
    rows: list of lists of strings for data rows
    """
    width = len(headers)

    def make_row(cells):
        return {
            "type": "table_row",
            "table_row": {
                "cells": [[rich_text(c)] for c in cells]
            },
        }

    header_row = make_row(headers)
    data_rows = [make_row(r) for r in rows]

    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": width,
            "has_column_header": True,
            "has_row_header": False,
            "children": [header_row] + data_rows,
        },
    }


def toggle(title_text, children_blocks):
    """Create a toggle block with children."""
    return {
        "object": "block",
        "type": "toggle",
        "toggle": {
            "rich_text": [rich_text(title_text, bold=True)],
            "children": children_blocks,
        },
    }


# ─────────────────────────────────────────────
# Build All Content Blocks
# ─────────────────────────────────────────────
def build_all_blocks():
    blocks = []

    # ── Header info ──
    blocks.append(callout(
        "If you're new to the team or picking up SideXSide work, read this page top to bottom. You'll have everything you need.",
        "📋"
    ))
    blocks.append(paragraph(
        rich_text("Created by: ", bold=True),
        rich_text("Allen Anant Thomas  |  "),
        rich_text("Last Updated: ", bold=True),
        rich_text("2026-03-03"),
    ))
    blocks.append(divider())

    # ── Section 1: What Is SideXSide? ──
    blocks.append(heading_1("What Is SideXSide?"))
    blocks.append(paragraph(
        "SideXSide is a ",
        rich_text("privacy-first campus safety companion app", bold=True),
        rich_text(" designed for U.S. colleges and universities. Think of it as a safety layer that sits alongside students throughout their campus life — without ever tracking them, collecting their data, or compromising their privacy."),
    ))
    blocks.append(callout("A campus safety app that protects students without spying on them.", "🎯"))
    blocks.append(bold_paragraph("Why it matters: ",
        "Every university in the U.S. is legally required to prioritize campus safety (Clery Act). Most current solutions rely on GPS tracking, invasive data collection, or clunky panic-button systems. SideXSide flips that — it delivers real safety features with zero tracking and zero data collection. That's the competitive edge."
    ))
    blocks.append(divider())

    # ── Section 2: The Product ──
    blocks.append(heading_1("The Product"))
    blocks.append(heading_2("Core Value Proposition"))
    blocks.append(bullet(rich_text("Privacy-first", bold=True), rich_text(" — Zero tracking. Zero data collection. Period.")))
    blocks.append(bullet(rich_text("Student-centric", bold=True), rich_text(" — Built for how students actually live on campus")))
    blocks.append(bullet(rich_text("University-friendly", bold=True), rich_text(" — White-label ready, easy to deploy, low friction for IT departments")))
    blocks.append(bullet(rich_text("Compliance-ready", bold=True), rich_text(" — Helps universities meet Clery Act and Title IX obligations")))

    blocks.append(heading_2("What Makes SideXSide Different"))
    blocks.append(table(
        ["Traditional Campus Safety Apps", "SideXSide"],
        [
            ["GPS tracking always on", "Zero location tracking"],
            ["Collects personal data", "Zero data collection"],
            ["Students feel surveilled", "Students feel empowered"],
            ["Privacy concerns = low adoption", "Privacy-first = high adoption"],
            ["One-size-fits-all", "White-label (university branding)"],
        ],
    ))
    blocks.append(divider())

    # ── Section 3: Business Model ──
    blocks.append(heading_1("Business Model — B2B White-Label SaaS"))
    blocks.append(callout("This is 100% a B2B play. We are NOT selling to students. We sell to universities, and universities deploy it to their students under their own brand.", "🏢"))

    blocks.append(heading_2("How It Works"))
    blocks.append(numbered("We license SideXSide to universities as a white-label SaaS product"))
    blocks.append(numbered("The university brands it as their own campus safety app (their logo, their colors, their name)"))
    blocks.append(numbered("Students download what looks like their university's own safety app"))
    blocks.append(numbered("University pays us a licensing fee (recurring monthly/annual)"))

    blocks.append(heading_2("Why White-Label?"))
    blocks.append(bullet("Universities want to show students they built something — not that they bought something"))
    blocks.append(bullet("White-labeling removes the \"third-party app\" objection"))
    blocks.append(bullet("Increases adoption because it feels native to the campus ecosystem"))
    blocks.append(bullet("Creates stickiness — once it's branded and deployed, switching costs are high"))

    blocks.append(heading_2("Revenue Model"))
    blocks.append(bullet("B2B SaaS licensing (recurring revenue per university)"))
    blocks.append(bullet("Target: 150-200 U.S. universities"))
    blocks.append(bullet("Focus: Mid-size schools with 10,000-30,000+ students"))
    blocks.append(divider())

    # ── Section 4: Target Market ──
    blocks.append(heading_1("Target Market"))
    blocks.append(heading_2("Ideal University Profile"))
    blocks.append(bullet(rich_text("Size: ", bold=True), rich_text("10,000 – 30,000+ enrolled students")))
    blocks.append(bullet(rich_text("Type: ", bold=True), rich_text("Public and private 4-year institutions")))
    blocks.append(bullet(rich_text("Location: ", bold=True), rich_text("United States (nationwide)")))
    blocks.append(bullet(rich_text("Pain Point: ", bold=True), rich_text("Need to demonstrate commitment to campus safety without invading student privacy")))
    blocks.append(bullet(rich_text("Budget: ", bold=True), rich_text("Has dedicated campus safety / student affairs budget")))

    blocks.append(heading_2("Why This Segment?"))
    blocks.append(bullet("Large enough to have real safety concerns and budget"))
    blocks.append(bullet("Small enough that they don't have the resources to build custom solutions in-house"))
    blocks.append(bullet("Most vulnerable to Title IX scrutiny and Clery Act compliance pressure"))
    blocks.append(bullet("Students at these schools are vocal about privacy — a tracking app would face backlash"))
    blocks.append(divider())

    # ── Section 5: Top 20 Priority Universities ──
    blocks.append(heading_1("Top 20 Priority Universities"))
    blocks.append(paragraph("These are our first-wave targets. Selected based on student population, safety needs, and market fit:"))
    blocks.append(table(
        ["#", "University", "Why It's a Priority"],
        [
            ["1", "NYU", "Large urban campus, high safety need"],
            ["2", "USC", "High-profile safety incidents in past"],
            ["3", "Ohio State", "60K+ students, massive campus"],
            ["4", "University of Michigan", "Big Ten, strong student culture"],
            ["5", "UT Austin", "50K+ students, urban campus"],
            ["6", "Penn State", "Huge enrollment, spread-out campus"],
            ["7", "University of Florida", "55K+ students"],
            ["8", "Arizona State", "Largest enrollment in U.S."],
            ["9", "University of Georgia", "40K+ students"],
            ["10", "Michigan State", "History of campus safety focus"],
            ["11", "Indiana University", "Big Ten, large campus"],
            ["12", "University of Minnesota", "Urban campus challenges"],
            ["13", "Purdue University", "Growing enrollment"],
            ["14", "University of Washington", "Urban setting, safety aware"],
            ["15", "University of Illinois", "Large student body"],
            ["16", "Rutgers University", "Multi-campus system"],
            ["17", "University of Maryland", "DC metro area challenges"],
            ["18", "Virginia Tech", "Post-incident safety focus"],
            ["19", "Texas A&M", "70K+ students"],
            ["20", "University of Oregon", "Progressive campus, privacy-conscious"],
        ],
    ))
    blocks.append(callout("Approach: Start conversations with 25-50 universities per day via cold email and LinkedIn. Scale to 100/day as templates get refined.", "📧"))
    blocks.append(divider())

    # ── Section 6: Sales Strategy ──
    blocks.append(heading_1("Sales Strategy — Who We're Selling To"))
    blocks.append(paragraph("We've identified ",
        rich_text("5 decision-maker personas", bold=True),
        rich_text(" within each university. You need to understand all of them because different schools have different buying structures."),
    ))

    blocks.append(heading_2("The 5 Decision-Maker Personas"))

    # Persona 1
    blocks.append(heading_3("1. VP of Student Affairs / Dean of Students"))
    blocks.append(bullet(rich_text("Role: ", bold=True), rich_text("Owns the student experience, campus life, and safety programs")))
    blocks.append(bullet(rich_text("Pain point: ", bold=True), rich_text("Needs to show the board they're proactive about safety")))
    blocks.append(bullet(rich_text("Pitch angle: ", bold=True), rich_text("\"Deploy a safety solution students actually want to use — because it respects their privacy\"")))

    # Persona 2
    blocks.append(heading_3("2. Chief Information Officer (CIO) / IT Director"))
    blocks.append(bullet(rich_text("Role: ", bold=True), rich_text("Evaluates and approves all campus technology")))
    blocks.append(bullet(rich_text("Pain point: ", bold=True), rich_text("Doesn't want another app that creates data liability")))
    blocks.append(bullet(rich_text("Pitch angle: ", bold=True), rich_text("\"Zero data collection means zero data breach risk for your IT department\"")))

    # Persona 3
    blocks.append(heading_3("3. Campus Police / Public Safety Director"))
    blocks.append(bullet(rich_text("Role: ", bold=True), rich_text("Manages on-the-ground safety operations")))
    blocks.append(bullet(rich_text("Pain point: ", bold=True), rich_text("Existing tools have low student adoption")))
    blocks.append(bullet(rich_text("Pitch angle: ", bold=True), rich_text("\"Students actually use this because they trust it — no tracking means no resistance\"")))

    # Persona 4
    blocks.append(heading_3("4. Title IX Coordinator"))
    blocks.append(bullet(rich_text("Role: ", bold=True), rich_text("Ensures compliance with federal safety and equity requirements")))
    blocks.append(bullet(rich_text("Pain point: ", bold=True), rich_text("Needs demonstrable safety infrastructure for audits")))
    blocks.append(bullet(rich_text("Pitch angle: ", bold=True), rich_text("\"SideXSide gives you documented safety infrastructure without the privacy controversy\"")))

    # Persona 5
    blocks.append(heading_3("5. University President / Provost"))
    blocks.append(bullet(rich_text("Role: ", bold=True), rich_text("Final budget approval and strategic direction")))
    blocks.append(bullet(rich_text("Pain point: ", bold=True), rich_text("Reputation and liability")))
    blocks.append(bullet(rich_text("Pitch angle: ", bold=True), rich_text("\"Be the university known for protecting students AND their privacy — that's a press story, not just a safety tool\"")))

    blocks.append(heading_2("Sales Cycle Expectation"))
    blocks.append(bullet("University procurement is slow — expect 3-6 month sales cycles"))
    blocks.append(bullet("Goal: Get pilot programs started (low-risk for the university, high-value for us)"))
    blocks.append(bullet("Once 2-3 pilots succeed, we use case studies to accelerate the next wave"))
    blocks.append(divider())

    # ── Section 7: Partnership Structure ──
    blocks.append(heading_1("Partnership Structure"))
    blocks.append(heading_2("The Growth Engine × SideXSide"))
    blocks.append(bullet(rich_text("The Growth Engine", bold=True), rich_text(" is our agency (Allen's company)")))
    blocks.append(bullet(rich_text("Amberley", bold=True), rich_text(" is the partner on the Growth Engine side")))
    blocks.append(bullet(rich_text("SOW (Statement of Work)", bold=True), rich_text(" has been signed between both parties")))
    blocks.append(bullet(rich_text("Monthly Fee: ", bold=True), rich_text("$1,900/month (covers marketing, website, content, outreach, strategy)")))

    blocks.append(heading_2("What The Growth Engine Delivers for SideXSide"))
    blocks.append(bullet("Full brand identity and design"))
    blocks.append(bullet("Website development and maintenance"))
    blocks.append(bullet("Content marketing (blog, social media)"))
    blocks.append(bullet("Cold email and LinkedIn outreach campaigns"))
    blocks.append(bullet("Sales strategy and funnel development"))
    blocks.append(bullet("Paid advertising (when ready)"))
    blocks.append(bullet("Ongoing strategic consulting"))
    blocks.append(divider())

    # ── Section 8: What's Been Done ──
    blocks.append(heading_1("What's Been Done (Completed)"))
    blocks.append(table(
        ["Deliverable", "Status", "Notes"],
        [
            ["Brand Identity", "✅ Done", "Logos, color palette, fonts — all finalized"],
            ["Marketing Strategy", "✅ Done", "Full go-to-market plan documented"],
            ["Sales Strategy", "✅ Done", "5 decision-maker personas identified"],
            ["15 Social Media Posts", "✅ Done", "Ready for deployment"],
            ["Legal Agreements", "✅ Done", "Growth Engine SOW signed"],
            ["Website Homepage", "✅ Done", "Live and completed"],
            ["7-Folder Project Structure", "✅ Done", "Contracts, Brand, Marketing, Website, Strategy, PM, Social"],
        ],
    ))
    blocks.append(divider())

    # ── Section 9: What's In Progress ──
    blocks.append(heading_1("What's In Progress"))
    blocks.append(table(
        ["Deliverable", "Status", "Priority", "Owner"],
        [
            ["Additional website pages", "⏳ In Progress", "🔴 Critical", "Allen / Dev Team"],
            ["Blog / Content section", "⏳ Starting", "🔴 Critical", "Allen"],
            ["Email campaign launch", "⏳ Pending Launch", "🔴 Critical", "Allen"],
            ["LinkedIn outreach setup", "⏳ Pending", "🟡 High", "Allen"],
            ["Banner & social media scripts", "⏳ Pending", "🟡 High", "Allen / Soumya"],
            ["Video content", "⏳ Pending", "🟡 High", "Abhijeet"],
            ["Pilot university partners", "⏳ Targeting 2-3", "🔴 Critical", "Allen"],
        ],
    ))
    blocks.append(divider())

    # ── Section 10: Current Deliverables & SOW ──
    blocks.append(heading_1("Current Deliverables & SOW"))
    blocks.append(heading_2("Monthly Scope ($1,900/month)"))
    blocks.append(bullet(rich_text("Website: ", bold=True), rich_text("Build and maintain sidexside website — homepage done, additional pages in progress")))
    blocks.append(bullet(rich_text("Content: ", bold=True), rich_text("Blog posts, social media content, email copy")))
    blocks.append(bullet(rich_text("Outreach: ", bold=True), rich_text("Cold email campaigns targeting university decision-makers (25-50/day → scale to 100/day)")))
    blocks.append(bullet(rich_text("Strategy: ", bold=True), rich_text("Ongoing B2B sales strategy, funnel optimization")))
    blocks.append(bullet(rich_text("Creative: ", bold=True), rich_text("Social media graphics, banner ads, video scripts")))
    blocks.append(bullet(rich_text("Advertising: ", bold=True), rich_text("Paid campaigns when funnel is validated (Meta, LinkedIn)")))
    blocks.append(divider())

    # ── Section 11: Website Status ──
    blocks.append(heading_1("Website Status"))
    blocks.append(table(
        ["Page", "Status", "Notes"],
        [
            ["Homepage", "✅ Completed", "Live"],
            ["About / How It Works", "⏳ In Progress", "Needs build"],
            ["For Universities (B2B landing)", "⏳ Planned", "Key conversion page"],
            ["Pricing / Plans", "⏳ Planned", "White-label licensing tiers"],
            ["Blog Section", "⏳ Starting", "Campus safety thought leadership"],
            ["Contact / Demo Request", "⏳ Planned", "Lead capture for demos"],
            ["Case Studies", "⏳ Future", "After pilot programs launch"],
        ],
    ))
    blocks.append(callout("Priority: The \"For Universities\" B2B landing page and blog section are the most important next builds. The landing page is where cold email traffic will land. The blog builds SEO and thought leadership for organic discovery.", "⚡"))
    blocks.append(divider())

    # ── Section 12: Outreach & Go-to-Market Plan ──
    blocks.append(heading_1("Outreach & Go-to-Market Plan"))

    blocks.append(heading_2("Phase 1 — Cold Outreach (Current Phase)"))
    blocks.append(numbered(rich_text("Email Campaigns: ", bold=True), rich_text("Target VP Student Affairs, CIOs, Campus Police Directors")))
    blocks.append(bullet("Volume: Start at 25-50 emails/day"))
    blocks.append(bullet("Scale: Ramp to 100/day as templates are proven"))
    blocks.append(bullet("Sequence: 3-4 email touches per prospect over 2 weeks"))
    blocks.append(numbered(rich_text("LinkedIn Outreach: ", bold=True), rich_text("Connect with decision-makers, share content, DM sequences")))
    blocks.append(numbered(rich_text("Goal: ", bold=True), rich_text("Book demo calls / intro meetings with university stakeholders")))

    blocks.append(heading_2("Phase 2 — Pilot Programs"))
    blocks.append(numbered("Secure 2-3 pilot universities willing to trial SideXSide"))
    blocks.append(numbered("Deploy white-label version on their campus"))
    blocks.append(numbered("Gather usage data, testimonials, and case studies"))
    blocks.append(numbered("Use pilot success stories to accelerate sales to next wave"))

    blocks.append(heading_2("Phase 3 — Scale"))
    blocks.append(numbered("Launch paid advertising (Meta, LinkedIn) targeting higher education professionals"))
    blocks.append(numbered("Attend higher education conferences (NASPA, EDUCAUSE, IACLEA)"))
    blocks.append(numbered("Build referral network through pilot university champions"))
    blocks.append(numbered("Content marketing flywheel: blog → SEO → inbound leads"))

    blocks.append(heading_2("Email Outreach Template Strategy"))
    blocks.append(bullet(rich_text("Email 1: ", bold=True), rich_text("Problem-aware (campus safety is broken, here's why)")))
    blocks.append(bullet(rich_text("Email 2: ", bold=True), rich_text("Solution-aware (privacy-first approach, no tracking)")))
    blocks.append(bullet(rich_text("Email 3: ", bold=True), rich_text("Social proof + demo offer (pilot program invitation)")))
    blocks.append(bullet(rich_text("Email 4: ", bold=True), rich_text("Breakup email (last touch, leave the door open)")))
    blocks.append(divider())

    # ── Section 13: Brand & Creative Assets ──
    blocks.append(heading_1("Brand & Creative Assets"))
    blocks.append(heading_2("Brand Identity"))
    blocks.append(bullet(rich_text("Logo: ", bold=True), rich_text("Finalized (multiple formats available)")))
    blocks.append(bullet(rich_text("Color Palette: ", bold=True), rich_text("Defined and documented")))
    blocks.append(bullet(rich_text("Typography: ", bold=True), rich_text("Brand fonts selected")))
    blocks.append(bullet(rich_text("Tone of Voice: ", bold=True), rich_text("Professional, trustworthy, student-friendly, privacy-forward")))

    blocks.append(heading_2("Content Assets Ready"))
    blocks.append(bullet("15 social media posts (approved and ready to publish)"))
    blocks.append(bullet("Brand guidelines document"))
    blocks.append(bullet("Marketing strategy document"))

    blocks.append(heading_2("Content Assets Needed"))
    blocks.append(bullet("Blog articles (campus safety, privacy, Clery Act, Title IX)"))
    blocks.append(bullet("Case study templates"))
    blocks.append(bullet("Email outreach sequences"))
    blocks.append(bullet("LinkedIn content for Allen's profile"))
    blocks.append(bullet("Video explainers for the product"))
    blocks.append(bullet("Banner ads for paid campaigns"))
    blocks.append(divider())

    # ── Section 14: Folder Structure ──
    blocks.append(heading_1("Folder Structure & Key Files"))
    blocks.append(heading_2("Project Organization (7-Folder Structure)"))
    blocks.append({
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [rich_text(
                "SideXSide Business - Organized/\n"
                "├── 01-Contracts-Legal/         # SOW, agreements, legal docs\n"
                "├── 02-Brand-Design/            # Logos, brand guidelines, color palette\n"
                "├── 03-Marketing-Campaigns/     # Cold email campaigns, ad copy, outreach\n"
                "├── 04-Website/                 # Website files, pages, blog content\n"
                "├── 05-Strategy/                # Go-to-market, sales strategy, personas\n"
                "├── 06-Project-Management/      # Timelines, task tracking, meeting notes\n"
                "└── 07-Social-Media/            # Posts, graphics, content calendar"
            )],
            "language": "plain text",
        },
    })

    blocks.append(heading_2("Key Reference Files"))
    blocks.append(table(
        ["File", "What It Contains"],
        [
            ["EXECUTIVE_SUMMARY.md", "10-minute investor-level brief of the entire business"],
            ["SIDEXSIDE_CLIENT_PROFILE.md", "Complete operational guide — the full deep dive"],
            ["QUICK_REFERENCE.md", "Sales team daily reference — key stats and talking points"],
            ["PROFILE_INDEX.md", "Navigation guide to find anything in the project"],
        ],
    ))
    blocks.append(divider())

    # ── Section 15: Team Responsibilities ──
    blocks.append(heading_1("Team Responsibilities"))
    blocks.append(table(
        ["Team Member", "Role on SideXSide", "What They Do"],
        [
            ["Allen", "Strategy Lead & Client Owner", "Sales strategy, outreach, client relationship, content direction, business development"],
            ["Amberley", "Growth Engine Partner", "Partnership coordination, strategic input"],
            ["Anthony", "Operations", "Project coordination, timeline tracking, deliverable management"],
            ["Abhijeet", "Video/Content Editor", "Video content, social media assets"],
            ["Soumya", "Graphic Designer", "Banner ads, social media creatives, visual assets"],
        ],
    ))
    blocks.append(divider())

    # ── Section 16: KPIs & Success Metrics ──
    blocks.append(heading_1("KPIs & Success Metrics"))

    blocks.append(heading_2("Outreach KPIs"))
    blocks.append(table(
        ["Metric", "Target"],
        [
            ["Cold emails sent per day", "25-50 (scaling to 100)"],
            ["Email open rate", ">40%"],
            ["Email reply rate", ">5%"],
            ["LinkedIn connections/week", "50+"],
            ["Demo calls booked/month", "5-10"],
        ],
    ))

    blocks.append(heading_2("Sales KPIs"))
    blocks.append(table(
        ["Metric", "Target"],
        [
            ["Pilot universities secured (30 days)", "2-3"],
            ["Sales cycle length", "3-6 months"],
            ["Pilot → paid conversion", ">50%"],
            ["Universities onboarded (Year 1)", "10-20"],
        ],
    ))

    blocks.append(heading_2("Website & Content KPIs"))
    blocks.append(table(
        ["Metric", "Target"],
        [
            ["Website pages live", "6+ (currently 1)"],
            ["Blog posts published/month", "4+"],
            ["Organic traffic growth", "Month-over-month increase"],
            ["Demo form submissions", "5+/month"],
        ],
    ))
    blocks.append(divider())

    # ── Section 17: Risks & Mitigation ──
    blocks.append(heading_1("Risks & Mitigation"))
    blocks.append(table(
        ["Risk", "Impact", "Mitigation"],
        [
            ["Website delay", "Can't drive outreach traffic anywhere meaningful", "Prioritize B2B landing page and blog section this week"],
            ["Slow university procurement", "Revenue takes time", "Start outreach NOW, build pipeline early, target multiple schools simultaneously"],
            ["Low email response rates", "Wasted effort", "A/B test subject lines, personalize per university, use multi-touch sequences"],
            ["No pilot case studies yet", "Harder to close deals", "Offer first 2-3 pilots at reduced cost or free trial to build credibility"],
            ["Privacy regulation changes", "Product positioning affected", "Stay current on FERPA, Clery Act, state privacy laws — adapt messaging"],
            ["Competition", "Market noise", "Double down on the privacy-first differentiator — nobody else is doing zero-tracking"],
        ],
    ))
    blocks.append(divider())

    # ── Section 18: Timeline & Milestones ──
    blocks.append(heading_1("Timeline & Milestones"))

    blocks.append(heading_2("Completed"))
    blocks.append(todo("Brand identity finalized", checked=True))
    blocks.append(todo("Marketing strategy documented", checked=True))
    blocks.append(todo("Sales strategy with 5 personas defined", checked=True))
    blocks.append(todo("15 social media posts created", checked=True))
    blocks.append(todo("Legal agreements (SOW) signed", checked=True))
    blocks.append(todo("Website homepage built", checked=True))
    blocks.append(todo("Project folder structure organized", checked=True))

    blocks.append(heading_2("March 2026 — Current Sprint"))
    blocks.append(todo("Build additional website pages (B2B landing, About, Pricing, Contact)"))
    blocks.append(todo("Launch blog section with first 2-4 articles"))
    blocks.append(todo("Launch cold email campaigns (25-50/day)"))
    blocks.append(todo("Begin LinkedIn outreach"))
    blocks.append(todo("Create banner and social media scripts"))
    blocks.append(todo("Produce video content"))

    blocks.append(heading_2("April 2026"))
    blocks.append(todo("Scale email outreach to 100/day"))
    blocks.append(todo("First demo calls with university prospects"))
    blocks.append(todo("Publish 4+ blog articles"))
    blocks.append(todo("Launch paid ads (Meta/LinkedIn) if funnel is converting"))
    blocks.append(todo("Begin pilot negotiations with 2-3 interested universities"))

    blocks.append(heading_2("May-June 2026"))
    blocks.append(todo("Secure first pilot university partners"))
    blocks.append(todo("Deploy white-label version for pilot schools"))
    blocks.append(todo("Build first case study from pilot results"))
    blocks.append(todo("Attend / sponsor a higher education event or webinar"))

    blocks.append(heading_2("Q3-Q4 2026"))
    blocks.append(todo("Use pilot case studies to accelerate outreach"))
    blocks.append(todo("Expand to 10-20 university clients"))
    blocks.append(todo("Build referral program"))
    blocks.append(todo("Consider raising prices based on proven value"))
    blocks.append(divider())

    # ── Section 19: FAQ for New Team Members ──
    blocks.append(heading_1("FAQ for New Team Members"))

    faqs = [
        ("Q: Is SideXSide Allen's own company or a client?",
         "A: Both. Allen is the founder of SideXSide and it's also a client of The Growth Engine (Allen's marketing agency). The Growth Engine handles all marketing, website, and outreach under a signed SOW."),
        ("Q: Are we selling to students?",
         "A: No. This is strictly B2B. We sell to universities. Universities deploy the app to students. We never market directly to students."),
        ("Q: What does \"white-label\" mean in this context?",
         "A: The university gets to put their own branding on the app. Students see their university's name and logo — not \"SideXSide.\" This increases trust and adoption."),
        ("Q: What's the biggest selling point?",
         "A: Zero tracking + zero data collection. Every other campus safety app tracks students. SideXSide doesn't. That's the entire pitch."),
        ("Q: Who do we contact at universities?",
         "A: Five personas — VP Student Affairs, CIO/IT Director, Campus Police Director, Title IX Coordinator, and University President/Provost. Start with VP Student Affairs and CIO."),
        ("Q: How much does it cost the university?",
         "A: Licensing is SaaS-based (recurring). Exact pricing tiers are being finalized — it will scale based on student enrollment."),
        ("Q: What's the most urgent thing right now?",
         "A: Three things — (1) Build the remaining website pages so outreach has a destination, (2) Launch cold email campaigns to start filling the pipeline, (3) Start the blog for SEO and thought leadership."),
        ("Q: Where do I find all the project files?",
         "A: Everything is in /SideXSide Business - Organized/ with a clean 7-folder structure. Start with EXECUTIVE_SUMMARY.md for the big picture."),
    ]

    for q, a in faqs:
        blocks.append(toggle(q, [paragraph(a)]))

    blocks.append(divider())

    # ── Section 20: Contact & Ownership ──
    blocks.append(heading_1("Contact & Ownership"))
    blocks.append(table(
        ["Role", "Person", "Contact"],
        [
            ["Client Owner & Strategy Lead", "Allen Anant Thomas", "allen@thegrowthengine.net"],
            ["Growth Engine Partner", "Amberley", "Via Allen"],
            ["Operations", "Anthony", "Internal team"],
            ["Content/Video", "Abhijeet", "Internal team"],
            ["Graphic Design", "Soumya", "Internal team"],
        ],
    ))
    blocks.append(divider())

    # ── Closing ──
    blocks.append(callout(
        "Bottom line: SideXSide is a massive opportunity. Privacy-first campus safety is a market gap. The product positioning is strong, the brand is ready, the strategy is defined. What we need now is execution — website pages, email outreach, blog content, and pipeline generation. Every day we're not reaching out to universities is a day someone else could fill this gap.",
        "🚀"
    ))
    blocks.append(paragraph(rich_text("Let's go.", bold=True)))
    blocks.append(paragraph(rich_text("— Allen", italic=True)))
    blocks.append(divider())
    blocks.append(paragraph(
        rich_text("This document should be updated as milestones are completed and strategy evolves. Last updated: 2026-03-03", italic=True)
    ))

    return blocks


# ─────────────────────────────────────────────
# API Calls
# ─────────────────────────────────────────────
def search_pages():
    """Search for pages the integration has access to."""
    resp = requests.post(
        f"{BASE_URL}/search",
        headers=HEADERS,
        json={"filter": {"property": "object", "value": "page"}, "page_size": 20},
    )
    resp.raise_for_status()
    return resp.json()


def create_page(parent_page_id, title, children_blocks):
    """Create a new page under the given parent. Returns the page ID."""
    # Notion limits children to 100 blocks per request
    first_batch = children_blocks[:100]

    payload = {
        "parent": {"page_id": parent_page_id},
        "icon": {"type": "emoji", "emoji": "🛡️"},
        "cover": None,
        "properties": {
            "title": [{"text": {"content": title}}]
        },
        "children": first_batch,
    }

    resp = requests.post(f"{BASE_URL}/pages", headers=HEADERS, json=payload)
    if resp.status_code != 200:
        print(f"Error creating page: {resp.status_code}")
        print(resp.text)
        resp.raise_for_status()

    page_id = resp.json()["id"]
    print(f"✅ Page created: {resp.json()['url']}")

    # Append remaining blocks in batches of 100
    remaining = children_blocks[100:]
    batch_num = 1
    while remaining:
        batch = remaining[:100]
        remaining = remaining[100:]
        batch_num += 1
        print(f"   Adding block batch {batch_num} ({len(batch)} blocks)...")

        append_resp = requests.patch(
            f"{BASE_URL}/blocks/{page_id}/children",
            headers=HEADERS,
            json={"children": batch},
        )
        if append_resp.status_code != 200:
            print(f"   ⚠️  Error appending batch {batch_num}: {append_resp.status_code}")
            print(f"   {append_resp.text}")
        else:
            print(f"   ✅ Batch {batch_num} added successfully")

    return page_id


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  SideXSide Client Brief → Notion Page Creator")
    print("=" * 60)
    print()

    # Step 1: Find available pages
    print("🔍 Searching for pages your integration has access to...")
    try:
        results = search_pages()
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Failed to connect to Notion API: {e}")
        print("\nMake sure:")
        print("  1. Your NOTION_TOKEN is correct")
        print("  2. You have internet access")
        sys.exit(1)

    pages = results.get("results", [])
    if not pages:
        print("\n❌ No pages found!")
        print("Make sure you've shared a page with your integration:")
        print("  1. Go to the Notion page you want to use as a parent")
        print("  2. Click the ... menu → 'Connect to' → select your integration")
        sys.exit(1)

    # Step 2: Let user pick a parent page
    print(f"\n📄 Found {len(pages)} accessible page(s):\n")
    for i, page in enumerate(pages):
        title_parts = page.get("properties", {}).get("title", {})
        if isinstance(title_parts, dict):
            title_parts = title_parts.get("title", [])
        elif isinstance(title_parts, list):
            pass
        else:
            title_parts = []

        title = ""
        for part in title_parts:
            if "plain_text" in part:
                title += part["plain_text"]
        if not title:
            title = "(Untitled)"

        print(f"  [{i + 1}] {title}")
        print(f"      ID: {page['id']}")

    print()

    if len(pages) == 1:
        choice = 1
        print(f"Auto-selecting the only available page.\n")
    else:
        while True:
            try:
                choice = int(input(f"Select parent page (1-{len(pages)}): "))
                if 1 <= choice <= len(pages):
                    break
                print(f"Please enter a number between 1 and {len(pages)}")
            except (ValueError, EOFError):
                print(f"Please enter a number between 1 and {len(pages)}")

    parent_page = pages[choice - 1]
    parent_id = parent_page["id"]

    # Step 3: Build and create the page
    print("\n🏗️  Building SideXSide Client Brief content...")
    all_blocks = build_all_blocks()
    print(f"   Generated {len(all_blocks)} content blocks")

    print(f"\n📝 Creating Notion page...")
    page_id = create_page(parent_id, "SideXSide — Complete Client Brief", all_blocks)

    print(f"\n{'=' * 60}")
    print(f"  ✅ Done! Your SideXSide Client Brief is now in Notion!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
