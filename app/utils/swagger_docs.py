create_subscription_doc = {
    "tags": ["Subscriptions"],
    "summary": "Create a new subscription",
    "description": "Creates a new subscription for the logged-in user.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "plan_id": {"type": "integer", "example": 1}
                },
                "required": ["plan_id"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "Subscription created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "user_id": {"type": "integer"},
                    "plan_id": {"type": "integer"}
                }
            }
        }
    }
}

cancel_subscription_doc = {
    "tags": ["Subscriptions"],
    "summary": "Cancel a subscription",
    "description": "Cancels the subscription with the given ID.",
    "parameters": [
        {
            "name": "subscription_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the subscription to cancel"
        }
    ],
    "responses": {
        200: {"description": "Subscription cancelled"},
        404: {"description": "Subscription not found"}
    }
}

upgrade_subscription_doc = {
    "tags": ["Subscriptions"],
    "summary": "Upgrade a subscription",
    "description": "Upgrades an existing subscription to a new plan.",
    "parameters": [
        {
            "name": "subscription_id",
            "in": "path",
            "type": "integer",
            "required": True
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "plan_id": {"type": "integer", "example": 2}
                },
                "required": ["plan_id"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "Subscription upgraded",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "user_id": {"type": "integer"},
                    "plan_id": {"type": "integer"}
                }
            }
        },
        404: {"description": "Subscription not found"}
    }
}

active_subscription_doc = {
    "tags": ["Subscriptions"],
    "summary": "Get active subscription",
    "description": "Retrieves the currently active subscription of the logged-in user.",
    "responses": {
        200: {
            "description": "Active subscription",
            "schema": {
                "type": "object"
            }
        },
        404: {"description": "No active subscription"}
    }
}

list_subscriptions_doc = {
    "tags": ["Subscriptions"],
    "summary": "List all subscriptions",
    "description": "Lists all subscriptions for the logged-in user.",
    "responses": {
        200: {
            "description": "List of subscriptions",
            "schema": {
                "type": "array",
                "items": {"type": "object"}
            }
        }
    }
}

subscription_history_doc = {
    "tags": ["Subscriptions"],
    "summary": "Subscription history",
    "description": "Returns historical subscription records for the logged-in user.",
    "responses": {
        200: {
            "description": "Subscription history",
            "schema": {
                "type": "array",
                "items": {"type": "object"}
            }
        }
    }
}

register_user_doc = {
    "tags": ["Auth"],
    "summary": "Register a new user",
    "description": "Register a new user with email and password. Returns the user ID and email on success.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "example": "user@example.com"
                    },
                    "password": {
                        "type": "string",
                        "example": "StrongPassword123!"
                    }
                },
                "required": ["email", "password"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "User registered successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "email": {"type": "string", "example": "user@example.com"}
                }
            }
        },
        400: {
            "description": "Invalid input or user already exists",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Email already exists"}
                }
            }
        }
    }
}
login_user_doc = {
    "tags": ["Auth"],
    "summary": "Login a user",
    "description": "Authenticate a user with email and password. Returns a JWT access token on success.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "example": "user@example.com"
                    },
                    "password": {
                        "type": "string",
                        "example": "StrongPassword123!"
                    }
                },
                "required": ["email", "password"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "Login successful",
            "schema": {
                "type": "object",
                "properties": {
                    "access_token": {"type": "string", "example": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."}
                }
            }
        },
        401: {
            "description": "Invalid email or password",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Invalid username or password"}
                }
            }
        }
    }
}

