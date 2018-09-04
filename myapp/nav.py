from flask import g
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask import url_for
nav = Nav()

@nav.navigation()
def mynavbar():
    items = [View('Home', 'index')]
    if g.user is None:
        items.append(View('Register', 'auth.register'))
        items.append(View('Login', 'auth.login'))
    else:
        items.append(View('Chat', 'index'))
        items.append(View('Logout', 'auth.logout'))

    return Navbar('SP',*items)

