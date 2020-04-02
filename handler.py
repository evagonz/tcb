import logging

from urllib.parse import parse_qs
from tcblib import db_functions, slack_functions

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def work(event, context):
    """Determine what type of event came in, and handle accordingly."""
    logger.info("Request received")

    # there has got to be a nicer way to differentiate between cloudwatch event & slack
    if 'detail-type' in event:
        logger.info('Cloudwatch scheduled trigger recieved')
        tc_rollup = db_functions.query_all()
        user_id = tc_rollup['Host']['M']['user_id']['S']
        stars_raw = tc_rollup['GoldStars']['L']
        stars_list = [star['S'] for star in stars_raw]
        msg = "Here are this week's gold stars -- sorry the formatting sucks right now: {0}".format(stars_list)
        slack_functions.send_message(user_id=user_id, msg=msg)
    else:
        if not slack_functions.validate_request(event):
            logger.error("Slack request not valid")
            return {}  # there needs to be actual error handling

        logger.debug("Parsing params...")
        req = parse_qs(event['body'])
        logger.debug("Params parsed: {0}".format(req))

        user_name = req['user_name'][0]
        user_id = req['user_id'][0]
        command = req['command'][0]

        if 'text' in req:
            cmd_text = req['text'][0]
        else:
            cmd_text = None

        if command == '/goldstar':
            logger.debug("Adding goldstar...")
            db_functions.add_goldstar(cmd_text)  # TODO: verify
            logger.debug("Goldstar added")
            msg = "And a gold star to *you* for your contribution to tech chat!"
            slack_functions.send_message(user_id=user_id, msg=msg)

        if command == '/tc-host':
            if cmd_text == 'me':
                tc_host = db_functions.update_host(user_id, user_name)  # TODO: verify
                logger.debug("Look at me: I'm the host now")
                msg = "You are now set to host tech chat on Friday!"
                slack_functions.send_message(user_id=user_id, msg=msg)
            else:
                tc_host = db_functions.query_host('name')
                msg = "Current host for this week: {0}\nIf you want to host, type `/tc-host me`".format(tc_host)

                slack_functions.send_message(user_id=user_id, msg=msg)

    return {}
