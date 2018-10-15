[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://choosealicense.com/)

<a href="https://www.udacity.com/">
  <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo svg">
</a> 

# Job Market

## Synopsis

* `Docker` 
* `Python`
* `Flask` 
* `SQLAlchemy`
* `Google oAuth 2.0`
* `Marshmallow`
* `Flask-Dance`
* `pip-env`
* `git`

## Screens

![screen shot 2018-10-11 at 1 07 18 am](https://user-images.githubusercontent.com/4943759/46782936-318ac800-ccf6-11e8-8882-1909ec48a332.png)

![screen shot 2018-10-11 at 12 44 56 am](https://user-images.githubusercontent.com/4943759/46781311-f89b2500-ccee-11e8-8cca-7db4ab5ba128.png)

![screen shot 2018-10-11 at 12 54 56 am](https://user-images.githubusercontent.com/4943759/46781655-ae1aa800-ccf0-11e8-9215-633493a16738.png)

![screen shot 2018-10-11 at 1 04 03 am](https://user-images.githubusercontent.com/4943759/46782943-364f7c00-ccf6-11e8-92b2-124ed5ec5a7f.png)

## Values

* `Clean, Readable Code and Design.` 
* `Simplicity over Complexity.`
* `Automation.` 
* `UI/UX matter.` 
* `Build to scale.` 

## Design and Architecture

This application is organized around a MVC pattern. 

```bash
.
├── config
└── app
    ├── models      # Model
    ├── routes      # Controller
    ├── templates   # View
    ├── forms
    └── static
```
Modules and features are isolated and decoupled for single responsibility and seperation of concerns. 

Organized into Package modules to promote code readability, re-use and collaboration.

```bash
.
├── Dockerfile                # Dockerfile is optimized for pip-install Container caching.
├── config                      
│   └── settings.py           # Considered YAML, environment classes inherit from Default class.
├── docker-compose.yml
├── app
│   ├── egu-nyc-dev-001.db    # Required db objects are seeded with Faker.
│   ├── forms
│   │   └── item.py           # Create/Update re-leverage/share unified form.
│   ├── models
│   │   ├── category.py       # Hybrid property/expression to dynamically calc child relationships.
│   │   ├── item.py
│   │   └── user.py
│   ├── routes
│   │   ├── category.py
│   │   ├── errorhandlers.py
│   │   ├── item.py
│   │   ├── main.py           # Leveraged marshmallow for serialization. Single endpoint with nested children.
│   │   └── userauth.py       # Flashes a signal/instance of blueprint and token via Flask-Dance.
│   ├── services
│   ├── static
│   │   ├── img
│   │   │   └── google.png
│   │   └── styles
│   │       └── main.css
│   └── templates             # Limited and avoided logic in templates. Responsive bootstrap with modal window.
│       ├── errors
│       │   ├── 403.html      # Custom error handlers
│       │   ├── 404.html
│       │   └── 500.html
│       ├── item.html
│       ├── layout.html
│       └── main.html
├── manage.py
└── requirements.txt
```

### Hybrid Property vs sqlalchemy_utils @Aggregated

SQLAlchemy-Utils is a popular open source lib that allows for aggregated attributes using @aggregated decorator.

(https://sqlalchemy-utils.readthedocs.io/en/latest/aggregates.html)

The weakness is:

 * `@aggregated decorator requires maintaining an explicit column.` 
 * `when child is updated, the aggregation trigger does not fire.`

Solution: 

 * `@hybrid_property and hybrid_expression to develop this phantom/virtual property that
crosses functionality between class and instance.`


``` python

from sqlalchemy_utils import aggregated


class Thread(Base):
    __tablename__ = 'thread'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Unicode(255))

    @aggregated('comments', sa.Column(sa.Integer))
    def comment_count(self):
        return sa.func.count('1')

    comments = sa.orm.relationship(
        'Comment',
        backref='thread'
    )

```

(https://docs.sqlalchemy.org/en/latest/orm/extensions/hybrid.html)

``` python

    @hybrid_property
    def item_count(self):
        return len(self.items)

    @item_count.expression
    def item_count(cls):
        return (select([func.count(Item.id)])
                .where(Item.category_id == cls.id)
                .label("item_count"))
```

## API

```bash
{URI}/api/v1/catalog/json
```

## Installation

### Requirements

Docker (https://www.docker.com/get-started)

### Deploy

```bash
# Clone this repository using git
cd src/web
docker-compose up --build
# Navigate to http://localhost:8000/
```

### Destroy

```bash
docker-compose down -v
```


[(Back to top)](#top)
