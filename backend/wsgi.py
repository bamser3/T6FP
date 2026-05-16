from dotenv import load_dotenv
load_dotenv()

import os
import sys
import json

sys.path.insert(0, os.path.dirname(__file__))

from src.app import create_app
from src.extensions import db
from src.models import Question

QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "..", "attached_assets", "mazeh_extracted", "techextract", "backend", "questions_seed.json")

app = create_app()

def seed_if_needed():
    with app.app_context():
        db.create_all()
        if Question.query.count() == 0:
            try:
                with open(QUESTIONS_FILE) as f:
                    questions_data = json.load(f)
                for q in questions_data:
                    db.session.add(Question(
                        id=q["id"],
                        category=q["category"],
                        skill=q["skill"],
                        difficulty=q["difficulty"],
                        question=q["question"],
                        answer=q["answer"],
                    ))
                db.session.commit()
                print(f"Seeded {len(questions_data)} flashcard questions")
            except Exception as e:
                print(f"Warning: could not seed questions: {e}")

seed_if_needed()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", debug=False, port=port)