
## Contributor's guide

### Setting up workspace of a contributor

1. Ensure you have the latest version of Node (https://nodejs.org/en/download/) installed. We also recommend you install Yarn (https://yarnpkg.com/en/docs/install) as well. You have to be on Node >= 8.x and Yarn >= 1.5.
1. Clone guzzle-docs repository from github https://github.com/justanalytics/guzzle-docs
1. checkout the "master" branch of that repository (git checkout master)
1. `cd website`
1. `npm install`
1. `yarn start` (or npm start)


### Workflow of contributing a specific change in documentation

1. Contributor forks a branch from the master branch `git checkout -b <new_branch_name>`
1. Makes changes to existing markdown file(s) and/or adds new markdown files and tests them by running the documentation site locally using `yarn start`.
1. Commits the changes to the branch, pushes the branch and creates a pull-request to merge that branch into the `master` branch.


### Adding a new page

1. Create the new markdown file that you want to add under /docs/ folder. 
1. It is advisable to follow some naming convention to manage growing number of markdown files immediately under /docs/ folder. One way to keep the files manageable is by prefixing the file names with it's top-level sidebar menu item. For example, all pages that belong to "Guzzle Fundamentals" could be prefixed with *fundamentals_* fundamentals_<sub_topic>.md
1. In the newly created md file, define a unique "id" which should be unique among all documentation pages. It could use similar convention as the filename. Id doesn't allow spaces. Choose appropriate label that will appear in the sidebar for this page.
1. Next thing to do is actually put this newly created md page under an appropriate top-level sidebar menu. For this, update the /website/sidebars.json file and add the *id* of the page to the list of the top-level item.


## Publishing 

### Publisher's environment setup

* The publisher (i.e. persons who should be allowed to publish changes to the documentation site), needs to do all the setup that is needed for Contributor's role.

* Additionally, the publisher should be allowed to push to the `master` branch of the repository.

* The publisher sets environment variable GIT_USER and sets it to his GitHub ID (not email address but just alphanumeric github ID).

* The Publisher reviews the pull-request and merges to `master` branch.

* Publisher updates his own local repository by doing a `git pull` and gets master branch which should have recently merged pull-requests which were accepted by the publisher.

* If the publisher himself is a contributor and wants to contribute a change, he may directly work on the master branch, commit and push the changes to the master branch. All steps related to creating a branch, raising a pull-request and merging pull request can be skipped. 


### Publishing from master branch

Publishing the current version of code in the `master` branch to the live documentation website. 


* Go to the guzzle-docs/website folder on the command prompt / terminal. 

* Execute the following command (assuming you have already set GIT_USER environment variable)

`cmd /C "set CURRENT_BRANCH=master && set USE_SSH=true && yarn run publish-gh-pages"`

Linux users can publish using the following command

`CURRENT_BRANCH=master USE_SSH=true yarn run publish-gh-pages`

The latest version of the website should be published within around a minute to the live website.


## Documentation Versioning

Documentation for different versions of Guzzle can be maintained.

Mainly, there would be following versions of the documentation (and also of the underlying product - Guzzle).

1. Next release where active development is in progress but not yet released
    * maintained under docs/ sub folder
2. Latest Stable Release
    * Documents maintained under `website/versioned_docs/version-{release_number}` folder
    * Sidebar for that version is maintained under `website/versioned_sidebars/version-{release_number}` folder
3. Past releases
    * Documents maintained under `website/versioned_docs/version-{release_number}` folder
    * Sidebar for that version is maintained under `website/versioned_sidebars/version-{release_number}` folder
    
### Creating a new release of documentation

* At the very beginning, when no stable releases of the documentation are done, there is only "next release" which is under development but not yet released. It is maintained under the 'docs' subfolder as mentioned earlier.
* The publisher wants to cut a new release from the current unreleased version, he runs the command `yarn run version 1.0.0` from the `website` subfolder. This creates a new release called 1.0.0 and new versioned release folders are created at `website/versioned_docs/version-1.0.0` and `website/versioned_sidebars/version-1.0.0`. This newly cut release now becomes the latest release or the stable release.
* At any point, contributor/publisher can edit any version's documents or sidebar configuration and publish the documentation using the normal process of publishing.



