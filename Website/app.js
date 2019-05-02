const search = instantsearch({
	appId: '41WVOJCLBK',
	apiKey: 'b49b156c22d16f2da5f23d131c97bc80',
	indexName: 'instant_search',
	urlSync: true;

});

search.addWidget(
	instantsearch.widgets.searchBox({
		container:'#search-input'
	})
	);
search.addWidget(
  instantsearch.widgets.hits({
	container:'#hits',
	hitsPerPage:10,
	templates:{
		item: document.getElementById('hit-template').innerHTML,
		empty:"We didn't find any thing <em>\"{{query}}\"<em>"
	}
  })
);
search.start();