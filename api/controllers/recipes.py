from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import recipes as model
from ..models import resources as resource_model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    # Verify all resources exist first
    resources = []
    for item in request.resources:
        resource = db.query(resource_model.Resource).filter(
            resource_model.Resource.id == item.resource_id
        ).first()
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource with id {item.resource_id} not found"
            )
        resources.append({"resource_id": item.resource_id, "amount": item.amount, "resource": resource})

    new_recipe = model.Recipe(
        sandwich_id=request.sandwich_id,
        is_vegetarian=request.is_vegetarian
    )

    try:
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        
        # Add resources to the recipe
        for item in resources:
            stmt = model.recipe_resource.insert().values(
                recipe_id=new_recipe.id,
                resource_id=item["resource_id"],
                amount=item["amount"]
            )
            db.execute(stmt)
        
        db.commit()
        # Manually construct the response with the proper structure
        return {
            "id": new_recipe.id,
            "sandwich_id": new_recipe.sandwich_id,
            "is_vegetarian": new_recipe.is_vegetarian,
            "resources": resources
        }
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}"
        )

def read_all(db: Session):
    try:
        recipes = db.query(model.Recipe).all()
        formatted_recipes = []
        
        for recipe in recipes:
            # Get all resources for this recipe
            recipe_resources = db.execute(
                model.recipe_resource.select().where(
                    model.recipe_resource.c.recipe_id == recipe.id
                )
            ).fetchall()
            
            resources = []
            for rr in recipe_resources:
                resource = db.query(resource_model.Resource).filter(
                    resource_model.Resource.id == rr.resource_id
                ).first()
                if resource:
                    resources.append({
                        "resource_id": rr.resource_id,
                        "amount": rr.amount,
                        "resource": resource
                    })
            
            formatted_recipes.append({
                "id": recipe.id,
                "sandwich_id": recipe.sandwich_id,
                "is_vegetarian": recipe.is_vegetarian,
                "resources": resources
            })
            
        return formatted_recipes
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def read_one(db: Session, recipe_id: int):
    try:
        recipe = db.query(model.Recipe).filter(model.Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
        
        # Get all resources for this recipe
        recipe_resources = db.execute(
            model.recipe_resource.select().where(
                model.recipe_resource.c.recipe_id == recipe.id
            )
        ).fetchall()
        
        resources = []
        for rr in recipe_resources:
            resource = db.query(resource_model.Resource).filter(
                resource_model.Resource.id == rr.resource_id
            ).first()
            if resource:
                resources.append({
                    "resource_id": rr.resource_id,
                    "amount": rr.amount,
                    "resource": resource
                })
        
        return {
            "id": recipe.id,
            "sandwich_id": recipe.sandwich_id,
            "is_vegetarian": recipe.is_vegetarian,
            "resources": resources
        }
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def update(db: Session, recipe_id: int, request):
    try:
        recipe = db.query(model.Recipe).filter(model.Recipe.id == recipe_id)
        if not recipe.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        
        update_data = request.dict(exclude_unset=True)
        recipe.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return recipe.first()

def delete(db: Session, recipe_id: int):
    try:
        # First delete all entries in recipe_resources for this recipe
        db.execute(
            model.recipe_resource.delete().where(
                model.recipe_resource.c.recipe_id == recipe_id
            )
        )
        
        # Then delete the recipe itself
        recipe = db.query(model.Recipe).filter(model.Recipe.id == recipe_id)
        if not recipe.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
        
        recipe.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)