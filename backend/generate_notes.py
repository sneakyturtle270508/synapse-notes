import httpx
import asyncio
import random

SERVER = "http://localhost:8000"

TOPICS = [
    "Morning routine", "Book reading", "Movie night", "Travel plans",
    "Guitar practice", "Photo walk", "Cooking dinner", "Gym workout",
    "Spanish lessons", "Breathing exercises", "Fixing shelves", "Plant care",
    "Sketching ideas", "Playlist making", "Series binge", "Journal writing",
    "Savings tracking", "New recipe", "Deadline management", "Scrolling habits",
    "Sleep quality", "Push ups", "Meal prep", "Body scan",
    "True crime podcast", "Nature doc", "Course progress", "App idea",
    "Coffee meeting", "Career path", "Python scripts", "Meeting notes",
    "Design mockups", "Bug hunting", "API endpoints", "Query optimization",
    "Server setup", "Firewall rules", "Unit tests", "CI pipeline",
    "Sprint review", "Retrospective", "Team sync", "Feature specs",
    "Risk register", "Budget forecast", "Resource plan", "Milestone"
]

async def create_note(client, title, content):
    try:
        resp = await client.post(f"{SERVER}/api/notes", json={"title": title, "content": content}, timeout=30)
        return resp.status_code == 200
    except:
        return False

async def main():
    notes = [(f"{t} #{i+1}", f"Notes about {t.lower()}.") for i, t in enumerate(TOPICS[:50])]
    
    async with httpx.AsyncClient() as client:
        success = 0
        for i, (title, content) in enumerate(notes):
            if await create_note(client, title, content):
                success += 1
            print(f"{i+1}/50", end="\r")
    print(f"\nCreated {success} notes")

asyncio.run(main())
