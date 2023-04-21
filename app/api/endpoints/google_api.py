from typing import List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.crud.charity_project import charity_crud
from app.services.google_api import (
    spreadsheets_create, set_user_permissions, spreadsheets_update_value
)
from app.schemas.charity_project import CharityDB


router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityDB],
    response_model_exclude_none=True
)
async def get_all_invested(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await charity_crud.get_projects_by_completion_rate(session)
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(
        spreadsheet_id, projects, wrapper_services
    )
    return projects
    # return f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
