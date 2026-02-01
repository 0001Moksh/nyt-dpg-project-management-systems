from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import ChatSession, User
from app.schemas.schemas import ChatbotQuestion, ChatbotResponse
from groq import Groq
from app.core.config import settings

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])

# Initialize Groq client
client = Groq(api_key=settings.GROQ_API_KEY)

# FAQ knowledge base
FAQ_DATABASE = {
    "enrollment": [
        {
            "q": "How do I enroll in a project?",
            "a": "Click on 'Enroll Project' and use the enrollment link/token provided by your supervisor or admin."
        },
        {
            "q": "What is the enrollment token?",
            "a": "The enrollment token is a unique link that allows you to join a specific project. You'll receive this from your project supervisor."
        }
    ],
    "submission": [
        {
            "q": "What are the submission stages?",
            "a": "There are 4 submission stages: 1) Synopsis, 2) Progress Report 1, 3) Progress Report 2, 4) Final Submission"
        },
        {
            "q": "Can I submit without team approval?",
            "a": "No, all team members must approve before a submission is considered valid."
        },
        {
            "q": "What is the file size limit?",
            "a": f"The maximum file size is {settings.MAX_FILE_SIZE_MB} MB."
        }
    ],
    "team": [
        {
            "q": "How do I create a team?",
            "a": "As a student, go to your project dashboard and click 'Create Team'. Set a team name and invite members via email."
        },
        {
            "q": "Can I be in multiple teams?",
            "a": "No, each student can only be in one team per project."
        },
        {
            "q": "What happens if a team member rejects the invitation?",
            "a": "The team remains in PENDING status. You'll need all members to accept before the team becomes ACTIVE."
        }
    ],
    "scoring": [
        {
            "q": "How is the final score calculated?",
            "a": "Final Score = (Supervisor Scores Average) + (Admin Score). Max = 30 points"
        },
        {
            "q": "Who gives the supervisor score?",
            "a": "Your project supervisor will review each submission and provide a score (0-10)."
        },
        {
            "q": "Who gives the admin score?",
            "a": "The department admin provides the final admin score (0-20) after all submissions are reviewed."
        }
    ],
    "general": [
        {
            "q": "What is this system?",
            "a": "This is the DPG Project Management System - a platform for managing student projects, submissions, and evaluations."
        },
        {
            "q": "Who can I contact for help?",
            "a": "Contact your project supervisor or the department admin for assistance."
        },
        {
            "q": "What is the deadline?",
            "a": "Check your project dashboard for the specific deadline for your project."
        }
    ]
}

def get_faq_context() -> str:
    """Generate FAQ context for RAG"""
    context = "FAQ Database:\n\n"
    for category, items in FAQ_DATABASE.items():
        context += f"## {category.upper()}\n"
        for item in items:
            context += f"Q: {item['q']}\nA: {item['a']}\n\n"
    return context

@router.post("/ask", response_model=ChatbotResponse)
async def ask_chatbot(
    question: ChatbotQuestion,
    user_id: int,  # From JWT token
    db: Session = Depends(get_db)
):
    """
    RAG-based chatbot using Groq LLM and FAQ knowledge base
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Build context with FAQ
        faq_context = get_faq_context()
        role_specific = f"User Role: {user.role}\n"
        
        # System prompt
        system_prompt = f"""You are a helpful assistant for the DPG Project Management System. 
Your role is to help students, supervisors, and admins with questions about the system.

{role_specific}

{faq_context}

Based on the FAQ above and your knowledge, answer the user's question helpfully.
If the question is not related to the system, politely redirect them to the FAQ.
Keep answers concise and clear."""
        
        # Call Groq API
        message = client.messages.create(
            model=settings.GROQ_MODEL_NAME,
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": question.question
                }
            ]
        )
        
        answer = message.content[0].text
        
        # Save chat session
        chat_session = ChatSession(
            user_id=user_id,
            question=question.question,
            answer=answer
        )
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
        
        return ChatbotResponse(
            answer=answer,
            session_id=chat_session.id,
            created_at=chat_session.created_at
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chatbot request: {str(e)}"
        )

@router.get("/sessions")
async def get_chat_history(
    user_id: int,  # From JWT token
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get chat history for a user
    """
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == user_id
    ).order_by(ChatSession.created_at.desc()).limit(limit).all()
    
    return {
        "user_id": user_id,
        "sessions": [
            {
                "id": s.id,
                "question": s.question,
                "answer": s.answer,
                "created_at": s.created_at
            }
            for s in sessions
        ]
    }

@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: int,
    user_id: int,  # From JWT token
    db: Session = Depends(get_db)
):
    """
    Delete a chat session
    """
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    
    return {
        "status": "success",
        "message": "Chat session deleted"
    }
