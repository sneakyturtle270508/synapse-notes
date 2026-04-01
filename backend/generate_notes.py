import httpx
import asyncio
import random

SERVER = "http://localhost:8000"

CATEGORIES = {
    "technology": [
        "Python vs JavaScript performance", "Docker containers explained", "API design patterns",
        "Database indexing strategies", "Microservices architecture", "Git workflows for teams",
        "Testing best practices", "CI/CD pipelines", "Cloud native applications",
        "Serverless computing", "Kubernetes basics", "Redis caching strategies",
        "GraphQL vs REST", "OAuth authentication", "WebSocket real-time apps",
        "React component patterns", "Node.js performance tuning", "MongoDB aggregation",
        "Nginx load balancing", "Terraform infrastructure as code"
    ],
    "science": [
        "Climate change mechanisms", "Quantum computing basics", "CRISPR gene editing",
        "Machine learning algorithms", "Neural network architectures", "Protein folding research",
        "Particle physics discoveries", "Ocean acidification effects", "Renewable energy storage",
        "Nuclear fusion progress", "Mars colonization challenges", "Dark matter evidence",
        "Antibiotic resistance", "Photosynthesis optimization", "Brain plasticity research",
        "Evolutionary biology", "Microbiome health", "Astrobiology findings",
        "Biomimicry engineering", "Climate modeling"
    ],
    "business": [
        "Startup funding rounds", "Product market fit", "Growth hacking strategies",
        "Customer acquisition cost", "Freemium business models", "SaaS pricing strategies",
        "Remote team management", "Venture capital terms", "Burn rate calculations",
        "Unit economics fundamentals", "Market segmentation", "Competitive analysis",
        "User retention metrics", "Business model canvas", "Pivot strategies",
        "Hiring for startups", "Customer development", "Minimum viable products",
        "Angel investor readiness", "Exit strategy planning"
    ],
    "philosophy": [
        "Consciousness and AI", "Ethical AI development", "Free will debate",
        "Meaning of life exploration", "Philosophy of mind", "Utilitarianism modern applications",
        "Existentialism in practice", "Stoicism for modern life", "Ethics of automation",
        "Privacy in digital age", "Identity in virtual worlds", "Moral responsibility",
        "Knowledge vs belief", "Truth in post-truth era", "Happiness economics",
        "Digital ethics", "Technology and morality", "Purpose in work life",
        "Mindfulness philosophy", "Responsibility for future generations"
    ],
    "arts": [
        "Color theory in design", "Typography principles", "Composition in photography",
        "Music theory basics", "Jazz improvisation", "Abstract expressionism",
        "Digital art tools", "Sculpture techniques", "Architecture sustainability",
        "Film noir aesthetics", "Street art movement", "Literary symbolism",
        "Performance art", "Ceramics glazing", "Textile patterns",
        "Graphic design trends", "Animation principles", "Sound design for film",
        "Calligraphy revival", "Installation art"
    ],
    "health": [
        "Sleep quality optimization", "Intermittent fasting benefits", "Cold exposure therapy",
        "Meditation techniques", "Zone 2 cardio", "Strength training progressive overload",
        "Gut microbiome health", "Chronic inflammation", "Mental health awareness",
        "Breathwork practices", "Stress management", "Recovery protocols",
        "Nutrient timing", "Flexibility training", "Blood sugar regulation",
        "Cognitive enhancement", "Longevity science", "Injury prevention",
        "Hydration strategies", "Eye strain reduction"
    ],
    "finance": [
        "Compound interest investing", "Dollar cost averaging", "Asset allocation strategies",
        "Tax loss harvesting", "Real estate investing", "Stock market volatility",
        "Retirement planning", "Emergency fund basics", "Credit score improvement",
        "Passive income streams", "Diversification principles", "Risk management",
        "Index fund investing", "Cryptocurrency basics", "Bond duration",
        "Estate planning", "Insurance fundamentals", "Portfolio rebalancing",
        "FIRE movement", "Behavioral finance"
    ],
    "cooking": [
        "Fermentation science", "Maillard reaction", "Knife skills fundamentals",
        "Emulsification techniques", "Bread making process", "Chocolate tempering",
        "Umami enhancement", "Acid balance in cooking", "Herb pairings",
        "Sous vide precision", "Smoking and curing", "Pastry lamination",
        "Sauce reduction", "Vegetable prep methods", "Wok technique",
        "Food plating design", "Spice combinations", "Gluten free baking",
        "Preservation methods", "Flavor layering"
    ],
    "travel": [
        "Solo travel safety", "Budget backpacking", "Digital nomad lifestyle",
        "Cultural immersion", "Sustainable tourism", "Language learning tips",
        "Travel photography", "Off the beaten path", "Long term travel planning",
        "Workation destinations", "Adventure travel", "Food tourism",
        "Slow travel movement", "Road trip planning", "Hostel culture",
        "Travel hacking", "Visa requirements", "Packing efficiently",
        "Local customs etiquette", "Trip journaling"
    ],
    "nature": [
        "Permaculture design", "Composting methods", "Seed saving",
        "Native plant gardening", "Pollinator habitats", "Rainwater harvesting",
        "Beekeeping basics", "Mushroom foraging", "Forest bathing",
        "Bird identification", "Night sky observation", "Soil health",
        "Regenerative agriculture", "Vertical gardening", "Seasonal eating",
        "Wildlife photography", "Natural building", "Water conservation",
        "Native species", "Ecological succession"
    ],
    "communication": [
        "Public speaking anxiety", "Storytelling techniques", "Active listening",
        "Negotiation tactics", "Feedback delivery", "Conflict resolution",
        "Executive presence", "Persuasive writing", "Body language",
        "Networking strategies", "Interview skills", "Meeting facilitation",
        "Cross-cultural communication", "Written communication", "Presentation design",
        "Emotional intelligence", "Rapport building", "Difficult conversations",
        "Mentorship dynamics", "Team dynamics"
    ],
    "learning": [
        "Spaced repetition systems", "Deliberate practice", "Bloom taxonomy",
        "Learning styles myth", "Note taking methods", "Focus enhancement",
        "Memory palace technique", "Reading retention", "Skill stacking",
        "Beginner mindset", "Knowledge synthesis", "Curiosity cultivation",
        "Educational technology", "Self-directed learning", "Critical thinking",
        "Concept mapping", "Teaching for understanding", "Learning burnout",
        "Microlearning", "Transfer of learning"
    ],
    "gaming": [
        "Game design principles", "Balancing mechanics", "Procedural generation",
        "Narrative design", "Multiplayer matchmaking", "Progression systems",
        "User interface design", "Sound design in games", "Virtual reality",
        "Competitive esports", "Game monetization", "Level design",
        "Character development", "Storytelling in games", "Player psychology",
        "Mobile gaming trends", "Retro game preservation", "Accessibility in games",
        "Game engine architecture", "Modding community"
    ],
    "writing": [
        "Blog post structure", "Copywriting persuasion", "Technical writing clarity",
        "Character development", "Plot pacing", "Dialogue naturalism",
        "World building", "Editing self revision", "Genre conventions",
        "Submitting to publications", "Writing routine", "Writer's block solutions",
        "Research for fiction", "Scene construction", "Point of view",
        "Opening hooks", "Ending satisfaction", "Revision process",
        "Publishing options", "Author platform building"
    ],
    "productivity": [
        "Deep work sessions", "Time blocking", "Inbox zero",
        "Task management systems", "Procrastination solutions", "Energy management",
        "Batching similar tasks", "Automation scripts", "Second brain systems",
        "Morning routines", "Evening routines", "Focus music",
        "Workspace optimization", "Meeting reduction", "Delegation strategies",
        "Priority frameworks", "Weekly reviews", "Goal setting systems",
        "Habit stacking", "Decision fatigue"
    ],
    "relationships": [
        "Long distance relationships", "Conflict de-escalation", "Boundary setting",
        "Family dynamics", "Dating apps etiquette", "Friendship maintenance",
        "Couple communication", "Parenting strategies", "Sibling relationships",
        "Caring for aging parents", "Ex relationship closure", "Trust rebuilding",
        "Social skill development", "Empathy cultivation", "Forgiveness practice",
        "Intimacy building", "Attachment styles", "Support networks",
        "Romantic gestures", "Healthy arguing"
    ],
    "sports": [
        "Marathon training", "Swimming technique", "Cycling position",
        "Rock climbing fundamentals", "Basketball shooting form", "Tennis grip types",
        "Golf swing mechanics", "Crossfit workouts", "Yoga for athletes",
        "Sports psychology", "Injury recovery", "Recovery nutrition",
        "Sports supplements", "Altitude training", "Periodization",
        "Mobility work", "Core stability", "Sport specific conditioning",
        "Race day preparation", "Cool down routines"
    ],
    "music": [
        "Music production DAW", "Guitar chord progressions", "Drum kit timing",
        "Vocal range expansion", "Music theory ear training", "Synthesizer basics",
        "Live performance", "Music mixing", "Folk music traditions",
        "Electronic music genres", "Classical music appreciation", "Jazz standards",
        "Songwriting hooks", "Music business", "Streaming royalties",
        "Album sequencing", "Rhythm fundamentals", "Music notation",
        "Piano arrangements", "Band dynamics"
    ],
    "history": [
        "Industrial revolution impact", "Ancient Rome government", "World war II causes",
        "Renaissance art", "Black history significant", "Colonialism effects",
        "Women's suffrage movement", "Cold war events", "Ancient Egypt culture",
        "Medieval castles", "Civil rights movement", "Trade routes history",
        "Scientific revolution", "Political philosophy origins", "Migration patterns",
        "Pandemic history", "Technological revolutions", "Cultural revolutions",
        "Imperial powers", "Archaeological discoveries"
    ],
    "environment": [
        "Carbon footprint reduction", "Zero waste living", "Electric vehicles",
        "Plastic pollution", "Ocean cleanup", "Deforestation",
        "Renewable energy transition", "Sustainable fashion", "Food waste reduction",
        "Green building design", "Air quality improvement", "Water purification",
        "Wildlife conservation", "Coral reef protection", "Urban farming",
        "Circular economy", "Ecosystem restoration", "Biodiversity loss",
        "Climate adaptation", "Environmental policy"
    ]
}

