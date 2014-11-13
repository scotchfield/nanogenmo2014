import flickrapi
import os
import random
import urllib

def getPhotos( flickr, search ):
    print( 'Searching for {0}'.format( search ) )
    photo_obj = flickr.photos.search(
        text = '{0} recipe'.format( search ),
        sort = 'relevance',
        per_page = 100
    )
    return photo_obj[ 'photos' ][ 'photo' ]

def getListFromFile( filename ):
    obj = []
    input_file = open( filename, 'r' )
    for line in input_file:
        obj.append( line.strip() )
    input_file.close()
    return obj

def getFile( url, url_filename ):
    if os.path.isfile( 'cache/{0}'.format( url_filename ) ):
        return

    print( 'File does not exist!' )

    urllib.urlretrieve( url, 'cache/{0}'.format( url_filename ) )

def getFood( prefix_obj, food_obj, suffix_obj ):
    food = []

    if random.randint( 1, 10 ) < 6:
        food.append( random.choice( prefix_obj ) )

    food.append( random.choice( prefix_obj ) )
    f = random.choice( food_obj )
    food.append( f )

    if random.randint( 1, 10 ) < 6:
        food.append( random.choice( suffix_obj ) )

    return ( f, ' '.join( food ) )

def getIngredient( food_obj, measure_obj, quantity_obj ):
    food = random.choice( food_obj ).lower()
    measure = random.choice( measure_obj ).split( ',' )
    quantity = random.choice( quantity_obj )

    if quantity in [ '1', 1, 'one' ]:
        amount = '{0} {1}'.format( quantity, measure[ 0 ] )
    else:
        amount = '{0} {1}'.format( quantity, measure[ 1 ] )

    return ( food, amount )

def getRecipe( prefix_obj, food_obj, suffix_obj, measure_obj, quantity_obj,
               combine_obj ):
    food = getFood( prefix_obj, food_obj, suffix_obj )

    ig_obj = []
    for i in range( random.randint( 5, 20 ) ):
        ig_obj.append(
            getIngredient( food_obj, measure_obj, quantity_obj ) )

    random.shuffle( ig_obj )
    instructions = []

    while ig_obj:
        combine = random.choice( combine_obj )
        if len( ig_obj ) < 2 and combine.find( '{1}' ) > -1:
            continue

        combine_ig = []

        if combine.find( '{1}' ) > -1:
            combine_ig.append( ig_obj.pop()[ 0 ].lower() )
        if combine.find( '{0}' ) > -1:
            combine_ig.append( ig_obj.pop()[ 0 ].lower() )

        while len( combine_ig ) < 2:
            combine_ig.append( '' )

        c = combine.format( combine_ig[ 0 ], combine_ig[ 1 ] )
        instructions.append( c )

    return ( food, ig_obj, instructions )

def writeHtml( param_obj, output_filename, n ):
    ( flickr, prefix_obj, food_obj, suffix_obj, measure_obj,
        quantity_obj, combine_obj, api_key ) = param_obj

    output_file = open( output_filename, 'w' )
    output_file.write( "<html><head><title>Delicious Recipes</title>" )
    output_file.write( "</head>\n<body>\n" )

    for i in range( n ):
        ( food, ig_obj, instructions ) = getRecipe(
            prefix_obj, food_obj, suffix_obj, measure_obj,
            quantity_obj, combine_obj )

        output_file.write( "<h1>{0}</h1>\n".format( food[ 1 ] ) )

        if len( api_key ) > 0:
            photo_obj = getPhotos( flickr, food[ 0 ] )
            if 0 == len( photo_obj ):
                print( 'No photos found for {0}!'.format( food[ 0 ] ) )
                continue

            photo = random.choice( photo_obj )

            url_filename = '{0}_{1}.jpg'.format(
                photo[ 'id' ], photo[ 'secret' ] )
            url = 'https://farm{0}.staticflickr.com/{1}/{2}'.format(
                photo[ 'farm' ], photo[ 'server' ], url_filename )

            getFile( url, url_filename )

            output_file.write( '<img src="cache/{0}">'.format( url_filename ) )

        print( food[ 1 ] )
        print( '--------' )

        ig_obj.sort()
        output_file.write( '<ul>' )
        for ig in ig_obj:
            output_file.write( '<li>{0} {1}</li>'.format( ig[ 1 ], ig[ 0 ] ) )
            print( '{0} {1}'.format( ig[ 1 ], ig[ 0 ] ) )
        output_file.write( '</ul>' )

        output_file.write( "<p>{0}</p>\n".format( ' '.join( instructions ) ) )
        print( ' '.join( instructions ) )

    output_file.write( '</body>' )


def main():
    prefix_obj = getListFromFile( 'prefix.txt' )
    food_obj = getListFromFile( 'food.txt' )
    suffix_obj = getListFromFile( 'suffix.txt' )
    measure_obj = getListFromFile( 'measure.txt' )
    quantity_obj = getListFromFile( 'quantity.txt' )
    combine_obj = getListFromFile( 'combine.txt' )

    api_key = u''
    api_secret = u''

    flickr = flickrapi.FlickrAPI( api_key, api_secret, format='parsed-json' )

    param_obj = ( flickr, prefix_obj, food_obj, suffix_obj, measure_obj,
                  quantity_obj, combine_obj, api_key )

    writeHtml( param_obj, 'new_recipe.html', 2 )


if __name__ == "__main__":
    main()
