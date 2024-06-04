import time
from threading import Thread
import src.utils as utils
from github import Github, Auth

max_commit_num = 10

auth = Auth.Token("")

g = Github(auth=auth)
user = g.get_user()

scan_repos_list = []

scan_repos_list.append(user.get_repos())
scan_repos_list.append(g.get_organization("team4388").get_repos())

page_html = "<h1 class='dark:text-white'>Loading...</h1>"

class Repository:
  def __init__(self, repo, branch):
    self.repo = repo
    self.branch = branch
    self.commits = None

  def commit_html(self):
    commit_html = ""

    for i, commit in enumerate(self.commits):
      if i >= min(max_commit_num, len(self.commits)):
        return commit_html

      html = utils.open_page_file("projects", "update.html")
      html = html.replace("<!-- time -->", str(commit.commit.committer.date).split("+")[0])
      html = html.replace("<!-- description -->", commit.commit.message)

      commit_html += html

    return commit_html



  def html(self):
    html = utils.open_page_file("projects", "repo.html")
    html = html.replace("<!-- name -->", (self.repo.full_name + ", " + self.branch))
    html = html.replace("<!-- avatar-url -->", self.repo.owner.avatar_url)

    if self.repo.description is not None:
      html = html.replace("<!-- description -->", self.repo.description)

    if self.commits is not None:
      try:
        html = html.replace("<!-- updates -->", self.commit_html())
      except Exception as e:
        print(e)

    return html

def branch_commits(current_commit):
  commits = []

  # get commit info
  while True:
    if len(current_commit.parents) == 1:
      # print(current_commit.committer.login )
      if current_commit.committer.login == user.login:
        commits.append(current_commit)
      current_commit = current_commit.parents[0]
    else:
      return commits

def parse_commits(commit_list):
  commits = []
  for commit in commit_list:
    commits.append(commit)
  return commits

def unique_commits(master_commits, branch_commits):
  msg_list = []
  for commit in master_commits:
    msg_list.append(commit.sha)
  return msg_list


def update_repos():
  repo_list_html = []

  # for repo_list in scan_repos_list:
  #   for repo in repo_list:

  repo = g.get_organization("team4388").get_repo("scoutingapp2024")
  print(repo)

  total_commits = 0

  try:
    master_commits = parse_commits(repo.get_commits(author=user))
    total_commits += len(master_commits)
  except Exception as e:
    return #continue


  repository = Repository(repo, repo.default_branch)
  repository.commits = master_commits
  html = repository.html()

  if total_commits > 0:
    repo_list_html.append(html)


  for branch in repo.get_branches():

    print(repo.full_name + ", " + branch.name)
    if branch.name == repo.default_branch:
      continue

    try:
      commits = branch_commits(branch.commit)
      total_commits += len(commits)

      print(unique_commits(master_commits, commits))
      print(len(commits) - len(master_commits), len(commits), len(master_commits))

      if len(commits) >= len(master_commits):
        repository = Repository(repo, branch.name)
        repository.commits = commits

        repo_list_html.append(repository.html())
    except Exception as e:
      print(e)
      continue

    # return utils.open_page_file("blocks", "blocks.html")

  # if total_commits > 0:
  global page_html
  print(total_commits)
  page_html = utils.open_page_file("projects", "projects.html").replace("<!-- repos -->", ''.join(repo_list_html))

def get_html():
  return page_html

Thread(target=update_repos).start()