def generate_response_prompt(user_query, age_vaccines):
    if age_vaccines:
        vac_lines = "\n".join([f"- {v['vaccine']} ({v['disease']}) - {v['schedule']}" for v in age_vaccines])
        return f"""The user asked: "{user_query}"

Their child's age corresponds to these recommended vaccines:

{vac_lines}

Explain this in a friendly and parent-appropriate tone.
"""
    return f"""The user asked: "{user_query}"

No specific vaccine match found by age, provide a helpful general answer based on vaccine knowledge base.
"""
