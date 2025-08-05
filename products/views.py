# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse, HttpResponseBadRequest
# from products.models import Product
# from products.forms import ProductForm


# def product_list(request):
#     products = Product.objects.all().order_by("-created_at")
#     return render(request, "products/list.html", {"products": products})


# def product_create(request):
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             product = form.save()
#             return render(
#                 request, "products/partial_product.html", {"product": product}
#             )
#         else:
#             return render(request, "products/form.html", {"form": form})
#     else:
#         form = ProductForm()
#     return render(request, "products/form.html", {"form": form})


# def product_update(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == "POST":
#         form = ProductForm(request.POST, instance=product)
#         if form.is_valid():
#             product = form.save()
#             return render(
#                 request, "products/partial_product.html", {"product": product}
#             )
#     else:
#         form = ProductForm(instance=product)
#     return render(request, "products/form.html", {"form": form, "product": product})


# def product_delete(request, pk):
#     if request.method == "POST":
#         product = get_object_or_404(Product, pk=pk)
#         product.delete()
#         return HttpResponse("")
#     return HttpResponseBadRequest("Invalid request")

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy

from .models import Product
from .forms import ProductForm


class ProductList(ListView):
    model = Product
    template_name = "new/list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")


class ProductCreate(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "new/form.html"

    def form_valid(self, form):
        product = form.save()
        html = render_to_string("new/partiallist.html", {"product": product})
        return HttpResponse(html)

    def form_invalid(self, form):
        return render_to_string("new/form.html", {"form": form})


class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "new/form.html"

    def form_valid(self, form):
        product = form.save()
        html = render_to_string("new/partiallist.html", {"product": product})
        return HttpResponse(html)

    def form_invalid(self, form):
        return render_to_string("new/form.html", {"form": form})


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy("new_product_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("")  # empty response to trigger HTMX removal
