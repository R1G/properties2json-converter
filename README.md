# properties2json-converter
Simple Python utility for converting .properties files and directories to .json. 

# usage
To copy a .properties file to a .json file
>`python properties2json.py <YOUR FILE>.properties`

To copy a directory containing .properties files to .json
>`python properties2json.py <SRC> <DEST>`

# examples
We convert the sample.properties file provided here
>`python properties2json.py sample.properties`

We convert the sample_locales directory (which contains several .properties files) here
>`python properties2json.py sample_locales locales_converted`

# features
properties2json-converter is non-destructive, and able to convert .properties files containing multiple '=' characters and special characters, making it ideal for .properties files containing hyperlinks, nested objects, etc.

### equals sign
```java 
some_link=<a href='/signin'>Log in</a>
```
Converts to
```yaml 
"some_link":"<a href='/signin'>Log in</a>"
```

### nested objects
Observe that [] and . notation may be used interchangeably through any depth.
```java 
A.B[C]=value
```
Converts to
```yaml
{
  "A": {
    "B": {
      "C": "value"
    }
  }
}
```

### encoding
We write to JSON's default `utf-8` encoding.
```java
country=中国
greeting=你好
```
Converts to
```yaml
{
    "name": "中国", 
    "greeting": "你好"
}
```







