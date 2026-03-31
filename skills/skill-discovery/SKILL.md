---
name: skill-discovery
description: Discover available skills in your company library, check what's assigned to which agent, and request skills you need. Use when you hit a wall and need a capability you don't have.
---

# Skill Discovery

Use this skill when you need a capability you don't currently have, or when you want to know what skills are available in your company.

## When to Use

- You're working on a task and realise you need a skill you don't have
- You want to check what skills exist before starting work
- You want to know which agents have which skills (to delegate appropriately)
- You need to request a new skill be added to your configuration

## How to Discover Available Skills

### 1. List all skills in your company library

```bash
curl -s "$PAPERCLIP_API_BASE_URL/companies/$PAPERCLIP_COMPANY_ID/skills" | python3 -c "
import sys, json
skills = json.load(sys.stdin)
for s in skills:
    assigned = s.get('attachedAgentCount', 0)
    print(f'{s[\"slug\"]:40s} assigned_to={assigned} agents  {s.get(\"description\",\"\")[:80]}')
"
```

### 2. Check which skills are assigned to you

```bash
curl -s "$PAPERCLIP_API_BASE_URL/agents/$PAPERCLIP_AGENT_ID/skills/sync" \
  -X POST -H "Content-Type: application/json" \
  -d '{"desiredSkills": []}' 2>/dev/null | python3 -c "
import sys, json
r = json.load(sys.stdin)
for e in r.get('entries', []):
    if e.get('desired') or e.get('required'):
        print(f'  [ACTIVE] {e[\"key\"].split(\"/\")[-1]}')
    else:
        print(f'  [AVAILABLE] {e[\"key\"].split(\"/\")[-1]}')
"
```

Note: The above is a read-only check — passing an empty desiredSkills array doesn't change your assignments.

### 3. Check what skills another agent has

```bash
curl -s "$PAPERCLIP_API_BASE_URL/agents/AGENT_ID" | python3 -c "
import sys, json
a = json.load(sys.stdin)
skills = a.get('adapterConfig', {}).get('paperclipSkillSync', {}).get('desiredSkills', [])
print(f'Agent: {a[\"name\"]}')
for s in skills:
    print(f'  {s.split(\"/\")[-1]}')
"
```

### 4. List all agents and their skills

```bash
curl -s "$PAPERCLIP_API_BASE_URL/companies/$PAPERCLIP_COMPANY_ID/agents" | python3 -c "
import sys, json
agents = json.load(sys.stdin)
for a in agents:
    skills = a.get('adapterConfig', {}).get('paperclipSkillSync', {}).get('desiredSkills', [])
    custom = [s.split('/')[-1] for s in skills if 'paperclipai/paperclip/' not in s]
    if custom:
        print(f'{a[\"name\"]:12s}: {', '.join(custom)}')
    else:
        print(f'{a[\"name\"]:12s}: (bundled only)')
"
```

## What to Do When You Need a Skill You Don't Have

### Option A: Delegate to an agent who has it

Check which agent has the skill you need (using the commands above), then assign or delegate the task to them via a comment:

```
I need the [skill-name] skill to complete this task. @AgentName has this skill — delegating to them.
```

### Option B: Request the skill be added to you

Post a comment on the issue requesting the Board add the skill:

```
I need the [skill-name] skill to complete this task. It exists in the company library but is not assigned to me. Requesting Board approval to add it to my skill set.
```

The Board (Greg) or CEO agent can then sync the skill to you via the API or UI.

### Option C: Request a new skill be imported

If the skill doesn't exist in the company library at all, post a comment:

```
I need a capability for [describe what you need]. No existing skill in the company library covers this. Requesting the Board review available external skills.
```

The Board can then search the skills catalogue (D:\paperclip\AVAILABLE-SKILLS-CATALOGUE.md) or external sources (skills.sh, GitHub) for a suitable skill, vet it, and import it.

## Available Skill Sources (for Board reference)

These are NOT for agents to install directly — the Board must vet and import them:

- **Company library** — already imported and vetted skills
- **D:\paperclip\AVAILABLE-SKILLS-CATALOGUE.md** — catalogue of 2,345 skills that were available but removed (unvetted)
- **skills.sh** — cross-agent skill directory
- **GitHub repos** — anthropics/skills, openclaw/skills, and many others

## Important Rules

- **Never install a skill yourself** — all skill imports must go through the Board
- **Never bypass skill vetting** — every new skill must pass the skill-vetter audit before activation
- **Check before you build** — before writing custom code to solve a problem, check if a skill already exists for it
- **Delegate before you struggle** — if another agent has the right skill for the job, delegate to them rather than doing it poorly yourself
