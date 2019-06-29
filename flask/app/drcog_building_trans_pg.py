def filterTags(attrs):
	if not attrs: return
	tags = {}
	#Add the source
	tags.update({'source':'DRCOG PLANIMETRICS DATA'})
	
	#tags.update({'building':'yes'})
	if attrs['bldg_type']:
		tags.update({'building':attrs['bldg_type'].strip(' ')})
	
	if attrs['housenumbr']:
		tags.update({'addr:housenumber':attrs['housenumbr'].strip(' ')})
		
	if attrs['city']:
		tags.update({'addr:city':attrs['city'].strip(' ')})		

	if attrs['street']:
		tags.update({'addr:street':attrs['street'].strip(' ')})		
	
	if attrs['state']:
		tags.update({'addr:state':'CO'})			
	
	if attrs['zip']:
		tags.update({'addr:postcode':attrs['zip'].strip(' ')})			

	if attrs['bldg_ht_m']:
		tags.update({'height':attrs['bldg_ht_m'].strip(' ')})		
	return tags
