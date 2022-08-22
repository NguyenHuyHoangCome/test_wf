![Build msa-front docker image](https://github.com/openmsa/msa-docker/workflows/Build%20msa-front%20docker%20image/badge.svg)
![Update Docker Image Tag](https://github.com/openmsa/msa-docker/workflows/Update%20Docker%20Image%20Tag/badge.svg)

# Create PR and release process for MSA-DOCKER project
## Main branches
* `master`: Main development branch
* `stable`: Release branch - only changes (mainly bug fixes)
* `next`: Features that are meant for a future release, not in development

## Branches map
Each project create a PR on msa-docker based on the branch they belong. Each
project/repo has a github action worflow to make this map (this need to be
configured on each project/repo).

* branch starting with `next_release/` => `next` => 2.7.0GA
* project develop branch => `master` => 2.6.1
* branch starting with `release/` => `stable` => 2.6.0GA

## Delivering changes
### Master (current development)
Commit/Merge changes to project-development branch, new PR will be created with
`master` as a target.

### Stable (release stabilization)
Commit/Merge changes to `release/` branch, PR will be created with `stable`
as a target

**Changes done on for `release/` also need to be done on the development
branch**

### Next (future development)
Commit/Merge changes to `next_release/` branch, new PR will be created with
`next` as a target

**Keep merging development branch into `next_release/` branch this will help to reduce
conflicts when this branch merge into development**

## Freeze Code / Cut Release
Whenever we reach the Freeze Code date. There is a rotation of meaning for
branches those branches.

* `master` branch will be moved to `stable`
* `next` branch will be moved to `master`
    * `next` branch will wait until new features for future release start to be
        developing

**All PRs can be manually merged after they pass the e2e tests**
**If there is more then one PR for the same project, consider merging the
latest one that have passed and just close the other ones**


# How to run msa-docker

`docker-compose.yml` is responsible for downloading and managing all the
images.

## Single mode
- if you have `bash` just run `./run_msa`
  - `./run_msa -h` to see all the options

### Update images

Download the new version of `docker-compose.yml` file (or just `git pull`) and
rerun the script

### Using a script
- if you have `bash` just run `./run_msa`
  - `./run_msa -h` to see all the options

### With no script
- if no `bash` run `docker-compose up -p dev-msa --build -d`
- if you want to run a lightweight version of the MSA which we use for e2e tests, run `docker-compose -f docker-compose.e2e.yml up --remove-orphans --build -d`

## HA mode
- to enable Docker Swarm: `docker swarm init`

### Using a script
- if you have `bash` just run `./ha_run_msa`
  - `./ha_run_msa -h` to see all the options

### With no script
 - `docker stack deploy --with-registry-auth -c docker-compose.ha.yml devmsa`


### Update images
Download the new version of `docker-compose.yml` file (or just `git pull`) and
rerun the script

# Submitting PR when there are msa2-front changes
Front image (msa2-front) is created by msa-docker, because of that, when generating a PR,
msa2-front is not created yet, so we need to create it manually for the PR:
## Changes only on msa2-front

- `cd front/` ... edit edit edit ... commit
- `docker build -t ubiqube/msa2-front:$(git rev-parse HEAD) .`
- `cd ../`
- `./update_tag ubiqube/msa2-front $(git rev-parse HEAD)`
- `docker push ubiqube/msa2-front:$(git rev-parse HEAD)`
- commit 'Update front tag'
- push branch, create a PR

## PR that depends on front change
In this case PR exists already and probably failed because changes on front is
needed:

- Checkout the PR branch
- `cd front/` ... edit edit edit ... commit
- `docker build -t ubiqube/msa2-front:$(git rev-parse HEAD) .`
- `cd ../`
- `./update_tag ubiqube/msa2-front $(git rev-parse HEAD)`
- `docker push ubiqube/msa2-front:$(git rev-parse HEAD)`
- commit 'Update front tag'
- push branch and your PR should probably pass now

# Running the end to end tests (only for Single mode)

These tests are meant to provide a baseline sanity check to confirm the components are working together as expected. It is most important
that they execute in a short set amount of time to ensure quick consistent integration. More exhaustive testing should happen elsewhere
and should not block merging.

The tests use [Cypress](https://www.cypress.io/). It is a lightweight Javascript based runner that runs in the same browser instance as the application.
This allows the tests to run with little latency which helps with speed and reliability. The requirements for the tests are:

- [Node JS](https://nodejs.org/en/)
- [Yarn](https://yarnpkg.com/getting-started/install)

Before you run the tests you will have to launch an instance of the MSA with test data:

- `docker stop $(docker ps -q)` - Stop all docker containers
- `docker ps` - List any containers still running, kill them if they exist.
- `./run_msa -k && ./run_msa -e`- Kill all containers running and starts e2e containers
- `/e2e/base_data/load_data.sh` - Pull in test data for e2e tests

To run the tests:

- `cd e2e`
- `yarn install`
- `yarn cypress:run`

This will run all the tests suites. To view them interactively you can run:

- `yarn cypress:open`
