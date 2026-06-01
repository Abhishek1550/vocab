GEMINI_TOOLS = [
    {
        "name": "get_domains",
        "description": "Get all domains belonging to the current user",
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "get_subdomains",
        "description": "Get subdomains of a domain",
        "parameters": {
            "type": "object",
            "properties": {
                "domain_name": {
                    "type": "string"
                }
            },
            "required": ["domain_name"]
        }
    },
    {
        "name": "get_items_in_domain",
        "description": "Get vocabulary items belonging to a domain",
        "parameters": {
            "type": "object",
            "properties": {
                "domain_name": {
                    "type": "string"
                }
            },
            "required": ["domain_name"]
        }
    }
]