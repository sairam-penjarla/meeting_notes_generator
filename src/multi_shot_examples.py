# Examples for each component
identify_participants_examples = [
    # Example 1
    {
        "role": "user",
        "content": "Transcript: The meeting started with an introduction by Alice, followed by a report from Bob, the operations manager. Charlie, the team lead, shared his feedback, and Dana concluded the session with her remarks.",
    },
    {
        "role": "assistant",
        "content": "- Alice\n- Bob (Operations Manager)\n- Charlie (Team Lead)\n- Dana",
    },
    # Example 2
    {
        "role": "user",
        "content": "Transcript: Participants included Dr. Emily White, CEO of HealthCorp, and John Doe, the lead researcher on the project.",
    },
    {
        "role": "assistant",
        "content": "- Dr. Emily White (CEO of HealthCorp)\n- John Doe (Lead Researcher)",
    },
]

write_summary_examples = [
    # Example 1
    {
        "role": "user",
        "content": "Transcript: The team reviewed the marketing budget and discussed increasing social media ad spend. Jane proposed allocating 20% more budget for Instagram ads. John supported the proposal, and the team agreed to revisit the results in two months.",
    },
    {
        "role": "assistant",
        "content": "- The meeting focused on the marketing budget.\n- Jane proposed increasing Instagram ad spend by 20%.\n- John supported the proposal.\n- The team agreed to evaluate the results in two months.",
    },
    # Example 2
    {
        "role": "user",
        "content": "Transcript: The development team discussed the upcoming product release timeline. Alex mentioned that testing would take two additional weeks, and Maria suggested delaying the launch to ensure quality.",
    },
    {
        "role": "assistant",
        "content": "- The team discussed the product release timeline.\n- Alex estimated two more weeks for testing.\n- Maria suggested delaying the launch to maintain quality.",
    },
]

write_notes_examples = [
    # Example 1
    {
        "role": "user",
        "content": "Transcript: During the meeting, Sarah highlighted a rise in website traffic. Mike suggested adding a feedback form to the homepage. John emphasized the need to monitor user behavior and generate a report by next week.",
    },
    {
        "role": "assistant",
        "content": "- Sarah reported an increase in website traffic.\n- Mike suggested adding a feedback form to the homepage.\n- John emphasized monitoring user behavior and requested a report by next week.",
    },
    # Example 2
    {
        "role": "user",
        "content": "Transcript: The team discussed hiring new developers. Jane proposed creating a job posting by the end of the day, while Bob recommended reviewing resumes within three days.",
    },
    {
        "role": "assistant",
        "content": "- Jane proposed creating a job posting by the end of the day.\n- Bob recommended reviewing resumes within three days.",
    },
]

write_action_items_examples = [
    # Example 1
    {
        "role": "user",
        "content": "Transcript: Sarah was tasked with preparing a presentation for the next client meeting. Mike agreed to review the draft and provide feedback by Friday. Alex was assigned to gather the necessary data for the presentation.",
    },
    {
        "role": "assistant",
        "content": "- Sarah: Prepare a presentation for the next client meeting.\n- Mike: Review Sarah's draft and provide feedback by Friday.\n- Alex: Gather necessary data for the presentation.",
    },
    # Example 2
    {
        "role": "user",
        "content": "Transcript: The team decided that Jane would schedule a meeting with the stakeholders. Bob would finalize the budget proposal, and Maria would prepare a project timeline by next week.",
    },
    {
        "role": "assistant",
        "content": "- Jane: Schedule a meeting with the stakeholders.\n- Bob: Finalize the budget proposal.\n- Maria: Prepare a project timeline by next week.",
    },
]

get_session_name_examples = [
    # Example 1
    {
        "role": "user",
        "content": "Transcript: The team discussed the quarterly financial report. Sarah presented the revenue analysis, while Mike suggested cost-cutting strategies. John emphasized the need for better expense tracking.",
    },
    {
        "role": "assistant",
        "content": "Quarterly Financial Review",
    },
    # Example 2
    {
        "role": "user",
        "content": "Transcript: The discussion focused on the new product launch. Jane shared updates on the design phase, Alex provided a development timeline, and Maria outlined the marketing campaign.",
    },
    {
        "role": "assistant",
        "content": "New Product Launch Strategy",
    },
    # Example 3
    {
        "role": "user",
        "content": "Transcript: The team planned the company's annual retreat. Locations were discussed, and Alex was assigned to coordinate logistics. Maria suggested including team-building activities.",
    },
    {
        "role": "assistant",
        "content": "Annual Retreat Planning",
    },
]

shorter_transcript_prompt_examples = [
    # Example 1
    {
        "role": "user",
        "content": "Transcript: Sarah: Here is the revenue analysis for the quarter. Mike: We should consider some cost-cutting strategies. John: We need to focus on better expense tracking.",
    },
    {
        "role": "assistant",
        "content": """Sarah: Here is the revenue analysis for the quarter.
Mike: We should consider some cost-cutting strategies.
John: We need to focus on better expense tracking.
""",
    },
    # Example 2
    {
        "role": "user",
        "content": "Transcript: Jane: The design phase is progressing well. Alex: Here is the development timeline. Maria: This is the outline for the marketing campaign.",
    },
    {
        "role": "assistant",
        "content": """Jane: The design phase is progressing well.
Alex: Here is the development timeline.
Maria: This is the outline for the marketing campaign.
""",
    },
    # Example 3
    {
        "role": "user",
        "content": "Transcript: Alex: I will coordinate the logistics. Maria: We should include team-building activities.",
    },
    {
        "role": "assistant",
        "content": """Alex: I will coordinate the logistics.
Maria: We should include team-building activities.
""",
    },
]

def get_examples(component):
    if component == "identify_participants":
        return identify_participants_examples
    elif component == "write_summary":
        return write_summary_examples
    elif component == "write_notes":
        return write_notes_examples
    elif component == "write_action_items":
        return write_action_items_examples
    elif component == "session_name":
        return get_session_name_examples
    elif component == "shorter_transcript_prompt":
        return shorter_transcript_prompt_examples
    else:
        return None

