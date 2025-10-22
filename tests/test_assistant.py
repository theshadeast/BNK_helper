from school_it_assistant import SupportAssistant


def test_available_topics_not_empty():
    assistant = SupportAssistant()
    topics = assistant.available_topics()
    assert topics, "expected at least one topic"


def test_printer_response_contains_greeting_and_steps():
    assistant = SupportAssistant()
    response = assistant.respond("printer_connection")
    lines = response.splitlines()
    assert lines[0] == "Здравствуйте!"
    # Ensure numbering for the first few steps
    numbered = [line for line in lines if line.startswith("1.") or line.startswith("2.")]
    assert numbered, "expected numbered steps in the response"


def test_command_rendered_as_code_block():
    assistant = SupportAssistant()
    response = assistant.respond("wifi")
    assert "```" in response
    assert "netsh wlan show interfaces" in response


def test_unknown_topic_requests_details():
    assistant = SupportAssistant()
    response = assistant.respond("unknown_topic")
    assert "Уточните, пожалуйста" in response


def test_details_prompt_for_tech_request():
    assistant = SupportAssistant()
    response = assistant.respond("tech_request")
    assert "Опишите, пожалуйста" in response
