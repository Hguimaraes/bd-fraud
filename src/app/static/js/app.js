'use strict';

var app = angular.module('ifds', ['ngRoute']);

app.constant('config', {
  baseURL: ""
});

app.config(function ($routeProvider, $locationProvider) {
    $routeProvider
      .when('/', {
        controller: 'HomeCtrl'
      })

      // use the HTML5 History API
      $locationProvider.html5Mode(true);
      $locationProvider.hashPrefix('');
});

app.controller("HomeCtrl", function ($scope, $routeParams, $location, $http, $window) {
  
});