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
        "name": "get_domain_details",
        "description": "Get details of a domain, including its subdomains",
        "parameters": {
            "type": "object",
            "properties": {
                "domain_name": {
                    "type": "string"
                }
            },
            "required": ["domain_name"]
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
    },
    {
        "name": "get_word_details",
        "description": "Get details about a word, including its domain and translations",
        "parameters": {
            "type": "object",
            "properties": {
                "word_name": {
                    "type": "string"
                }
            },
            "required": ["word_name"]
        }
    },
    {
        "name": "search_words",
        "description": "Search for words across domains, items, and translations",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string"
                }
            },
            "required": ["query"]
        }
    }
]