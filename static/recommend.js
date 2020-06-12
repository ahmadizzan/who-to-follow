$(document).ready(function(){

	var queryString = window.location.search;
	var urlParams = new URLSearchParams(queryString);
	var username = urlParams.get('username');
	var limit = urlParams.get('limit');

	function updateLoadBar(text) {
		$('.load-bar').text(text)
	}

	function generateWhyFollowText(followedByList) {
		let length = followedByList.length;
		let text = 'Followed by '
		if (length <= 2) {
			text += followedByList.join(', ');
		} else {
			text += followedByList.slice(0, 2).join(', ') + ' and at least ' + (length - 2) + ' others';
		}
		return text;
	}

	function renderRecommendationResult(profile) {
		let result = '';
		result += '<div class="result-item">';
		result +=   '<div class="result-wrap">'
		result +=     '<div class="result-wrap-text">';
		result += 	    '<a href="https://twitter.com/' + profile['profile']['username'] + '"><p class="result-name">' + profile['profile']['name'] + '</a></p>';
		result +=       '<p class="result-bio">' + profile['profile']['bio'] + '</p>';
		result +=     '</div>';
		result +=     '<div class="result-wrap-img">';
		result +=       '<img class="result-img" src="' + profile['profile']['profile_photo'] + '"></img>';
		result +=     '</div>';
		result +=   '</div>';
		result +=   '<p class="result-why"><b>Why follow?</b></p>';
		result +=   '<p class="result-why">' + profile['why'] + '</p>';
		result += '</div>';
		return result;
	}

	
  	// Get following list.
  	updateLoadBar('Fetching people you followed recently...')
  	$.ajax({
		url: '/followings/' + username + '?limit=' + limit,
		type: 'GET',
		dataType: 'json',
		success: function(data){
			updateLoadBar('Analyzing following list...');
			var followingList = data['following_list'];
			var first = true;
			var chain = $.Deferred();
			var looper = $.Deferred().resolve();

			var counter = {};
			var followedBy = {};

			$.when.apply($, $.map(followingList, function(followingUsername, i) {
				looper = looper.then(function() {
					let deferred = $.Deferred();

				    $.ajax({
						url: '/followings/' + followingUsername + '?limit=' + '60',
						type: 'GET',
						dataType: 'json',
						success: function(data) {
							console.log('Analyzing @' + followingUsername + ' recent follows...');
							updateLoadBar('Analyzing @' + followingUsername + ' recent follows...')
							console.log(data);

							for (let childUsername of data['following_list']) {
								if (childUsername == username || childUsername in followingList) {
									continue;
								}
								if (!(childUsername in counter)) {
									counter[childUsername] = 0;
									followedBy[childUsername] = [];
								}
								counter[childUsername]++;
								followedBy[childUsername].push(followingUsername);
							}

							deferred.resolve();
							
						},
						error: function() {
							deferred.resolve();
						}
					})

				    return deferred.promise();
				});

				return looper;
			})).then(function() {
				updateLoadBar('Based on the people you followed...');

				var sortable = [];
				for (var key in counter) {
				sortable.push([key, counter[key]]);
				}

				sortable.sort(function(a, b) {
					return b[1] - a[1];
				});

				var finalList = [];

				var maxResult = 10;
				for (var i = 0; i < sortable.length; i++) {
					if (maxResult == 0) {
						break;
					}
					let resultUsername = sortable[i][0];
					finalList.push({
						username: resultUsername,
						why: generateWhyFollowText(followedBy[resultUsername])
					})
					maxResult--;
				}

				var looper = $.Deferred().resolve();
				$.when.apply($, $.map(finalList, function(obj, i) {
					looper = looper.then(function() {
						let deferred = $.Deferred();

					    $.ajax({
							url: '/profile/' + obj['username'],
							type: 'GET',
							dataType: 'json',
							success: function(data) {
								console.log('Getting profile @' + obj['username']);
								console.log(data);

								obj['profile'] = data['profile'];
								$('.result').append(renderRecommendationResult(obj))

								deferred.resolve();
								
							}
						})

					    return deferred.promise();
					});

					return looper;
				})).then(function() {
					console.log('ALL DONE')
				});
			});

		}
	})

});