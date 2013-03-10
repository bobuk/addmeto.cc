import json, ast, requests, sys
import pdb

# python 2/3 mismatch, no workaround
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

class user:
    # Example:
    # client = kippt_wrapper.user('myUsername','kjsdfklj2lhg323423klj42')
    def __init__(self, username, apitoken):
        self.username = username
        self.apitoken = apitoken
        self.header = {'X-Kippt-Username': username,
                       'X-Kippt-API-Token': apitoken,
                       'X-Kippt-Client': 'Kippt-Python-Wrapper,me@ThomasBiddle.com,https://github.com/thomasbiddle/Kippt-Projects',
                       'content-type': 'application/vnd.kippt.20120609+json'}

    # Check if our credentials are valid.
    # Example:
    # user.checkAuth()
    #
    # Return True on success and False on failure.
    def checkAuth(self):
        r = requests.get('https://kippt.com/api/account/', headers=self.header)
        if r.status_code is 200: return True
        else: return False

    # Get our lists.
    # Example:
    # meta, lists = user.getLists(offset = 5)
    # meta, lists = user.getLists(50, 5) # (limit, offset)
    # meta, lists = user.getLists()
    # x = meta['total_count']
    # for i in lists: print i['title'] ( Returns Python list of Kippt Lists )
    #
    # Available values in meta:
    # total_count, limit, offset
    # Available values in each list:
    # rss_url, updated, title, created, slug, id, resource_uri
    #
    # Returns data on success, and false on failure.
    def getLists(self, limit = 0, offset = 0):
        url = 'https://kippt.com/api/lists?limit=' + str(limit) + '&offset=' + str(offset)
        r = requests.get(url, headers=self.header)
        if r.status_code is 200: return r.json()['meta'], r.json()['objects']
        else: return False, False

    # Get a list.
    # Example:
    # myList = user.getList(54433)
    # x = myList['title']
    #
    # Available values in list:
    # rss_url, updated, title, created, slug, id, resource_uri
    #
    # Returns data on success, and false on failure.
    def getList(self, id):
        r = requests.get('https://kippt.com/api/lists/' + str(id), headers=self.header)
        if r.status_code is 200: return r.json
        else: return False

    # Get list collaborators
    # Example:
    # myCollabs = user.getListCollab(54433)
    # for i in myCollabs: print i['username']
    #
    # Available values in list:
    # username, avatar_url, id, resource_uri
    #
    # Returns data on success, and false on failure.
    def getListCollab(self, id):
        r = requests.get('https://kippt.com/api/lists/' + str(id) + '/collaborators', headers=self.header)
        if r.status_code is 200: return r.json
        else: return False

    # Get our clips.
    # Example:
    # myClips = user.getClips()
    # myClips = user.getClips(54332, 20, 5) # (listID, limit, offset)
    # myClips = user.getClips(limit = 20)
    #
    # Available values in meta:
    # total_count, limit, offset
    # Available values in clip:
    # id, url, title, list, notes, is_starred, url_domain, created, updated, resource_uri
    #
    # Returns data on success, and false on failure.
    def getClips(self, listID = None, limit = 0, offset = 0):
        params = { "limit": str(limit),
                   "offset": str(offset) }
        url = 'https://kippt.com/api/clips?limit={limit}&offset={offset}'.format(**params)
        if not listID is None: url = url + '&list=' + str(listID)
        r = requests.get(url, headers=self.header)
        if r.status_code is 200: return r.json()['meta'], r.json()['objects']
        else: return False, False

    # Get a clip.
    # Example:
    # myClip = user.getClip(2027593)
    # x = myClip['title']
    #
    # Available values in clip:
    # id, url, title, list, notes, is_starred, url_domain, created, updated, resource_uri
    #
    # Returns data on success, and false on failure.
    def getClip(self, id):
        r = requests.get('https://kippt.com/api/clips/' + str(id), headers=self.header)
        if r.status_code is 200: return r.json()
        else: return False

    # Search for a query.
    # Example:
    # mySearch = user.search("Programming")
    #
    # Available values in meta:
    # total_count, limit, offset
    # Available values in clip:
    # id, url, title, list, notes, is_starred, url_domain, created, updated, resource_uri
    #
    # Returns data on success, and false on failure.
    def search(self, query, limit = 0, offset = 0):
        query = quote_plus(query)
        params = { "query": query,
                    "limit": str(limit),
                    "offset": str(offset)
        }
        r = requests.get('https://kippt.com/api/search/clips/?q={query}&limit={limit}&offset={offset}'.format(**params),
                        headers=self.header)
        if r.status_code is 200: return r.json()['meta'], r.json()['objects']
        else: return False, False

    # Create a list.
    # Examples:
    # user.createList('My New List!')
    #
    # Will return data on success and False on failure.
    def createList(self, name):
        clipdata = {'title': name}
        r = requests.post('https://kippt.com/api/lists/', data=json.dumps(clipdata), headers=self.header)
        if r.status_code is 201: return r.json()
        else: return False

    # Add a clip.
    # Examples:
    # user.addClip('www.kippt.com')
    # user.addClip('www.kippt.com',title="My Title!")
    # user.addClip('www.kippt.com',1234,starred="true",notes='My Notes!')
    #
    # Will return data on success and False on failure.
    def addClip(self, url, listID=0, title = None, starred = None, notes = None, ):
        clipdata = {'url': url, 'list': '/api/lists/' + str(listID)}
        if not title is None: clipdata['title'] = title
        if not starred is None: clipdata['is_starred'] = starred
        if not notes is None: clipdata['notes'] = notes
        r = requests.post('https://kippt.com/api/clips/', data=json.dumps(clipdata), headers=self.header)
        if r.status_code is 201: return r.json()
        else: return False

    # Create a list.
    # Examples:
    # newList = user.createList('Programming')
    # print newList
    def createList(self, name):
        clipdata = {'title': name}
        r = requests.post('https://kippt.com/api/lists/', data=json.dumps(clipdata), headers=self.header)
        if r.status_code is 201: return r.json()
        else: return False

    # Delete a clip ( Only clip owners can modify or delete clips, not collaborators! )
    # Examples:
    # user.deleteClip(2028643)
    #
    # Will return True on success, and False on failure
    def deleteClip(self, id):
        r = requests.delete('https://kippt.com/api/clips/' + str(id), headers=self.header)
        if r.status_code is 204: return True
        else: return False

    # Delete a List
    # Examples:
    # user.deleteList(54433)
    #
    # Will return True on success, and False on failure
    def deleteList(self, id):
        r = requests.delete('https://kippt.com/api/lists/' + str(id), headers=self.header)
        if r.status_code is 204: return True
        else: return False

    # Update a Clip ( Only clip owners can modify or delete clips, not collaborators! )
    # Example:
    # pyRespUpdateClip(id=2027593, list_uri='/api/lists/55284/')
    #
    # Returns True on success, False on failure.
    def updateClip(self, id, title = None, notes = None, listID = None, starred = None):
        clipdata = {}
        if not title is None: clipdata['title'] = title
        if not notes is None: clipdata['notes'] = notes
        if not starred is None: clipdata['is_starred'] = starred
        if not listID is None: clipdata['list'] = '/api/lists/' + str(listID)
        r = requests.put('https://kippt.com/api/clips/' + str(id), data=json.dumps(clipdata), headers=self.header)
        # import pdb; pdb.set_trace();
        if r.status_code is 200: return True
        else: return False

    # Updating List ( With Python Requests )
    # Example:
    # client.updateList(55284, title="New Title!")
    #
    # Returns True on success, False on failure.
    def updateList(self, id, title = None):
        clipdata = {}
        if not title is None: clipdata['title'] = title
        r = requests.put('https://kippt.com/api/lists/' + str(id), data=json.dumps(clipdata), headers=self.header)
        if r.status_code is 200: return True
        else: return False

