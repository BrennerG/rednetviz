# ALGORITHM FOR rednetviz

substore = ['r/a', 'r/b', ...]
refstore = [
	{
		'source' : 'r/a',
		'target' : 'r/b',
		'value' : 'x'
	},
	...
]

for sub in subreddit
	if sub not in substore:
		for post in sub
			post.check_for_refs()
			if refstore.checkifexists()
				refstore.ref.value++
			else
				refstore.newref
	else:
		pass
