# Network

[Website](#)
[GitHub](#)
[YouTube](#)

---

This Django project displays on the home page (**/**) a list of posts (maximum characters are 126) paginated by 10. If the user is authenticated, a form appears where the user can write a brand new post.

Each post displayed contains a link with the name of the author who wrote the post. That link directs the user to a page that list all of that user's posts (**/<username>**), paginated by 10 posts. Logged in users have the option of following the user profiled on that page, and unfollowing if the user is following.

A logged in user can visit a page (**/following**) where every user followed by the authenticated user is displayed (again paginated by 10).

The main pages all display lists of posts. If an authenticated user wrote a post, he or she can toggle an edit form to post new data. At the bottom of the post is a black heart with a number. This is the number of likes a post has. Authenticated users can click on the heart to like a post, and the user can click on a liked post to unlike it.

## Environment Variables

The base directory need to have an **.env** file to work properly, with the minimum of these settings:

| Name | Description |
|------| ------------|
|DEBUG | If true, web project is running in debug mode.
|SECRET_KEY| A string of characters used for securing signed data|
|DATABASE_URL| The URL for the database. For development, `sqlite:///.db` can be used for SQLite.
|ALLOWED HOSTS|A comma-delimited list of hosts allowed to run site.

The project uses [django-environ](https://django-environ.readthedocs.io/en/latest/) to handle environment variables and settings.

## config/

The main Django directory.

**asgi.py** - The main ASGI file.

**settings.py** - The main settings file.

**urls.py** - The main url file.

**wsgi.py** - The main WSGI file.

## api/

Folder contains Django REST Framework views, permissions, urls, and serializers.

**apps.py** - File used to install the app in **config/settings.py.**

**permissions.py** - File containing class that secures posts from being changed by users who
did not write it (`IsAuthorOrReadOnly`)

**serializers.py** - File that classes that convert JSON into Python types (and vice versa).

**urls.py** - The urls for the app.

**views.py** - The views for the app.

## posts/

App that handles posts for the web application.

**migrations/** - Folder holding the migrations for the app. The framework generates the migration files.

**admin.py** - File for handling how the admin works with Post models.

**apps.py** - File used to install the app in **config/settings.py.**

**forms.py** - File that contains a Django Model Form for pushing Posts to database.

**models.py** - Contains the Post model.

**urls.py** - The urls belonging to the app.

**views.py** - The views for the app. Note: `context_object_name` is `posts` for views capable of displaying multiple posts.

## static/

This folder contains the static files for the project. It contains two folders.

### css

Contains **styles.css**, the custom style sheet for the app. The application uses CSS, not SCSS.

## js

Contains **index.js**, the file responsible for allowing data updates for Posts, Likes, and Follows without a full page refresh. There are four event handlers wrapped inside of a `DOMContentLoaded` event handler:

|name|description
|---|---|
|handleLinkClick|Toggles edit panel and content panel|
handleFormSubmit|Submits the new content for the post|
|handleLikeClick|Toggles liking and unliking and sends data to server|
handleFollowClick|Toggles following and unfollowing and sends data to server.|

## templates

Directory that contains the templae files.

**base.html** - The base template for the application.

### account/

Directory for custom [allauth](https://django-allauth.readthedocs.io/en/latest/)

### includes/

Directory for different UI widgets that appear in the project.

**navbar.html** - The bootstrap navigation bar.

**pagination.html** - 'Prev' and 'Next' links that appear if the page is paginated.

**post_card.html** - The card that holds the post data buttons for likes and editing, and editing form.

**post_form.html** - Form for writing new post. Form uses [Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)

**post_list.html** - Template for displaying a list of posts, and a message if there are no posts.

### posts/

Django templates for the main pages in the project.

**index.html** - Displays all of the posts.

**profile.html** - Displays all of the posts for a particular user.

**following.html** - Displays all of the posts an authenticated user is following.

## tests/

Directory that contains unit tests for the application. The project uses [pytest](https://docs.pytest.org/en/stable/) and [pytest-django](https://pytest-django.readthedocs.io/en/latest/) for application testing.

### api/
Module that tests the api endpoints. Contains only **test_views.py** and **__init__.py** files.

### posts/

Module that tests views and models for the **posts** app. Contains **test_views.py**,
**test_models.py** and **__init__.py** files.

### users/
Module that tests **CustomUser** model. Contains only **test_models.py** and **__init__.py** files.

**conftest.py** - Contains the fixtures used throughout the application.

**factories.py** - Creates dummy test data to be used for testing.

## users/

App that handles **CustomUser** for the web application.

**migrations/** - Folder holding the migrations for the app. The framework generates the migration files.

**admin.py** - File for handling how the admin works with **CustomUser**.

**apps.py** - File used to install the app in **config/settings.py.**

**forms.py** - File that contains the custom forms for **CustomUser**.

**models.py** - Contains the **CustomUser** model.

## .coveragerc

File containing options for running **coverage.py** test coverage.

## pytest.ini

