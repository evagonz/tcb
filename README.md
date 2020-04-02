# Tech Chat Bot

A small Slackbot that accepts & stores gold stars and sends them to the tech chat host 1-2 hours before tech chat.

## Development

TCB was built using the [Serverless](https://serverless.com/framework/docs/providers/aws/) framework, which is an npm thing. It has a single plugin (in `package.json`) that helps with building Python libraries when deploying (more on that [here](https://serverless.com/plugins/serverless-python-requirements/)).

`serverless.yml` defines the lambda, its triggers, and a DynamoDB table (the bottom handles raw Cloudformation). It's triggered mainly by the Slack slash commands `/tc-host` and `/goldstar`, but on Fridays a Cloudwatch Event (aka a cronjob) pokes it so it'll send the gold stars for the week to the current host. Slackbot-side configuration is done [here](https://api.slack.com/apps/A010RH3LT89).

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


