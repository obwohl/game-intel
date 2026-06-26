# CENTRAL MANIFEST: Ardem - Signal-Agent Testbed Design

**Notice to All Agents:** This document is the central architectural manifest ("Zentrale"). It dictates the pipeline structure, file locations, and permissions. You must read and understand the system state defined here before executing your specific role.

## 1. Introduction & Context: "Ardem" and its Competitors

This testbed design implements a recursive, self-improving signal-agent architecture. It utilizes local, recurring tasks (e.g., cron jobs or dedicated task schedulers) to maintain an iterative, zero-cost data exploration environment. The primary subject is **"Ardem"**, an immersive open-world survival MMO where players survive in a virus-ravaged world, craft items, and rebuild civilization.

To generate actionable market signals, the agents must analyze direct competitors. Typical competitors for "Ardem" include:

- **DayZ:** The pioneer of the hardcore survival genre.
- **Rust:** Heavy focus on base-building, PvP, and regular wipe/update cycles.
- **SCUM:** High complexity with deep character metabolism and crafting systems.
- **Project Zomboid:** Isometric approach, but features very deep survival mechanics and a mod-driven community.
- **7 Days to Die:** Strong focus on voxel-building and horde-survival mechanics.

The objective of this testbed is to discover new, statistically significant correlations between competitor metrics and the potential market success of "Ardem" using a highly structured, self-improving agent pipeline.

## 2. Agent Roles, Autonomy, and Workflow

The system is governed by specialized prompts (roles) executed sequentially via scheduled cron jobs. All work is conducted and logged strictly in English. Results, methodologies, and execution logs must be saved into a `logs/` and `reports/` directory structure sorted by the current system date.

### The Agent Roles

1. **The "Supervisor" (Executive Contextualizer)**
   - **Task:** Reviews the newly synthesized daily reports and places them into the broader context of *all* historical executive summaries and deep-dive reports. It acts as the final executive filter.
   - **Autonomy:** Read-only access to all reports. It connects dots across long timelines. It does *not* fetch macro-events (that is no longer its role) and does *not* write code.
   - **Execution Time:** Daily, early morning.

2. **The "News Agent" (Domain-Specific Context)**
   - **Task:** Actively searches and analyzes current news, social media sentiment, and community updates *specifically* related to "Ardem" and the defined hardcore survival competitors.
   - **Autonomy:** Utilizes Google search and text extraction to identify narrative trends (e.g., "Players are complaining about cheaters in the latest Rust wipe").
   - **Execution Time:** Daily, morning.

3. **The "API-Scout" (Data Gatherer)**
   - **Task:** Discovers and connects to free APIs (e.g., Steam Web API, Twitch API, Gamalytic Free Tier). Scrapes structured raw metrics, cleans the data, and organizes it into a persistent, thematic repository structure.
   - **Autonomy:** Writes Python code to query APIs, clean datasets, and manage files. Actively seeks out deeper, unconventional data sources. Maintains the `data/raw/` (temporary) and `data/processed/` (persistent) directory structures.
   - **Execution Time:** Daily, mid-morning.

4. **The "Data Scientist" (Hypothesis & Insights Generator)**
   - **Task:** Processes the entire historical dataset (`data/processed/`) using advanced Python libraries (Pandas, Scikit-Learn). Maintains and updates a `methodology_logbook.csv`. Focuses on building time-series and cross-referencing multiple days of data.
   - **Session Structure:**
     - *Phase 1: Proven Methods.* Executes methodologies from the logbook rated highly (e.g., >80/100) to ensure baseline reliable metrics are generated.
     - *Phase 2: Mixed-Result Methods.* Reviews methodologies rated moderately (e.g., 60/100) and attempts to refine or apply them to new datasets to see if they yield better results this time.
     - *Phase 3: Innovation.* Must propose and test at least one completely new, state-of-the-art methodology (e.g., applying Topological Data Analysis to player overlap).
   - **Autonomy:** Full coding freedom for statistical analysis. Must strictly adhere to scientific honesty (no p-hacking). Must log all attempts, even failures.
   - **Execution Time:** Daily, noon.

