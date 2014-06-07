var nomenklatura = angular.module('nomenklatura', ['ngRoute', 'ngUpload', 'ui.bootstrap']);

nomenklatura.config(['$routeProvider', '$locationProvider', '$sceProvider',
    function($routeProvider, $locationProvider, $sceProvider) {

  $routeProvider.when('/', {
    templateUrl: 'home.html',
    controller: HomeCtrl
  });

  $routeProvider.when('/docs/:page/:anchor', {
    templateUrl: 'pages/template.html',
    controller: DocsCtrl
  });

  $routeProvider.when('/docs/:page', {
    templateUrl: 'docs/template.html',
    controller: DocsCtrl
  });

  $routeProvider.when('/datasets/:name', {
    templateUrl: 'datasets/view.html',
    controller: DatasetsViewCtrl
  });

  $routeProvider.when('/datasets/:dataset/uploads/:upload', {
    templateUrl: 'mapping.html',
    controller: MappingCtrl
  });

  $routeProvider.when('/datasets/:dataset/review/:what', {
    templateUrl: 'review.html',
    controller: ReviewCtrl
  });

  $routeProvider.when('/entities/:id', {
    templateUrl: 'entities/view.html',
    controller: EntitiesViewCtrl
  });

  $locationProvider.html5Mode(false);
  //$sceProvider.enabled(false);
}]);

//function visitPath(o, path) {
//  window.location.reload(true);
//}


nomenklatura.handleFormError = function(form) {
  return function(data, status) {
    if (status == 400) {
        var errors = [];
        for (var field in data.errors) {
            form[field].$setValidity('value', false);
            form[field].$message = data.errors[field];
            errors.push(field);
        }
        if (angular.isDefined(form._errors)) {
            angular.forEach(form._errors, function(field) {
                if (errors.indexOf(field) == -1) {
                    form[field].$setValidity('value', true);
                }
            });
        }
        form._errors = errors;
    } else {
      // TODO: where is your god now?
      if (angular.isObject(data) && data.message) {
        alert(data.message);
      }
      //console.log(status, data);
    }
  };
};
