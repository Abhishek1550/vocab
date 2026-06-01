from core.models import Domain, Item, Translation

def get_domains(user):

    domains = Domain.objects.filter(
        user=user,
        parent__isnull=True
    )

    return [
        {
            "id": domain.id,
            "name": domain.name,
            "description": domain.description,
        }
        for domain in domains
    ]

def get_domain_details(user, domain_name):
    try:
        domain = Domain.objects.get(
            user=user,
            name__iexact=domain_name,
        )

    except Domain.DoesNotExist:
        return {
            "error": f"Domain '{domain_name}' not found."
        }

    return {
        "id": domain.id,
        "name": domain.name,
        "description": domain.description,
        "subdomains": [
            {
                "id": sub.id,
                "name": sub.name,
                "description": sub.description,
            }
            for sub in domain.subdomains.all()
        ],
        "subdomains_count": domain.subdomains.count(),
    }

def get_subdomains(user, domain_name):

    try:
        domain = Domain.objects.get(
            user=user,
            name__iexact=domain_name,
        )

    except Domain.DoesNotExist:
        return {
            "error": f"Domain '{domain_name}' not found."
        }

    subdomains = domain.subdomains.all()

    return [
        {
            "id": sub.id,
            "name": sub.name,
            "description": sub.description,
        }
        for sub in subdomains
    ]

def get_items_in_domain(user, domain_name):

    try:
        domain = Domain.objects.get(
            user=user,
            name__iexact=domain_name,
        )

    except Domain.DoesNotExist:
        return {
            "error": f"Domain '{domain_name}' not found."
        }

    items = Item.objects.filter(
        user=user,
        domain=domain
    )

    result = []

    for item in items:

        primary = item.translations.filter(
            is_primary=True
        ).first()

        result.append(
            {
                "id": item.id,
                "word": primary.word if primary else f"Item {item.id}"
            }
        )

    return result

def get_word_details(user, word_name):
    try:
        translation = Translation.objects.get(
            user=user,
            word__iexact=word_name,
        )
        return {
            "domain": {
                "id": translation.item.domain.id,
                "name": translation.item.domain.name,
                "description": translation.item.domain.description,
            },
            "word_details": {
                "id": translation.item.id,
                "word": translation.word,
                "description": translation.description,
                "is_primary": translation.is_primary,
            },
            "translations": [
                {
                    "id": t.id,
                    "word": t.word,
                    "description": t.description,
                    "is_primary": t.is_primary,
                }
                for t in translation.item.translations.all()
            ],
        }

    except Translation.DoesNotExist:
        return {
            "error": f"Word '{word_name}' not found."
        }

def search_words(user, query):
    # Simple search across whole database for the user

    # search in domain names
    domains = Domain.objects.filter(
        user=user,
        name__icontains=query,
    )

    # search in item names
    items = Item.objects.filter(
        user=user,
        name__icontains=query,
    )

    # search in translations
    translations = Translation.objects.filter(
        user=user,
        word__icontains=query,
    )

    return {
        "domains": [
            {
                "id": domain.id,
                "name": domain.name,
                "description": domain.description,
            }
            for domain in domains
        ],
        "items": [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
            }
            for item in items
        ],
        "translations": [
            {
                "id": translation.id,
                "word": translation.word,
                "description": translation.description,
                "is_primary": translation.is_primary,
            }
            for translation in translations
        ]
    }

def get_translations():
    pass

def count_items_in_domain():
    pass

def count_subdomains_in_domain():
    pass

def count_domains():
    pass


TOOLS = {
    "get_domains": get_domains,
    "get_subdomains": get_subdomains,
    "get_items_in_domain": get_items_in_domain,
    "get_domain_details": get_domain_details,
    "get_word_details": get_word_details,
    "search_words": search_words,
}