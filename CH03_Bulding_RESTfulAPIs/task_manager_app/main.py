from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

from fastapi.exceptions import HTTPException
from models import (
    Task,
    TaskWithID,
    TaskV2WithID
)
from operations import (
    read_all_tasks,
    read_all_tasks_v2,
    read_task,
    create_task,
    modify_task,
    remove_task
)

# VERSIONING
# Besides the URL-based approach that we used in the recipe, there are other common approaches to
# API versioning, such as the following:
# • Query parameter versioning: Version information is passed as a query parameter in the API
# request. For example, see the following:
# https://api.example.com/resource?version=1
# This method keeps the base URL uniform across versions.
# • Header versioning: The version is specified in a custom header of the HTTP request:
# GET /resource HTTP/1.1
# Host: api.example.com
# X-API-Version: 1
# This keeps the URL clean but requires clients to explicitly set the version in their requests.
# • Consumer-based versioning: This strategy allows customers to choose the version they need.
# The version available at their first interaction is saved with their details and used in all future
# interactions unless they make changes.

# Postman Blog API Versioning: https://www.postman.com/api-platform/
# api-versioning/

app = FastAPI()


@app.get("/tasks", response_model=list[TaskWithID])
def get_tasks(status: Optional[str] = None, title: Optional[str] = None):
    tasks = read_all_tasks()
    if status:
        tasks = [task for task in tasks if task.status == status]
    if title:
        tasks = [task for task in tasks if task.title == title]

    return tasks


@app.get("/v2/tasks", response_model=list[TaskV2WithID])
def get_tasks_v2():
    tasks = read_all_tasks_v2()
    return tasks


@app.get("/tasks/search", response_model=list[TaskWithID])
def search_tasks(keyword: str):
    tasks = read_all_tasks()
    filtered_tasks = [
        task for task in tasks
        if keyword.lower()
        in (task.title + task.description).lower()
    ]
    return filtered_tasks



@app.get("/task/{task_id}")
def get_task(task_id: int):
    task = read_task(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task Not Found"
        )

    return task


@app.post("/task", response_model=TaskWithID)
def add_task(task: Task):
    return create_task(task)


class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


@app.put("/task/{task_id}", response_model=TaskWithID)
def update_task(task_id: int, task_update: UpdateTask):
    modified = modify_task(
        task_id,
        task_update.model_dump(exclude_unset=True),
    )
    if not modified:
        raise HTTPException(
            status_code=404, detail="task not found"
        )

    return modified


@app.delete("/task/{task_id}", response_model=Task)
def delete_task(task_id: int):
    removed_task = remove_task(task_id)
    if not removed_task:
        raise HTTPException(
            status_code=404, detail="task not found"
        )
    return removed_task


from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from security import (
    UserInDB,
    fake_token_generator,
    fakely_hash_password,
    fake_users_db
)


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    print(user_dict)
    if not user_dict:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    user = UserInDB(**user_dict)
    hashed_password = fakely_hash_password(form_data.password)
    print(hashed_password, user.hashed_password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )

    token = fake_token_generator(user)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


from security import (
    get_user_from_token,
    User
)

@app.get("/users/me", response_model=User)
def read_users_me(current_user: User = Depends(get_user_from_token)):
    return current_user
