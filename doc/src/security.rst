Security
========

Secret key
----------

In order to perform security related operations Ampho needs a security key. Ampho uses the `JWK`_ to store a key and
have a CLI command to easily generate it:

.. sourcecode:: shell

    flask ampho sec-gen-key

.. sourcecode:: json

    {"k":"PkJ4gc1vCESz212pozSfjxpU66osYOIpi3X14OoHv7s","kty":"oct"}

Generated key must be placed into ``AMPHO_SECURITY_KEY`` configuration parameter. I hope that it's not necessary to
say one more time that **keeping the key in secret is vital**.


RESTful API
-----------

Ampho provides the RESTful API to the security functions. Each security endpoint start with a prefix defined by
``AMPHO_SECURITY_REST_PREFIX`` configuration parameter with default value of ``/api/security``.


Request authorization
^^^^^^^^^^^^^^^^^^^^^

Whenever you need to authorize a request to certain view or RESTful resource, you may use
``flask_ampho.security.authorize`` decorator. It analyzes the ``Authorization`` HTTP header, extracts access token from
it, check extracted token for validity and performs user authentication and authorization.

.. sourcecode:: python

    from flask_ampho.security import authorize

    @authorize
    def protected_view(auth: dict):
        return f'This is highly protected resource. Current user is {auth.login}.'

Is the token is valid and current user is authorized, the decorated functions will receive authorization data in the
``auth`` named argument. The 401-response will be returned otherwise.

While accessing resources from client's side it's necessary to provide access token using `Authorization HTTP header`_,
and `bearer`_ authentication scheme, i. e.:

.. sourcecode:: text

    Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTY4OTg3MDQsImxvZ2luIjoiYXNkIn0.IUYmf5uFUrOhwpmyUoHoCfUL1JimIBM5lcxntAka3kk


POST /login
^^^^^^^^^^^

Obtain an access token.

Request arguments:

* **required** **str** ``login``
* **str** ``password``

Success response fields:

* **int** ``starts``. Timestamp since the token is valid.
* **int** ``expires``. Timestamp after the token is invalid.
* **int** ``ttl``. Token validity time in seconds.
* **int** ``leeway``. Token validity leeway.

Error response fields:

* **str** ``message``. Error explanation.

Request example:

.. sourcecode:: text

Successful response example:

.. sourcecode:: text

Failed response example:

.. sourcecode:: text


POST /renew
^^^^^^^^^^^

Renew an access token.


Configuration parameters
------------------------

* **required** **json** ``AMPHO_SECURITY_KEY``. Private encryption key.
* **str** ``AMPHO_SECURITY_REST_PREFIX``. Prefix of RESTful API endpoints. Default is ``/api/security``


.. _JWK: https://tools.ietf.org/html/rfc7517
.. _Authorization HTTP header: https://tools.ietf.org/html/rfc7235#section-4.2
.. _bearer: https://tools.ietf.org/html/rfc6750
