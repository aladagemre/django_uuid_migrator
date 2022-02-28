# Django UUID Migrator

When you want to add a unique UUIDField to your Django model, creating 3 consecutive migration files is necessary to avoid unique constraint violation.

This app automatically creates 3 migration scripts for a given Django model so that the model has unique uuid field after the operation.

* Migration 1: Add uuid field with null=True
* Migration 2: Populate db with random uuid.
* Migration 3: Add unique constraint to uuid field (remove null allowance).

See Django Migrations Documentation - [Migrations that add unique fields](https://docs.djangoproject.com/en/dev/howto/writing-migrations/#migrations-that-add-unique-fields) section for more information.

# Installation

If you don't use `pipx`, you're missing out.
Here are [installation instructions](https://github.com/pypa/pipx).

Simply run:

    $ pipx install .


# Usage

To use it:

    $ uuid-migrator /Users/user/projects/bookstore/bookstore/books Book

Arguments are:

* the folder path containing the app (/Users/user/projects/bookstore/bookstore/books)
* model name (Book)
