from webassets import Bundle

from nomenklatura.core import assets

deps_assets = Bundle(
    'jquery/dist/jquery.js',
    'bootstrap/js/collapse.js',
    'angular/angular.js',
    'angular-route/angular-route.js',
    'angular-bootstrap/ui-bootstrap-tpls.js',
    'ngUpload/ng-upload.js',
    filters='uglifyjs',
    output='assets/deps.js'
)

app_assets = Bundle(
    'js/app.js',
    'js/services/session.js',
    'js/directives/pagination.js',
    'js/directives/keybinding.js',
    'js/directives/authz.js',
    'js/controllers/app.js',
    'js/controllers/import.js',
    'js/controllers/home.js',
    'js/controllers/docs.js',
    'js/controllers/review.js',
    'js/controllers/datasets.js',
    'js/controllers/entities.js',
    'js/controllers/profile.js',
    filters='uglifyjs',
    output='assets/app.js'
)

css_assets = Bundle(
    'bootstrap/less/bootstrap.less',
    'font-awesome/less/font-awesome.less',
    'style/style.less',
    filters='less,cssrewrite',
    output='assets/style.css'
)

assets.register('deps', deps_assets)
assets.register('app', app_assets)
assets.register('css', css_assets)