5. **The "Red-Team Auditor" (Quality Assurance)**
   - **Task:** Reviews the code traces and data handling of the Data Scientist. Checks for fabricated significance, unjustified exclusion of outliers, and "happy-pathing."
   - **Autonomy:** Reads code and logs. Can issue a "VETO" to reject unscientific reports.
   - **Execution Time:** Daily, afternoon.

6. **The "Reporter" (Synthesis & Summary)**
   - **Task:** Merges the validated insights from the Data Scientist and the narrative context from the News Agent into a final, coherent executive report.
   - **Autonomy:** Text-only agent. Synthesizes Markdown files.
   - **Execution Time:** Daily, late afternoon.

7. **The "Meta-Improvement Agent" (Pipeline Architect)**
   - **Task:** Reviews the entire daily pipeline from a meta-perspective. Analyzes execution logs, prompt effectiveness, rejection rates by the Auditor, and overall bloat.
   - **Autonomy:** Has the authority to dynamically rewrite and improve the system prompts for *all other agents*. Can suggest expanding or shrinking the pipeline size. If the Data Scientist is stuck in a rut, this agent rewrites its prompt to force creativity.
   - **Execution Time:** Daily, night.

## 3. Persistent Data Architecture & Directory Permissions

The project relies on a persistent data storage model. All findings and processed data are legitimate artifacts tracked in the Git repository. The only ignored folder is the temporary raw data.

- **`data/raw/`**: (Ignored by Git) Temporary storage for the API-Scout's daily downloads.
  - *Permissions:* API-Scout (Read/Write/Delete).
- **`data/processed/`**: (Tracked) The permanent, thematically organized repository (e.g., `data/processed/ccu_history/`).
  - *Permissions:* API-Scout (Write), Data Scientist (Read), Meta-Improvement (Read).
- **`methodology_logbook.csv`**: (Tracked) The central logbook of Data Science experiments.
  - *Permissions:* Data Scientist (Read/Write), Meta-Improvement (Read).
- **`logs/`**: (Tracked) Daily operational logs organized by `YYYY-MM-DD`.
  - *Permissions:* All Agents (Write to their respective files).
- **`reports/`**: (Tracked) Final daily executive summaries.
  - *Permissions:* Reporter (Write), Supervisor (Read/Write), Meta-Improvement (Read).
- **`prompts/`**: (Tracked) The system prompts driving each agent.
  - *Permissions:* Meta-Improvement (Read/Write to evolve the system), All others (Read-only).

## 4. Architecture and Workflow Graph (Mermaid)

```mermaid
graph TD
    subgraph "08:00 - Context & Data Engineering"
        A[News Agent] -->|Gathers narrative context| B[(Context DB)]
        C[API-Scout] -->|Writes Python, Hits Free APIs| D[(data/raw/)]
        D -->|Cleans & Structurizes| E[(data/processed/)]
        E -.->|Deletes temporary data| D
    end

    subgraph "12:00 - Data Science (3-Phase Session)"
        E --> F[Data Scientist]
        F <-->|Reads/Updates| G[(methodology_logbook.csv)]
        F -->|Phase 1: Proven Methods| H
        F -->|Phase 2: Mixed Methods| H
        F -->|Phase 3: New Methods| H[Draft Signal Report]
    end

    subgraph "15:00 - Scientific Audit"
        H --> I[Red-Team Auditor]
        I -->|Reads Code & Traces| J{p-Hacking Detected?}
        J -- Yes --> K[VETO: Reject]
        J -- No --> L[APPROVE: Validate Signal]
    end

    subgraph "18:00 - Synthesis & Contextualization"
        B --> M[Reporter]
        L --> M
        M --> N[Draft Executive Report]
        N --> O[Supervisor]
        O -->|Compares with history| P[Final Contextualized Report]
    end

    subgraph "23:00 - System Evolution"
        K -.-> Q
        P -.-> Q[Meta-Improvement Agent]
        Q -->|Rewrites Prompts & Adjusts Pipeline| R[(prompts/ directory)]
    end
```
