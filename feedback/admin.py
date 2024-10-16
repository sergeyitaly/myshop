from django.contrib import admin
from django.db.models import Avg
from .models import Feedback, OverallAverageRating
from django.utils.safestring import mark_safe

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'comment', 'rating_1', 'rating_2', 'rating_3', 'rating_4', 'rating_5', 
                    'rating_6', 'rating_7', 'rating_8', 'rating_9', 'rating_10']
    readonly_fields = ['question1', 'answer1', 'question2', 'answer2']

    def save_model(self, request, obj, form, change):
        """Override to recalculate the overall average rating after saving a feedback."""
        super().save_model(request, obj, form, change)
        self.update_overall_average_ratings()

    def update_overall_average_ratings(self):
        """Calculate the overall average ratings and update the OverallAverageRating model."""
        feedbacks = Feedback.objects.all()
        avg_rating_1 = feedbacks.aggregate(Avg('rating_1'))['rating_1__avg'] or 0
        avg_rating_2 = feedbacks.aggregate(Avg('rating_2'))['rating_2__avg'] or 0
        avg_rating_3 = feedbacks.aggregate(Avg('rating_3'))['rating_3__avg'] or 0
        avg_rating_4 = feedbacks.aggregate(Avg('rating_4'))['rating_4__avg'] or 0
        avg_rating_5 = feedbacks.aggregate(Avg('rating_5'))['rating_5__avg'] or 0
        avg_rating_6 = feedbacks.aggregate(Avg('rating_6'))['rating_6__avg'] or 0
        avg_rating_7 = feedbacks.aggregate(Avg('rating_7'))['rating_7__avg'] or 0
        avg_rating_8 = feedbacks.aggregate(Avg('rating_8'))['rating_8__avg'] or 0
        avg_rating_9 = feedbacks.aggregate(Avg('rating_9'))['rating_9__avg'] or 0
        avg_rating_10 = feedbacks.aggregate(Avg('rating_10'))['rating_10__avg'] or 0

        overall_avg, created = OverallAverageRating.objects.get_or_create(id=1)
        overall_avg.avg_rating_1 = avg_rating_1
        overall_avg.avg_rating_2 = avg_rating_2
        overall_avg.avg_rating_3 = avg_rating_3
        overall_avg.avg_rating_4 = avg_rating_4
        overall_avg.avg_rating_5 = avg_rating_5
        overall_avg.avg_rating_6 = avg_rating_6
        overall_avg.avg_rating_7 = avg_rating_7
        overall_avg.avg_rating_8 = avg_rating_8
        overall_avg.avg_rating_9 = avg_rating_9
        overall_avg.avg_rating_10 = avg_rating_10
        overall_avg.save()

@admin.register(OverallAverageRating)
class OverallAverageRatingAdmin(admin.ModelAdmin):
    list_display = ['ratings_table']
    readonly_fields = ['ratings_table']

    def has_add_permission(self, request):
        """Prevent creating new OverallAverageRating instances through the admin."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the OverallAverageRating instance."""
        return False

    def ratings_table(self, obj):
        """Return a table displaying the average ratings for each aspect."""
        table_html = f'''
        <table style="border-collapse: collapse; width: 50%;">
            <tr>
                <th style="border: 1px solid black; padding: 8px;">Aspect</th>
                <th style="border: 1px solid black; padding: 8px;">Average Rating</th>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 8px;">Aspect 1</td>
                <td style="border: 1px solid black; padding: 8px;">{obj.avg_rating_1}</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 8px;">Aspect 2</td>
                <td style="border: 1px solid black; padding: 8px;">{obj.avg_rating_2}</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 8px;">Aspect 3</td>
                <td style="border: 1px solid black; padding: 8px;">{obj.avg_rating_3}</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 8px;">Aspect 4</td>
                <td style="border: 1px solid black; padding: 8px;">{obj.avg_rating_4}</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 8px;">Aspect 5</td>
                <td style="border: 1px solid black; padding: 8px;">{obj.avg_rating_5}</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 8px;">Aspect 6</td>
                <td style="border: 1px solid black; padding: 8px;">{obj.avg_rating_6}</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 8px;">Aspect 7</td>
                <td style="border: 1px solid black; padding: 8px;">{obj.avg_rating_7}</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 8px;">Aspect 8</td>
                <td style="border: 1px solid black; padding: 8px;">{obj.avg_rating_8}</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 8px;">Aspect 9</td>
                <td style="border: 1px solid black; padding: 8px;">{obj.avg_rating_9}</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 8px;">Aspect 10</td>
                <td style="border: 1px solid black; padding: 8px;">{obj.avg_rating_10}</td>
            </tr>
        </table>
        '''
        return mark_safe(table_html)

    ratings_table.short_description = "Average Ratings Table"