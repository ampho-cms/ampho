Signals
=======

bundle_registered
-----------------

Fires when a bundle is registered.

Arguments:

- :py:class:`ampho.Bundle`: bundle object which has been registered.

Example:

.. sourcecode:: python

    from ampho import Bundle
    from ampho.signals import bundle_registered


    def on_bundle_registered(b: Bundle):
        """Signal handler function
        """
        print(f'{b.name} has been registered')


    # Call on_bundle_registered() each time when a bundle is registered
    bundle_registered.connect(on_bundle_registered)

