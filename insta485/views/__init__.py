"""Views, one for each Insta485 page."""
from insta485.views.index import show_index
from insta485.views.user import show_user, check_in_db
from insta485.views.users_followers import show_followers
from insta485.views.users_following import show_following
from insta485.views.logout import logout
from insta485.views.explore import show_explore
from insta485.views.post import show_post
from insta485.views.likes import likes
from insta485.views.comments import comments
from insta485.views.accounts_post import post_account
from insta485.views.accounts_get import create, delete, edit, password, login
from insta485.views.following import post_following
from insta485.views.post_posts import post_posts
