# A git-based development model

Version 1.0-rc.1

Git/Github have become the standard source code development tools, that allow
teams of people to construct complex projects, run continuous intergration for
testing, produce software releases, and maintain them. However, just like any
tool, it needs personalization and customization to satisfy different project
requirements.

One of the most popular development models is Vincent Driessen's [git-flow
model](https://nvie.com/posts/a-successful-git-branching-model/). It is
suitable for large projects with periodic releases. The drawbacks are:
- it is fairly heavy for applications that are in early stages and need more 
  nimble deployment;
- does not integrate particularly well with Github -- one would have to   
  manually synchronize with the main repository, open PRs, etc.;
- and uses the master branch as the production branch, which is typically not 
  playing well with different CI tools.

Ultimately, git-flow is just git + a set of conventions that can be customized, 
and thus is our favorite model with some customization:
- to allow rapid development, we use 'master' as the development branch. This
  enables an easy Github workflow and rapid deployment when needed.
- we use 'production' in place of the git-flow 'master' branch. We thus have a
  branch that is always ready to be released and referred to as the ground
  truth.

## Workflow Setup
Install git-flow:
```
brew install git-flow
```
and customize it:
```
git config --global gitflow.branch.master production
git config --global gitflow.branch.develop master
git config --global gitflow.prefix.versiontag v
git config --global gitflow.prefix.hotfix "fix-"
```
Follow git-flow's process, and:
- feature branches: pull and rebase on master as often as possible;
- Avoid merge commits as much as possible, as they polute the log history;
- push your changes to Github as often as possible: enable collaboration
and serves as a backup;
- open pull requests against master;
- delete remote branches when merged.

## Committing
Commit messages are important. They foster understanding and collaboration,
and when used appropriately, allow the automation of software management:
- automatically closing and referring to issues;
- generation of release notes;
See [How to write a good commit message](https://chris.beams.io/posts/git-commit/)
blog post for good advice on structuring commit messages.

## Automation
### Git hook to automatically tag commits
TBA

### Git hook to automatically run linter
TBA

### Release notes
TBD

## References
- [Pro Git](https://git-scm.com/book/en/v2) book
- Vincent Driessen's [git-flow model](https://nvie.com/posts/a-successful-git-branching-model/)
- Github's [workflow](http://scottchacon.com/2011/08/31/github-flow.html)
- Gitlab's [workflow](https://about.gitlab.com/blog/2014/09/29/gitlab-flow/)
- HubFlow [workflow](https://datasift.github.io/gitflow/TheHubFlowTools.html)
- [How to write a good commit message](https://chris.beams.io/posts/git-commit/)