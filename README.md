# gaia
An alternative to retrieve Salesforce's B2C Commerce's Account Manager's users with relevant information and capabilities to export the result as a CSV file.

I made this tool to supplement Salesforce B2C Commerce Account Manager missing features.

In order to use this tool, a running python3 environment is needed.
The list of dependencies will be updated as time goes but actually, the most important are the support of requests and flask.

# Dependencies

This project requires the following Python packages and modules:

## Standard Library Dependencies
- **json**: For JSON parsing and serialization
- **os**: For operating system dependent functionality like file path operations
- **sys**: For system-specific parameters and functions
- **configparser**: For working with configuration files (used for reading `config.cfg`)
- **urllib.parse**: For URL parsing and manipulation (imported as `parse`)
- **array**: For array data types

## External Dependencies
- **Flask**: Web framework for building the application
  - Specific components: `Flask`, `render_template`, `request`, `current_app`, `send_file`
- **requests**: For making HTTP requests

## Custom Modules
- **SfccConnector**: Custom module for Salesforce Commerce Cloud connectivity, used to obtain JWT tokens

## Installation

You can install the required external dependencies using pip:

```bash
pip install flask requests
```

### Using a requirements.txt file (Optional)

If you want to formalize dependencies for development or deployment environments, you can create a `requirements.txt` file:

```
Flask>=2.0.0
requests>=2.25.0
```

And install using:

```bash
pip install -r requirements.txt
```

This approach is useful for both standard Python projects and containerized environments like Docker.

Note: The custom `SfccConnector` module is part of this project and does not need separate installation as long as it's in your Python path.

## Python Version

This project is developed and tested with Python 3.6+.

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

# User Management Tool - User Guide

## Introduction

This tool allows you to manage users in your Salesforce Commerce Cloud instance. It provides a simple interface to view, search, and export user information.

## Installing and Running the Application

### Installing Dependencies

Before running the application, make sure you have installed all the required dependencies:

```bash
pip install flask requests
```

### Running the Application

To start the application:

1. Navigate to the directory containing the application files
2. Run the main application file using Python:
   ```bash
   python gaia.py
   ```
3. The application will start and by default will be accessible at http://localhost/
4. You should see console output indicating that the server is running

### Accessing the Application

Once the application is running:
1. Open your web browser and go to the following URL:
   ```
   http://localhost/
   ```

## User Interface

After logging in, you'll see the "User Management" page which displays a table with user information.

![User Management Interface](user_management_interface.png)

### Main Features

#### Viewing Users

The table displays the following information for each user:

- **ID**: Unique identifier for the user
- **Email**: User's email address
- **First Name**: User's first name
- **Last Name**: User's last name
- **Display Name**: User's full name as displayed in the system
- **Roles**: Roles assigned to the user (e.g., 'appd-dashboards', 'api-admin')
- **Primary Organization**: Organization the user is associated with
- **Last Login**: Date of the user's last login
- **Status**: User account status (ENABLED, DISABLED, etc.)

#### Available Actions

Several actions are available via the buttons above the table:

1. **Export to CSV**: Export the user list to a CSV file
2. **Print**: Print the current user list
3. **Manage Columns**: Choose which columns to display in the table

#### Navigation and Filtering

- **Display**: Choose how many entries to show per page (dropdown menu "Show")
- **Search**: Use the search field in the top right to filter users
- **Pagination**: Navigate between pages using the "Previous", "Next" buttons and page numbers

## Step-by-Step Usage

### Searching for a User

1. Go to the main page at http://localhost/
2. Use the search field in the top right
3. Type any term (name, email, role, etc.)
4. Results will automatically update to show only matching users

### Exporting the User List

1. Go to the main page at http://localhost/
2. Click the "Export to CSV" button
3. Select the location where you want to save the file
4. The CSV file containing all user data will be downloaded

### Customizing the Display

1. Go to the main page at http://localhost/
2. Click the "Manage Columns" button
3. Select or deselect the columns you want to display
4. The table display will update according to your choices

## Configuration

To configure the tool, make sure the `config.cfg` file is properly filled with the following information:

- `clientId`: The Client ID configured in Account Manager (with read permission)
- `password`: The password associated with the Client ID. Not needed when using OAuth2 version.
- `amLocation`: The Account Manager instance URL (default: account.demandware.com)
- `organizationId`: The ID of the organization for which you want to extract the user list. To be removed in the future.

## Troubleshooting

If you encounter issues:

1. Verify that the application is running
2. Ensure that the configuration information is correct
3. Check that your account has the necessary permissions
4. If the problem persists, check the application logs for more details

