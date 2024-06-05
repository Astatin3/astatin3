import time
import numpy as np
from threading import Thread
import src.utils as utils
from github import Github, Auth

auth = Auth.Token(utils.open_file("api_key.txt"))
g = Github(auth=auth)
user = g.get_user()




scan_repos = {
  'users': [
    # 'Astatin3'
  ],
  'orgs': [
    # 'team4388'
  ],
  'additional_repos': [
    # g.get_organization("team4388").get_repo("ScoutingApp2024"),
    # g.get_organization("team4388").get_repo("ScoutingApp2025"),
    g.get_organization("team4388").get_repo("autoPlanner2025")
  ]
}

max_commit_num = 6





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
        html = utils.open_page_file("activity", "additional_commit.html")
        html = html.replace("<!-- href -->", f'{self.repo.html_url}/commits/{self.branch}')
        html = html.replace("<!-- text -->", f'{len(self.commits) - max_commit_num} more commits')
        commit_html += html

        return commit_html

      html = utils.open_page_file("activity", "commit.html")
      html = html.replace("<!-- time -->", commit.commit.committer.date.strftime('%s'))
      html = html.replace("<!-- href -->", str(commit.commit.html_url))
      html = html.replace("<!-- description -->", commit.commit.message)

      commit_html += html

    return commit_html


  def html(self):
    html = utils.open_page_file("activity", "repo.html")
    html = html.replace("<!-- name -->", self.repo.full_name)
    html = html.replace("<!-- branch -->", self.branch)
    html = html.replace("<!-- href -->", f'{self.repo.html_url}/tree/{self.branch}')
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

def un_pageinate(list):
  return_elems = []
  for elem in list:
    return_elems.append(elem)
  return return_elems

def unique_commits(master_commits, branch_commits):
  sha_list = []
  for commit in master_commits:
    sha_list.append(commit.sha)
  commit_list = []
  for commit in branch_commits:
    if commit.sha not in sha_list:
      commit_list.append(commit)
  return commit_list

def commits_time(commits):
  if len(commits) >= 0:
    return int(commits[0].commit.committer.date.strftime('%s'))
  return 0


def update_repos():

  repos_list = scan_repos['additional_repos']

  for scan_user in scan_repos['users']:
    repos_list += un_pageinate(g.get_user(scan_user).get_repos())

  for scan_org in scan_repos['orgs']:
    repos_list += un_pageinate(g.get_organization(scan_org).get_repos())

  print(f"Scanning {len(repos_list)} repositories...")

  repo_list_html = []
  time_arr = []

  for i, repo in enumerate(repos_list):
    print(f"Scanning repo {i+1}/{len(repos_list)}.")

    total_commits = 0

    try:
      master_commits = un_pageinate(repo.get_commits(author=user))
      total_commits += len(master_commits)
    except Exception as e:
      continue


    repository = Repository(repo, repo.default_branch)
    repository.commits = master_commits
    html = repository.html()

    if total_commits > 0:
      time_arr.append(commits_time(master_commits))
      repo_list_html.append(html)


    for branch in repo.get_branches():

      if branch.name == repo.default_branch:
        continue

      try:
        commits = branch_commits(branch.commit)
        total_commits += len(commits)
        unique = unique_commits(master_commits, commits)

        if len(unique) > 0:
          repository = Repository(repo, branch.name)
          repository.commits = unique

          time_arr.append(commits_time(unique))

          repo_list_html.append(repository.html())
      except Exception as e:
        print(e)
        continue

  global page_html
  timeinds = np.array(time_arr).argsort()
  np_list_html = np.array(repo_list_html)
  page_html = utils.open_page_file("activity", "activity.html").replace("<!-- repos -->", ''.join(np_list_html[timeinds[::-1]]))

def update_repos_loop():
  while True:
    update_repos()
    time.sleep(60 * 60) # One hour

def get_html(path):
  return page_html, False

def init():
  Thread(target=update_repos_loop).start()