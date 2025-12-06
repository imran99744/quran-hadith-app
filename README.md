<<<<<<< HEAD
# quran-hadith-app



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

* [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
* [Add files using the command line](https://docs.gitlab.com/topics/git/add_files/#add-files-to-a-git-repository) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/imranops/quran-hadith-app.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

* [Set up project integrations](https://gitlab.com/imranops/quran-hadith-app/-/settings/integrations)

## Collaborate with your team

* [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
* [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
* [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
* [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
* [Set auto-merge](https://docs.gitlab.com/user/project/merge_requests/auto_merge/)

## Test and Deploy

Use the built-in continuous integration in GitLab.

* [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/)
* [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
* [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
* [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
* [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
=======
# Quran Hadith API

A comprehensive FastAPI backend for Quran and Hadith application with PostgreSQL database.

## Features

- **Quran Data Management**
  - Complete Surah and Ayah database
  - Juz (section) support
  - Arabic text with English translations
  - Search functionality in Arabic and English
  - Random verse functionality

- **Hadith Data Management**
  - Multiple collections (Sahih Bukhari, Sahih Muslim, etc.)
  - Book and chapter organization
  - Arabic text with English translations
  - Authentication grading (Sahih, Hasan, Da'if)
  - Advanced search and filtering

- **User Management**
  - JWT-based authentication
  - User registration and login
  - Admin user support
  - Protected endpoints

- **API Features**
  - RESTful API design
  - Automatic API documentation (OpenAPI/Swagger)
  - Pagination support
  - Search and filtering
  - CORS support
  - Health checks

## Technology Stack

- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Documentation**: OpenAPI/Swagger
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd quran-hadith-app
```

2. Start the application:
```bash
docker-compose up --build
```

3. Access the API:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL database and update `.env`:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. Run database migrations/seed:
```bash
python -m app.db.seed
```

4. Start the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info

### Quran
- `GET /api/v1/quran/surahs` - List all surahs
- `GET /api/v1/quran/surahs/{surah_number}` - Get specific surah
- `GET /api/v1/quran/surahs/{surah_number}/ayahs` - Get surah with all ayahs
- `GET /api/v1/quran/surahs/{surah_number}/ayahs/{ayah_number}` - Get specific ayah
- `GET /api/v1/quran/juzs` - List all juzs
- `GET /api/v1/quran/juzs/{juz_number}` - Get specific juz
- `GET /api/v1/quran/juzs/{juz_number}/ayahs` - Get ayahs in juz
- `GET /api/v1/quran/search` - Search Quran
- `GET /api/v1/quran/random-ayah` - Get random ayah

### Hadith
- `GET /api/v1/hadith/collections` - List all collections
- `GET /api/v1/hadith/collections/{collection_id}` - Get specific collection
- `GET /api/v1/hadith/collections/{collection_id}/books` - Get books in collection
- `GET /api/v1/hadith/collections/{collection_id}/hadiths` - Get hadiths in collection
- `GET /api/v1/hadith/books/{book_id}` - Get specific book
- `GET /api/v1/hadith/books/{book_id}/hadiths` - Get hadiths in book
- `GET /api/v1/hadith/hadiths/{hadith_id}` - Get specific hadith
- `GET /api/v1/hadith/chapters/{chapter_id}` - Get specific chapter
- `GET /api/v1/hadith/chapters/{chapter_id}/hadiths` - Get hadiths in chapter
- `GET /api/v1/hadith/search` - Search hadiths
- `GET /api/v1/hadith/random-hadith` - Get random hadith

## Sample Data

The application comes with sample data including:
- **Admin User**: `admin` / `admin123`
- **Quran Data**: 3 Surahs with complete Al-Fatihah ayahs
- **Hadith Data**: Sahih Bukhari and Sahih Muslim collections with sample hadiths

To populate the database:
```bash
python -m app.db.seed
```

## API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

Run tests with:
```bash
pytest
```

## Environment Variables

Key environment variables in `.env`:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/quran_hadith_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME="Quran Hadith API"
APP_VERSION="1.0.0"
DEBUG=True
```

## Database Schema

### Tables
- `users` - User authentication and management
- `surahs` - Quran chapters
- `ayahs` - Quran verses
- `juzs` - Quran sections
- `collections` - Hadith collections (Bukhari, Muslim, etc.)
- `books` - Books within collections
- `hadiths` - Individual hadith records
- `chapters` - Chapters within books

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- CORS configuration
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy ORM

## Development

### Adding New Data
1. Add records to database via API or direct database operations
2. Use the seed script pattern for bulk data import
3. Follow the existing schema patterns

### API Extensions
- Add new routes in `app/api/routes/`
- Follow the existing patterns for authentication and database access
- Update schemas in `app/schemas/`

## Production Deployment

1. Update environment variables
2. Use a production-ready PostgreSQL instance
3. Configure proper CORS origins
4. Set up reverse proxy (nginx)
5. Implement SSL/TLS
6. Set up monitoring and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License.
>>>>>>> d440e5e (Initial commit: Complete Quran Hadith API with FastAPI and Terraform infrastructure)
