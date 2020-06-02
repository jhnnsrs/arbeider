import rest_access_policy


class AccessPolicy(rest_access_policy.AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": "authenticated",
            "effect": "allow"
        },
    ]