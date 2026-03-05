import os
import uuid
from backend.db.snowflake_utils import get_session

class ZenRepository:

    def __init__(self):
        self.session = get_session()

    def create_ticket(self, user: str, subject: str, priority: str, type: str, queue: str) -> str:
        ticket_id = str(uuid.uuid4())

        self.session.sql("""
            INSERT INTO ZEN_TICKETS
            VALUES (?, ?, ?, ?, ?, ?, 'OPEN', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())
        """, params=[ticket_id, user, subject, priority, type, queue]).collect()

        return ticket_id

    def add_message(self, ticket_id: str, role: str, content: str):
        # role should be 'USER', 'AGENT_AI', or 'AGENT_HUMAN'
        self.session.sql("""
            INSERT INTO ZEN_MESSAGES
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP())
        """, params=[str(uuid.uuid4()), ticket_id, role, content]).collect()
        self.session.sql(
            "UPDATE ZEN_TICKETS SET UPDATED_AT = CURRENT_TIMESTAMP() WHERE TICKET_ID = ?",
            params=[ticket_id]
        ).collect()

    def get_all_tickets(self):
        query = """
            SELECT 
                TICKET_ID, 
                SUBJECT, 
                PRIORITY, 
                STATUS, 
                CREATED_AT,
                UPDATED_AT
            FROM ZEN_TICKETS 
            ORDER BY UPDATED_AT DESC
        """
        results = self.session.sql(query).collect()        
        return [row.as_dict() for row in results]

    def get_ticket_status(self, ticket_id: str):
        query = "SELECT STATUS, SUBJECT, PRIORITY FROM ZEN_TICKETS WHERE TICKET_ID = ?"
        result = self.session.sql(query, params=[ticket_id]).collect()
        return result[0].as_dict() if result else None

    def get_ticket_messages(self, ticket_id: str):
        query = """
            SELECT SENDER_ROLE, CONTENT 
            FROM ZEN_MESSAGES 
            WHERE TICKET_ID = ? 
            ORDER BY CREATED_AT ASC
        """
        results = self.session.sql(query, params=[ticket_id]).collect()
        messages = []
        for row in results:
            messages.append({
                "role": row['SENDER_ROLE'], # 'USER', 'AGENT_AI', or 'AGENT_HUMAN'
                "content": row['CONTENT']
            })
        return messages

    def close_ticket(self, ticket_id: str):
        """Updates ticket status to CLOSED and sets UPDATED_AT timestamp."""
        if not ticket_id:
            return
            
        self.session.sql("""
            UPDATE ZEN_TICKETS 
            SET STATUS = 'CLOSED', 
                UPDATED_AT = CURRENT_TIMESTAMP() 
            WHERE TICKET_ID = ?
        """, params=[ticket_id]).collect()