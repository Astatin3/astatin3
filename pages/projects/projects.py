from threading import Thread
import src.utils as utils
from github import Github, Auth

max_commit_num = 10

class Repository:
  def __init__(self, repo, branch):
    self.repo = repo
    self.branch = branch
    self.commits = None

  def commit_html(self):
    commit_html = ""

    for i, commit in enumerate(self.commits):
      if i >= min(max_commit_num, self.commits.totalCount):
        return commit_html

      html = utils.open_page_file("projects", "update.html")
      html = html.replace("<!-- time -->", str(commit.commit.committer.date).split("+")[0])
      html = html.replace("<!-- description -->", commit.commit.message)

      commit_html += html

    return commit_html




  def html(self):
    html = utils.open_page_file("projects", "repo.html")
    html = html.replace("<!-- name -->", (self.repo.full_name + ", " + self.branch.name))
    html = html.replace("<!-- avatar-url -->", self.repo.owner.avatar_url)

    if self.repo.description is not None:
      html = html.replace("<!-- description -->", self.repo.description)

    if self.commits is not None:
      try:
        html = html.replace("<!-- updates -->", self.commit_html())
      except:
        pass

    return html

COMMIT_SVG = '<svg aria-hidden="true" focusable="false" role="img" class="Octicon-sc-9kayk9-0" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" style="display:inline-block;user-select:none;vertical-align:text-bottom;overflow:visible"><path d="M11.93 8.5a4.002 4.002 0 0 1-7.86 0H.75a.75.75 0 0 1 0-1.5h3.32a4.002 4.002 0 0 1 7.86 0h3.32a.75.75 0 0 1 0 1.5Zm-1.43-.75a2.5 2.5 0 1 0-5 0 2.5 2.5 0 0 0 5 0Z"></path></svg>'

auth = Auth.Token("<api key>")

g = Github(auth=auth)

scan_repos_list = []

scan_repos_list.append(g.get_user().get_repos())
scan_repos_list.append(g.get_organization("team4388").get_repos())

page_html = "<h1 class='dark:text-white'>Loading...</h1>"

def update_repos():
  repo_list_html = []

  for repo_list in scan_repos_list:
    for repo in repo_list:

      master_commits = None

      # print(repo.full_name)

      try:
        master_commits = repo.get_commits(author=g.get_user())
        if master_commits.totalCount == 0:
          continue
      except Exception as e:
        continue

      for branch in repo.get_branches():

        print(repo.full_name + ", " + branch.name)
        if branch.name == repo.default_branch:
          repository = Repository(repo, branch)
          repository.commits = master_commits

          repo_list_html.append(repository.html())
          continue

        commits = None

        try:
          commits = repo.get_commits(author=g.get_user())
          if commits.totalCount == 0:
            print("continue")
            continue
        except Exception as e:
          print(e)
          continue

        print(commits.totalCount-master_commits.totalCount)

        if commits.totalCount > master_commits.totalCount:
          repository = Repository(repo, branch)
          repository.commits = commits

          print(repository.html())

    # return utils.open_page_file("blocks", "blocks.html")
  global page_html
  page_html = utils.open_page_file("projects", "projects.html").replace("<!-- repos -->", ''.join(repo_list_html))

def get_html():
  return page_html

Thread(target=update_repos).start()