# Job Board / Recruitment API — Full Spec

## 1. User Roles

Same pattern as your Hospital Management API's `CustomUser` + role field.

```python
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
```

- **Recruiter** → owns a `Company`, posts jobs, moves applications through states, schedules interviews.
- **Candidate** → applies to jobs, views/withdraws own applications.
- **Admin** → full access, moderation.

---

## 2. Models

```python
class Company(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class JobPosting(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )
    STATUS_CHOICES = (('open', 'Open'), ('closed', 'Closed'))

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    skills = models.CharField(max_length=500, help_text="comma-separated")
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    search_vector = SearchVectorField(null=True)  # for full-text search
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [GinIndex(fields=['search_vector'])]


class ScreeningQuestion(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)


class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    )
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job_posting', 'candidate')  # one application per job


class ApplicationAnswer(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(ScreeningQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField()


class Interview(models.Model):
    MODE_CHOICES = (('onsite', 'Onsite'), ('remote', 'Remote'), ('phone', 'Phone'))
    STATUS_CHOICES = (('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled'))

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    scheduled_at = models.DateTimeField()
    interviewer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
```

---

## 3. Application State Machine

```
applied → screening → interview → offer → hired
   ↓           ↓            ↓         ↓
withdrawn   rejected     rejected  rejected
```

