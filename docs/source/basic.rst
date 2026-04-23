The Basics: Getting a Grid (Pygame)
===================================

Consider the following introductory example from `Pygame-ce <https://pyga.me/docs/>`:

.. code-block:: python
   import pygame

   # pygame setup
   pygame.init()
   screen = pygame.display.set_mode((1280, 720))
   clock = pygame.time.Clock()
   running = True
   
   while running:
       # poll for events
       # pygame.QUIT event means the user clicked X to close your window
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False

       # fill the screen with a color to wipe away anything from last frame
       screen.fill("purple")

       # RENDER YOUR GAME HERE

       # flip() the display to put your work on screen
       pygame.display.flip()

       clock.tick(60)  # limits FPS to 60
   
   pygame.quit()

It currently displays a purple screen. Let us adapt this to draw a ``(5, 5)`` grid across the entire screen. We start of with some imports:

.. code-block:: python

   from lpyout import Grid
   from lpyout.pygame import screen_wrapper
   from lpyout.pygame.render import fast_render

The first import gives us the ability to create ``Grid`` objects. Each ``Grid`` object should be contained in a ``Screen`` (that is, the actual viewport, such as a window). We provide some defaults for ``pygame``. The second import gives us the entire window created by ``pygame``. Lastly, a ``Grid`` object just stores coordinates, so we implement some basic rendering routines for ``pygame`` that actually let you display the grid.

Now, after ``running = True`` add:

.. code-block:: python

   screen_wrapper.update()
   grid = Grid.fill_screen(screen_wrapper, 5, 5)

``screen_wrapper.update()`` gets the dimensions of the current ``pygame`` window. Because there are *so* many ways to make a grid, we have various class methods that act as simplified constructors. ``fill_screen`` makes the grid fill the specified screen (which in our case, fills the window).

Now, replace ``screen.fill("purple")`` with ``screen.fill("black")`` and right below it add:

.. code-block:: python

       # fill the screen with a color to wipe away anything from last frame
       screen.fill("black")
    
       # Render grid
       screen_wrapper.update()
       fast_render(grid, screen)

Like above, in case the window changes size, we ``.update`` the ``screen_wrapper`` object. Lastly, we make a call to ``fast_render(grid, screen)`` to actually render the grid!
