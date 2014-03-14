#Set up
You need to make a .project.ini file at the root of the project with the following contents:
[data1] 
MODE = dev ;can choose: dev | prod | preview | test
SECRET_KEY= <secret key here>
DB_NAME=	<db name here>
DB_HOST= 	<db host here>
DB_PORT= 	<db port here>
DB_USER=	<db port here>
DB_PW=		<db password>




#Structure of Repo

│__ .project.ini
│
├── headsOfState
│   ├── db.sqlite3
│   ├── headsOfState
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── ticTacToe
│       ├── admin.py
│       ├── migrations
│       │   ├── 0001_initial.py
│       │   └── __init__.py
│       ├── models.py
│       ├── static
│       │   ├── appframework
│       │   │   ├── af.ui.css
│       │   │   ├── appframework.ui.min.js
│       │   │   ├── icons.css
│       │   │   └── plugins
│       │   │       ├── af.8tiles.js
│       │   │       ├── af.actionsheet.js
│       │   │       ├── af.css3animate.js
│       │   │       ├── af.desktopBrowsers.js
│       │   │       ├── af.msPointerEvents.js
│       │   │       ├── af.passwordBox.js
│       │   │       ├── af.popup.js
│       │   │       ├── af.scroller.js
│       │   │       ├── af.selectBox.js
│       │   │       ├── af.slidemenu.js
│       │   │       ├── af.touchEvents.js
│       │   │       └── af.touchLayer.js
│       │   ├── css
│       │   │   └── app.css
│       │   ├── images
│       │   │   ├── gameIcon.png
│       │   │   ├── obama.png
│       │   │   └── putin.png
│       │   ├── js
│       │   │   ├── app_object.js
│       │   │   ├── computer_object.js
│       │   │   ├── grid_object.js
│       │   │   ├── initialize.js
│       │   │   ├── music_object.js
│       │   │   └── table_object.js
│       │   └── sounds
│       │       ├── music1.mp3
│       │       └── music2.mp3
│       ├── templates
│       │   ├── index.html
│       │   └── index.html~
│       ├── tests.py
│       ├── urls.py
│       └── views.py
└── readme.md

