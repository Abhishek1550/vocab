from core.models import Domain, Item

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
    pass

def search_words(user, query):
    pass

TOOLS = {
    "get_domains": get_domains,
    "get_subdomains": get_subdomains,
    "get_items_in_domain": get_items_in_domain,
}