Rules to enforce in serializer `validate()`:
- Only recruiter who owns the job's company can move status **forward** (applied→screening→interview→offer→hired) or to `rejected`.
- Only the candidate can move their own application to `withdrawn`, and only if status is `applied` or `screening` (can't withdraw after an offer, business rule you can justify however you like).
- No skipping stages forward (applied can't jump straight to offer) — but rejection can happen from any non-terminal state.
- Terminal states (`hired`, `rejected`, `withdrawn`) can't transition anywhere.

```python
VALID_TRANSITIONS = {
    'applied': ['screening', 'rejected', 'withdrawn'],
    'screening': ['interview', 'rejected', 'withdrawn'],
    'interview': ['offer', 'rejected'],
    'offer': ['hired', 'rejected'],
    'hired': [],
    'rejected': [],
    'withdrawn': [],
}
```

---

## 4. Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register as candidate or recruiter |
| POST | `/api/auth/login/` | Returns JWT access + refresh |
| POST | `/api/auth/refresh/` | Refresh access token |

### Companies
| Method | Endpoint | Who | Description |
|---|---|---|---|
| POST | `/api/companies/` | Recruiter | Create company profile (one per recruiter) |
| GET | `/api/companies/<id>/` | Any | View company + its open jobs |
| PATCH | `/api/companies/<id>/` | Owner | Update company |

### Job Postings
| Method | Endpoint | Who | Description |
|---|---|---|---|
| GET | `/api/jobs/` | Any | List/search/filter jobs |
| POST | `/api/jobs/` | Recruiter | Create job posting (nested screening questions) |
| GET | `/api/jobs/<id>/` | Any | Job detail |
| PATCH | `/api/jobs/<id>/` | Owner recruiter | Edit job / close it |
| DELETE | `/api/jobs/<id>/` | Owner recruiter | Delete |

**Search/filter query params:** `?search=django+backend&location=Kathmandu&job_type=remote&min_salary=50000`


//continue from here

### Applications
| Method | Endpoint | Who | Description |
|---|---|---|---|
| POST | `/api/jobs/<id>/apply/` | Candidate | Submit application (nested resume + answers) |
| GET | `/api/applications/` | Candidate: own / Recruiter: for their jobs | List, filterable by `?status=` |
| GET | `/api/applications/<id>/` | Owner candidate or owning recruiter | Detail |
| PATCH | `/api/applications/<id>/status/` | Recruiter (forward/reject) or Candidate (withdraw) | State transition |

### Interviews
| Method | Endpoint | Who | Description |
|---|---|---|---|
| POST | `/api/applications/<id>/interviews/` | Recruiter | Schedule interview |
| GET | `/api/applications/<id>/interviews/` | Recruiter or candidate | List interviews for an application |
| PATCH | `/api/interviews/<id>/` | Recruiter | Update notes/status |

---

## 5. Sample Payloads

### Create job posting (nested screening questions)
`POST /api/jobs/`
```json
{
  "title": "Backend Developer (Django)",
  "description": "Build and maintain REST APIs...",
  "requirements": "2+ years Django, DRF, PostgreSQL",
  "skills": "django,drf,postgresql,docker",
  "location": "Kathmandu",
  "job_type": "full_time",
  "salary_min": 60000,
  "salary_max": 90000,
  "questions": [
    { "question_text": "Years of Django experience?" },
    { "question_text": "Are you comfortable with on-site work in Kathmandu?" }
  ]
}
```
This is a **writable nested serializer** — the `JobPostingSerializer` overrides `create()` to pop `questions` data and bulk-create related `ScreeningQuestion` objects, similar to how you'd handle nested writes anywhere else, just one level deeper than your Hospital API's flat serializers.

### Apply to a job (nested resume + answers in one request)
`POST /api/jobs/14/apply/`
```json
{
  "resume": "<file upload, multipart/form-data>",
  "cover_letter": "I'm excited to apply because...",
  "answers": [
    { "question": 1, "answer_text": "3 years" },
    { "question": 2, "answer_text": "Yes" }
  ]
}
```
Since this includes a file (`resume`), the request must be `multipart/form-data`, not JSON — worth practicing since your Hospital API was probably pure JSON. The serializer's `create()` pulls `answers` out of `validated_data`, creates the `Application`, then bulk-creates `ApplicationAnswer` rows tied to it.

### Update application status (recruiter advances candidate)
`PATCH /api/applications/22/status/`
```json
{ "status": "interview" }
```
Response:
```json
{
  "id": 22,
  "status": "interview",
  "updated_at": "2026-08-06T10:15:00Z"
}
```
The serializer's `validate_status()` checks the transition against `VALID_TRANSITIONS` and raises `ValidationError` if invalid, and `has_object_permission` checks whether the requesting user is the owning recruiter (for forward/reject) or the candidate (for withdraw only).

### Schedule an interview
`POST /api/applications/22/interviews/`
```json
{
  "scheduled_at": "2026-08-12T14:00:00Z",
  "mode": "remote",
  "notes": "Technical round — DRF + system design"
}
```

### Search jobs
`GET /api/jobs/?search=django backend&location=Kathmandu`
Uses `SearchVector('title', 'description', 'requirements', 'skills')` + `SearchQuery` in the queryset, or `django_filters` combined with Postgres full-text search via a custom filter backend.

---

## 6. Permissions Structure

```python
class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'recruiter'

class IsJobOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.company.owner == request.user

class IsApplicationCandidateOrJobOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.candidate == request.user or obj.job_posting.company.owner == request.user
        # for status PATCH — check who can do what inside the view/serializer logic
        return obj.candidate == request.user or obj.job_posting.company.owner == request.user
```

Note the same distinction you nailed in the Hospital project: `get_queryset()` filters *what a user can see*, `has_object_permission` gates *what they can do* to a specific object once fetched. For `Application`, `get_queryset()` should return `Application.objects.filter(candidate=user)` for candidates and `Application.objects.filter(job_posting__company__owner=user)` for recruiters — never let a candidate query filter leak into what a recruiter is allowed to touch.

---

## 7. `SerializerMethodField` vs Annotated Queryset — where it applies here

- **`applicant_count`** on `JobPostingSerializer` → annotate in `get_queryset()`: `.annotate(applicant_count=Count('applications'))`. Faster, works with ordering/filtering.
- **`is_applied`** (whether the *current* requesting candidate already applied to this job) → must be a `SerializerMethodField`, since it depends on `request.user`, which annotation can't access without a subquery keyed to the request — same lesson you hit in the blog project with annotated fields vs `@property`.

---

## 8. Suggested Build Order

1. `CustomUser` + role-based registration/login (JWT)
2. `Company` CRUD (recruiter-only creation)
3. `JobPosting` CRUD + nested `ScreeningQuestion` create
4. Full-text search on `JobPosting` (`SearchVector`, `GinIndex`)
5. `Application` submission with nested `ApplicationAnswer` + file upload
6. Status state machine + permissions
7. `Interview` scheduling
8. Filtering/pagination polish (`django-filter`, `PageNumberPagination`)
