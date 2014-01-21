var app = angular.module("orgApp", [])
	.config(function($interpolateProvider){
	        $interpolateProvider.startSymbol('[[').endSymbol(']]');
	    }
	);

app.controller('BillingController', ['$scope', function($scope) {

}]);