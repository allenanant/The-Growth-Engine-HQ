# AGENTS.md - Claude Assistant Workspace

**Project:** Allen Anant Thomas - Personal AI Assistant & Client Management System  
**Location:** `/Users/allenanantthomas/Documents/Claude Assistant/`  
**Last Updated:** 2026-02-27  

---

## Project Overview

This is a **static client management system** built for Allen Anant Thomas, a marketing consultant and founder of SideXSide (a campus safety SaaS). The system acts as a "digital clone" - an AI-powered workspace where Claude (this assistant) maintains comprehensive records of 6 active clients, tracks deliverables, monitors revenue (~$8,190/month), and manages a 3-person team.

**Key Characteristics:**
- **Zero dependencies** - No build process, no package managers, no frameworks
- **Static files only** - HTML, CSS, and Markdown
- **Self-contained** - All data stored in human-readable Markdown files
- **Dual-interface** - Markdown for editing, HTML dashboard for visualization

---

## Technology Stack

| Component | Technology | Notes |
|-----------|------------|-------|
| **Dashboard UI** | Vanilla HTML5 + CSS3 | Single-file SPA with tab navigation |
| **Data Storage** | Markdown files | Human-readable, version-control friendly |
| **Styling** | CSS Variables (custom properties) | Dark theme (#0d0f14 base) |
| **Interactivity** | Vanilla JavaScript | Simple tab-switching only |
| **Configuration** | JSON | Claude permissions in `.claude/settings.local.json` |

**No Build Process:** Open `dashboard.html` directly in any modern browser.

---

## File Structure

```
/Users/allenanantthomas/Documents/Claude Assistant/
├── README.md                      # Main guide & onboarding documentation
├── MASTER_CLIENT_DATABASE.md      # Complete client profiles (6 active + archived)
├── CONTACTS_DATABASE.md           # All contact information & communication preferences
├── CLIENT_STATUS_DASHBOARD.md     # Priority matrix, weekly tasks, revenue tracker
├── dashboard.html                 # Visual HTML dashboard (746 lines, single file)
├── AGENTS.md                      # This file - technical documentation for AI agents
└── .claude/
    └── settings.local.json        # Claude tool permissions
```

### File Purposes

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `README.md` | Onboarding guide for Allen, explains the entire system | Rarely |
| `MASTER_CLIENT_DATABASE.md` | Source of truth for client details, services, deliverables | As needed |
| `CONTACTS_DATABASE.md` | Contact directory with timezone/meeting preferences | When contacts change |
| `CLIENT_STATUS_DASHBOARD.md` | **Primary working file** - priorities, tasks, weekly updates | Weekly (Mondays) |
| `dashboard.html` | Visual dashboard - mirrors data from markdown files | Manually synced |

---

## Data Model

### Active Clients (6 Total)

| Client | Monthly Fee | Priority | Industry | Key Contact |
|--------|-------------|----------|----------|-------------|
| Hoogah | $2,400 | 🔴 Highest | B2B SaaS | Khushi Yadav (8am CT) |
| Restart Medical | £1,600 (~$2,000) | 🔴 Highest | Medical Aesthetics | Alan RN (07506 689894) |
| SideXSide | $1,900 | 🟡 High | Campus Safety SaaS | Allen (You) |
| Dr Sw Clinics | £850 (~$1,050) | 🔴 Highest | Medical Aesthetics | sherif@drswclinics.com |
| Frenchify | ₹40,000 (~$480) | 🟢 Medium | EdTech | Vyom |
| KP Singh | ₹30,000 (~$360) | 🟢 Medium | Music/Artist Dev | Via Grawoth Services |

**Total Monthly Revenue:** $8,190 USD

### Team Structure

| Member | Role | Responsibilities |
|--------|------|------------------|
| Allen Anant Thomas | Founder/Strategy | All client relationships, sales, strategy |
| Anthony | Operations | Project coordination, timeline management |
| Abhijeet | Editor | Video editing, HeyGen AI avatar production |

### Task Status System

Tasks use a 4-state system with visual indicators:

| Status | Indicator | Icon | Meaning |
|--------|-----------|------|---------|
| Done | `tc-done` | ✓ | Completed |
| Doing | `tc-doing` | → | In progress |
| Pending | `tc-pending` | · | Not started |
| Blocked | `tc-blocked` | ! | Waiting on external input |

Priority levels: 🔴 Highest / 🟡 High / 🟢 Medium

---

## Development Conventions

### Date Format
- Use ISO format: `2026-02-27`
- Include timezone context for meetings (e.g., "8am CT")

### Currency Handling
- Store in original currency (GBP, INR, USD)
- Always include USD equivalent in parentheses: `£1,600 (~$2,000)`

### File Editing
- **Markdown files:** Free-form editing, maintain consistency with existing patterns
- **dashboard.html:** Update HTML sections to match markdown changes
- Use emojis for visual scanning: 🔴 🟡 🟢 ✅ ⏳ ⚠️

### Confidentiality Markers
- **NDA Required:** Explicitly note when content cannot be shared (e.g., Dr Sw's "O Concept™")
- **IP Protection:** Some client assets are proprietary - never assume portfolio rights

---

## Workflow Guidelines

### Weekly Update Cycle (Every Monday)

1. **Review** `CLIENT_STATUS_DASHBOARD.md` "Weekly Priorities" section
2. **Update** task statuses based on Allen's progress
3. **Sync** changes to `dashboard.html` (manual - keep data consistent)
4. **Report** completion status to Allen

### Client Work Flow

When Allen asks about a specific client:
1. Check `CLIENT_STATUS_DASHBOARD.md` for current status
2. Reference `MASTER_CLIENT_DATABASE.md` for full context
3. Use `CONTACTS_DATABASE.md` for contact details
4. Provide specific next actions

### Revenue Tracking

Monthly recurring revenue (MRR) is calculated from:
- Fixed monthly retainers (not project-based)
- Currency converted to USD at approximate rates
- Updated when contract values change

---

## Key Integrations (Planned)

| System | Status | Notes |
|--------|--------|-------|
| Notion | ⏳ Pending | Workspace connection deferred |
| Google Calendar | ⏳ Pending | Meeting scheduling automation |
| Email CRM | ⏳ Pending | Client communication tracking |

Current integration is **manual** - Allen updates Claude, Claude updates files.

---

## Security Considerations

1. **Client Data:** Files contain real client names, emails, phone numbers - protect accordingly
2. **Contract Terms:** Some files contain confidential business terms
3. **NDA Compliance:** Dr Sw Clinics has strict IP protection - never expose "O Concept™" details
4. **No Secrets in Code:** No API keys or credentials stored in this directory

---

## How to Update

### Adding a New Client

1. Add to `MASTER_CLIENT_DATABASE.md` under "ACTIVE CLIENTS"
2. Add contacts to `CONTACTS_DATABASE.md`
3. Create task tracking in `CLIENT_STATUS_DASHBOARD.md`
4. Add card to `dashboard.html` (copy existing pattern)
5. Update revenue totals everywhere

### Updating Task Status

1. Edit `CLIENT_STATUS_DASHBOARD.md` "Weekly Priorities" section
2. Update the specific client's task list in the same file
3. Sync to `dashboard.html` client cards and milestones section
4. Update progress percentages in dashboard

### Modifying Dashboard UI

The dashboard is a single HTML file with:
- CSS variables in `:root` for theming
- Tab-based navigation via `show()` JavaScript function
- Responsive grid layouts (3-column client cards)
- No external dependencies

---

## Common Tasks

### "What's urgent this week?"
→ Read `CLIENT_STATUS_DASHBOARD.md` "Weekly Priorities" → "MUST DO" section

### "Update dashboard - I completed X"
→ Update task status in `CLIENT_STATUS_DASHBOARD.md` → Sync to `dashboard.html`

### "Show me [client] contact info"
→ Query `CONTACTS_DATABASE.md` for that client's contact section

### "What's my revenue?"
→ Read `CLIENT_STATUS_DASHBOARD.md` "Revenue Tracker" section

### "Draft an email to [client]"
→ Check `CONTACTS_DATABASE.md` for preferred contact method → Draft accordingly

---

## Architecture Notes

### Why Static Files?
- **Portability:** Works on any device with a browser
- **Simplicity:** No servers, no databases, no auth
- **Transparency:** Allen can read/edit everything directly
- **AI-Friendly:** Markdown is optimal for LLM context windows

### Dashboard Design
- Single-page application (SPA) using CSS `display` toggling
- CSS Grid for responsive layouts
- Custom properties for consistent theming
- No framework = no build step = instant updates

### Data Redundancy
Some data exists in both Markdown and HTML. This is intentional:
- Markdown = Source of truth (editable by Allen)
- HTML = Visual presentation (read-only dashboard)
Keep them in sync when updating.

---

## Custom Commands

The system recognizes this custom command:

- `/generate-restart-scripts` - Generates 30 social media scripts for Restart Medical (HeyGen AI Avatar ready)

---

## Contact

**Project Owner:** Allen Anant Thomas  
**Email:** allen@thegrowthengine.net  
**Business:** The Growth Engine / SideXSide  
**Assistant:** Claude (AI)  

---

*This AGENTS.md file should be updated when:
- New clients are added/removed
- File structure changes
- New conventions are established
- Major workflow changes occur*
