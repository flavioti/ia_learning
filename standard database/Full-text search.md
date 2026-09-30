Is an advanced search technique to search text in a table

```SQL
CREATE FULLTEXT INDEX search_idx ON products (name, description);
SELECT * FROM products WHERE MATCH(name, description) AGAINST ('bluetooth');
```


Example of a commom search using like keyword:
```SQL
SELECT * FROM products WHERE name LIKE '%bluetooth%';
```



[[Postgres]]|[[MySQL]]