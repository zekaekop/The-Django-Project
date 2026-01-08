from django.shortcuts import render
from admin_panel.forms import ContactusForm

# Create your views here.


class Info:

    def about_us(request):
        return render(request, "info/about.html")

    def contact_us(request):
        form = ContactusForm(request.POST or None)

        if form.is_valid():
            contact = form.save(commit=False)

            # Attach user only if logged in
            if request.user.is_authenticated:
                contact.user = request.user

            contact.save()

            return render(
                request,
                "info/contact.html",
                {
                    "form": ContactusForm(),
                    "title": "Info",
                    "success": True,
                }
            )

        return render(
            request,
            "info/contact.html",
            {
                "form": form,
                "title": "Info",
            }
        )