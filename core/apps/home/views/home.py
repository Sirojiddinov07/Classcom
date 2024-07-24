from django import shortcuts, views


class HomeView(views.View):
    def get(self, request):
        return shortcuts.render(request, "user/home.html")
