from django.core.management.base import BaseCommand
from job.models import Job, Category
from django.contrib.auth.models import User
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Add sample jobs for each category'

    def handle(self, *args, **kwargs):
        # Get or create a company user
        company_user, created = User.objects.get_or_create(
            username='sample_company',
            defaults={
                'email': 'company@example.com',
                'is_staff': True
            }
        )
        if created:
            company_user.set_password('company123')
            company_user.save()

        # Sample job data for each category
        jobs_data = {
            'Information Technology': {
                'title': 'Senior Software Developer',
                'description': 'Looking for an experienced software developer to join our team.',
                'requirements': '5+ years of experience in Python/Django development',
                'responsibilities': 'Develop and maintain web applications',
                'job_type': 'Full Time',
                'job_level': 'Senior',
                'salary_min': 80000,
                'salary_max': 120000,
                'experience_min': 5,
                'experience_max': 10,
                'skills': 'Python, Django, JavaScript, React'
            },
            'Marketing & Sales': {
                'title': 'Digital Marketing Manager',
                'description': 'Lead our digital marketing initiatives and drive growth.',
                'requirements': '3+ years in digital marketing',
                'responsibilities': 'Develop and execute marketing strategies',
                'job_type': 'Full Time',
                'job_level': 'Mid Level',
                'salary_min': 60000,
                'salary_max': 90000,
                'experience_min': 3,
                'experience_max': 7,
                'skills': 'SEO, Social Media, Analytics'
            },
            'Finance & Accounting': {
                'title': 'Financial Analyst',
                'description': 'Join our finance team to analyze and report on financial data.',
                'requirements': 'Bachelor\'s in Finance or related field',
                'responsibilities': 'Financial analysis and reporting',
                'job_type': 'Full Time',
                'job_level': 'Mid Level',
                'salary_min': 65000,
                'salary_max': 95000,
                'experience_min': 2,
                'experience_max': 5,
                'skills': 'Financial Analysis, Excel, Accounting'
            },
            'Healthcare': {
                'title': 'Registered Nurse',
                'description': 'Provide quality patient care in our healthcare facility.',
                'requirements': 'Valid RN license',
                'responsibilities': 'Patient care and medical procedures',
                'job_type': 'Full Time',
                'job_level': 'Mid Level',
                'salary_min': 55000,
                'salary_max': 85000,
                'experience_min': 1,
                'experience_max': 5,
                'skills': 'Patient Care, Medical Procedures'
            },
            'Education': {
                'title': 'High School Teacher',
                'description': 'Join our education team to inspire young minds.',
                'requirements': 'Teaching certification',
                'responsibilities': 'Classroom teaching and student development',
                'job_type': 'Full Time',
                'job_level': 'Mid Level',
                'salary_min': 45000,
                'salary_max': 75000,
                'experience_min': 2,
                'experience_max': 8,
                'skills': 'Teaching, Curriculum Development'
            },
            'Engineering': {
                'title': 'Mechanical Engineer',
                'description': 'Design and develop mechanical systems.',
                'requirements': 'Bachelor\'s in Mechanical Engineering',
                'responsibilities': 'System design and development',
                'job_type': 'Full Time',
                'job_level': 'Mid Level',
                'salary_min': 70000,
                'salary_max': 100000,
                'experience_min': 3,
                'experience_max': 7,
                'skills': 'CAD, Mechanical Design'
            },
            'Design & Creative': {
                'title': 'UI/UX Designer',
                'description': 'Create beautiful and functional user interfaces.',
                'requirements': '3+ years in UI/UX design',
                'responsibilities': 'Design user interfaces and experiences',
                'job_type': 'Full Time',
                'job_level': 'Mid Level',
                'salary_min': 60000,
                'salary_max': 90000,
                'experience_min': 3,
                'experience_max': 6,
                'skills': 'Figma, Adobe XD, UI/UX Design'
            },
            'Customer Service': {
                'title': 'Customer Support Specialist',
                'description': 'Provide excellent customer service and support.',
                'requirements': '2+ years in customer service',
                'responsibilities': 'Handle customer inquiries and support',
                'job_type': 'Full Time',
                'job_level': 'Entry Level',
                'salary_min': 35000,
                'salary_max': 55000,
                'experience_min': 1,
                'experience_max': 3,
                'skills': 'Customer Service, Communication'
            },
            'Human Resources': {
                'title': 'HR Manager',
                'description': 'Lead our human resources department.',
                'requirements': '5+ years in HR management',
                'responsibilities': 'HR operations and employee relations',
                'job_type': 'Full Time',
                'job_level': 'Senior',
                'salary_min': 70000,
                'salary_max': 100000,
                'experience_min': 5,
                'experience_max': 10,
                'skills': 'HR Management, Employee Relations'
            },
            'Operations & Logistics': {
                'title': 'Supply Chain Manager',
                'description': 'Manage our supply chain operations.',
                'requirements': '4+ years in supply chain management',
                'responsibilities': 'Oversee supply chain operations',
                'job_type': 'Full Time',
                'job_level': 'Mid Level',
                'salary_min': 65000,
                'salary_max': 95000,
                'experience_min': 4,
                'experience_max': 8,
                'skills': 'Supply Chain, Logistics'
            },
            'Legal': {
                'title': 'Corporate Lawyer',
                'description': 'Join our legal team for corporate matters.',
                'requirements': 'Law degree and bar admission',
                'responsibilities': 'Handle corporate legal matters',
                'job_type': 'Full Time',
                'job_level': 'Senior',
                'salary_min': 90000,
                'salary_max': 150000,
                'experience_min': 5,
                'experience_max': 12,
                'skills': 'Corporate Law, Legal Research'
            },
            'Research & Science': {
                'title': 'Research Scientist',
                'description': 'Conduct scientific research and analysis.',
                'requirements': 'PhD in relevant field',
                'responsibilities': 'Research and data analysis',
                'job_type': 'Full Time',
                'job_level': 'Senior',
                'salary_min': 75000,
                'salary_max': 120000,
                'experience_min': 3,
                'experience_max': 8,
                'skills': 'Research, Data Analysis'
            },
            'Media & Communications': {
                'title': 'Content Writer',
                'description': 'Create engaging content for various platforms.',
                'requirements': '2+ years in content writing',
                'responsibilities': 'Content creation and editing',
                'job_type': 'Full Time',
                'job_level': 'Mid Level',
                'salary_min': 45000,
                'salary_max': 75000,
                'experience_min': 2,
                'experience_max': 5,
                'skills': 'Content Writing, SEO'
            },
            'Hospitality & Tourism': {
                'title': 'Hotel Manager',
                'description': 'Manage our hotel operations.',
                'requirements': '3+ years in hotel management',
                'responsibilities': 'Oversee hotel operations',
                'job_type': 'Full Time',
                'job_level': 'Mid Level',
                'salary_min': 55000,
                'salary_max': 85000,
                'experience_min': 3,
                'experience_max': 7,
                'skills': 'Hotel Management, Customer Service'
            },
            'Construction & Real Estate': {
                'title': 'Project Manager',
                'description': 'Manage construction and real estate projects.',
                'requirements': '4+ years in project management',
                'responsibilities': 'Project planning and execution',
                'job_type': 'Full Time',
                'job_level': 'Mid Level',
                'salary_min': 70000,
                'salary_max': 100000,
                'experience_min': 4,
                'experience_max': 8,
                'skills': 'Project Management, Construction'
            }
        }

        # Create jobs for each category
        for category_name, job_data in jobs_data.items():
            try:
                category = Category.objects.get(name=category_name)
                
                # Create the job
                job = Job.objects.create(
                    owner=company_user,
                    title=job_data['title'],
                    company_name='Sample Company',
                    company_description='A leading company in various industries',
                    location='New York, NY',
                    description=job_data['description'],
                    requirements=job_data['requirements'],
                    responsibilities=job_data['responsibilities'],
                    job_type=job_data['job_type'],
                    job_level=job_data['job_level'],
                    category=category,
                    salary_min=job_data['salary_min'],
                    salary_max=job_data['salary_max'],
                    experience_min=job_data['experience_min'],
                    experience_max=job_data['experience_max'],
                    skills=job_data['skills'],
                    vacancy=1,
                    is_active=True,
                    is_featured=True,
                    slug=slugify(job_data['title'])
                )
                
                self.stdout.write(self.style.SUCCESS(f'Created job: {job.title} in {category_name}'))
                
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Category not found: {category_name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating job for {category_name}: {str(e)}')) 