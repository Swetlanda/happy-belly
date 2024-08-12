<img src="static/images/logo.jpg" alt="Happy Belly logo" width="120">

# Welcome to Happy Belly recipes

Welcome to Happy Belly Recipes – a responsive website where users can find easy-to-follow recipes, add their own culinary creations, and share them with other food enthusiasts. Users who are not registered, can browse recipes. By creating a personal account, users can add, edit and delete new recipes, as well as easily manage their own or favorites recipes. 

[View the live project here](https://happy-belly-recipes-b223bbac9b55.herokuapp.com/)

This website was created as a portfolio project for the Full-Stack Software Development Programme by the Code Institute .

# Table of Contents
- Purpose and Target Audience
- UX
- Agile Development
- Features implemented
- Features Left to Implement
- Technology used
- Testing and validation
- Bugs
- Deployment
- Resources
- Credits and acknowledgements

# Purpose and Target Audience 
- Problem Statement: 
	- Cooking enthusiasts and home chefs often struggle to find a user-friendly platform for sharing, discovering, and managing recipes. 
- Purpose: 
	- The Happy Belly recipe website aims to be a platform for creating, managing, and sharing recipes. It makes user interactions enjoyable, enhances recipe discovery with search and favourite options, and provides easy recipe management tools - create, edit and delete recipes. All recipes created are sent to admin for approval to ensure for security purposes.
- Target Audience:
	- Home Chefs: People who love cooking at home and want to share and find new recipes.
	- Cooking Enthusiasts: Passionate cooks who enjoy exploring recipes, sharing feedback, and connecting with others.
	- Beginners: New cooks looking for simple recipes, tips, and advice.
	- Food Bloggers: Creators who want to showcase their recipes and engage with their audience.

# UX
## Database planning

In the project, I used the Django AllAuth User Model and custom made models:

**Django AllAuth User Model:**

|       Name        |        Type         |  Key  |
|-------------------|---------------------|-------|
| `id`              | AutoField           |  PK   |
| `username`        | CharField           |       |
| `email`           | EmailField          |       |
| `password`        | CharField           |       |

**Custom-made Recipe Model:**

|       Name       |         Type         |  Key  |
|------------------|----------------------|-------|
| `title`          | CharField            |       |
| `user`           | User Model           |  FK   |
| `slug`           | SlugField            |       |
| `description`    | TextField            |       |
| `ingredients`    | TextField            |       |
| `instructions`   | TextField            |       |
| `tag`            | TaggableManager      |       |
| `status`         | IntegerField         |       |
| `image`          | CloudinaryField      |       |
| `image_alt`      | CharField            |       |
| `serving`        | IntegerField         |       |
| `created_on`     | DateTimeField        |       |
| `updated_on`     | DateTimeField        |       |

Additional model features:
- User relationship: Each recipe is linked to the user who created it via a foreign key.
- Null handling: If a user or recipe is deleted, the corresponding favorite entry is set to NULL rather than being deleted.
- Slug generation: Slugs are automatically generated from the title and are ensured to be unique using a method "generate_unique_slug". Also a method "populate_slug" is used to automatically populate the slug field before saving.
- Status field: Controls recipe visibility with 2 status - Draft and Published.
- Image management: Recipes can include images managed by Cloudinary. 
- Tags: TaggableManager enables flexible tagging for categorising recipes.
- Ordering: Recipes are displayed in descending order.

**Custom-made Favorite Model**

|       Name       |         Type         |  Key  |
|------------------|----------------------|-------|
| `user`           | ForeignKey (User)    |  FK   |
| `recipe`         | ForeignKey (Recipe)  |  FK   |


Additional model features:
- User relationship: Connects users to their favorite recipes via foreign keys.	
- Unique constraint: Ensures a user can favorite a recipe only once.
- Null handling: If a user or recipe is deleted, the corresponding favorite entry is set to NULL rather than being deleted.

## Design

### Wireframes
The Happy Belly recipes website is designed with Bootstrap to allow for responsivness so can be easily used on mobile, tablet and desktop devices.

I used Balsamiq to create the wireframes. They were served as initial thnking and evolved during the build in line with Agile methodology.

### Features
- Recipe listing:
	- Recipes are displayed as cards with an image, title, description, tags, user and posting date.
	- Recipe listings are paginated by 8 to improve loading times and user experience, with navigation controls for easy browsing.
	- Each recipe card is clickable, leading to a full detailed view of the recipe.
	
Welcome page

- Search:
	- Users can search for recipes by title, description, ingredients, or tags.



## Technology used
- Django: Web framework for building the site.
- Heroku: Platform for hosting and deployment.
- HTML & CSS: For page structure and custom styling.
- Bootstrap 5: Ensures responsive design.
- Python: Backend logic and processing.
- JavaScript: Additional functionality, like checking passwords to match during log in.
- PostgreSQL: Relational database system.
- Cloudinary: Image hosting service.
- Font Awesome: Icons for UI enhancement.
- Google Fonts: Custom typography.
- GitHub: Source code repository and project management.
- Git: Version control for code management.
- ChatGPT: create logo, images, content for the website and help during coding.\

# Testing and validation

##  Responsiveness
I used the Website Mockup Generator to test the website for responsivness

**Laptop**
![Screenshot of homepage view on laptop](/static/images/documentation/laptop.png)

**Tablet**
![Screenshot of homepage view on tablet](/static/images/documentation/tablet-black.png)

**Mobile**
![Screenshot of homepage view on mobile](/static/images/documentation/mobile-black.png)

# Bugs and Issues


# Deployment
I followed the  Django Deployment Instructions 2024 provided by Code of Institute
Repository was created in Git
Deployed to Heroku
Connected Secret Keys to config vars
Connected Code Institute PostGres Database

# Credits and acknowledgements
I would like to thank the following individuals and resources for their support and inspiration during this project:
- **Code Institute LMS Content**: For providing the educational materials that guided my learning process.
- **Course Facilitators**: Special thanks to Alexander and David Calikes for their support and  guidance.
- **Tutor Kevin Loughrey**: His SME sessions were important in shaping my approach and were a key resource throughout the project.
- **Rachel Cutler and the RecipMe Project**: Rachel's RecipMe project was a crucial reference for the structure and foundation of my work [RecipMe Django Cookbook](https://github.com/rachbry/recipme-django-cookbook/blob/main/README.md).
- **Influential Projects**: I also drew inspiration from the following projects for building my ReadMe file:
  - [The Beara Directory Blog](https://github.com/Gordon-Meade/thebearadirectoryblog?tab=readme-ov-file#technology-used)
  - [Sojourn Scribbles V3](https://github.com/katiejanecoughlan/sojourn-scribbles-V3?tab=readme-ov-file#technology-used)