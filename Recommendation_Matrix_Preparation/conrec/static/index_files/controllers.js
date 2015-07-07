'use strict';

/* Controllers */

var phonecatApp = angular.module('phonecatApp', ["checklist-model",'ngSanitize', 'ui.select']);

phonecatApp.controller('PhoneListCtrl', function($scope, $http) {


  $scope.foursquare = [
    {'name': 'Nexus S1','id': 'asdaweqw1'},
	{'name': 'Nexus S2','id': 'asdaweqw2'},
	{'name': 'Nexus S3','id': 'asdaweqw3'},
	{'name': 'Nexus S4','id': 'asdaweqw4'},
    {'name': 'Nexus S5','id': 'asdaweqw5'},
    {'name': 'Nexus S6','id': 'asdaweqw6'},
	{'name': 'Nexus S7','id': 'asdaweqw7'},
	{'name': 'Nexus S8','id': 'asdaweqw8'},
	{'name': 'Nexus S9','id': 'asdaweqw9'},
    {'name': 'Nexus S10','id': 'asdaweqw10'}
	];


	$http.get('../categories').
	success(function(data, status, headers, config)
	{
		$scope.foursquare = data;
	}).
	error(function(data, status, headers, config) {
		alert("Fetching the foursquare poi failed!")
	});

	$scope.categories = [{ "name" : "Banana", "foursquare" : []}, 
						 { "name" : "Orange", "foursquare" : []}, 
						 { "name" : "Apple", "foursquare" : []}, 
						 { "name" : "Mango", "foursquare" : []}];

	$scope.cat_index = 0;

	$scope.time_intervals = [[1,2,3,4],[1,2,3,4],[1,2,3,4]];
	$scope.time_interval_names = ["asd", "bsd", "fsd"];

	$scope.activities = ["sitting", "walking", "standing", "upstairs", "downstairs"];
	$scope.selected_activities = [];

	$scope.addCategories = function()
	{
		$scope.categories.push({'name' : 'Banana', 'foursquare' : []});
		$scope.allocateMatrix();
	};

	$scope.removeCategories = function()
	{
		$scope.categories.pop();
		$scope.allocateMatrix();
	};

	$scope.addInterval = function()
	{
		$scope.time_intervals.push([1,2,3,4]);
		$scope.time_interval_names.push("Interval name");
		$scope.allocateMatrix();
	};

	$scope.removeInterval = function()
	{
		$scope.time_intervals.pop()
		$scope.time_interval_names.pop();
		$scope.allocateMatrix();
	};

	$scope.allocateMatrix = function()
	{
		$scope.matrix = new Array($scope.time_intervals.length * $scope.selected_activities.length);
		for(var i = 0; i < $scope.selected_activities.length * $scope.time_intervals.length; i++)
		{
			$scope.matrix[i] = new Array($scope.categories.length)
		}
	};

	$scope.post = function()
	{
		var data = { periods : [], categories : [], activities : $scope.selected_activities,  matrix : $scope.matrix }
		
		for(var i = 0; i < $scope.time_intervals.length; i++)
		{
			var interval = {};
			interval[$scope.time_interval_names[i]] = $scope.time_intervals[i];
			data.periods.push(interval);
		}
		
		for(var i = 0; i < $scope.categories.length; i++)
		{
			var category = {};
			category[$scope.categories[i].name] = $scope.categories[i].foursquare;
			data.categories.push(category);
		}
		
		console.log(JSON.stringify(data));
		$http.post('../matrix', data).
		success(function(data, status, headers, config) {
			alert("Data sent!")
		}).
		error(function(data, status, headers, config) {
			alert("Sending failed!");
		});
	};

});
