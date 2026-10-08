import json
import random
import datetime
import os
import boto3

MODEL_ID = os.environ.get("MODEL_ID")

THEMES = [
    "a lighthouse keeper who talks to ships",
    "a robot learning to garden",
    "a city built inside a giant tree",
    "a librarian who collects lost dreams",
    "a cafe that only serves at midnight",
    "a cartographer mapping places that don't exist yet",
    "a musician who plays songs for the weather",
    "a shop that repairs broken memories",
]

def generate_spark():
    if not MODEL_ID:
        raise RuntimeError(
            "Set MODEL_ID to an Amazon Bedrock model ID before generating a spark."
        )

    bedrock = boto3.client("bedrock-runtime")
    theme = random.choice(THEMES)
    today = datetime.date.today().isoformat()

    prompt = (
        f"Write a very short (under 120 words), whimsical micro-story about {theme}. "
        f"End with a single italicized one-line takeaway. "
        f"Return ONLY the story text, no preamble."
    )

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}],
        }),
    )

    result = json.loads(response["body"].read())
    story_text = result["content"][0]["text"].strip()
    return {"date": today, "theme": theme, "story": story_text}

if __name__ == "__main__":
    payload = generate_spark()
    os.makedirs("site/archive", exist_ok=True)

    with open("site/latest.json", "w") as f:
        json.dump(payload, f, indent=2)

    with open(f"site/archive/{payload['date']}.json", "w") as f:
        json.dump(payload, f, indent=2)

    print("Generated spark:", payload["date"], "-", payload["theme"])
