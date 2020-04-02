import boto3
import hmac
import slack

def validate_request(req):
    """Validate slack request to prevent the hax."""
    slack_signing_secret = boto3.client('ssm').get_parameter(
        Name='/slack/tcb/signing_secret',
        WithDecryption=True
    )['Parameter']['Value']
    signing_secret = str.encode(slack_signing_secret)

    slack_request_timestamp = req['headers']['X-Slack-Request-Timestamp']
    request_body = req['body']

    token = 'v0:{0}:{1}'.format(
        slack_request_timestamp,
        request_body
    )
    encoded_token = str.encode(token)

    slack_signature = req['headers']['X-Slack-Signature']

    encrypted_secret = hmac.new(
        key=signing_secret,
        msg=encoded_token,
        digestmod='sha256'
    ).hexdigest()

    expected_signature = 'v0={0}'.format(encrypted_secret)

    if not hmac.compare_digest(expected_signature, slack_signature):
        return False

    return True

def send_message(user_id, msg):
    """DM the user because Slack changed bot permissions and it's the easiest way to go about it."""
    slack_token = boto3.client('ssm').get_parameter(
        Name='/slack/tcb/bot_oauth',
        WithDecryption=True
    )['Parameter']['Value']

    client = slack.WebClient(token=slack_token)

    return client.chat_postMessage(
            channel=user_id,
            username='tcb',
            icon_emoji=':meow-goldstar:',
            type='section',
            text=msg
    )
