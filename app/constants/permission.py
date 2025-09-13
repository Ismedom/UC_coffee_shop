permissions_data = [
    {"name": "user.read", "resource": "users", "action": "read"},
    {"name": "user.edit", "resource": "users", "action": "edit"},
    {"name": "user.update", "resource": "posts", "action": "update"},
    {"name": "user.delete", "resource": "posts", "action": "delete"},
]

role_permissions_map = {
    "admin": ["user.read", "user.edit", "user.update", "user.delete"],
    "user": ["user.read"]
}
