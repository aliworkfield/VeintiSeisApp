from fastapi import APIRouter, Depends
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.models import Message, UserOld
import app.utils

router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/test-email", dependencies=[Depends(get_current_active_superuser)])
def test_email(current_user: CurrentUser, session: SessionDep) -> Message:
    """
    Test emails.
    """
    email_data = app.utils.generate_test_email(email_to=current_user.email)
    app.utils.send_email(
        email_to=current_user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")