from .models import Plans


class PlanService:

    def get_plan(self):
        # TODO: Hozirgi oydagi planni olish logikasini yozish kerak
        return Plans.objects.first()