CONTENT_TEMPLATES = [
    "Exploring the fundamentals of {topic} and how it applies to modern contexts. Key considerations include methodology, practical implementation, and real-world examples. This area of study offers fascinating insights into human behavior and systemic patterns.",
    "A deep dive into {topic} with analysis of current research and emerging trends. The intersection of theory and practice reveals important opportunities for innovation. Understanding these dynamics is crucial for anyone working in this field.",
    "Personal reflections on {topic} based on extensive reading and hands-on experience. The journey toward mastery involves continuous learning and adaptation. These observations capture key lessons and potential pitfalls to avoid.",
    "Comprehensive overview of {topic} covering historical context, current state, and future possibilities. The interconnected nature of this subject with other domains creates rich opportunities for exploration. Critical thinking and open-mindedness are essential.",
    "Case study examination of {topic} with practical applications and strategic considerations. Analyzing successful and unsuccessful approaches provides valuable lessons. The goal is to distill complex ideas into actionable insights."
]

async def create_note(client: httpx.AsyncClient, title: str, content: str):
    try:
        resp = await client.post(f"{SERVER}/api/notes", json={"title": title, "content": content}, timeout=60)
        if resp.status_code == 200:
            return True
        else:
            print(f"Error creating note '{title}': {resp.status_code} {resp.text}")
            return False
    except Exception as e:
        print(f"Exception creating note '{title}': {e}")
        return False

