from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Idea, status_code=status.HTTP_201_CREATED)
async def post_idea(
    *,
    db: Session = Depends(deps.get_db),
    idea_in: schemas.IdeaCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    idea = crud.item.create_with_owner(db=db, obj_in=idea_in, owner_id=current_user.id)
    return idea


@router.delete("/{id}", status_code=status.HTTP_201_CREATED)
def delete_idea(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    idea = crud.item.get(db=db, id=id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    if idea.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.idea.remove(db=db, id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Idea)
def update_idea(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    idea_in: schemas.IdeaUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    idea = crud.idea.get(db=db, id=id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    if idea.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    idea = crud.idea.update(db=db, db_obj=idea, obj_in=idea_in)
    return idea


# get paginated list of ideas‚
@router.get("/", response_model=List[schemas.Idea])
def get_ideas(
    db: Session = Depends(deps.get_db),
    page: Optional[int] = 1,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve ideas.
    """
    ideas = crud.item.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=(page - 1) * 10, limit=10
    )
    return ideas
