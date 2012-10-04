## General aspects

* All the API requests that contain a body must encode it using the JSON format (and include the relevant HTTP Header).
* All the API responses will be encoded using the JSON format.
* The API will use the standard HTTP Status codes to notify the client about the request result:
* *Endpoint*: https://juandebravo:hackaton@juandebravo.cloudant.com/hackaton
* Every response will have two elements in the JSON object: **_id** and **_rev**

```
curl https://juandebravo:hackaton@juandebravo.cloudant.com/hackaton
```

### Create a new organization

```
POST /
    data: {"_id": "organizations", "organizations": ["name1", "name2"]}
```

Example:

```
curl -i -H 'Content-Type: application/json' -d '{"_id": "organizations", "organizations": ["telefonicaid"]}' https://juandebravo:hackaton@juandebravo.cloudant.com/hackaton
```

### Get all organizations

```
GET /organizations
    {"organizations": ["name1", "name2"]}
```

Example:

```
curl -i https://juandebravo:hackaton@juandebravo.cloudant.com/hackaton/organizations

{"_id":"organizations","_rev":"1-4135be63312eb95026197197050f36b6","organizations":["name1","name2"]}

```

### Create organization data

```
POST /
    data: {"_id": "organizations_<organization>", "data": {}}
```

Example:

```
curl -i -H 'Content-Type: application/json' -d '{"_id": "organizations_telefonicaid", "users":[{"pepito":{"points": 30,"badges":[{"padowan":"20121002"},{"adventurer":"20121001"}]}}]}' https://juandebravo:hackaton@juandebravo.cloudant.com/hackaton
```



### Get organization data

```
GET /organizations_<organization>
    {"users":[
        {"pepito":
            {
            "points": 30,
            "badges": [{"padowan": "20121002"},
                       {adventurer": "20121001"}]
            }
        }
    ]}
```

Example:

```
curl https://juandebravo:hackaton@juandebravo.cloudant.com/hackaton/organizations_telefonicaid
```

### Get user extend data

```
GET /organizations_<organization>_users_<user>
    {"points":
        {
            "20121001": {
                "points": 10,
                "rank": 1
            },
            "20121002": {
                "points": -1,
                "rank": 2
            },
            "20120930": {
                "points": 20,
                "rank": 1
            },
        },
     "badges":
        {
            "20121002": "padowan",
            "20121001": "adventurer"
        }
    }

```