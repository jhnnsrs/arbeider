from rest_access_policy.access_policy import AccessPolicy


class RepresentationAccessPolicy(AccessPolicy):
    statements = [
        ## ... other statements ...
        {
            "action": ["withdraw"],
            "principal": ["*"],
            "effect": "allow",
            "condition": ["balance_is_positive", "user_must_be:owner"]     
        },
        {
            "action": ["upgrade_to_gold_status"],
            "principal": ["*"],
            "effect": "allow",
            "condition": ["user_must_be:account_advisor"]
        }
        ## ... other statements ...
    ]