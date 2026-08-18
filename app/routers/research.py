from fastapi import APIRouter

from app.schemas.research import ResearchBrief, ResearchRequest
from app.services.research import run_research

router = APIRouter(prefix="/research", tags=["research"])


@router.post("/companies/{company_id}", response_model=ResearchBrief)
def research_company(company_id: str, req: ResearchRequest) -> ResearchBrief:
    return run_research(company_id, req)
