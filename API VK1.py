def get_friends(user_id, fields):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    import requests
    domain = "https://api.vk.com/method"
    access_token = '1efb9991613d1e0c7597cae85db190f37bbda497579e92b05af4352bc694c66fd3883d0ff1b875b53a98d'
    user_id = user_id

    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(
        **query_params)
    response = requests.get(query)
    friends_list = response.json()['response']['items']
    return friends_list


def age_predict(user_id):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, 'bdate')
    count, sum_age = 0, 0
    for item in friends:
        if 'bdate' in item:
            if len(item['bdate']) > 5:
                count += 1
                sum_age += 2018 - int(item['bdate'][-4:])
    return sum_age // count


print(age_predict(6449222))
