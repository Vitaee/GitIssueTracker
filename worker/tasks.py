
import celery, os, sys
from celery import Celery
from app.core.github_client import GitHubClient
from app.crud import get_repos, update_last_checked_repo
from app.core.email_sender import send_email
from datetime import datetime, timezone
from app.db.session import SessionLocal
from app.config import settings
from sqlalchemy.orm import Session
from .async_task import async_task
from collections import defaultdict


celery_app = Celery('tasks', broker=settings.REDIS_URL)
celery_app.conf.enable_utc = True
celery_app.conf.timezone = "UTC"


@async_task(celery_app, bind=True)
async def check_github_issues(self: celery.Task):
    db: Session = SessionLocal()
    github_client = GitHubClient()

    try:
        repos = get_repos(db)

        repo_users = defaultdict(list)

        for repo in repos:
            for user in repo.users:
                repo_users[(repo.owner, repo.name)].append(user.email)

        for (owner, name), user_emails in repo_users.items():
            last_checked = min([r.last_checked for r in repos if r.owner == owner and r.name == name]) or datetime(1970, 1, 1)

            if last_checked.tzinfo is None:
                last_checked = last_checked.replace(tzinfo=timezone.utc)
            else:
                last_checked = last_checked.astimezone(timezone.utc)

            issues = github_client.get_issues(owner, name, True)
            
            updated_issues = []
            for issue in issues:
                issue_updated_at = datetime.strptime(issue['updated_at'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

                if issue_updated_at > last_checked:
                    updated_issues.append(issue)

            if updated_issues:
                issues_summary = "\n".join([f"Issue #{issue['number']}: {issue['title']}" for issue in updated_issues])

                for email in user_emails:
                    await send_email(
                        to_email=email,
                        subject=f"Update in {owner}/{name} - {len(updated_issues)} new or updated issues.",
                        body=f"The following issues have been updated:\n{issues_summary}"
                    )

            for repo in repos:
                if repo.owner == owner and repo.name == name:
                    update_last_checked_repo(db, repo.id, datetime.now(timezone.utc))

    finally:
        db.close()


@celery_app.task(ignore_result=True)
def say_hello(who: str = "Test"):
    print(f"Hello {who}")


schedule_sec = 45 # per 45 seconds

if os.getenv('ENV', 'development') == 'production': schedule_sec = 9999 # or 3600 for per hour

celery_app.conf.beat_schedule = {
    'check-github-issues-every-hour': {
        'task': 'worker.tasks.check_github_issues',
        'schedule': schedule_sec
    },
}
