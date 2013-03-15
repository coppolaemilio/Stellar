layers = (sge.BackgroundLayer(fence_sprite, 0, 380, 0, yrepeat=False),)
background = sge.Background(layers, 0xffffff)

circle = Circle(game.width // 2, game.height // 2)
objects = [circle]

views = (sge.View(0, 0),)

rm_0 = sge.Room(tuple(objects), views=views, background=background)
