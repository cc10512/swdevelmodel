#! /usr/bin/env python3

import logging
import subprocess
import shlex
import traceback
import json

debug = 0
issues = {
         "issue summary": "issue description"
}
logging.basicConfig(level = logging.DEBUG)

apiToken = "..."
credentials = '"cascaval@barefootnetworks.com:{}"'.format(apiToken)

def runCmd(cmd, logger, dry_run = False, print_on_error = True):
    """
    Run a command, capture its output and print it
    Return the exit code of the command
    """
    if dry_run:
        logger.info(' '.join(cmd))
        return 0
    else:
        logger.debug(' '.join(cmd))

    try:
        p = subprocess.Popen(shlex.split(" ".join(cmd)),
                             stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    except:
        logger.error("error invoking {}".format(" ".join(cmd)))
        logger.error(traceback.format_exc())
        return 1

    (outlog, errlog) = p.communicate() # wait for command completion

    if p.returncode != 0:
        if print_on_error:
            logger.info("Output:\n%s", outlog.decode())
        else:
            logger.debug("Output:\n%s", outlog.decode())
        logger.error("Errors:\n%s", errlog.decode())
    else:
        logger.debug("\n%s%s", outlog.decode(), errlog.decode())

    return p.returncode

def outputCmd(cmd, logger, dry_run = False):
    """
    Run a command, capture and return its output
    """
    if dry_run:
        logger.info(' '.join(cmd))
        return "Can't really say!"
    else:
        logger.debug(' '.join(cmd))

    try:
        return subprocess.run(shlex.split(' '.join(cmd)),
                              # shell=True, # check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()
    except:
        logger.error("error invoking {}".format(' '.join(cmd)))
        raise

def createIssue(projectName, summary, description,
                labels = [], epicLink = None,
                attachments = None, dry_run = False):
    issueTemplate = {
        "fields" : {
            "project" : { "key" : projectName },
            "summary" : summary,
            "description" : description,
            "issuetype" : { "name" : "Bug" },
            "labels" : labels,
            "fixVersions":[{"self":"https://barefootnetworks.atlassian.net/rest/api/2/version/16935",
                            "id": "16935",
                            "name": "9.2.0",
                            "archived": False,
                            "released": False,
                            "releaseDate":"2020-03-31"}],
            "components":[{"self":"https://barefootnetworks.atlassian.net/rest/api/2/component/15734",
                           "id":"15734",
                           "name":"sdle"}],
            "versions":[{"self":"https://barefootnetworks.atlassian.net/rest/api/2/version/16909",
                         "id":"16909","description":"",
                         "name":"9.1.0",
                         "archived": False,
                         "released": True,
                         "releaseDate":"2020-01-15"}]
        }
    }
    if epicLink is not None:
        # customfield_10008 == Epic Link
        issueTemplate["fields"]["customfield_10008"] = epicLink,
    with open('issue.data.json', 'w') as out_file:
        json.dump(issueTemplate, out_file)

    cmd = ['curl', '-S', '-u', credentials, '-X', 'POST',
           '-H', '"Content-Type: application/json"',
           '--data' '@issue.data.json',
           'https://barefootnetworks.atlassian.net/rest/api/2/issue/' ]
    issuesJSON = outputCmd(cmd, logging.getLogger(), dry_run)
    if debug = 0:
        os.remove('issue.data.json')
    if dry_run:
        issue = { "issues": [ { "key": 'TEST-1234' } ]}
    else:
        issue = json.loads(issuesJSON)
    key = issue["issues"][0]["key"]
    logging.info('Created issue {}'.format(key))
    if attachments is not None:
        for f in attachments:
            logging.info("Creating attachment: {}".format(f))
            cmd = ['curl', '-D', '-u', credentials, '-X', 'POST',
                   '-H', '"X-Atlassian-Token: no-check"',
                   '-F', '"file=@{}"'.format(f),
                   'https://barefootnetworks.atlassian.net/rest/api/2/issue/{}/attachments'.format(key) ]
            runCmd(cmd, logging.getLogger(), dry_run)

for i in issues:
    createIssue('P4C', i, issues[i], ['SDLe'], epicLink = 'P4C-2499', dry_run = True)
