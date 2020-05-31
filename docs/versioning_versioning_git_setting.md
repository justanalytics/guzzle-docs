---
id: versioning_versioning_git_setting
title: Guzzle – Versioning (Git Settings)
sidebar_label: Guzzle – Versioning (Git Settings)
---

## Guzzle – Git Settings

Guzzle supports GIT integration to enable code versioning which eventually also protects job definition from getting overwritten in case of concurrent development happening on the same Guzzle job in shared development environment.

- Enable GIT integration for Non-prod environment is must - so that all the changes done in the jobs are tracked automatically.
- It is recommended to follow gitflow as the GIT workflow (https://datasift.github.io/gitflow/IntroducingGitFlow.html)
- After GIT integration, create and lock the "collaboration" and "master" branches for your Guzzle jobs configurations.
- Developers can pull out from collaboration branch and create another branch where they can modify code and then submit those changes back to collaboration branch. 
- Before committing changes to collaboration branch, developer can also compare the changes between collaboration branch and tropical branch they have created for making code changes. They can also view the history of changes they have made in the code.