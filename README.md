# gaia
A Salesforce alternative to retrieve Account Manager users with relevant information and capabilities to export the result as a CSV file.

I made this tool to supplement Salesforce B2C Commerce Account Manager missing features.

In order to use this tool, a running python3 environment is needed.
The list of dependencies will be updated as time goes but actually, the most important are the support of requests and flask.

Configuration

# Configuration

## config.cfg

The application uses a configuration file (`config.cfg`) to store credentials and connection information. Make sure to set up this file correctly before running the application.

### Parameters

| Parameter | Description |
|-----------|-------------|
| `clientId` | The name of the Client ID configured in Account Manager. This ID must have Account Administrator read-only permission at minimum. |
| `password` | The password associated with the Client ID. |
| `amLocation` | The Account Manager instance URL to connect to. The default location is `account.demandware.com`. You may need to change this in specific deployment scenarios. |
| `organizationId` | The ID of the organization for which you want to pull the user list. |

### Example

```
clientId=your_client_id
password=your_secure_password
amLocation=account.demandware.com
organizationId=your_organization_id
```

### Security Notes

- Never commit this file with actual credentials to your Git repository
- Add `config.cfg` to your `.gitignore` file
- Consider using environment variables for sensitive information in production environments

## Setup Instructions

1. Create a copy of `config.cfg.template` and rename it to `config.cfg`
2. Fill in your specific credentials and organization information
3. Ensure the file has appropriate read permissions for the application
