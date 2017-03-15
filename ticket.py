"""a class to hold ticket data and related methods"""
class Ticket(object):
    """a jira ticket"""
    def __init__(self, project, issuetype):
        self.project = {'key': project}
        self.issuetype = {'name': issuetype}
        self.summary = "None"
        self.description = "None"
    def __str__(self):
        return "Ticket for {0}. Summary: {1}, Description: {2}. Type is {3}".format(
            self.project, self.summary, self.description, self.issuetype
        )
    def format_summary(self, format_string, *format_values):
        """creates a summary field from string + kwargs values"""
        if len(format_values) > 0:
            self.summary = format_string.format(*format_values)
        else:
            self.summary = format_string

    def format_description(self, format_string, *format_values):
        """creates a description field from string + kwargs values"""
        if len(format_values) > 0:
            self.description = format_string.format(*format_values)
        else:
            self.description = format_string
