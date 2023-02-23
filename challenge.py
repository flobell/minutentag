"""
Refactor the next function using yield to return the array of objects found by the
`s3.list_objects_v2` function that matches the given prefix.
"""
def get_s3_objects(bucket, prefix=''):
    s3 = boto3.client('s3')

    kwargs = {'Bucket': bucket}
    next_token = None
    if prefix:
        kwargs['Prefix'] = prefix
    while True:
        if next_token:
            kwargs['ContinuationToken'] = next_token
        resp = s3.list_objects_v2(**kwargs)
        contents = resp.get('Contents', [])
        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix):
                yield obj
        next_token = kwargs.get('NextContinuationToken', None)
        if not next_token:
            break


"""
Please, explain and document iterations, conditionals, and the
function as a whole
"""
def fn(main_plan, obj, str_id, pm, extensions=[]):
    """
        It process a list of product with price and quantities, compares with 
        the main plan price resulting on a list of products with identifiers,
        price, quantities and a flag indicating if it is deleted.

    
        Arguments:
            main_plan <Price object>: main plan price
            obj dict: a dictionary with a key item and value of array of Item objects, { 'items': [<Item object>] }
            str_id str: an string identifier
            pm <PaymentMethod object>: payment method
            extension array: an array of dicts, [ {'price': <Price object>, 'qty': int } ]

        Returns:
            A list of dict
    """

    items = []
    sp = False
    cd = False

    ext_p = {}

    for ext in extensions:
        ext_p[ext['price'].id] = ext['qty']

    for item in obj['items'].data:
        product = {
            'id': item.id
        }

        if item.price.id != main_plan.id and item.price.id not in ext_p:
            product['deleted'] = True
            cd = True
        elif item.price.id in ext_p:
            qty = ext_p[item.price.id]
            if qty < 1:
                product['deleted'] = True
            else:
                product['qty'] = qty
            del ext_p[item.price.id]
        elif item.price.id == main_plan.id:
            sp = True

        items.append(product)
    
    if not sp:
        items.append({
            'price': main_plan.id,
            'quantity': 1
        })
    
    for price, qty in ext_p.items():
        if qty < 1:
            continue
        items.append({
            'price': price,
            'quantity': qty
        })
    
    kwargs = {
        'items': items,
        'default_payment_method': pm.id,
        'api_key': API_KEY,
    }
    
    return items


"""
Having the class `Caller` and the function `fn`
Refactor the function `fn` to execute any method from `Caller` using the argument `fn_to_call`
reducing the `fn` function to only one line.
"""
class Caller:
    add = lambda a, b : a + b
    concat = lambda a, b : f'{a},{b}'
    divide = lambda a, b : a / b
    multiply = lambda a, b : a * b

def fn(fn_to_call, *args): execute=dict(add=Caller.add(*args), concat=Caller.concat(*args), divide=Caller.divide(*args), multiply=Caller.multiply(*args)); return execute[fn_to_call]


"""
A video transcoder was implemented with different presets to process different videos in the application. The videos should be
encoded with a given configuration done by this function. Can you explain what this function is detecting from the params
and returning based in its conditionals?
"""
def fn(config, w, h):
    """
        It returns a configuration for encoding the video, compares
        the width and height of the presets with the given in config.

        Arguments:
            config dict: configuration for video encoding
            w float: width of the presets
            h float: height of the presets

        Returns:
            A list of dicts which have the configuration for the video to be encoded.
    """

    v = None
    ar = w / h

    if ar < 1:
        v = [r for r in config['p'] if r['width'] <= w]
    elif ar > 4 / 3:
        v = [r for r in config['l'] if r['width'] <= w]
    else:
        v = [r for r in config['s'] if r['width'] <= w]

    return v


"""
Having the next helper, please implement a refactor to perform the API call using one method instead of rewriting the code
in the other methods.
"""
import requests
class Helper:
    DOMAIN = 'http://example.com'
    SEARCH_IMAGES_ENDPOINT = 'search/images',
    GET_IMAGE_ENDPOINT = 'image',
    DOWNLOAD_IMAGE_ENDPOINT = 'downloads/images'


    AUTHORIZATION_TOKEN = {
        'access_token': None,
        'token_type': None,
        'expires_in': 0,
        'refresh_token': None
    }

    def callAPI(self, endpoint:str, method:str, **kwargs):
        token_type = self.AUTHORIZATION_TOKEN['token_type']
        access_token = self.AUTHORIZATION_TOKEN['access_token']

        headers = {
            'Authorization': f'{token_type} {access_token}',
        }

        send = {
            'headers': headers,
            'data': kwargs
        }

        URL = f'{self.DOMAIN}/{endpoint}'

        request = dict(
            POST=requests.get(URL, **send),
            GET=requests.get(URL, **send),
            DELETE=requests.delete(URL, **send),
            PUT=requests.delete(URL, **send),
        )

        return request[method]

    def search_images(self, **kwargs):
        return self.callAPI(f'{self.SEARCH_IMAGES_ENDPOINT}', 'GET', **kwargs)
        
    def get_image(self, image_id, **kwargs):
        return self.callAPI(f'{self.GET_IMAGE_ENDPOINT}/{image_id}', 'GET', **kwargs)
    
    def download_image(self, image_id, **kwargs):
        return self.callAPI(f'{self.DOWNLOAD_IMAGE_ENDPOINT}/{image_id}', 'POST', **kwargs)