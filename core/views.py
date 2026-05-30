from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from core.utils.generate_image import generate_image_from_prompt
from .models import Domain, Item, Translation
from .forms import DomainForm, ItemForm, TranslationForm
from django.contrib.auth.decorators import login_required

# ==================== Landing Page ====================

def vocab(request):
    return render(request, "index.html")

# ==================== DOMAIN VIEWS ====================
@login_required
def domain_list(request):
    """List all domains"""
    domains = Domain.objects.filter(user=request.user, parent=None).order_by('name')
    return render(request, "domains/domain_list.html", {
        'domains': domains
    })

@login_required
def domain_detail(request, domain_id):
    """Show one domain and its items"""
    domain = get_object_or_404(Domain, id=domain_id, user=request.user)
    items = domain.items.prefetch_related('translations').all()
    subdomains = domain.subdomains.all()
    
    return render(request, "domains/domain_detail.html", {
        'domain': domain,
        'items': items,
        'subdomains': subdomains
    })

@login_required
def domain_create(request):
    """Create new domain"""
    if request.method == 'POST':
        form = DomainForm(request.POST, request.FILES)
        if form.is_valid():
            domain = form.save(commit=False)
            domain.user = request.user
            domain.save()
            messages.success(request, "Domain created successfully!")
            return redirect('domain_list')
    else:
        form = DomainForm()
    
    return render(request, "domains/domain_form.html", {
        'form': form
    })

@login_required
def domain_create_subdomain(request, parent_domain_id=None):
    """Create new domain or subdomain"""
    parent_domain = None
    if parent_domain_id:
        parent_domain = get_object_or_404(Domain, id=parent_domain_id, user=request.user)
    
    if request.method == 'POST':
        form = DomainForm(request.POST, request.FILES)
        if form.is_valid():
            domain = form.save(commit=False)
            domain.user = request.user
            if parent_domain:
                domain.parent = parent_domain
            domain.save()
            messages.success(request, "Domain created successfully!")
            return redirect('domain_list')
    else:
        form = DomainForm()
    
    return render(request, "domains/domain_form.html", {
        'form': form,
        'parent_domain': parent_domain
    })

@login_required
def domain_update(request, domain_id):
    """Edit existing domain"""
    domain = get_object_or_404(Domain, id=domain_id, user=request.user)
    
    if request.method == 'POST':
        form = DomainForm(request.POST, request.FILES ,instance=domain)
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

@login_required
def item_create(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id, user=request.user)
    
    if request.method == 'POST':
        item_form = ItemForm(request.POST, request.FILES)
        translation_form = TranslationForm(request.POST)
        
        if item_form.is_valid() and translation_form.is_valid():
            # Save Item first
            item = item_form.save(commit=False)
            item.domain = domain
            item.user = request.user

            prompt = item_form.cleaned_data.get('generation_prompt')
            if prompt:
                try:
                    image_file = generate_image_from_prompt(prompt)
                    item.image.save(f"ai_generated_{item.id}.png", image_file, save=False)
                    item.ai_generated = True
                    item.generation_prompt = prompt
                except Exception as e:
                    messages.error(request, f"Image generation failed: {str(e)}")
                    return redirect('domain_detail', domain_id=domain.id)
                
            item.save()
            
            # Save Translation
            translation = translation_form.save(commit=False)
            translation.item = item
            translation.user = request.user
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

@login_required
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id, domain__user=request.user)
    translations = item.translations.all()
    
    return render(request, "items/item_detail.html", {
        'item': item,
        'translations': translations
    })

@login_required
def item_update(request, item_id):
    item = get_object_or_404(Item, id=item_id, domain__user=request.user)
    
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

@login_required
def item_delete(request, item_id):
    item = get_object_or_404(Item, id=item_id, domain__user=request.user)
    if request.method == 'POST':
        domain_id = item.domain.id
        item.delete()
        messages.success(request, "Item deleted successfully!")
        return redirect('domain_detail', domain_id=domain_id)
    
    return render(request, "items/item_confirm_delete.html", {'item': item})

# ==================== ITEM VIEWS ====================

@login_required
def translation_create(request, item_id):
    item = get_object_or_404(Item, id=item_id, domain__user=request.user)
    
    if request.method == 'POST':
        form = TranslationForm(request.POST)
        if form.is_valid():
            translation = form.save(commit=False)
            translation.item = item
            translation.user = request.user
            translation.save()
            messages.success(request, "New translation added successfully!")
            return redirect('item_detail', item_id=item.id)
    else:
        form = TranslationForm(initial={'is_primary': False})
    
    return render(request, "items/translation_form.html", {
        'form': form,
        'item': item
    })

@login_required
def translation_update(request, translation_id):
    translation = get_object_or_404(Translation, id=translation_id, user=request.user)
    item = translation.item
    
    if request.method == 'POST':
        form = TranslationForm(request.POST, instance=translation)
        if form.is_valid():
            form.save()
            messages.success(request, "Translation updated successfully!")
            return redirect('item_detail', item_id=item.id)
    else:
        form = TranslationForm(instance=translation)
    
    return render(request, "items/translation_form.html", {
        'form': form,
        'item': item,
        'translation': translation,
        'is_edit': True
    })

@login_required
def translation_delete(request, translation_id):
    translation = get_object_or_404(Translation, id=translation_id, user=request.user)
    item = translation.item
    
    if request.method == 'POST':
        translation.delete()
        messages.success(request, "Translation deleted successfully!")
        return redirect('item_detail', item_id=item.id)
    
    return render(request, "items/translation_confirm_delete.html", {
        'translation': translation,
        'item': item
    })