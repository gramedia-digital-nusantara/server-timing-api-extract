# Server Timing API Header Extract

Simple python script to read `Server Timing API` then output to command-line table.

## Requirements
```
requests<2.29
prettytable<3.4
```


## Usage
```bash
python main.py --config ./input.example.json
```

## Examples
### Config
```json
// input.example.json
[
    {
        "name": "Server Timing Endpoint 1",
        "url": "http://localhost:3000/api/product-search"
    },
    {
        "name": "Server Timing with IP",
        "host": "my-web.com",
        "url": "http://localhost/api/product-search"
    }
]
```

### Output
```
################################
##  Server Timing Endpoint 1  ##
################################

Info :
+-----------+------------------------------------------+
| URL       | http://localhost:3000/api/product-search |
| Body Size | 6 kB                                     |
+-----------+------------------------------------------+

Timing Metrics :
+----------------------+----------+--------------------------------+
| Name                 | Duration | Description                    |
+----------------------+----------+--------------------------------+
| get_product_list     |    46 ms | Product Search View            |
| solr                 |    29 ms | Solr search                    |
| search_parse         |    17 ms | Parse search result            |
| result_serializer    |     0 ms | Serialize search result        |
| vendor_facet         |     4 ms | Vendor facet                   |
| search_category_tree |     5 ms | Create category tree for facet |
| attribute_facet      |     3 ms | Attribute facet                |
| attribute_facet      |     0 ms | Attribute facet                |
| price_facet          |     0 ms | Price facet                    |
+----------------------+----------+--------------------------------+


#############################
##  Server Timing with IP  ##
#############################

Info :
+-----------+-------------------------------------+
| Host      | my-web.com                          |
| URL       | http://localhost/api/product-search |
| Body Size | 86 kB                               |
+-----------+-------------------------------------+

Timing Metrics :
+----------------------+----------+--------------------------------+
| Name                 | Duration | Description                    |
+----------------------+----------+--------------------------------+
| get_product_list     |   397 ms | Product Search View            |
| solr                 |    87 ms | Solr search                    |
| search_parse         |   309 ms | Parse search result            |
| result_serializer    |     0 ms | Serialize search result        |
| vendor_facet         |    51 ms | Vendor facet                   |
| search_category_tree |   240 ms | Create category tree for facet |
| attribute_facet      |     0 ms | Attribute facet                |
| attribute_facet      |     3 ms | Attribute facet                |
| attribute_facet      |     0 ms | Attribute facet                |
| attribute_facet      |     0 ms | Attribute facet                |
| attribute_facet      |     0 ms | Attribute facet                |
| price_facet          |     0 ms | Price facet                    |
+----------------------+----------+--------------------------------+
```