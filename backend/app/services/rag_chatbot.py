import logging
from typing import List, Optional
from groq import Groq
from app.config import settings

logger = logging.getLogger(__name__)


class RAGChatbotService:
    """Service for RAG-based chatbot with Groq LLM"""

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL_NAME

    async def get_response(
        self,
        user_message: str,
        role: str,
        chat_history: List[dict] = None,
        relevant_context: Optional[str] = None,
    ) -> dict:
        """Get chatbot response using Groq LLM"""
        try:
            # Build system prompt based on role
            system_prompt = self._get_system_prompt(role)

            # Build messages
            messages = []

            if chat_history:
                for msg in chat_history:
                    messages.append({"role": msg["sender"], "content": msg["content"]})

            # Add context if provided
            if relevant_context:
                context_msg = f"Relevant Project Information:\n{relevant_context}\n\n"
                user_message = context_msg + user_message

            messages.append({"role": "user", "content": user_message})

            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system_prompt}] + messages,
                temperature=0.7,
                max_tokens=1024,
            )

            bot_response = response.choices[0].message.content

            return {
                "success": True,
                "response": bot_response,
                "tokens_used": response.usage.total_tokens,
            }

        except Exception as e:
            logger.error(f"Chatbot error: {str(e)}")
            return {
                "success": False,
                "response": "Sorry, I encountered an error. Please try again.",
                "error": str(e),
            }

    @staticmethod
    def _get_system_prompt(role: str) -> str:
        """Get system prompt based on user role"""
        base_prompt = """You are an AI assistant for the DPG Project Management System at DPG ITM College.
        You help users with project management, academic guidance, and system navigation.
        Always be helpful, professional, and provide clear guidance."""

        role_specific_prompts = {
            "STUDENT": """
            You are a helpful assistant for students in the DPG Project Management System.
            Help them with:
            - Understanding project requirements and deadlines
            - Team formation and collaboration tips
            - Submission guidelines and format requirements
            - General academic guidance
            - Troubleshooting and support
            """,
            "SUPERVISOR": """
            You are an assistant for project supervisors in the DPG PMS.
            Help them with:
            - Evaluation criteria and scoring guidelines
            - Project management best practices
            - Feedback writing and communication
            - Handling submissions and reviews
            - Analytics and performance insights
            """,
            "ADMIN": """
            You are an assistant for administrators in the DPG PMS.
            Help them with:
            - Project setup and configuration
            - Team and enrollment management
            - User management and access control
            - System monitoring and analytics
            - Reporting and documentation
            """,
        }

        prompt = base_prompt + (role_specific_prompts.get(role, "") or "")
        return prompt.strip()

    async def answer_faq(self, question: str, role: str) -> dict:
        """Answer frequently asked questions"""
        faqs = {
            "STUDENT": {
                "How do I form a team?": "To form a team, log in to your dashboard, navigate to your project, and select team members from the available list. All members must approve before the team is locked.",
                "What are the submission deadlines?": "Check your project dashboard for specific deadlines. There are 4 stages: Synopsis, Progress 1, Progress 2, and Final Submission.",
                "How is my project scored?": "Your project is scored out of 30: Supervisor average (out of 10) + Admin score (out of 20).",
            },
            "SUPERVISOR": {
                "How do I score submissions?": "Review the submission documents and provide a score out of 10 along with detailed feedback.",
                "What should I focus on during evaluation?": "Evaluate based on the submission requirements, code quality, documentation, and presentation.",
                "How can I communicate with teams?": "Use the notification system and in-app messaging to communicate with teams.",
            },
            "ADMIN": {
                "How do I create a project?": "Click 'Create Project', fill in project details, select branch/batch, assign supervisor, and generate enrollment link.",
                "How do I manage users?": "Use the Users section to manage roles, permissions, and access control.",
                "How do I view analytics?": "The Analytics dashboard shows project progress, completion rates, and performance metrics.",
            },
        }

        answer = faqs.get(role, {}).get(question, None)

        if answer:
            return {"success": True, "answer": answer, "type": "FAQ"}
        else:
            # If not in FAQ, use LLM
            return await self.get_response(question, role)


# Singleton instance
rag_chatbot = RAGChatbotService()
