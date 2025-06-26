import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    salary_min = django_filters.NumberFilter(field_name='salary', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary', lookup_expr='lte')
    
    # Dynamically get unique locations from the Job model
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get unique locations and create choices
        locations = Job.objects.values_list('location', flat=True).distinct().order_by('location')
        location_choices = [('', 'Select Location')] + [(loc, loc) for loc in locations if loc]
        self.filters['location'].extra['choices'] = location_choices
        self.filters['location'].extra['empty_label'] = 'Select Location'
        
        # Add CSS classes for better styling
        self.filters['location'].field.widget.attrs.update({
            'class': 'form-control',
            'style': 'cursor: pointer;'
        })
        self.filters['category'].field.widget.attrs.update({
            'class': 'form-control',
            'style': 'cursor: pointer;'
        })

    location = django_filters.ChoiceFilter(
        field_name='location', 
        lookup_expr='exact',
        empty_label='Select Location'
    )
    
    class Meta:
        model = Job
        fields = '__all__'
        exclude = [
            'owner', 'published_at', 'image', 'slug',
            'description', 'requirements', 'responsibilities',
            'vacancy', 'is_featured', 'skills',
            'experience', 'experience_min', 'experience_max' , 'company_description','is_active','salary'
        ]