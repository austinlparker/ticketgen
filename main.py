#!/usr/bin/env python
"""This script creates release tasks in Jira"""

import argparse
import json
import ConfigParser

import ticket

from jira import JIRA

CONFIG = ConfigParser.ConfigParser()

def main():
    """creates tickets for a release task"""
    parser = argparse.ArgumentParser(description='Creates tickets for release certification')
    parser.add_argument('-u', '--username', help='jira username', default='admin')
    parser.add_argument('-p', '--password', help='jira password', default='admin')
    parser.add_argument('-c', '--config', help='path to config file', default='./options.ini')
    parser.add_argument('-j', '--jira', help='url of jira server', default='http://localhost:8080')

    args = parser.parse_args()

    jira_user = args.username
    jira_pass = args.password
    jira_server = args.jira
    config_file_path = args.config
    CONFIG.read(config_file_path)

    parent_ticket = config_map('JiraOptions')['parent_ticket']
    apprenda_version = config_map('VersionInfo')['to_version']
    jira_project = config_map('JiraOptions')['project']
    jira_issue_type = config_map('JiraOptions')['issue_type']
    jira = JIRA(jira_server, basic_auth=(jira_user, jira_pass))

    parent_issue = jira.issue(parent_ticket)
    ticket_list = []

    # create clean install tickets
    clean_strings = config_map('CleanInstallSection')
    for cloud in ['single', 'hybrid']:
        ticket_to_add = ticket.Ticket(jira_project, jira_issue_type)
        ticket_to_add.format_summary(clean_strings['summary'], apprenda_version, cloud)
        ticket_to_add.format_description(clean_strings['description'])
        ticket_list.append(ticket_to_add.__dict__)

    # create upgrade tickets
    from_versions = json.loads(config_map('VersionInfo')['from_versions'])
    upgrade_strings = config_map('UpgradeSection')

    # single cloud
    for version in from_versions:
        ticket_to_add = ticket.Ticket(jira_project, jira_issue_type)
        ticket_to_add.format_summary(upgrade_strings['summary'], apprenda_version, version,
                                     "single")
        ticket_to_add.format_description(upgrade_strings['description'])
        ticket_list.append(ticket_to_add.__dict__)

    # hybrid cloud
    for version in from_versions:
        ticket_to_add = ticket.Ticket(jira_project, jira_issue_type)
        ticket_to_add.format_summary(upgrade_strings['summary'], apprenda_version, version,
                                     "hybrid")
        ticket_to_add.format_description(upgrade_strings['description'])
        ticket_list.append(ticket_to_add.__dict__)

    # create testing tickets for other tasks
    for section in CONFIG.sections():
        if 'Ticket' in section:
            strings = config_map(section)
            ticket_to_add = ticket.Ticket(jira_project, jira_issue_type)
            ticket_to_add.format_summary(strings['summary'], apprenda_version)
            ticket_to_add.format_description(strings['description'])
            ticket_list.append(ticket_to_add.__dict__)

    print 'Created {0} tickets, now sending them to Jira'.format(len(ticket_list))
    # send issues to jira and create tickets and links
    issues = jira.create_issues(field_list=ticket_list)

    for item in issues:
        jira.create_issue_link(
            type="Task of Story",
            outwardIssue=item['issue'].key,
            inwardIssue=parent_issue.key,
        )

    print 'Finished linking issues, exiting.'

def config_map(section):
    """given a config section, return a map of values"""
    result = {}
    options = CONFIG.options(section)
    for option in options:
        try:
            result[option] = CONFIG.get(section, option)
            if result[option] == -1:
                print 'skipping {0}'.format(option)
        except:
            print 'exception on {0}'.format(option)
            result[option] = None
    return result

if __name__ == '__main__':
    main()
