# gaia
A Salesforce alternative to retrieve Account Manager users with relevant information and capabilities to export the result as a CSV file.

I made this tool to supplement Salesforce B2C Commerce Account Manager missing features.

In order to use this tool, a running python3 environment is needed.
The list of dependencies will be updated as time goes but actually, the most important are the support of requests and flask.

Configuration

config.cfg file has four parameters

clientId <- This is the name of the Client ID configured in Account Manager. This ID must have Account Administrator read only permission at least.
password: The password associated with the Client ID
amLocation: In some situations you may want to use this tool against specific Account Manager instances. hHowever, the default location should be account.demandware.com
organizationId: is the ID of the organization for which you want to pull the user list.
