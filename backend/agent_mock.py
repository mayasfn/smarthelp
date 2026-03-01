"""
Mock agent pour tester l'interface Streamlit sans dépendre d'OpenAI/Snowflake
"""

def run_agent_mock(user_message: str, ticket_id: str | None = None):
    """
    Simule les réponses de l'agent pour le testing
    """
    import uuid
    from datetime import datetime
    
    # Déterminer la priorité selon le message
    if any(word in user_message.lower() for word in ['urgent', 'critical', 'crash', 'down', 'broke']):
        priority = "URGENT"
    elif any(word in user_message.lower() for word in ['important', 'issue', 'problem', 'error']):
        priority = "HIGH"
    elif any(word in user_message.lower() for word in ['help', 'question', 'how']):
        priority = "MEDIUM"
    else:
        priority = "LOW"
    
    # Créer un ticket si c'est un nouveau problème
    if ticket_id is None:
        ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
    
    # Réponses mockées
    responses = {
        "login": "I understand you're having trouble logging into your account. This is a common issue. Could you please tell me:\n1. What error message are you seeing?\n2. Have you tried resetting your password?\n3. Are you using the correct email/username?\n\nI've created ticket {} for you. Priority: {}".format(ticket_id, priority),
        "password": "For password-related issues, I recommend:\n1. Click 'Forgot Password' on the login page\n2. Check your email (including spam folder) for the reset link\n3. If you don't receive the email, verify your email address is correct\n\nTicket {} has been updated. Priority: {}".format(ticket_id, priority),
        "payment": "Regarding payment issues, please note:\n1. We accept all major credit cards and PayPal\n2. Check if your card is expired or blocked\n3. Ensure your billing address matches your card details\n\nI'm escalating your ticket {} to our billing team. Priority: {}".format(ticket_id, priority),
        "default": "Thank you for contacting us. I understand your concern about: '{}'\n\nI've analyzed your request and created/updated ticket {}. Our team will get back to you shortly.\n\nPriority Level: {}\n\nWhat else can I help you with?".format(user_message, ticket_id, priority)
    }
    
    # Sélectionner la réponse appropriée
    user_lower = user_message.lower()
    if any(word in user_lower for word in ['login', 'sign in', 'account', 'password']):
        response = responses["login"]
    elif any(word in user_lower for word in ['password', 'reset', 'forgot']):
        response = responses["password"]
    elif any(word in user_lower for word in ['payment', 'billing', 'card', 'charge']):
        response = responses["payment"]
    else:
        response = responses["default"]
    
    return {
        "response": response,
        "ticket_id": ticket_id,
        "priority": priority,
        "timestamp": datetime.now().isoformat()
    }
