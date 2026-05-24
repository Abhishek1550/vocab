from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Domain
from .forms import DomainForm


def vocab(request):
    """Landing Page"""
    return render(request, "index.html")


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
            return redirect('domains:domain_list')
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
            return redirect('domains:domain_detail', domain_id=domain.id)
    else:
        form = DomainForm(instance=domain)
    
    return render(request, "domains/domain_form.html", {
        'form': form
    })