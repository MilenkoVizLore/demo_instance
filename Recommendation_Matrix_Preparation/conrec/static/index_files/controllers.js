'use strict';

/* Controllers */

var phonecatApp = angular.module('phonecatApp', ["checklist-model",'ngSanitize', 'ui.select']);

phonecatApp.controller('PhoneListCtrl', function($scope, $http) {

	$scope.activities = ["sitting", "walking", "standing", "upstairs", "downstairs"];
	$scope.hours = [];
	$scope.minutes = [];
	
	for(var i = 0; i < 24; i++)
		$scope.hours.push(i);
	
	for(var i = 0; i < 60; i++)
		$scope.minutes.push(i);
	
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
		alert("Foursquare data not loaded!")
	});

	$scope.categories = [{ "name" : "Cat 1", "foursquare" : []}];

	$scope.addCategories = function()
	{
		$scope.categories.push({'name' : 'Cat', 'foursquare' : []});
		
		for(var i = 0; i < $scope.profiles.length; i++)
		{
			$scope.profiles[i].array.push(0);
		}
	};

	$scope.removeCategories = function()
	{
		$scope.categories.pop();
		
		for(var i = 0; i < $scope.profiles.length; i++)
		{
			$scope.profiles[i].array.pop();
		}
	};
	
	$scope.profiles = [];
	
	$scope.addProfile = function()
	{
		var vector = [];
		
		for(var i = 0; i < $scope.categories.length; i++)
			vector.push(0);
	
		$scope.profiles.push({ 
			"name" : "",
			"time" : [[0,0,0,0]], 
			"activity" : [], 
			"array" : vector
		});
	};
	
	$scope.removeProfile = function()
	{
		$scope.profiles.pop();
	};
	
	$scope.addInterval = function(profile)
	{
		profile.time.push([0,0,0,0]);
	};
	
	$scope.removeInterval = function(profile)
	{
		profile.time.pop();
	};

	$scope.validate = function()
	{
		for(var i in $scope.categories)
		{
			if($scope.categories[i].foursquare.length == 0)
				return false;
		}
		return true;
	};

	$scope.post = function()
	{
		if(!$scope.validate())
		{
			alert("You must select a foursquare category for each category!");
			return false;
		}

		var data = { "categories" : $scope.categories, "profiles" : $scope.profiles};
		
		console.log(data);
		$http.post('../matrix', data).
		success(function(data, status, headers, config) {
			alert(data)
		}).
		error(function(data, status, headers, config) {
			alert("Sending failed!");
		});
	};
});
