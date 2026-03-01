import uuid
from datetime import datetime
from backend.db.snowflake_utils import get_session

class ZenRepository:

    def __init__(self):
        self.session = get_session()

    def create_ticket(self, subject: str, priority: str) -> str:
        ticket_id = str(uuid.uuid4())

        self.session.sql("""
            INSERT INTO ZEN_TICKETS
            VALUES (?, ?, ?, 'OPEN', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())
        """, params=[ticket_id, subject, priority]).collect()

        return ticket_id

    def add_message(self, ticket_id: str, role: str, content: str):
        self.session.sql("""
            INSERT INTO ZEN_MESSAGES
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP())
        """, params=[
            str(uuid.uuid4()),
            ticket_id,
            role,
            content
        ]).collect()

    def get_all_tickets(self):
        query = """
            SELECT 
                TICKET_ID, 
                SUBJECT, 
                PRIORITY, 
                STATUS, 
                CREATED_AT 
            FROM ZEN_TICKETS 
            ORDER BY CREATED_AT DESC
        """
        results = self.session.sql(query).collect()        
        return [row.as_dict() for row in results]
