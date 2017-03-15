# ticketgen.py

This utility will create tickets for you based on options contained in the `options.ini` file. 

## How To Run Locally
1. Ensure you have Python 2.7.12+ installed with `python` available on your system path.
2. Clone this repository.
3. Ensure the `options.ini` file is updated with the appropriate information in the `[JiraOptions]` and `[VersionInfo]` sections.
4. Switch to your checkout directory and `python main.py -u <jira username> -p <jira password> -c <path to config file> -j <jira url>`

## How To Build and Run Via Docker 
1. Ensure you have Docker installed and running.
2. Clone this repository.
3. Perform whatever updates you'd like to make to the `options.ini` file.
4. In the checkout, run `docker build -t taskgen .`
5. You can then run the image with `docker run taskgen`

## Using The `options.ini` File

The options file should be fairly self explanatory. There's a few things to keep in mind, though.

- You **must** update the `VersionInfo` section for each release to include the correct `from_versions` and the correct `to_version`.
- **Ensure that the `JiraOptions` section has the proper `parent_ticket` and `project` entries** depending on if you're testing a new version or running the tool in production.

The following table summarizes the possible options and acceptable values for each configuration block.

| Section | Value | Description |
| ------- | ----- | ----------- |
| JiraOptions | parent_ticket | The 'parent' ticket for all generated tasks |
| JiraOptions | project | The JIRA project that issues will be created in. |
| JiraOptions | issue_type | The JIRA issue type that issues should be created as. Case-sensitive. These can be discovered through JIRA Rest API calls. |
| VersionInfo | to_version | The **new** software version that will be created. |
| VersionInfo | from_versions | An array of versions the new version will be upgradeable from |
| *Section/Ticket | summary | The ticket summary (title). Can be token-switched. |
| *Section/Ticket | description | The ticket description (body text). Can be token-switched. |

The `CleanInstall` and `Upgrade` sections are special cases that are handled uniquely by the script. This is because their summary formatting is different than the normal tickets.

### Adding a new ticket
Adding a ticket is very straightforward. Simply create a new configuration block at the end of the file where the config name ends with `Ticket`, for example -
```
[TestTicket]
summary: rel-{0}: New ticket to be generated
description: Do a thing!
  # step 1
  # step 2
  Now you're done!
```
You can create multiline bodies by simply adding a new line to the description. Make sure that you indent your new lines! Any JIRA markdown should work.

### Modifying a ticket
Change the description text in the `options.ini` file.