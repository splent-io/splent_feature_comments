from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from splent_io.splent_feature_comments import comments_bp
from splent_io.splent_feature_comments.models import Comment
from splent_io.splent_feature_comments.signals import (
    comment_created,
    comment_submitting,
)
from splent_framework.db import db
from splent_framework.services.service_locator import service_proxy

comments_service = service_proxy("CommentsService")


# =====================================================================
# PUBLIC — submit a comment (rendered into the post via the hook)
# =====================================================================
@comments_bp.route("/comments/<int:post_id>", methods=["POST"])
def create(post_id):
    # Let any listener (a captcha provider, a spam filter…) veto the submission.
    # comments knows nothing about captchas — they connect to this signal.
    results = comment_submitting.send(
        None, post_id=post_id, form=request.form, remoteip=request.remote_addr
    )
    if any(value is False for _, value in results):
        flash("Spam check failed — please try again.", "danger")
        return redirect(request.referrer or url_for("post.index"))

    name = (request.form.get("author_name") or "").strip()
    content = (request.form.get("content") or "").strip()
    if not (name and content):
        flash("Name and comment are required.", "danger")
        return redirect(request.referrer or url_for("post.index"))

    comment = Comment(
        post_id=post_id,
        author_name=name,
        author_email=(request.form.get("author_email") or "").strip(),
        content=content,
        approved=False,
    )
    db.session.add(comment)
    db.session.commit()
    comment_created.send(None, comment=comment)
    flash("Your comment was submitted and is awaiting moderation.", "success")
    return redirect(request.referrer or url_for("post.index"))


# =====================================================================
# ADMIN — moderation
# =====================================================================
@comments_bp.route("/admin/comments", methods=["GET"])
@login_required
def admin_index():
    return render_template(
        "comments/admin/list.html", comments=comments_service.all_comments()
    )


@comments_bp.route("/admin/comments/<int:comment_id>/approve", methods=["POST"])
@login_required
def admin_approve(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.approved = True
    db.session.commit()
    flash("Comment approved.", "success")
    return redirect(url_for("comments.admin_index"))


@comments_bp.route("/admin/comments/<int:comment_id>/delete", methods=["POST"])
@login_required
def admin_delete(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash("Comment removed.", "success")
    return redirect(url_for("comments.admin_index"))
