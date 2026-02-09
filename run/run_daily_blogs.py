# run/run_daily_blogs.py
from __future__ import annotations

import os
import sys
import logging
import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load env vars (LangSmith, API keys)
load_dotenv()

# Add project root to sys.path to allow importing 'agents'
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Setup logging
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = LOGS_DIR / f"execution_{timestamp}.log"

# Configure logging to write to file AND stdout
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
       # Also write to log file
       try:
           with open(log_file, "a", encoding="utf-8") as f:
               f.write(data)
       except Exception:
           pass
   def flush(self):
       self.stream.flush()

# Redirect stdout and stderr to capture all print statements from agents
sys.stdout = Unbuffered(sys.stdout)
sys.stderr = Unbuffered(sys.stderr)

print(f"📝 Logging execution to: {log_file}")

from agents.explorer.explorer_agent import run_explorer_agent
# Updated import to point to the new modular backend runner
from agents.blog_writer.runner import generate_blog

BLOGS_PER_RUN = 1

def main():
    print(f"\n🚀 One-Click Blog Run Started [{timestamp}]\n")

    try:
        print("🔍 Running Explorer Agent...")
        explorer_result = run_explorer_agent()
        topics = explorer_result.topics
        print(f"📊 Found {len(topics)} topics.")

        # Prefer tech / AI / startup for now
        preferred = [
            t for t in topics
            if t.category in {"tech", "ai", "startup"}
        ]

        if len(preferred) < BLOGS_PER_RUN:
            print("⚠️ Not enough preferred topics, using fallback")
            preferred = topics

        selected = preferred[:BLOGS_PER_RUN]

        for i, topic in enumerate(selected, 1):
            print(f"\n▶️ ({i}/{BLOGS_PER_RUN}) Processing Topic: {topic.title}")
            print(f"   Category: {topic.category}, Score: {topic.score}")
            
            try:
                generate_blog(topic.title)
            except Exception as e:
                print(f"❌ Error generating blog for '{topic.title}': {e}")
                import traceback
                traceback.print_exc()

        print("\n✅ One-Click Blog Run Finished\n")

    except Exception as e:
        print(f"❌ Fatal error in daily run: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
