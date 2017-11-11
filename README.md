# New Terms

* **g** - A global object that Flask uses for passing information between views and modules.
* **before_request** - A decorator to mark a function as running before the request hits a view.
* **after_request** - A decorator to mark a function as running before the response is returned.

# Authentication

## Loading users

You will need to provide a **user_loader** callback. This callback is used to reload the user object from the user ID stored in the session. It should take the unicode ID of a user, and return the corresponding user object. It should return None (not raise an exception) if the ID is not valid. (In that case, the ID will manually be removed from the session and processing will continue.)

* **LoginManager** - An appliance to handle user authentication.
* **user_loader** - A decorator to mark the function responsible for loading a user from whatever data source we use.
* **current_user** - Global object in templates that represents the current user.
* **is\_authenticated**  - Property on current_user that returns whether the user is authenticated or not.
* **get_flashed_messages(with_categories=True)** - Gets flashed messages with their categories.

## Creating forms

### Create a form model

### Create a form view

#### Add a route to the view
* form.validate_on_submit() - When the form is submitted through POST, make sure the data is valid.
* *Macro* - A custom, executable bit of templating.
* form.hidden_tag() - Renders hidden fields inside of a hidden <div>.

#### Login users

Parameter validation is not done on the script, but rather on the route config.

* login_user - Function to log a user in and set the appropriate cookie so they'll be considered authenticated by Flask-Login

#### Logout users

* logout_user() - Method to remove a user's session and sign them out.
* @login_required - Decorator to mark a view as requiring a user to be logged in before they can access the view.

# Foreign Keys in Peewee

Foreign keys are created using a special field class ```ForeignKeyField```. Each foreign key also creates a back-reference on the related model using the specified related_name.

**Note**

In SQLite, foreign keys are not enabled by default. Most things, including the Peewee foreign-key API, will work fine, but ON DELETE behaviour will be ignored, even if you explicitly specify on\_delete to your ForeignKeyField. In conjunction with the default PrimaryKeyField behaviour (where deleted record IDs can be reused), this can lead to surprising (and almost certainly unwanted) behaviour where if you delete a record in table A referenced by a foreign key in table B, and then create a new, unrelated, record in table A, the new record will end up mis-attached to the undeleted record in table B. To avoid the mis-attachment, you can use ```PrimaryKeyAutoIncrementField```, but it may be better overall to ensure that foreign keys are enabled with _pragmas=((‘foreign_keys’, ‘on’),)_ when you instantiate SqliteDatabase.

## Traversing foreign keys
Referring back to the User and Tweet models, note that there is a ForeignKeyField from Tweet to User. The foreign key can be traversed, allowing you access to the associated user instance:

```
>>> tweet.user.username
'charlie'
```