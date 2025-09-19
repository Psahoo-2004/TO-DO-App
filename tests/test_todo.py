from typing import List
from app import schemas
import pytest

def test_all_tasks(authorized_client,test_tasks):
    res = authorized_client.get("/todo/")
    def validate(task):
        return schemas.ToDoOut(**task)
    task_map=map(validate,res.json())
    tasks_list=list(task_map)
    # assert len(res.json()) == len(test_tasks)
    assert res.status_code == 200

def test_unauthorized_user_get_all_tasks(client,test_tasks):
    res=client.get("/todo/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_tasks(client,test_tasks):
    res=client.get(f"/todo/{test_tasks[0].id}")
    assert res.status_code == 401

def test_get_one_tasks_not_exits(authorized_client,test_tasks):
    res=authorized_client.get(f"/todo/88888")
    assert res.status_code == 404

def test_get_one_posts(authorized_client,test_tasks):
    res=authorized_client.get(f"/todo/{test_tasks[0].id}")
    task =schemas.ToDoOut(**res.json())
    # print(post)
    assert res.status_code == 200
    assert task.id == test_tasks[0].id
    assert task.title == test_tasks[0].title

@pytest.mark.parametrize("title, completed",[
    ("Task 1",True),
    ("Task 2",True),
    ("Task 3",False),
    ("Task 4",False)
])
def test_create_post(authorized_client,test_user,test_tasks,title,completed):
    res=authorized_client.post("/todo/",json={"title":title,"completed":completed})
    create_task=schemas.ToDo(**res.json())
    assert res.status_code == 200
    assert create_task.title == title
    assert create_task.completed == completed


def test_unauthorized_user_create_task(client,test_user,test_tasks):
    res=client.post("/todo/",json={"title":"arbritary title","content":"arbritary content"})
    assert res.status_code == 401

def test_unauthorized_user_delete_tasks(client,test_user,test_tasks):
    res=client.delete(f"/todo/{test_tasks[0].id}")
    assert res.status_code == 401

def test_delete_task_success(authorized_client,test_user,test_tasks):
    res=authorized_client.delete(f"/todo/{test_tasks[0].id}")
    assert res.status_code == 200

def test_delete_task_non_exist(authorized_client,test_user,test_tasks):
    res=authorized_client.delete(f"/todo/8888")
    assert res.status_code == 404

def test_delete_other_user_task(authorized_client,test_tasks,test_user):
    res=authorized_client.delete(f"/todo/{test_tasks[3].id}")
    assert res.status_code == 403

def test_update_tasks(authorized_client,test_user,test_tasks):
    data={
        "completed":True,
        "id":test_tasks[0].id
    }
    res=authorized_client.put(f"/todo/{test_tasks[0].id}",json=data)
    updated_post=schemas.ToDo(**res.json())
    assert res.status_code == 200

def test_update_other_user_task(authorized_client,test_user,test_user2,test_tasks):
    data={
        "completed":True,
        "id":test_tasks[3].id
    }
    res=authorized_client.put(f"/todo/{test_tasks[3].id}",json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_tasks(client,test_tasks,test_user):
    res=client.put(f"/todo/{test_tasks[0].id}")
    assert res.status_code == 401

def test_update_task_non_exist(authorized_client,test_user,test_tasks):
    data={
        "completed":True,
        "id":test_tasks[3].id
    }
    res=authorized_client.put(f"/posts/8888",json=data)
    assert res.status_code == 404