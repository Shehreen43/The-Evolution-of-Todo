# Todo AI Chatbot - Model Context Protocol (MCP) Server

The Model Context Protocol (MCP) server provides a standardized interface for AI agents to interact with the Todo application. It enables AI models to perform todo operations through well-defined tools and context providers.

## Overview

The MCP server implements the [Model Context Protocol](https://modelcontextprotocol.io/) specification, allowing AI agents to:

- Create, read, update, and delete todo tasks
- Access contextual information about user tasks
- Perform operations securely with proper authentication

## Architecture

```
AI Agent ←→ MCP Server ←→ Database
     ↓           ↓           ↓
  Tools    Context      SQLModel
Providers   Providers    Models
```

## Available Tools

### 1. add_task
- **Purpose**: Create a new task for the user
- **Parameters**:
  - `user_id` (string, required): User identifier
  - `title` (string, required): Task title (max 200 characters)
  - `description` (string, optional): Task description (max 1000 characters)
- **Usage**: When user wants to add, create, or remember something

### 2. list_tasks
- **Purpose**: Retrieve a list of tasks for the user
- **Parameters**:
  - `user_id` (string, required): User identifier
  - `status` (string, optional): Filter by status ("all", "pending", "completed"; default: "all")
  - `limit` (integer, optional): Max number of tasks to return (default: 10)
- **Usage**: When user wants to see, view, or check their tasks

### 3. update_task
- **Purpose**: Update an existing task for the user
- **Parameters**:
  - `task_id` (integer, required): Task identifier
  - `user_id` (string, required): User identifier
  - `title` (string, optional): New task title
  - `description` (string, optional): New task description
  - `completed` (boolean, optional): New completion status
  - `priority` (string, optional): New task priority ("low", "medium", "high")
- **Usage**: When user wants to modify, edit, or change a task

### 4. delete_task
- **Purpose**: Delete an existing task for the user
- **Parameters**:
  - `task_id` (integer, required): Task identifier
  - `user_id` (string, required): User identifier
- **Usage**: When user wants to remove, delete, or eliminate a task

### 5. complete_task
- **Purpose**: Mark a task as completed or incomplete for the user
- **Parameters**:
  - `task_id` (integer, required): Task identifier
  - `user_id` (string, required): User identifier
  - `completed` (boolean, optional): Whether task is completed (default: true)
- **Usage**: When user wants to mark, complete, or finish a task

## Context Providers

### 1. read_user_tasks
- **URI**: `todo://user/{user_id}/tasks`
- **Purpose**: Provides a summary of the user's current tasks
- **Content**: List of tasks with titles, descriptions, and completion status

### 2. read_user_task_details
- **URI**: `todo://user/{user_id}/task/{task_id}`
- **Purpose**: Provides detailed information about a specific task
- **Content**: Complete task details in JSON format

### 3. list_user_resources
- **Purpose**: Lists available resources for the user
- **Content**: Collection of task URIs and descriptions

## Installation

The MCP server is integrated into the Todo application. Ensure you have the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The server can be configured using environment variables:

```bash
export MCP_SERVER_HOST=localhost     # Host to bind to
export MCP_SERVER_PORT=8080         # Port to bind to
export MCP_SERVER_SSL=false         # Enable SSL
```

## Running the Server

Start the MCP server using the provided script:

```bash
# Navigate to the backend directory
cd backend

# Run the MCP server
python -m app.run_mcp_server --host localhost --port 8080
```

Or use the direct approach:

```bash
cd backend
python -c "from app.mcp.main import start_mcp_server; import asyncio; asyncio.run(start_mcp_server())"
```

## Integration with AI Models

To integrate with AI models that support MCP:

1. Start the MCP server
2. Configure your AI client to connect to the MCP server
3. The AI model will automatically discover available tools and context providers
4. Use natural language to interact with the todo system

## Security

- All operations require a valid `user_id` parameter
- Database queries are filtered by `user_id` to ensure data isolation
- Input validation is performed on all parameters
- Proper error handling prevents information disclosure

## Error Handling

The server returns appropriate error messages for:
- Invalid input parameters
- Unauthorized access attempts
- Database connection issues
- Missing resources

## Development

### Adding New Tools

To add a new MCP tool:

1. Create a new file in `app/mcp/tools/`
2. Define the tool using the `Tool` class
3. Implement the handler function
4. Import and register the tool in `app/mcp/server/server.py`

### Testing

The MCP server follows the same testing patterns as the rest of the application. Use pytest to run tests:

```bash
pytest tests/ -v
```

## Troubleshooting

### Common Issues

1. **Connection refused**: Ensure the MCP server is running on the correct host/port
2. **Authentication failed**: Verify that the `user_id` parameter is valid
3. **Tool not found**: Check that the tool is properly registered in the server

### Logging

The server logs important events and errors. Check the logs for debugging information:

```bash
# Increase log level for debugging
export LOG_LEVEL=DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes with proper tests
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.