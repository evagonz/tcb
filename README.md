# Tech Chat Bot

A small Slackbot that accepts & stores gold stars and sends them to the tech chat host 1-2 hours before tech chat.

## Design

The TCB 'service' or 'applicaton' technically involves two separate Lambda functions with the same codebase: one to handle slack requests, the other to handle automated cloudwatch prompts, since you can't have one lambda with two handlers. The slack commands currently supported are:

* `/goldstar` -- to submit an anonymous gold star for tech chat
* `/tc-host` -- to find out who's hosting tech chat this week
* `/tc-host me` -- to sign up to host tech chat this week

Because reasons involving how Slack works and user IDs and whatnot, there's no way to sign someone else up to host right now.
Slack slash commands are configured [here](https://api.slack.com/apps/A010RH3LT89).

Goldstars and host information are saved to a DynamoDB table, structured like this:
*Date*:  # primary key; in YYYYMMDD format
  - Host:  # a map
      name: twinkie  # human-readable, for `/tc-host` queries 
      user_id: UH123456  # slack needs this to communicate back
  - Goldstars:  # a list
    - to twinkie for being a cute cat
    - to lori for staying home and saving lives
    - to $coworker for $workaccomplishment
    
On Fridays at noon (CST) or 1 p.m. (CDT), depending on where we are in relation to UTC, Cloudwatch will poke the lambda and send the gold stars for that week to the host.

## Development

TCB was built using the [Serverless](https://serverless.com/framework/docs/providers/aws/) framework, which is an npm thing. It has a single plugin (in `package.json`) that helps with building Python libraries when deploying (more on that [here](https://serverless.com/plugins/serverless-python-requirements/)).

`serverless.yml` defines the lambda, its triggers, and a DynamoDB table (the bottom handles raw Cloudformation).

If you've made changes to the code and want to deploy them, after you've [set up Serverless](https://serverless.com/framework/docs/providers/aws/guide/installation/) on your workstation, assume the `superuser` role in `secure` and `sls deploy`.

### Testing

doitlive.jpg

## Maintainer

Slack-side bot maintenance and this repo are both the resonsibility of the current [tech chat coordinator](https://civisanalytics.atlassian.net/wiki/spaces/TECH/pages/31555933/Tech+Team+Working+Groups+and+Other+Roles) or whatever you want to call them but absolutely don't hesitate to submit PRs for cool stuff.

## Future cool stuff ideas maybe

* doc activity counter
* fancy schmancy message formatting
* presentation sign-ups & 'hey sign up to present at tech chat there are roughly x minutes still' auto-messages to tech-internal
* dumping aforementioned presentations (and gold stars?) to...a doc or something