async def main():
    notes = []
    
    for category, topics in CATEGORIES.items():
        for base_topic in topics:
            for i in range(2):
                title = f"{base_topic} #{len(notes) + 1}"
                template = random.choice(CONTENT_TEMPLATES)
                content = template.format(topic=base_topic.lower())
                notes.append((title, content))
                
                if len(notes) >= 2000:
                    break
            if len(notes) >= 2000:
                break
        if len(notes) >= 2000:
            break
    
    extra_topics = [
        "Personal development journey", "Creative problem solving", "Systematic thinking",
        "Data analysis methods", "Critical reasoning", "Innovation frameworks",
        "Team collaboration", "Quality standards", "Risk assessment",
        "Project management", "Strategic planning", "Operational efficiency",
        "Customer experience", "User research", "Market analysis",
        "Brand development", "Content strategy", "Community building",
        "Mentorship and guidance", "Continuous improvement", "Adaptive leadership",
        "Emotional resilience", "Work life harmony", "Digital literacy",
        "Information verification", "Complex problem decomposition", "Solution architecture",
        "Feedback loops", "Iterative development", "Sustainable practices",
        "Cross-functional collaboration", "Stakeholder management", "Change management",
        "Knowledge sharing", "Performance metrics", "Impact measurement",
        "Resource optimization", "Scalability planning", "Security fundamentals",
        "Data privacy", "Ethical considerations", "Transparency practices",
        "Accountability structures", "Governance frameworks", "Compliance requirements",
        "Best practice adoption", "Innovation culture", "Experimental mindset",
        "Hypothesis testing", "Evidence based decisions", "Root cause analysis"
    ]
    
    for i, topic in enumerate(extra_topics):
        if len(notes) >= 2000:
            break
        title = f"{topic} #{len(notes) + 1}"
        template = random.choice(CONTENT_TEMPLATES)
        content = template.format(topic=topic.lower())
        notes.append((title, content))
    
    print(f"Generated {len(notes)} notes. Starting creation...")
    
    async with httpx.AsyncClient() as client:
        success = 0
        batch_size = 10
        for i in range(0, len(notes), batch_size):
            batch = notes[i:i+batch_size]
            tasks = [create_note(client, title, content) for title, content in batch]
            results = await asyncio.gather(*tasks)
            success += sum(1 for r in results if r)
            print(f"Progress: {min(i+batch_size, len(notes))}/{len(notes)} notes created ({success} successful)")
    
    print(f"\nDone! Created {success} notes out of {len(notes)}")
    print("Notes are now being processed and linked based on semantic similarity.")

if __name__ == "__main__":
    asyncio.run(main())
