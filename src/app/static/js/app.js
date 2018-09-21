'use strict';

var app = angular.module('ifds', ['ngRoute', 'chart.js']);

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

app.controller("DoughnutCtrl", function ($scope, $http, $interval) {
	// Chart options for bargraph
  $scope.chartOptions = {
        scales: {
            xAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
  };

  // Initialize parameters
  $scope.labels = ['Fraude', 'Legítimo']
  $scope.data_bargraph = [0, 0]
  $scope.data_doughnut = [0, 0]

  var data_request = function(){
    // Request data to python API
    var req = {
      method: 'GET',
      url: '/stats'
    }

    $http(req).then(function(response){
      var num_fraud = response.data.fraud;
      var num_legit = response.data.legit;
      var sum_total = num_fraud + num_legit  
      $scope.data_bargraph = [num_fraud, num_legit]
      $scope.data_doughnut = [num_fraud/sum_total, num_legit/sum_total]

    }, function(err){ 
      // Help to debug
      console.log(err);
    });
  };

  $interval(data_request, 500);

});