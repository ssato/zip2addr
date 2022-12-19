# Info

This is a study project to learn how to develop and test web application with
using fast-api and related software.

# Goals

- Develop a simple web application to convert a zip code given by user to an
  address and show it to the user.
- Test the web application

## Non goals

- Develop a full-featured web application such like the one can process zip
  codes outside of Japan.

# Design and implementation details

- Expected original input data is the CSV files provided by JP from
  https://www.post.japanpost.jp/zipcode/dl/oogaki-zip.html.

  - For example,
    https://www.post.japanpost.jp/zipcode/dl/oogaki/zip/ken_all.zip

## Usecases

# Convert a zip code given by user to an address

## Help

1. User: GET request without query parameters
1. App: Returns a string gives usage

## Convert a zip code

1. User: GET request with query parameter represents a zip code
1. App: Returns a string represents an address

# Limitations and issues

- lorem ipsum
- lorem ipsum

# References

- https://fastapi.tiangolo.com/
- https://docs.pydantic.dev/
- https://typer.tiangolo.com/
- https://hypothesis.readthedocs.io/en/latest/
