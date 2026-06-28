"""Signals emitted by the comments feature.

comments stays decoupled from anti-spam: it emits ``comment-submitting`` and any
listener (a captcha provider, a spam filter…) may return False to veto the
submission. ``comment-created`` fires after a comment is stored, for things like
notifications or counters.
"""

from splent_framework.signals.signal_utils import define_signal

comment_submitting = define_signal("comment-submitting", "splent_feature_comments")
comment_created = define_signal("comment-created", "splent_feature_comments")
