ACTIONS = ["create", "read", "update", "delete"]

RESOURCES = [
    "users",
    "roles",
    "permissions",
    "products",
    "purchase_orders",
    "purchase_order_details",
]

PERMISSIONS = [
    {"name": f"{resource}.{action}", "resource": resource, "action": action}
    for resource in RESOURCES
    for action in ACTIONS
]

# ROLE_PERMISSIONS_MAP = {
#     "admin": [perm["name"] for perm in PERMISSIONS],
#     "user": [perm["name"] for perm in PERMISSIONS if perm["action"] == "read"],
# }
