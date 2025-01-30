identify_participants_prompt = """
### Task

You are tasked with identifying the participants in a conversation or meeting transcript. Your job is to extract and list all the participants mentioned in the given text.

### Guidelines

- Extract the names of all individuals or groups mentioned in the conversation.
- Ensure the list is complete and includes all parties involved.
- Format the list as bullet points, with each participant's name on a separate line.
- Include any titles or roles if provided in the transcript (e.g., "Dr. Smith", "CEO of XYZ").
- If unsure, you may infer participants based on context.
- Do not give any heading or title. Just bullet points.

### Example Transcript

*The meeting began with a brief introduction by John Doe, CEO of the company. Jane Smith, the project manager, then presented the quarterly report. Other participants included Alex Brown, the senior developer, and Maria Green, the marketing specialist.*

### Output Format

- John Doe
- Jane Smith
- Alex Brown
- Maria Green

"""


write_summary_prompt = """
### Task

You are tasked with writing a concise summary for a meeting or conversation transcript. The summary should capture the key points discussed, decisions made, and any action items assigned.

### Guidelines

- Focus on the most important information such as decisions, outcomes, or notable points discussed.
- Avoid including unnecessary details or filler.
- Write in a clear, professional tone, ensuring the summary is easy to read.
- Provide a clear and structured summary that can be quickly understood.
- Do not give any heading or title. Just bullet points.

### Example Transcript

*The team discussed the upcoming product launch and marketing strategy. John emphasized the need for a targeted email campaign, while Jane suggested creating a social media plan. The group agreed to focus on reaching a younger demographic and to have the marketing materials ready by next week.*

### Output Format

  - The meeting focused on the upcoming product launch.
  - John suggested a targeted email campaign.
  - Jane proposed creating a social media plan.
  - The team agreed to target a younger demographic and set a deadline for next week.

"""


write_notes_prompt = """
### Task

You are tasked with writing detailed notes from a meeting or conversation. These notes should capture all important details, including ideas, suggestions, and observations.

### Guidelines

- Provide a structured and organized format for the notes.
- Include any action items, deadlines, and key points mentioned.
- Ensure the notes are clear and can be used for future reference.
- Use bullet points or numbered lists to separate different ideas or discussion topics.
- Do not give any main heading like "Meeting Notes - 26 November 2024, 01:07pm" etc.

### Example Transcript

*During the meeting, the team discussed the quarterly sales report. Sarah mentioned that sales were down in the Northern region, while Mike suggested that a new marketing campaign could help improve numbers. John requested that Sarah send a detailed report on regional sales by the end of the week.*

### Output Format

  - Sarah reported a decline in sales in the Northern region.
  - Mike suggested launching a new marketing campaign.
  - John asked Sarah to send a detailed regional sales report by the end of the week.

"""


write_action_items_prompt = """
### Task

You are tasked with writing action items based on a meeting or conversation transcript. Action items should be clear, concise, and actionable.

### Guidelines

- Focus on tasks assigned to specific individuals or teams.
- Include deadlines or timeframes if mentioned in the transcript.
- Ensure each action item is actionable and includes the responsible party.
- Write in a professional and direct tone.
- Do not give any heading or title. Just bullet points.

### Example Transcript

*During the meeting, Jane assigned Alex the task of creating a prototype for the new website design. Sarah was tasked with researching user preferences for the mobile app, and Mike agreed to follow up with potential investors by next Tuesday.*

### Output Format

  - Alex: Create a prototype for the new website design.
  - Sarah: Research user preferences for the mobile app.
  - Mike: Follow up with potential investors by next Tuesday.

"""

session_name_prompt = """
### Task

You are tasked with generating a concise and meaningful session name based on a given meeting or conversation transcript. The session name should summarize the main topic or focus of the discussion in a few words.

### Guidelines

- Extract the core topic or purpose of the meeting.
- Keep the session name concise (ideally 3 to 6 words).
- Avoid generic names like "Meeting Notes" or "Discussion Summary."
- Ensure clarity so users can recognize the session's content at a glance.
- If no clear topic is present, generate a reasonable name based on context.

### Example Transcript

*The team discussed the upcoming product launch and marketing strategy. John emphasized the need for a targeted email campaign, while Jane suggested creating a social media plan. The group agreed to focus on reaching a younger demographic and to have the marketing materials ready by next week.*

### Output Format

Product Launch Strategy
"""

shorter_transcript_prompt = """
### Task

You are tasked with reducing the size of a given meeting or conversation transcript while preserving all key aspects of the conversation. Your response should be in the form of bullet points that capture the essence of the conversation.
Make sure that you reduce the transcript into half of it's length.

### Guidelines

- **Bullet Points**: Capture the key points discussed in the conversation.  
- Maintain clarity and conciseness while ensuring completeness.  
- Do not include unnecessary details or filler words.  
- No headings, titles, or subheadings.  
- Ensure the reduced transcript is accurate and free of errors.
- Make sure that you reduce the transcript into half of it's length.

### Example Transcript

*The team discussed the upcoming product launch and marketing strategy. John emphasized the need for a targeted email campaign, while Jane suggested creating a social media plan. The group agreed to focus on reaching a younger demographic and to have the marketing materials ready by next week.*

### Output Format

- Discussed product launch and marketing strategy.  
- John emphasized the need for a targeted email campaign.  
- Jane suggested creating a social media plan.  
- Agreed to focus on reaching a younger demographic.  
- Marketing materials to be ready by next week.  
"""


def get_prompt(component):
    if component == "identify_participants":
        instructions = identify_participants_prompt
    elif component == "write_summary":
        instructions = write_summary_prompt
    elif component == "write_notes":
        instructions = write_notes_prompt
    elif component == "write_action_items":
        instructions = write_action_items_prompt
    elif component == "session_name":
        instructions = session_name_prompt
    elif component == "shorter_transcript_prompt":
        instructions = shorter_transcript_prompt
    else:
        instructions = "Invalid component"
    
    return instructions
