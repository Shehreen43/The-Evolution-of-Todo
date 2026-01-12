---
name: sp.api-contract
description: Generate OpenAPI specifications and API contracts from requirements. Use when designing REST API endpoints, documenting API contracts, or creating API tests for Phase II+ applications.
---

# API Contract Generator

Generate OpenAPI 3.0 specifications and API contracts for the todo application.

## API Contract Structure

Generate a contracts/openapi.yaml file:

```yaml
openapi: 3.0.3
info:
  title: The Evolution of Todo API
  description: Full-Stack Todo Web Application API with JWT authentication
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com

servers:
  - url: http://localhost:8000
    description: Development server
  - url: https://api.example.com
    description: Production server

security:
  - BearerAuth: []

tags:
  - name: Tasks
    description: Task CRUD operations
  - name: Auth
    description: Authentication endpoints

paths:
  /health:
    get:
      summary: Health check endpoint
      responses:
        '200':
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: healthy

  /api/{user_id}/tasks:
    get:
      tags:
        - Tasks
      summary: List all tasks for a user
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
          description: User ID from JWT token
        - name: status
          in: query
          schema:
            type: string
            enum: [all, pending, completed]
            default: all
          description: Filter tasks by status
        - name: sort
          in: query
          schema:
            type: string
            enum: [created, title, updated]
            default: created
          description: Sort field
        - name: order
          in: query
          schema:
            type: string
            enum: [asc, desc]
            default: desc
          description: Sort order
        - name: limit
          in: query
          schema:
            type: integer
            default: 100
          description: Maximum results
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
          description: Results to skip
      responses:
        '200':
          description: List of tasks
          content:
            application/json:
              schema:
                type: object
                properties:
                  tasks:
                    type: array
                    items:
                      $ref: '#/components/schemas/Task'
                  total:
                    type: integer
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'

    post:
      tags:
        - Tasks
      summary: Create a new task
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskCreate'
      responses:
        '201':
          description: Task created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'

  /api/{user_id}/tasks/{task_id}:
    get:
      tags:
        - Tasks
      summary: Get a specific task
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
        - name: task_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Task details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'

    put:
      tags:
        - Tasks
      summary: Update a task
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
        - name: task_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskUpdate'
      responses:
        '200':
          description: Task updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'

    delete:
      tags:
        - Tasks
      summary: Delete a task
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
        - name: task_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Task deleted successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Task deleted successfully
                  id:
                    type: integer
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'

  /api/{user_id}/tasks/{task_id}/complete:
    patch:
      tags:
        - Tasks
      summary: Toggle task completion status
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
        - name: task_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Task completion toggled
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    Task:
      type: object
      properties:
        id:
          type: integer
          example: 1
        user_id:
          type: string
          format: uuid
          example: "550e8400-e29b-41d4-a716-446655440000"
        title:
          type: string
          minLength: 1
          maxLength: 200
          example: "Buy groceries"
        description:
          type: string
          maxLength: 1000
          nullable: true
          example: "Milk, eggs, bread"
        completed:
          type: boolean
          default: false
        created_at:
          type: string
          format: date-time
          example: "2024-01-15T10:30:00Z"
        updated_at:
          type: string
          format: date-time
          example: "2024-01-15T10:30:00Z"

    TaskCreate:
      type: object
      required:
        - title
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
          example: "Buy groceries"
        description:
          type: string
          maxLength: 1000
          nullable: true
          example: "Milk, eggs, bread"

    TaskUpdate:
      type: object
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 1000
          nullable: true

    Error:
      type: object
      properties:
        detail:
          type: string
          example: "Error message"

  responses:
    BadRequest:
      description: Validation error or invalid input
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Missing or invalid JWT token
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          headers:
            WWW-Authenticate:
              schema:
                type: string
                example: Bearer
    Forbidden:
      description: Valid token but unauthorized access
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    InternalServerError:
      description: Server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

## Generate FastAPI from Contract

### src/app.py
```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="The Evolution of Todo API",
        version="1.0.0",
        description="Full-Stack Todo Web Application API with JWT authentication",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI()
app.openapi = custom_openapi
```

## Error Response Standards

| Status Code | Name | Description |
|-------------|------|-------------|
| 200 | OK | Success |
| 201 | Created | Resource created |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Invalid/missing token |
| 403 | Forbidden | Valid token, wrong user |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server error |

## Error Response Format

```json
{
  "detail": "Error message describing the issue"
}
```

## Guardrails

### Do
- Use semantic HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Return appropriate status codes
- Include error details in responses
- Document all parameters and request bodies
- Use consistent naming conventions

### Do Not
- Use non-restful action names in URLs
- Return sensitive data in error messages
- Mix different response formats
- Omit authentication requirements

## Triggers

Use this skill when:
- User asks to "create API contract"
- Designing new API endpoints
- Documenting existing APIs
- Generating OpenAPI specs
- Creating API tests from contracts
