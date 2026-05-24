from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Domain, Item
from .forms import DomainForm, ItemForm, TranslationForm

# ==================== Landing Page ====================

def vocab(request):
    return render(request, "index.html")

# ==================== DOMAIN VIEWS ====================

def domain_list(request):
    """List all domains"""
    domains = Domain.objects.all().order_by('name')
    return render(request, "domains/domain_list.html", {
        'domains': domains
    })


def domain_detail(request, domain_id):
    """Show one domain and its items"""
    domain = get_object_or_404(Domain, id=domain_id)
    items = domain.items.prefetch_related('translations').all()
    
    return render(request, "domains/domain_detail.html", {
        'domain': domain,
        'items': items
    })


def domain_create(request):
    """Create new domain"""
    if request.method == 'POST':
        form = DomainForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Domain created successfully!")
            return redirect('domain_list')
    else:
        form = DomainForm()
    
    return render(request, "domains/domain_form.html", {
        'form': form
    })


def domain_update(request, domain_id):
    """Edit existing domain"""
    domain = get_object_or_404(Domain, id=domain_id)
    
    if request.method == 'POST':
        form = DomainForm(request.POST, instance=domain)
        if form.is_valid():
            form.save()
            messages.success(request, "Domain updated successfully!")
            return redirect('domain_detail', domain_id=domain.id)
    else:
        form = DomainForm(instance=domain)
    
    return render(request, "domains/domain_form.html", {
        'form': form
    })

# ==================== ITEM VIEWS ====================

def item_create(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)
    
    if request.method == 'POST':
        item_form = ItemForm(request.POST, request.FILES)
        translation_form = TranslationForm(request.POST)
        
        if item_form.is_valid() and translation_form.is_valid():
            # Save Item first
            item = item_form.save(commit=False)
            item.domain = domain
            item.save()
            
            # Save Translation
            translation = translation_form.save(commit=False)
            translation.item = item
            translation.save()
            
            messages.success(request, "Word and translation added successfully!")
            return redirect('domain_detail', domain_id=domain.id)
    else:
        item_form = ItemForm()
        translation_form = TranslationForm(initial={'is_primary': True, 'language_code': 'en'})
    
    return render(request, "items/item_form.html", {
        'item_form': item_form,
        'translation_form': translation_form,
        'domain': domain
    })


def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    translations = item.translations.all()
    
    return render(request, "items/item_detail.html", {
        'item': item,
        'translations': translations
    })


def item_update(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Get the primary translation (or first one)
    primary_translation = item.translations.filter(is_primary=True).first()
    if not primary_translation:
        primary_translation = item.translations.first()
    
    if request.method == 'POST':
        item_form = ItemForm(request.POST, request.FILES, instance=item)
        translation_form = TranslationForm(request.POST, instance=primary_translation)
        
        if item_form.is_valid() and translation_form.is_valid():
            item_form.save()
            translation_form.save()
            messages.success(request, "Word updated successfully!")
            return redirect('item_detail', item_id=item.id)
    else:
        item_form = ItemForm(instance=item)
        translation_form = TranslationForm(instance=primary_translation)
    
    return render(request, "items/item_form.html", {
        'item_form': item_form,
        'translation_form': translation_form,
        'domain': item.domain,
        'item': item,           # Important for template
        'is_edit': True         # To change title
    })

def item_delete(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        domain_id = item.domain.id
        item.delete()
        messages.success(request, "Item deleted successfully!")
        return redirect('domain_detail', domain_id=domain_id)
    
    return render(request, "items/item_confirm_delete.html", {'item': item})

# ==================== ITEM VIEWS ====================

def translation_create(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        form = TranslationForm(request.POST)
        if form.is_valid():
            translation = form.save(commit=False)
            translation.item = item
            translation.save()
            messages.success(request, "New translation added successfully!")
            return redirect('item_detail', item_id=item.id)
    else:
        form = TranslationForm(initial={'is_primary': False})
    
    return render(request, "items/translation_form.html", {
        'form': form,
        'item': item
    })