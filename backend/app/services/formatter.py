from typing import List, Dict


def format_recommendations(recommendations: List[Dict]) -> str:
    formatted = []
    for rec in recommendations:
        followed_attendees = rec.get("followed_attendees", [])
        attendee_info = (
            f" Your connections {', '.join(followed_attendees)} are attending!"
            if followed_attendees
            else ""
        )
        formatted.append(
            f"Event: {rec['title']} - {rec['description']} (Location: {rec['location']}, Date: {rec['date']}, Attendees: {rec['attendees']}).{attendee_info}"
        )
    return "\n".join(formatted)
