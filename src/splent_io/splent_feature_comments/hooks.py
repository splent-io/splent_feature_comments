from flask import render_template, request, url_for

from splent_framework.hooks.template_hooks import register_template_hook
from splent_framework.services.service_locator import service_proxy


def post_comments(post):
    """Rendered into the post detail through the 'post.comments' hook.

    Receives the current post and renders the approved comments plus the
    submission form (with a Turnstile widget if cloudflare is installed).
    """
    comments = service_proxy("CommentsService").approved_for(post.id)
    return render_template("comments/thread.html", post=post, comments=comments)


def comments_sidebar_link():
    active = (
        "active"
        if request.endpoint and request.endpoint.startswith("comments.admin")
        else ""
    )
    pending = 0
    try:
        pending = len(service_proxy("CommentsService").pending())
    except Exception:
        pass
    badge = f' <span class="badge bg-danger">{pending}</span>' if pending else ""
    return (
        f'<li class="sidebar-item {active}">'
        f'<a class="sidebar-link" href="{url_for("comments.admin_index")}">'
        '<i class="align-middle" data-feather="message-square"></i> '
        f'<span class="align-middle">Comments</span>{badge}</a></li>'
    )


register_template_hook("post.comments", post_comments)
register_template_hook("layout.authenticated_sidebar", comments_sidebar_link)
