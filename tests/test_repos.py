import sys,os
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tests.repos import create_random_repo_for_user




def test_track_repo(test_client, db: Session, user_token_headers: tuple) -> None:
    data = {"name": "ApexiveDjangoTask", "owner": "Vitaee"} # used real github repo
    user, headers = user_token_headers
    response = test_client.post(
        f"/repos/track", headers=headers, json=data,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["owner"] == data["owner"]
    assert "id" in content


def test_untrack_repo(test_client, db: Session, user_token_headers: tuple) -> None:
    user, headers = user_token_headers

    repo = create_random_repo_for_user(db, user) 

    response = test_client.delete(
        f"/repos/untrack/{repo.id}", headers=headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == repo.id

def test_read_tracked_repos(test_client, db: Session, user_token_headers: tuple) -> None:
    user, headers = user_token_headers
    repo = create_random_repo_for_user(db, user)  
    response = test_client.get(f"/repos/tracked", headers=headers)
    assert response.status_code == 200
    content = response.json()
    assert len(content) > 0
    assert any(r["id"] == repo.id for r in content["data"])

def test_get_repo_issues_wrong_token(test_client, db: Session, user_token_headers: tuple) -> None:
    user, headers = user_token_headers
    repo = create_random_repo_for_user(db, user) 
    response = test_client.get(
        f"/repos/{repo.id}/issues", headers=headers,
    )
    assert response.status_code == 500
    #content = response.json()
    #assert isinstance(content["data"], list)