import functools

from flask import request, jsonify, current_app
from werkzeug.local import LocalProxy

from ...application.errors.errors import ApiError
from ...domain.exceptions.authentication_error import AuthenticationError
from ...infrastructure.config.container import DependencyContainer

# Create a proxy to access the dependency container
container = LocalProxy(lambda: current_app.container if hasattr(current_app, 'container') else DependencyContainer())


def token_required(authorized_roles=None):
    """
    Decorator to validate JWT token for protected endpoints

    Args:
        authorized_roles: List of roles that can access the endpoint. If None, only 'VENDEDOR' is allowed.
    """
    if authorized_roles is None:
        authorized_roles = ['VENDEDOR', 'DIRECTIVO']

    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            # Extract token from Authorization header
            auth_header = request.headers.get('Authorization')

            if not auth_header:
                return jsonify({'error': 'Authorization header is missing'}), 401

            try:
                # Check if the header has the correct format
                parts = auth_header.split()
                if len(parts) != 2 or parts[0].lower() != 'bearer':
                    return jsonify({'error': 'Invalid authorization format. Use: Bearer <token>'}), 401

                token = parts[1]

                # Validate token using the auth service
                auth_service = container.token_validator
                user_data = auth_service.validate_token(token)

                # Check if the user has any of the required roles
                if user_data['role'] not in authorized_roles:
                    return jsonify({'error': 'User does not have the required role'}), 403

                # Add user data to the request context for use in the endpoint
                request.user = user_data

                return f(*args, **kwargs)

            except AuthenticationError as e:
                return jsonify({'error': str(e)}), 401
            except ApiError as e:
                current_app.logger.error(f"API error: {str(e.description)}")
                return jsonify({"msg": e.description}), e.code
            except Exception as e:
                current_app.logger.error(f"Authentication error: {str(e)}")
                return jsonify({'error': 'Internal server error during authentication'}), 500

        return decorated_function

    # Handle both @token_required and @token_required(['ROLE1', 'ROLE2']) usage
    # if callable(authorized_roles):
    #     f = authorized_roles
    #     authorized_roles = ['DIRECTIVO']
    #     return decorator(f)

    return decorator
