import os
import json
import base64
from openai import OpenAI
from dotenv import load_dotenv
from code.prompts import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

MODEL = "google/gemini-2.5-flash"


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def analyze_claim(claim_text, claim_object, image_paths):

    image_ids = []

    for p in image_paths:
        image_id = os.path.splitext(os.path.basename(p))[0]
        image_ids.append(image_id)

    prompt = f"""

    {SYSTEM_PROMPT}

    Claim object:
    {claim_object}

    Claim text:
    {claim_text}

    Available image IDs:
    {";".join(image_ids)}

    IMPORTANT OUTPUT RULES:

    Return ONLY valid JSON.

    Allowed claim_status:
    supported
    contradicted
    not_enough_information

    Allowed issue_type:
    dent
    scratch
    crack
    glass_shatter
    broken_part
    missing_part
    torn_packaging
    crushed_packaging
    water_damage
    stain
    none
    unknown

    Allowed severity:
    none
    low
    medium
    high
    unknown

    Allowed risk_flags:
    none
    blurry_image
    cropped_or_obstructed
    low_light_or_glare
    wrong_angle
    wrong_object
    wrong_object_part
    damage_not_visible
    claim_mismatch
    possible_manipulation
    non_original_image
    text_instruction_present
    user_history_risk
    manual_review_required

    For supporting_image_ids:
    Use ONLY IDs from Available image IDs.
    Example: img_1
    Example: img_1;img_2
    If no image supports the claim return: none
    Never invent image IDs.
    Never use image_1.
    Never use filenames with extensions.
    """

    content = [
        {
            "type": "text",
            "text": prompt
        }
    ]

    for p in image_paths:
        img = encode_image(p)

        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img}"
                }
            }
        )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
        max_tokens=1000
    )

    text = response.choices[0].message.content.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        return {"raw_response": text}
