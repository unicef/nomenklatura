var config = {
    'APP_NAME': "{{app_name}}",
    'APP_VERSION': "{{app_version}}",
    'NOMENKLATURA_ROOT': "{{ui_root}}",
    'API_ROOT': "{{api_root}}",
    'SCHEMA_OBJS': {{schema_objs}}
};

angular.module('nomenklatura.config', [])
    .constant('config',config);
