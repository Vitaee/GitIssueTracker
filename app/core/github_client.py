import requests
from app.config import settings

class GitHubClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        print(settings.GITHUB_TOKEN)
        print(f"Bearer {settings.GITHUB_TOKEN}")
        self.headers = {"Authorization" : f"Bearer {settings.GITHUB_TOKEN}"}

    def get_repo(self, owner: str, repo: str):
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_issues(self, owner: str, repo: str):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {"state": "all"} 
        issues = []
        while url:
            response = self.session.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            issues.extend([{"number": i["number"], "title": i["title"]} for i in response.json()])
            
            if "next" in response.links:
                url = response.links["next"]["url"]
                params = None 
            else:
                url = None
        return issues

    def get_issue(self, owner: str, repo: str, issue_number: int):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()