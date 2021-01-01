"""

This file houses functions used for tampering with Roblox Datastores

"""

from urllib.parse import quote
from math import floor
import re

endpoint = "http://gamepersistence.roblox.com/"

class DataStore:
    """
    Represents the in-game datastore system for storing data for games (https://gamepersistence.roblox.com).
    This is only available for authenticated clients, and games that they own.

    Parameters
    ----------
    requests : ro_py.utilities.requests.Requests
        Requests object to use for API requests.
    placeId : int
        PlaceId to modify the DataStores for, 
        if the currently authenticated user doesn't have sufficient permissions, 
        it will raise a NotAuthorizedToModifyPlaceDataStores exception
    name : str
        The name of the DataStore, 
        as in the Second Parameter of 
        `std::shared_ptr<RBX::Instance> DataStoreService::getDataStore(const DataStoreService* this, std::string name, std::string scope = "global")`
    scope : str, optional
        The scope of the DataStore,
        as on the Second Parameter of
         `std::shared_ptr<RBX::Instance> DataStoreService::getDataStore(const DataStoreService* this, std::string name, std::string scope = "global")`
    legacy : bool, optional
        Describes whether or not this will use the legacy endpoints, 
        over the new v1 endpoints (Does not apply to getSortedValues)
    legacyNamingScheme : bool, optional
        Describes whether or not this will use legacy names for data stores, if true, the qkeys[idx].scope will match the current scope (global by default), 
        there will be no qkeys[idx].target (normally the key that is passed into each method), 
        and the qkeys[idx].key will match the key passed into each method.
    """
    def __init__(self, requests, placeId, name, scope, legacy = True, legacyNamingScheme = False):
       self.requests = requests
       self.placeId = placeId
       self.legacy = legacy
       self.legacyNamingScheme = legacyNamingScheme
       self.name = name
       self.scope = scope if scope != None else "global"

    async def get(self, key):
        """
        Represents a get request to a data store,
        using legacy works the same

        Parameters
        ----------
        key : str
            The key of the value you wish to get, 
            as in the Second Parameter of 
            `void DataStore::getAsync(const DataStore* this, std::string key, boost::function<void(RBX::Reflection::Variant)> resumeFunction, boost::function<void(std::string)> errorFunction)`
        
        Returns
        -------
        typing.Any
        """
        if self.legacy == True:
            data = f"qkeys[0].scope={quote(self.scope)}&qkeys[0].target=&qkeys[0].key={quote(key)}" if self.legacyNamingScheme == True else f"qkeys[0].scope={quote(self.scope)}&qkeys[0].target={quote(key)}&qkeys[0].key={quote(self.name)}"
            r = await self.requests.post(
                url=endpoint + f"persistence/getV2?placeId={str(self.placeId)}&type=standard&scope={quote(self.scope)}", 
                headers={
                    'Roblox-Place-Id': str(self.placeId),
                    'Content-Type': 'application/x-www-form-urlencoded'
            }, data=data)
            if len(r.json()['data']) == 0:
                return None
            else:
                return r.json()['data'][0]['Value']
        else:
            url = endpoint + f"v1/persistence/ro_py?type=standard&key={quote(key)}&scope={quote(self.scope)}&target=" if self.legacyNamingScheme == True else endpoint + f"v1/persistence/ro_py?type=standard&key={quote(self.name)}&scope={quote(self.scope)}&target={quote(key)}"
            r = await self.requests.get(
                url=url,
                headers={
                    'Roblox-Place-Id': str(self.placeId)
            })
            if r.status_code == 204:
                return None
            else:
                return r.text;
            
    async def set(self, key, value):
        """
        Represents a set request to a data store,
        using legacy works the same

        Parameters
        ----------
        key : str
            The key of the value you wish to get, 
            as in the Second Parameter of 
            `void DataStore::getAsync(const DataStore* this, std::string key, boost::function<void(RBX::Reflection::Variant)> resumeFunction, boost::function<void(std::string)> errorFunction)`
        value
            The value to set for the key,
            as in the 3rd parameter of
            `void DataStore::setAsync(const DataStore* this, std::string key, RBX::Reflection::Variant value, boost::function<void()> resumeFunction, boost::function<void(std::string)> errorFunction)`
        
        Returns
        -------
        typing.Any
        """
        if self.legacy == True:
            data = f"value={quote(str(value))}"
            url = endpoint + f"persistence/set?placeId={str(self.placeId)}&type=standard&key={quote(key)}&type=standard&scope={quote(self.scope)}&target=&valueLength={str(len(str(value)))}" if self.legacyNamingScheme == True else endpoint + f"persistence/set?placeId={str(self.placeId)}&type=standard&key={quote(self.name)}&type=standard&scope={quote(self.scope)}&target={quote(key)}&valueLength={str(len(str(value)))}"
            r = await self.requests.post(
                url=url, 
                headers={
                    'Roblox-Place-Id': str(self.placeId),
                    'Content-Type': 'application/x-www-form-urlencoded'
            }, data=data)
            if len(r.json()['data']) == 0:
                return None
            else:
                return r.json()['data']
        else:
            url = endpoint + f"v1/persistence/ro_py?type=standard&key={quote(key)}&scope={quote(self.scope)}&target=" if self.legacyNamingScheme == True else endpoint + f"v1/persistence/ro_py?type=standard&key={quote(self.name)}&scope={quote(self.scope)}&target={quote(key)}"
            r = await self.requests.post(
                url=url,
                headers={
                    'Roblox-Place-Id': str(self.placeId),
                    'Content-Type': '*/*',
                    'Content-Length': str(len(str(value)))
            }, data=quote(str(value)))
            if r.status_code == 200:
                return value;

    async def setIfValue(self, key, value, expectedValue):
        """
        Represents a conditional set request to a data store,
        only supports legacy

        Parameters
        ----------
        key : str
            The key of the value you wish to get, 
            as in the Second Parameter of 
            `void DataStore::getAsync(const DataStore* this, std::string key, boost::function<void(RBX::Reflection::Variant)> resumeFunction, boost::function<void(std::string)> errorFunction)`
        value
            The value to set for the key,
            as in the 3rd parameter of
            `void DataStore::setAsync(const DataStore* this, std::string key, RBX::Reflection::Variant value, boost::function<void()> resumeFunction, boost::function<void(std::string)> errorFunction)`
        expectedValue
            The expectedValue for that key, if you know the key doesn't exist, then set this as None

        Returns
        -------
        typing.Any
        """
        data = f"value={quote(str(value))}&expectedValue={quote(str(expectedValue)) if expectedValue != None else ''}"
        url = endpoint + f"persistence/set?placeId={str(self.placeId)}&type=standard&key={quote(key)}&type=standard&scope={quote(self.scope)}&target=&valueLength={str(len(str(value)))}&expectedValueLength={str(len(str(expectedValue))) if expectedValue != None else str(0)}" if self.legacyNamingScheme == True else endpoint + f"persistence/set?placeId={str(self.placeId)}&type=standard&key={quote(self.name)}&type=standard&scope={quote(self.scope)}&target={quote(key)}&valueLength={str(len(str(value)))}&expectedValueLength={str(len(str(expectedValue))) if expectedValue != None else str(0)}"
        r = await self.requests.post(
            url=url, 
            headers={
                'Roblox-Place-Id': str(self.placeId),
                'Content-Type': 'application/x-www-form-urlencoded'
        }, data=data)
        try:
            if r.json()['data'] != 0:
                return r.json()['data']
        except KeyError:
            return r.json()['error']

    async def setIfIdx(self, key, value, idx):
        """
        Represents a conditional set request to a data store,
        only supports new endpoints,

        Parameters
        ----------
        key : str
            The key of the value you wish to get, 
            as in the Second Parameter of 
            `void DataStore::getAsync(const DataStore* this, std::string key, boost::function<void(RBX::Reflection::Variant)> resumeFunction, boost::function<void(std::string)> errorFunction)`
        value
            The value to set for the key,
            as in the 3rd parameter of
            `void DataStore::setAsync(const DataStore* this, std::string key, RBX::Reflection::Variant value, boost::function<void()> resumeFunction, boost::function<void(std::string)> errorFunction)`
        idx : int
            The expectedidx, there

        Returns
        -------
        typing.Any
        """
        url = endpoint + f"v1/persistence/ro_py?type=standard&key={quote(key)}&scope={quote(self.scope)}&target=" if self.legacyNamingScheme == True else endpoint + f"v1/persistence/ro_py?type=standard&key={quote(self.name)}&scope={quote(self.scope)}&target={quote(key)}&usn=0.0"
        r = await self.requests.post(
            url=url,
            headers={
                'Roblox-Place-Id': str(self.placeId),
                'Content-Type': '*/*',
                'Content-Length': str(len(str(value)))
        }, data=quote(str(value)))
        if r.status_code == 409:
            usn = r.headers['roblox-usn']
            split = usn.split('.')
            msn_hash = split[0]
            current_value = split[1]
            url = endpoint + f"v1/persistence/ro_py?type=standard&key={quote(key)}&scope={quote(self.scope)}&target=" if self.legacyNamingScheme == True else endpoint + f"v1/persistence/ro_py?type=standard&key={quote(self.name)}&scope={quote(self.scope)}&target={quote(key)}&usn={msn_hash}.{hex(idx).split('x')[1]}"
            r2 = await self.requests.post(
                url=url,
                headers={
                    'Roblox-Place-Id': str(self.placeId),
                    'Content-Type': '*/*',
                    'Content-Length': str(len(str(value)))
            }, data=quote(str(value)))
            if r2.status_code == 409:
                return "Expected idx did not match current idx, current idx is " + str(floor(int(current_value, 16)))
            else:
                return value

    async def increment(self, key, delta = 0):
        """
        Represents a conditional set request to a data store,
        only supports legacy

        Parameters
        ----------
        key : str
            The key of the value you wish to get, 
            as in the Second Parameter of 
            `void DataStore::getAsync(const DataStore* this, std::string key, boost::function<void(RBX::Reflection::Variant)> resumeFunction, boost::function<void(std::string)> errorFunction)`
        delta : int, optional
            The value to set for the key,
            as in the 3rd parameter of
            `void DataStore::setAsync(const DataStore* this, std::string key, RBX::Reflection::Variant value, boost::function<void()> resumeFunction, boost::function<void(std::string)> errorFunction)`
        
        Returns
        -------
        typing.Any
        """
        data = ""
        url = endpoint + f"persistence/increment?placeId={str(self.placeId)}&type=standard&key={quote(key)}&type=standard&scope={quote(self.scope)}&target=&value={str(delta)}" if self.legacyNamingScheme else endpoint + f"persistence/increment?placeId={str(self.placeId)}&type=standard&key={quote(self.name)}&type=standard&scope={quote(self.scope)}&target={quote(key)}&value={str(delta)}"

        r = await self.requests.post(
            url=url, 
            headers={
                'Roblox-Place-Id': str(self.placeId),
                'Content-Type': 'application/x-www-form-urlencoded'
        }, data=data)
        try:
            if r.json()['data'] != 0:
                return r.json()['data']
        except KeyError:
            cap = re.search("\(.+\)", r.json()['error'])
            reason = cap.group(0).replace("(", "").replace(")", "")
            if reason == "ExistingValueNotNumeric":
                return "The requested key you tried to increment had a different value other than byte, short, int, long, long long, float, double or long double"
    
    async def remove(self, key):
        """
        Represents a get request to a data store,
        using legacy works the same

        Parameters
        ----------
        key : str
            The key of the value you wish to remove, 
            as in the Second Parameter of 
            `void DataStore::removeAsync(const DataStore* this, std::string key, boost::function<void(RBX::Reflection::Variant)> resumeFunction, boost::function<void(std::string)> errorFunction)`

        Returns
        -------
        typing.Any
        """
        if self.legacy == True:
            data = ""
            url = endpoint + f"persistence/remove?placeId={str(self.placeId)}&type=standard&key={quote(key)}&type=standard&scope={quote(self.scope)}&target=" if self.legacyNamingScheme else endpoint + f"persistence/remove?placeId={str(self.placeId)}&type=standard&key={quote(self.name)}&type=standard&scope={quote(self.scope)}&target={quote(key)}"
            r = await self.requests.post(
                url=url, 
                headers={
                    'Roblox-Place-Id': str(self.placeId),
                    'Content-Type': 'application/x-www-form-urlencoded'
            }, data=data)
            if r.json()['data'] == None:
                return None
            else:
                return r.json()['data']
        else:
            url = endpoint + f"v1/persistence/ro_py/remove?type=standard&key={quote(key)}&scope={quote(self.scope)}&target=" if self.legacyNamingScheme == True else endpoint + f"v1/persistence/ro_py/remove?type=standard&key={quote(self.name)}&scope={quote(self.scope)}&target={quote(key)}"
            r = await self.requests.post(
                url=url,
                headers={
                    'Roblox-Place-Id': str(self.placeId)
            })
            if r.status_code == 204:
                return None
            else:
                return r.text;