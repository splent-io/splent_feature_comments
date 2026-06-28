// Entry point for splent_feature_comments frontend assets.
// Add your JavaScript here. Webpack compiles this into assets/dist/splent_feature_comments.bundle.js
//
// To load the compiled bundle in the product layout, register it in hooks.py:
//
//   from splent_framework.hooks.template_hooks import register_template_hook
//   from flask import url_for
//
//   def comments_scripts():
//       return '<script src="' + url_for("comments.assets", subfolder="dist", filename="splent_feature_comments.bundle.js") + '"></script>'
//
//   register_template_hook("layout.scripts", comments_scripts)
